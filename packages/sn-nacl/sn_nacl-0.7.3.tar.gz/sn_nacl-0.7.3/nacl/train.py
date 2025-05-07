import collections
import logging
import os
from dataclasses import dataclass
from typing import Optional

import dill
import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
import pandas


from saltworks import FitParameters

from nacl.dataset import TrainingDataset
from nacl.loglikelihood import LogLikelihood
from nacl.minimize import Minimizer
from nacl.models import salt2
from nacl.plotting import control_plot

from sksparse.cholmod import CholmodNotPositiveDefiniteError


logger = logging.getLogger(__name__)


@dataclass
class FitResults:
    pars: FitParameters
    v: Optional[tuple] = None  # (vector, jacobian)
    var_v: Optional[tuple] = None  # (vector, jacobian)

    def __post_init__(self):
        self.ll = None  # LogLikelihood
        self.minz = None  # Minimizer


class TrainSALT2Like:
    def __init__(
            self,
            tds,
            variance_model=None,
            calib_variance=None,
            color_scatter=False,
            dust_extinction=True):
        """
        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Your training dataset
        variance_model : str or int or float
            if an error model needs to be fitted default is None

        Examples
        --------

        >>> from nacl import TrainingDataset
        >>> from lemaitre import bandpasses
        >>> filterlib = bandpasses.get_filterlib()  #doctest: +ELLIPSIS
        >>> tds = TrainingDataset.read_parquet(
        ...     "data/test_datasets/test_datasets_blind.parquet",
        ...     filterlib=filterlib)
        >>> trainer = TrainSALT2Like(
        ...     tds, variance_model='simple_snake')  #doctest: +ELLIPSIS

        """
        self.tds = tds
        if self.tds.spec_data is not None:
            self._clean_dataset(tds)

        self.extinction = None
        if dust_extinction:
            nacl_dust = salt2.DustExtinction()
            self.extinction = nacl_dust.CCM89_dust()

        self.model = salt2.get_model(
            tds, dust_extinction_model=self.extinction)

        if calib_variance is not None:
            self.prior = [salt2.CalibErrorModel(
                self.model,
                calib_variance=calib_variance)]
        else:
            self.prior = None
        self.color_scatter = color_scatter
        if color_scatter:
            if self.prior is not None:
                self.prior.append(salt2.ColorScatter(self.model))
            else:
                self.prior = [salt2.ColorScatter(self.model)]

        if variance_model is not None:
            if variance_model == 'simple_snake':
                variance_model = salt2.get_simple_snake_error(self.model)

            elif variance_model == 'local_snake':
                variance_model = salt2.get_local_snake_error(self.model)

            elif variance_model == 'sn_lambda_snake':
                variance_model = salt2.get_sn_lambda_snake_error(self.model)

            elif variance_model == 'sn_local_snake':
                variance_model = salt2.get_sn_local_snake_error(self.model)
            else:
                raise ValueError("Input error_model not recognised, try simple_snake, local_snake, sn_lambda_snake or sn_local_snake")
        self.variance_model = variance_model
        self.log = []
        self.mu_reg = 1e-2
        self.mu_cons = 1e+5

        # recalibrate the spectra
        if tds.spec_data is not None:
            ll = LogLikelihood(self.model)
            self.v_init = self.model(ll.pars)
            self.spec_recal_init = self._recalib_spectra(self.tds, self.v_init)
            # ll.pars['SpectrumRecalibration'].full[3::4] = np.log(r)

        # register the initial state (PETS sncosmo/salt2 fits)
        # into the internal log
        ll = LogLikelihood(self.model)
        f0 = FitResults(pars=ll.pars)
        f0.ll = ll
        f0.v = self.model(f0.pars)
        f0.var_v = None
        self.log.append(f0)

    def fit(self, fix=None, p_init=None,
            p_init_blocks=None,
            fit_variance_model=False,
            force_spec_recalibration=False,
            max_iter=100):
        """
        """
        reg = salt2.get_regularization_prior(self.model, pars=self.model.init_pars(), mu=self.mu_reg, order=1, check=True)

        cons = salt2.get_constraint_prior(self.model, linear=True,
                                      mu=self.mu_cons, Mb=-19.5,
                                      check=True)
        if fit_variance_model:
            ll = LogLikelihood(self.model, variance_model=self.variance_model, priors=self.prior)
            reg = salt2.get_regularization_prior(self.model, pars=ll.pars, mu=self.mu_reg, order=1, check=True)
            ll = LogLikelihood(self.model, variance_model=self.variance_model, reg=[reg], cons=[cons], priors=self.prior)
        else:
            if self.prior is not None:
                ll = LogLikelihood(self.model, reg=[reg], cons=[cons], priors=self.prior)
                reg = salt2.get_regularization_prior(self.model, pars=ll.pars, mu=self.mu_reg, order=1, check=True)
            ll = LogLikelihood(self.model, reg=[reg], cons=[cons], priors=self.prior)

        if force_spec_recalibration:
            ll.pars['SpectrumRecalibration'].full[3::4] = np.log(self.spec_recal_init)

        if fix:
            for block_name in fix:
                ll.pars[block_name].fix()

        if p_init:
            for block_name in p_init._struct.slices:
                if block_name not in ll.pars._struct.slices:
                    continue
                ll.pars[block_name].full[:] = p_init[block_name].full[:]

        if p_init_blocks:
            for block_name in p_init_blocks:
                if block_name not in ll.pars._struct.slices:
                    continue
                ll.pars[block_name].full[:] = p_init_blocks[block_name]

        # fit
        minz = Minimizer(ll)
        p = minz.minimize_lm(ll.pars.free, max_iter=max_iter)

        t = np.array(minz.get_log()['time'])
        logger.info(f'fitting took {t[-1] - t[0]} seconds')

        res = FitResults(pars=ll.pars, v=self.model(ll.pars, jac=0), var_v=None)
        res.ll = ll
        res.minz = minz
        if self.variance_model is not None and fit_variance_model:
            res.v_var = self.variance_model(ll.pars, jac=0)

        return res

    def train_salt2_model(self, save=False, path=None):
        """Full model training
        """
        full_pars_blocks = ['M0', 'M1', 'CL', 'X0', 'X1', 'c', 'tmax']
        spec_recal = False
        if self.tds.spec_data is not None:
            full_pars_blocks.append('SpectrumRecalibration')
            spec_recal = True
        if self.color_scatter:
            full_pars_blocks.append('sigma_kappa')
            full_pars_blocks.append('kappa_color')

        first_fixed_pars = ['M0', 'M1', 'CL']
        if self.color_scatter:
            first_fixed_pars.append('sigma_kappa')
            first_fixed_pars.append('kappa_color')
            color_scatter_params = ['sigma_kappa', 'kappa_color']
        else :
            color_scatter_params = None

        # initialization : fit the light curves and spectra
        # no error model
        f1 = self.fit(fix=first_fixed_pars,
                      fit_variance_model=False,
                      force_spec_recalibration=spec_recal,
                      max_iter=10)
        self.log.append(f1)

        # fit error model
        f2 = self.fit(fix=full_pars_blocks,
                      fit_variance_model=True,
                      p_init=f1.ll.pars,
                      max_iter=20)
        self.log.append(f2)

        # refit all pars,
        # with an error model
        f3 = self.fit(fix=color_scatter_params,
                      fit_variance_model=True,
                      p_init=f2.ll.pars,
                      max_iter=15)
        self.log.append(f3)

        #refit with a color scatter
        f4 = self.fit(fix=None,
                      fit_variance_model=True,
                      p_init=f3.ll.pars,
                      max_iter=50)
        self.log.append(f4)

        # train
        #f4 = self.fit(variance_model=True,
        #              p_init=f3.ll.pars)
        #self.log.append(f4)

        if save and path is not None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            sn_data = pandas.DataFrame(data=self.tds.sn_data.nt)
            columns_rename = {'x0':'x0_init', 'x1':'x1_init', 'c':'c_init', 'tmax':'tmax_init'}
            sn_data = sn_data.rename(columns = columns_rename)
            sn_data = sn_data.assign(x0 = f4.pars['X0'].full[self.tds.sn_data.sn_index])
            sn_data = sn_data.assign(x1 = f4.pars['X1'].full[self.tds.sn_data.sn_index])
            sn_data = sn_data.assign(c = f4.pars['c'].full[self.tds.sn_data.sn_index])
            sn_data = sn_data.assign(t0 = f4.pars['tmax'].full[self.tds.sn_data.sn_index])
            try:
                sn_data = sn_data.assign(gamma_sn = f4.pars['gamma_sn'].full[self.tds.sn_data.sn_index])
            except:
                logger.info('No SN weights to save')
            sn_data.to_parquet(path + '_params' + '.parquet')

            try:
                cov_mat = f4.minz.get_cov_matrix()[0]
                cov_reduced = cov_mat[:4 * len(self.tds.sn_data), :4 * len(self.tds.sn_data)]
                ii = [self.tds.sn_data.sn_index + i * len(self.tds.sn_data) for i in range(4)]
                iii = np.hstack(ii)
                cov_reduced = cov_reduced[:, iii][iii]
                np.save(path + '_cov' + '.npy', cov_reduced.toarray())
            except CholmodNotPositiveDefiniteError:
                logger.error(f"Hessian is not positive definite. I save H for degguging.")
                llk, grad, H = f4.ll(f4.ll.pars.free, deriv=True)
                H_reduced = H[:4 * len(self.tds.sn_data), :4 * len(self.tds.sn_data)]
                ii = [self.tds.sn_data.sn_index + i * len(self.tds.sn_data) for i in range(4)]
                iii = np.hstack(ii)
                H_reduced = H_reduced[:, iii][iii]
                np.save(path + '_H' + '.npy', H_reduced.toarray())

    def train_salt2_model_simple(self, save=False, path=None):
        """
        Model training without any error models
        """
        first_fixed_pars = ['M0', 'M1', 'CL']

        ll = LogLikelihood(self.model)
        f0 = FitResults(pars=ll.pars)
        f0.ll = ll
        f0.v = self.model(f0.pars)
        f0.var_v = None
        self.log.append(f0)

        # initialization : fit the light curves and spectra
        f1 = self.fit(fix=first_fixed_pars,
                      fit_variance_model=False,
                      force_spec_recalibration=True,
                      max_iter=10)
        self.log.append(f1)

        # full fit
        f2 = self.fit(fix=None,
                      fit_variance_model=False,
                      p_init=f1.ll.pars,
                      max_iter=100)
        f2.v_var = np.zeros(len(f2.v))
        self.log.append(f2)

        if save and path is not None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            sn_data = pandas.DataFrame(data=self.tds.sn_data.nt)
            columns_rename = {'x0':'x0_init', 'x1':'x1_init', 'c':'c_init', 'tmax':'tmax_init'}
            sn_data = sn_data.rename(columns = columns_rename)
            sn_data = sn_data.assign(x0 = f2.pars['X0'].full[self.tds.sn_data.sn_index])
            sn_data = sn_data.assign(x1 = f2.pars['X1'].full[self.tds.sn_data.sn_index])
            sn_data = sn_data.assign(c = f2.pars['c'].full[self.tds.sn_data.sn_index])
            sn_data = sn_data.assign(t0 = f2.pars['tmax'].full[self.tds.sn_data.sn_index])
            sn_data.to_parquet(path + '_params' + '.parquet')
            try:
                cov_mat = f2.minz.get_cov_matrix()[0]
                cov_reduced = cov_mat[:4 * len(self.tds.sn_data), :4 * len(self.tds.sn_data)]
                ii = [self.tds.sn_data.sn_index + i * len(self.tds.sn_data) for i in range(4)]
                iii = np.hstack(ii)
                cov_reduced = cov_reduced[:, iii][iii]
                np.save(path + '_cov' + '.npy', cov_reduced.toarray())
            except CholmodNotPositiveDefiniteError:
                logger.error(f"Hessian is not positive definite. I save H for degguging.")
                llk, grad, H = f2.ll(f2.ll.pars.free, deriv=True)
                H_reduced = H[:4 * len(self.tds.sn_data), :4 * len(self.tds.sn_data)]
                ii = [self.tds.sn_data.sn_index + i * len(self.tds.sn_data) for i in range(4)]
                iii = np.hstack(ii)
                H_reduced = H_reduced[:, iii][iii]
                np.save(path + '_H' + '.npy', H_reduced.toarray())

    def train_salt2_model_test(
            self,
            save=False,
            path=None,
            max_iter=(50, 100, 100)):
        """Model training without any error models

        Notes
        -----
        The `max_iter` argument is usefull mainly to reduce computation while
        testing. If an integer, the same max_iter if used for the 3 fits. If a
        sequence, must be of length 3 to specify a distinct max_iter for the 3
        fits.

        """
        if not isinstance(max_iter, collections.abc.Sequence):
            max_iter = [max_iter]
        if len(max_iter) not in (1, 3):
            raise ValueError(
                'max_iter must be an integer or a triplet of integers')
        if len(max_iter) == 1:
            max_iter = list(max_iter) * 3

        first_fixed_pars = [
            'M0', 'M1', 'CL', 'gamma_sn', 'gamma_snake']
        full_pars = [
            'X0', 'X1', 'c', 'tmax', 'M0', 'M1', 'CL', 'SpectrumRecalibration']

        ll = LogLikelihood(self.model)
        f0 = FitResults(pars=ll.pars)
        f0.ll = ll
        f0.v = self.model(f0.pars)
        f0.var_v = None
        self.log.append(f0)

        # f2 = self.fit(
        #     fix=full_pars,
        #     fit_variance_model=True,
        #     force_spec_recalibration=True,
        #     max_iter=100)
        # self.log.append(f2)

        # initialization : fit the light curves and spectra
        f1 = self.fit(
            fix=first_fixed_pars,
            fit_variance_model=True,
            force_spec_recalibration=True,
            max_iter=max_iter[0])
        self.log.append(f1)

        # full fit
        f2 = self.fit(
            fix=full_pars,
            fit_variance_model=True,
            p_init=f1.ll.pars,
            max_iter=max_iter[1])
        # f2.v_var = np.zeros(len(f2.v))
        self.log.append(f2)

        f3 = self.fit(
            fix=['gamma_sn', 'gamma_snake'],
            fit_variance_model=True,
            p_init=f2.ll.pars,
            max_iter=max_iter[2])
        # f2.v_var = np.zeros(len(f2.v))
        self.log.append(f3)

        # f4 = self.fit(
        #     fix=None,
        #     fit_variance_model=True,
        #     p_init=f3.ll.pars,
        #     max_iter=100)
        # f2.v_var = np.zeros(len(f2.v))
        # self.log.append(f4)

        if save and path is not None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            sn_data = pandas.DataFrame(data=self.tds.sn_data.nt)
            sn_data = sn_data.rename(columns={
                'x0': 'x0_init',
                'x1': 'x1_init',
                'c': 'c_init',
                'tmax': 'tmax_init'})

            sn_index = self.tds.sn_data.sn_index
            sn_data = sn_data.assign(x0=f3.pars['X0'].full[sn_index])
            sn_data = sn_data.assign(x1=f3.pars['X1'].full[sn_index])
            sn_data = sn_data.assign(c=f3.pars['c'].full[sn_index])
            sn_data = sn_data.assign(t0=f3.pars['tmax'].full[sn_index])
            sn_data.to_parquet(path + '_params' + '.parquet')

            try:
                cov_mat = f3.minz.get_cov_matrix()[0]
                cov_reduced = cov_mat[
                    :4 * len(self.tds.sn_data),
                    :4 * len(self.tds.sn_data)]
                iii = np.hstack(
                    [sn_index + i * len(self.tds.sn_data) for i in range(4)])
                cov_reduced = cov_reduced[:, iii][iii]

                covmatrix_file = path + '_cov' + '.npy'
                np.save(covmatrix_file, cov_reduced.toarray())
                logger.info('saved covariance matrix to %s', covmatrix_file)
            except CholmodNotPositiveDefiniteError:
                logger.error("Hessian is not positive definite.")
                _, _, H = f3.ll(f3.ll.pars.free, deriv=True)
                H_reduced = H[
                    :4 * len(self.tds.sn_data),
                    :4 * len(self.tds.sn_data)]
                iii = np.hstack(
                    [sn_index + i * len(self.tds.sn_data) for i in range(4)])
                H_reduced = H_reduced[:, iii][iii]

                hessian_file = path + '_H' + '.npy'
                np.save(hessian_file, H_reduced.toarray())
                logger.info('saved non posdef hessian to %s', hessian_file)

    def initial_log(self, init_M0=None, init_M1=None, init_CL=None, init_x0=None, init_x1=None, init_c=None, init_tmax=None):
        """
        Initialising a trainer
        """
        ll = LogLikelihood(self.model)
        ll.pars['SpectrumRecalibration'].full[3::4] = np.log(self.spec_recal_init)
        if init_M0 is not None:
            ll.pars['M0'].full[:] = init_M0
        if init_M1 is not None:
            ll.pars['M1'].full[:] = init_M1
        if init_CL is not None:
            ll.pars['CL'].full[:] = init_CL
        if init_x0 is not None:
            ll.pars['X0'].full[self.tds.sn_data.sn_index] = init_x0
        if init_x1 is not None:
            ll.pars['X1'].full[self.tds.sn_data.sn_index] = init_x1
        if init_c is not None:
            ll.pars['c'].full[self.tds.sn_data.sn_index] = init_c
        if init_tmax is not None:
            ll.pars['tmax'].full[self.tds.sn_data.sn_index] = init_tmax

        f0 = FitResults(pars=ll.pars)
        f0.ll = ll
        f0.v = self.model(f0.pars)
        f0.var_v = None
        self.log.append(f0)

    def fit_err_model_test(self):
        """light curve fitting plus error model
        """
        full_pars_blocks = ['M0', 'M1', 'CL', 'X0', 'X1', 'c', 'tmax']
        if self.tds.spec_data is not None:
            full_pars_blocks.append('SpectrumRecalibration')
        # initialization: PETS sncosmo/salt2 fits
        ll = LogLikelihood(self.model)
        f0 = FitResults(pars=ll.pars, v=self.model(ll.pars), var_v=None)
        f0.ll = LogLikelihood(self.model)
        self.log.append(f0)

        # initialization : fit the light curves and spectra
        # no error model
        f1 = self.fit(fix=['M0', 'M1', 'CL'],
                      fit_variance_model=False,
                      force_spec_recalibration=True,
                      max_iter=10)
        self.log.append(f1)

        # fit an error model, all other pars fixed
        f2 = self.fit(fix=full_pars_blocks,
                      fit_variance_model=True,
                      p_init=f1.ll.pars,
                      p_init_blocks={'gamma': -5.},
                      max_iter=10)
        self.log.append(f2)

        # refit the light curves and spectra,
        # with an error model
        f3 = self.fit(fix=['M0', 'M1', 'CL'],
                      fit_variance_model=True,
                      p_init=f2.ll.pars,
                      max_iter=10)
        self.log.append(f3)

        # train
        #f4 = self.fit(variance_model=True,
        #              p_init=f3.ll.pars)
        #self.log.append(f4)

    def _clean_dataset(self, tds, phase_range=(-20., +50.)):
        """
        """
        # clean ZTF19adcecwu
        # TODO: protocol to clean manually identified datapoints
        # idx = (tds.lc_data.sn == 'ZTF19adcecwu') & (tds.lc_data.mjd > 58840) & (tds.lc_data.flux<10000.)
        # logger.info(f'removing {idx.sum()} outliers identified on ZTF19adcecwu g- and r- DR2 lightcurves')
        # tds.lc_data.valid[idx] = 0

        # phase range (photometric data)
        tmax = np.zeros(len(tds.sn_data))
        tmax[tds.sn_data.sn_index] = tds.sn_data.tmax
        phot_tmax = tmax[tds.lc_data.sn_index]
        phase = (tds.lc_data.mjd - phot_tmax) / (1. + tds.lc_data.z)

        idx = (phase<phase_range[0]) | (phase>phase_range[1])
        logger.info(f'removing {idx.sum()} photometric points outside phase range')
        tds.lc_data.valid[idx] = 0

        # phase range (spectra)
        spec_tmax = tmax[tds.spec_data.sn_index]
        phase = (tds.spec_data.mjd - spec_tmax) / (1. + tds.spec_data.z)
        idx = (phase<phase_range[0]) | (phase>phase_range[1])
        logger.info(f'removing {idx.sum()} spectroscopic points outside phase range')
        tds.spec_data.valid[idx] = 0

        # points of the edge of the wavelength basis
        # no: this version does not what we want to do
        # i_basis_max = tds.spec_data.i_basis.max()
        # idx = (tds.spec_data.i_basis < 3) | (tds.spec_data.i_basis >= (i_basis_max-3))
        #
        # we need to determine, for each spectrum, the i_basis_min and i_basis_max
        b_bins = np.arange(-0.5, tds.spec_data.i_basis.max() + 1.5, 1)
        s_bins = np.arange(-0.5, tds.spec_data.spec_index.max() + 1.5, 1)
        h, _, _ = np.histogram2d(tds.spec_data.i_basis, tds.spec_data.spec_index, bins=(b_bins, s_bins))
        bb = np.arange(0, tds.spec_data.i_basis.max() + 1, 1)
        ss = np.arange(0, tds.spec_data.spec_index.max() + 1, 1)
        bb, ss = np.meshgrid(bb, ss)
        u = bb * h.T
        mb = ma.masked_array(u, mask=u==0.)
        b_min, b_max = np.array(np.min(mb, axis=1)), np.array(np.max(mb, axis=1))
        to_kill  = np.array(b_min).astype(int)[tds.spec_data.spec_index] == tds.spec_data.i_basis
        to_kill |= np.array(b_max).astype(int)[tds.spec_data.spec_index] == tds.spec_data.i_basis

        logger.info(f'removing {np.sum(to_kill)} spectroscopic points outside wavelength range')
        tds.spec_data.valid[to_kill] = 0


        # I think that most of the above, can be replace with this line
        valid = salt2.SALT2Like.flag_out_of_range_datapoints(tds, compress=True)

        # remove the spectral points with an uncertainty larger than 1.E6

        # clean all SNe below 0.02
        #idx = (tds.lc_data.z < 0.01)
        #logger.info(f'removing {idx.sum()} very low redshift SNe')
        #tds.lc_data.valid[idx] = 0

        # tds.compress()

    def _recalib_spectra(self, tds, v):
        """rough recalibration of the spectra
        """
        vv = v[len(tds.lc_data):]
        ii = np.arange(len(vv))
        idx = np.abs(tds.spec_data.fluxerr / tds.spec_data.flux) < 1.
        zero_fluxerr = np.abs(tds.spec_data.fluxerr) <= 0.
        logger.info(f'ignoring {zero_fluxerr.sum()} points with buggy flux errs')
        idx &= ~zero_fluxerr
        neg_flux = tds.spec_data.flux <= 0.
        idx &= ~neg_flux

#        fig, axes = pl.subplots(nrows=3, ncols=1, figsize=(8, 10),
#                                sharex=True)
#        axes[0].errorbar(ii[idx], tds.spec_data.flux[idx],
#                         yerr=tds.spec_data.fluxerr[idx], ls='', marker='.')
#        axes[0].plot(ii[idx], vv[idx], marker='.', color='r')
        ii = vv[idx] == 0.
        r = np.abs(tds.spec_data.flux[idx][~ii] / vv[idx][~ii])
        r_err = tds.spec_data.fluxerr[idx][~ii] / np.abs(vv[idx][~ii])
#        axes[1].plot(ii[idx], r[idx],
#                     ls='', marker='.')

        w = 1. / r_err**2
        n = np.bincount(tds.spec_data.spec_index[idx][~ii], weights=(w*r))
        d = np.bincount(tds.spec_data.spec_index[idx][~ii], weights=w)
        recal = n / d

        v_recal = vv * recal[tds.spec_data.spec_index]

        #axes[2].errorbar(ii[idx], tds.spec_data.flux[idx],
        #                 yerr=tds.spec_data.fluxerr[idx], ls='', marker='.')
#        axes[2].plot(ii[idx], tds.spec_data.flux[idx],
#                     ls='', marker='.')
#        axes[2].plot(ii[idx], v_recal[idx], ls='', marker='.', color='r')

        return recal

    def _get_models_to_plot(self, numfit, pars):
        """
        """
        fits = []

        if numfit is not None:
            try:
                iter(numfit)
                fits.extend(self.log[i] for i in numfit)
            except:
                fits.append(self.log[numfit])

        if pars is not None:
            try:
                iter(pars)
                for p in pars:
                    ff = FitResults(pars=pars, v=self.model(pars))
                    if self.variance_model:
                        ff.var_v = self.variance_model(pars)
                    fits.append(ff)
            except:
                ff = FitResults(pars=pars, v=self.model(pars))
                if self.variance_model:
                    ff.var_v = self.variance_model(pars)
                fits.append(ff)

        return fits


    def plot_lc(self, sn, numfit=None, pars=None,
                phase=False, norm=1.,
                plot_variance=False):
        """plot light curve data + models

        Parameters
        ----------
        sn : (int | str)
          the supernova to plot
        numfit : int, optional
          which fit to plot (drawn from logs)
        pars : FitParameters, optional
          plot an alternate fit, not from self.log
        phase : bool, default False
          whether to plot the the light curve as a function of the phase
        plot_variance : bool, default=False
          whether to plot the error model, if available

        Returns
        -------
        None
        """
        sel = self.tds.lc_data.sn == sn
        bands = np.unique(self.tds.lc_data.band[sel]).tolist()
        bands.sort(key=_get_band_order)
        nrows = len(bands)

        sn_idx = self.tds.sn_data.sn == sn
        tmax = float(self.tds.sn_data.tmax[sn_idx])
        z = float(self.tds.sn_data.z[sn_idx])
        sn_index = int(self.tds.sn_data.sn_index[sn_idx])

        # clone the dataset
        t = clone(self.tds, sn)
        to_plot = self._get_models_to_plot(numfit, pars)
        m = salt2.get_model(t, dust_extinction_model=self.extinction)
        if self.variance_model is not None:
            vm = self.variance_model.__class__(m)
        else:
            vm = None
        plotters = [ModelPlotter(m, sn_index, tp.ll.pars, variance_model=vm) \
                    for tp in to_plot]

        # plots
        fig, axes = plt.subplots(nrows=nrows, ncols=1,
                                figsize=(8,12),
                                sharex=True)
        for i,b in enumerate(bands):
            idx = sel & (self.tds.lc_data.band == b)
            wl = self.tds.lc_data.wavelength[idx].mean()
            color = plt.cm.jet(int((wl-2000)/(11000.-2000.) * 256))

            if phase:
                xx = (self.tds.lc_data.mjd[idx] - tmax) / (1. + z)
                axes[i].axvline(0., ls=':')
            else:
                xx = self.tds.lc_data.mjd[idx]
                axes[i].axvline(tmax, ls=':')

            # we plot the calibrated fluxes. Therefore, we rescale them, using
            # the zero points reported with each flux measurement in the TrainingDataset
            axes[i].errorbar(xx, self.tds.lc_data.flux[idx] * np.power(10, -0.4*self.tds.lc_data.zp[idx]),
                             yerr=self.tds.lc_data.fluxerr[idx] * np.power(10, -0.4*self.tds.lc_data.zp[idx]),
                             ls='', marker='.', color=color)

            for p in plotters:
                p.plot(b, ax=axes[i],
                       color=color,
                       phase=phase,
                       ylabel=b)
            if phase:
                axes[-1].set_xlabel('mjd [days]')
            else:
                axes[-1].set_xlabel('phase [restframe days]')
            plt.subplots_adjust(hspace=0.05)
            fig.suptitle(f'{sn} @ z={z:4.3}')

    def plot_spec(self, spec, numfit=None, pars=None, alpha=0.5):
        """
        """
        sel = self.tds.spec_data.spec == spec

        fig, axes = plt.subplots(nrows=1, ncols=1,
                                figsize=(8,8),
                                sharex=True)

        axes.errorbar(self.tds.spec_data.wavelength[sel], self.tds.spec_data.flux[sel],
                      yerr=self.tds.spec_data.fluxerr[sel],
                      ls='', marker='.', color='blue')

        to_plot = self._get_models_to_plot(numfit, pars)
        for tp in to_plot:
            vv = tp.v[len(self.tds.lc_data):][sel]
            axes.plot(self.tds.spec_data.wavelength[sel], vv, 'r+:')
            if tp.v_var is not None:
                vv_var = tp.v_var[len(self.tds.lc_data):][sel]
                vmin = vv - np.sqrt(vv_var)
                vmax = vv + np.sqrt(vv_var)
                axes.fill_between(self.tds.spec_data.wavelength[sel],
                                  vmin, vmax,
                                  color='r', alpha=alpha)

        axes.set_ylabel('flux')
        axes.set_xlabel('mjd')

        sn = np.unique(self.tds.spec_data.sn[sel])
        assert len(sn) == 1
        sn = sn[0]
        z = np.unique(self.tds.spec_data.z[sel])
        assert len(z) == 1
        z = z[0]
        axes.set_title(f'{sn} @ z={z:4.3}')
        plt.subplots_adjust(hspace=0.05)

    def plot_control(self, path=None):
        """
        """
        if self.color_scatter:
            control_plot.plot_cs_variance(self.tds, self.log[-1].pars, self.log[-1].ll.priors[-1])
            control_plot.plot_cs_cl(self.tds, self.log, self.log[-1].ll.model.color_law)
            control_plot.plot_kappa(self.tds, self.log[-1].pars)
        else:
            control_plot.plot_cl(self.tds, self.log, self.log[-1].ll.model.color_law, path=path)
        control_plot.plot_stacked_residuals_snake(self.tds, self.log[-1].pars, self.log[-1].v, self.log[-1].v_var, path=path)
        control_plot.plot_band_residuals_z(self.tds, self.log[-1].v, self.log[-1].v_var, path=path)
        control_plot.plot_band_residuals_phase(self.tds, self.log[-1].pars, self.log[-1].v, self.log[-1].v_var, path=path)
        control_plot.plot_band_pulls_phase(self.tds, self.log[-1].pars, self.log[-1].v, self.log[-1].v_var, path=path)

    def cut_lc_outliers(self, pars, nsig=10):
        """
        """
        v = self.model(pars)
        if self.variance_model is not None and 'gamma' in pars._struct.slices:
            var_v = self.variance_model(pars)
        else:
            var_v = None

        vv = v[:len(self.tds.lc_data)]
        if var_v is not None:
            var_vv = var_v[:len(self.tds.lc_data)]
        else:
            var_vv = None

        bands = np.unique(self.tds.lc_data.band)
        nbands = len(bands)

        for i,band in enumerate(bands):
            sel = self.tds.lc_data.band == band
            var = self.tds.lc_data.fluxerr**2
            if var_vv is not None:
                var += var_vv
            w = 1. / var
            res = vv - self.tds.lc_data.flux
            wres = np.sqrt(w) * res

            cut = (np.abs(wres) > nsig)
            cc = cut[sel]
            logger.info(f'cutting {cc.sum()}/{len(cc)}={100*cc.sum()/len(cc):4.3}% outliers in {band}')
            self.tds.lc_data.valid[sel] = (~cut)[sel]

            jj = (~cut)[sel]
            print(jj.sum(), self.tds.lc_data.valid[sel].sum(), len(self.tds.lc_data.valid[sel]))


    def plot_lc_training_residuals(self, pars, v=None, var_v=None,
                                   phases=False,
                                   weighted_residuals=False,
                                   hexbin=False):
        """global fit residuals
        """
        if not v:
            v = self.model(pars)
        if not var_v and self.variance_model is not None and 'gamma' in pars._struct.slices:
            var_v = self.variance_model(pars)

        vv = v[:len(self.tds.lc_data)]
        if var_v is not None:
            var_vv = var_v[:len(self.tds.lc_data)]
        else:
            var_vv = None

        tmax = pars['tmax'].full[self.tds.lc_data.sn_index]
        z = self.tds.lc_data.z

        bands = np.unique(self.tds.lc_data.band)
        nbands = len(bands)
        fig, axes = plt.subplots(figsize=(6,12),
                                nrows=nbands, ncols=2,
                                sharex=0, sharey=1,
                                gridspec_kw={'width_ratios': [3,1]})
        for i, band in enumerate(bands):
            sel = self.tds.lc_data.band == band
            wl = self.tds.lc_data.wavelength[sel].mean()
            color = plt.cm.jet(int((wl-2000)/(11000.-2000.) * 256))
            if phases:
                x = (self.tds.lc_data.mjd - tmax) / (1. + z)
            else:
                x = np.arange(len(sel))

            var = self.tds.lc_data.fluxerr**2
            if var_vv is not None:
                var += var_vv
            w = 1. / var
            res = vv - self.tds.lc_data.flux
            wres = np.sqrt(w) * res
            y = wres if weighted_residuals else res
            if hexbin:
                axes[i,0].hexbin(x[sel], y[sel],
                                 gridsize=(100, 500),
                                 extent=(-30, 50, -100, 100),
                                 mincnt=1)
            else:
                axes[i,0].plot(x[sel], y[sel],
                               # yerr=tds.lc_data.fluxerr[sel],
                               ls='', marker='.', color=color)
            axes[i,1].hist(y[sel], bins=500,
                           color=color,
                           density=True,
                           # orientation='vertical')
                           )

            # if var_vv is not None:
            #    ii = np.argsort(x[sel])
            # axes[i].fill_between(x[sel][ii], -np.sqrt(var_vv[sel][ii]), np.sqrt(var_vv[sel][ii]),
            #                      alpha=0.25, color=color)
            axes[i,0].set_ylabel(band)
        axes[-1,0].set_xlabel('phases [days]' if phases else 'index')
        plt.subplots_adjust(hspace=0.01, wspace=0.01)

        return v, var_v


    def plot_spec_training_residuals(self, pars, v=None, var_v=None):
        """global fit residuals
        """
        if not v:
            v = self.model(pars)
        if not var_v and self.variance_model is not None and 'gamma' in pars._struct.slices:
            var_v = self.variance_model(pars)

        vv = v[len(self.tds.lc_data):]
        if var_v is not None:
            var_vv = var_v[len(self.tds.lc_data):]
        else:
            var_vv = None

        sel = self.tds.spec_data.valid

        tmax = pars['tmax'].full[self.tds.spec_data.sn_index]
        z = self.tds.spec_data.z
        phases = (self.tds.spec_data.mjd - tmax) / (1. + z)

        fig, axes = plt.subplots(nrows=1, ncols=1)
        # color = plt.cm.jet(int(phases/(50+25) * 256))
        x = self.tds.spec_data.wavelength
        ii = np.argsort(x)
        axes.errorbar(x[sel], vv[sel] - self.tds.spec_data.flux[sel],
                      yerr=self.tds.spec_data.fluxerr[sel],
                      ls='', marker=',', color='gray')
        #        if var_vv is not None:
        #            axes[i].fill_between(x[sel][ii], -np.sqrt(var_vv[sel][ii]), np.sqrt(var_vv[sel][ii]),
        #                                 alpha=0.25, color='gray')
        axes.set_xlabel(r'wavelength [$\AA$]')
        plt.subplots_adjust(hspace=0.05)

        return v, var_v


    def plot_lightcurves(self, pars, v=None, var_v=None, phases=False):
        """global fit residuals
        """
        if not v:
            v = self.model(pars)
        if not var_v and self.variance_model is not None and 'gamma' in pars._struct.slices:
            var_v = self.variance_model(pars)

        vv = v[:len(self.tds.lc_data)]
        if var_v is not None:
            var_vv = var_v[:len(self.tds.lc_data)]
        else:
            var_vv = None

        tmax = pars['tmax'].full[self.tds.lc_data.sn_index]
        z = self.tds.lc_data.z

        bands = np.unique(self.tds.lc_data.band)
        nbands = len(bands)
        fig, axes = plt.subplots(nrows=nbands, ncols=1, sharex=phases)
        for i, band in enumerate(bands):
            sel = self.tds.lc_data.band == band
            wl = self.tds.lc_data.wavelength[sel].mean()
            color = plt.cm.jet(int((wl-2000)/(9000.-2000.) * 256))
            if phases:
                x = (self.tds.lc_data.mjd - tmax) / (1. + z)
            else:
                x = self.tds.lc_data.mjd
            ii = np.argsort(x[sel])

            axes[i].errorbar(x[sel][ii], self.tds.lc_data.flux[sel][ii],
                             yerr=self.tds.lc_data.fluxerr[sel][ii],
                             ls='', marker=',', color=color)
            axes[i].plot(x[sel][ii], vv[sel][ii],
                         ls='', marker='+', color=color)

            if var_vv is not None:
                axes[i].fill_between(x[sel][ii], vv[sel]-np.sqrt(var_vv[sel][ii]), vv[sel]+np.sqrt(var_vv[sel][ii]),
                                     alpha=0.5, color=color)
            axes[i].set_ylabel(band)
        axes[-1].set_xlabel('phases [days]' if phases else 'index')
        plt.subplots_adjust(hspace=0.05)

        return v, var_v

    def save(self, fn):
        with open(fn, 'wb') as f:
            dill.dump(self, f)

    @classmethod
    def load(cls, fn):
        with open(fn, 'rb') as f:
            return dill.load(f)


_band_ordering = {'u': 0, 'U': 0, 'g': 1, 'B': 2, 'r': 3, 'r2': 3,
                  'R': 4, 'i': 5, 'i2': 5, 'I': 6, 'z': 7, 'Y': 8}

def _get_band_order(band):
    b = band.split('::')[-1]
    return _band_ordering.get(b, 100)


def order_bands(bands):
    l = bands.sort(key=_get_band_order)
    return l


def clone(tds, sn, phase_range=(-25, 51., 1.)):
    """Create a clone of the `TrainingDataset` object for a specific supernova,
    allowing for a different (finer) sampling of the light curves.

    This function is primarily used to generate data for plotting models like
    NaCl / SALT2 over observed data points, with the option to adjust the phase
    grid of the light curves, to plot smoother models.

    Parameters:
    -----------
    tds : TrainingDataset
        The original training dataset containing the supernova data.

    sn : str
        The identifier of the supernova to clone.

    phase_range : tuple, optional
        A tuple specifying the phase range (start, end, step) for generating
        new light curve data. Default is (-25, 51, 1).

    Returns:
    --------
    TrainingDataset
        A new `TrainingDataset` object containing cloned data for the specified
        supernova. The lightcurve data is sampled over the new phase grid, and
        zero-point (zp) values are set to zero. The magnitude system is
        preserved from the original dataset.

    Notes:
    ------
    - This method verifies that all magnitudes in the lightcurve data are in the
      same magnitude system before proceeding.
    - The model predicts observer fluxes (not calibrated fluxes). In the
      plotting routine, model fluxes need to be renormalized to calibrated
      (generally AB) fluxes.
    - If any of the lightcurve, spectral, or spectrophotometric data are absent
      in the original dataset, they will be set to `None` in the cloned object.
    """
    # sn metadata
    sn_data = tds.sn_data.nt[tds.sn_data.sn == sn]

    # lightcurve data
    if tds.lc_data is not None:
        lc_data = tds.lc_data.nt[tds.lc_data.sn == sn]

        # figure out which magnitude system to use
        magsys = np.unique(lc_data.magsys)
        assert len(magsys) == 1

        tmax = float(sn_data.tmax)
        z = float(sn_data.z)
        phase = np.arange(*phase_range)
        mjd = phase * (1.+z) + tmax
        N = len(mjd)
        l = []
        for b in np.unique(lc_data.band):
            d = lc_data[lc_data.band == b]
            Z = np.full(len(mjd), d[0])
            Z['mjd'] = mjd
            Z['flux'] = 0.
            Z['fluxerr'] = 0.
            Z['valid'] = 1
            # we want the model to predict AB (normalized) fluxes
            # so, explicitely set the zero points to zero
            Z['zp'] = 0.
            Z['magsys'] = magsys[0]
            l.append(Z)
        lc_data = np.rec.array(np.hstack(l))
    else:
        lc_data = None

    if tds.spec_data is not None:
        spec_data = tds.spec_data.nt[tds.spec_data.sn == sn]
    else:
        spec_data = None
    if tds.spectrophotometric_data is not None:
        spectrophotometric_data = tds.spectrophotometric_data.nt[tds.spectrophotometric_data.sn == sn]
    else:
          spectrophotometric_data = None


    tds = TrainingDataset(sn_data, lc_data=lc_data,
                          spec_data=None,
                          spectrophotometric_data=None,
                          basis=tds.basis,
                          filterlib=tds.filterlib)

    return tds


class ModelPlotter:
    """
    A utility class to plot a smooth, oversampled photometric model along with
    its variance, if available. This is useful for visualizing the fitted model
    and its associated uncertainties over a supernova dataset.
    """
    def __init__(self, model, sn_index, init_pars, variance_model=None):
        """
        Constructor - Initializes the ModelPlotter by evaluating the model and,
        optionally, the error model.

        Parameters:
        -----------
        model : Model (e.g. `nacl.models.salt2.SALT2Like`)
            The photometric model to be plotted. It should support evaluation
            given a set of parameters.

        sn_index : int
            The index of the specific supernova for which the model is being
            plotted, used to select the appropriate parameters from the dataset.

        init_pars : dict
            A dictionary of initial parameters for the model, containing both
            global parameters (e.g., 'M0', 'M1') and supernova-specific
            parameters (e.g., 'X0', 'X1', 'c', 'tmax').

        variance_model : Model, optional
            An optional variance model. If provided, the plotter will also
            compute and display the variance (or error) bands around the model
            predictions.
        """
        self.model = model
        self.tds = model.training_dataset
        self.init_pars = init_pars
        self.variance_model = variance_model
        self._init_local_pars(init_pars, sn_index)

        # evaluate model and variance model
        self.v = self.model(self.pars)
        if variance_model is not None:
            self.v_var = self.variance_model(self.pars)
        else:
            self.v_var = None

    def _init_local_pars(self, init_pars, sn_index):
        """
        Initialize the parameter vector for the selected supernova from a global
        parameter set.

        Parameters:
        -----------
        init_pars : dict
            The initial parameter values for the model, including global and
            supernova-specific parameters.

        sn_index : int
            The index of the supernova in the dataset, used to extract the
            relevant parameters for the current supernova.

        Returns:
        --------
        pars : dict
            A dictionary of parameters specific to the current supernova,
            ready to be used in model evaluation.
        """
        if self.variance_model is not None:
            ll = LogLikelihood(self.model, variance_model=self.variance_model)
            self.pars = ll.pars.copy()
        else:
            self.pars = self.model.init_pars()

        for nm in ['M0', 'M1', 'CL']:
            self.pars[nm].full[:] = init_pars[nm].full[:]
        for nm in ['X0', 'X1', 'c', 'tmax']:
            self.pars[nm].full[0] = init_pars[nm].full[sn_index]
        if 'gamma' in init_pars._struct.slices:
            self.pars['gamma'].full[:] = init_pars['gamma'].full[:]
        if 'gamma_sn' in init_pars._struct.slices:
            self.pars['gamma_sn'].full[0] = init_pars['gamma_sn'].full[sn_index]
        if 'gamma_snake' in init_pars._struct.slices:
            self.pars['gamma_snake'].full[:] = init_pars['gamma_snake'].full[:]
        # else:
        #    self.pars['gamma'].full[:] = 0.

        return self.pars

    def plot(self, band, ax=None, **kwargs):
        """
        Plot the photometric model for a given band, optionally including the
        error model if provided.

        Parameters:
        -----------
        band : str
            The photometric band for which to plot the model (e.g., 'g', 'r').

        ax : matplotlib.axes.Axes, optional
            The matplotlib axes to plot on. If not provided, the current axes
            will be used (plt.gca()).

        **kwargs : dict, optional
            Additional plot parameters, including:
            - phase: bool, whether to plot in phase space (relative to tmax) or
              in MJD (default: False).
            - color: str, the color for the plot (default: 'b').
            - ls: str, the line style for the plot (default: ':').
            - label: str, the label for the plot (default: '').
            - xlabel: str, label for the x-axis (default: None).
            - ylabel: str, label for the y-axis (default: None).
            - title: str, title for the plot (default: None).
            - alpha: float, transparency level for the variance band (default: 0.25).
            - legend: str, location of the legend (default: None).

        Notes:
        ------
        - If a variance model is provided, shaded error bands representing
          ±1σ will be plotted around the model predictions.
        - The method plots calibrated fluxes in the magnitude system specified.
          The fluxes are scaled using the zero points (`zp`) provided in the
          dataset. Since the model predicts fluxes in observer units, it's
          crucial that the `clone()`d dataset has its `zp` values set to zero,
          ensuring that the model generates calibrated fluxes.
        - The `phase` option allows for plotting the time axis either in
          rest-frame phase (relative to tmax) or directly in modified Julian
          dates (MJD).
        """
        if not ax:
            ax = plt.gca()

        phase = kwargs.get('phase', False)
        color = kwargs.get('color', 'b')
        ls = kwargs.get('ls', ':')
        label = kwargs.get('label', '')
        xlabel= kwargs.get('xlabel', None)
        ylabel= kwargs.get('ylabel', None)
        title = kwargs.get('title', None)
        alpha = kwargs.get('alpha', 0.25)
        legend = kwargs.get('legend', None)

        tmax = float(self.tds.sn_data.tmax[0])
        z = float(self.tds.sn_data.z[0])

        idx = self.tds.lc_data.band == band
        if phase:
            xx = (self.tds.lc_data.mjd - tmax) / (1. + z)
            ax.axvline(0., ls=':')
        else:
            xx = self.tds.lc_data.mjd
            ax.axvline(tmax, ls=':')

        ax.plot(xx[idx], self.v[idx] * np.power(10, -0.4*self.tds.lc_data.zp[idx]), color=color, ls=ls, label=label)
        if self.variance_model is not None:
            vm = (self.v[idx] - np.sqrt(self.v_var[idx])) # * np.power(10, -0.4*self.tds.lc_data.zp[idx])
            vp = (self.v[idx] + np.sqrt(self.v_var[idx])) # * np.power(10, -0.4*self.tds.lc_data.zp[idx])
            ax.fill_between(xx[idx], vm, vp, alpha=0.5, color=color)

        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        if title is not None:
            ax.set_title(title)
        if legend:
            ax.legend(loc=legend)
