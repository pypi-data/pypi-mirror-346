
import logging
import pathlib
import dill

import numpy as np
import scipy
import pandas

from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
from saltworks import DataProxy
from saltworks.plottools import mad
import saltworks.linearmodels as lm

from nacl.models import salt2
from nacl.models.salt2.variancemodels import SimpleErrorSnake, LocalErrorSnake, SNLocalErrorSnake2
from nacl.models.salt2.constraints import nacl_linear_constraints
from nacl.dataset import TrainingDataset
from nacl.loglikelihood import LogLikelihood
from nacl.minimize import Minimizer
from nacl import plotting


def _to_list(x):
    return list(x) if isinstance(x, (list, tuple)) else [x]


class Chi2:
    r"""
    Computes weighted chi-squared (\(\chi^2\)) values for different data subsets
    (e.g., light curves, spectra) based on a given model and training dataset.

    Parameters
    ----------
    model : object
        A model object that provides a callable interface for generating predictions
        and contains a `training_dataset` attribute.
    pars : dict
        Parameters for evaluating the model.
    snake : callable or None
        Optional regularization function applied to the parameters.

    Attributes
    ----------
    model : object
        The model used to predict flux values.
    pars : dict
        Parameters used to evaluate the model.
    snake : callable or None
        Regularization function or None.
    tds : object
        Training dataset containing flux and flux error information.
    model_val : ndarray
        Predicted flux values from the model.
    snake_val : ndarray
        Regularization values computed from the `snake` function.
    wres : ndarray
        Weighted residuals computed as `(observed - predicted) / error`.
    """
    def __init__(self, model, pars, snake):
        """
        Initializes the Chi2 calculator with a model, parameters, and optional regularization.

        Parameters
        ----------
        model : object
            A `nacl.models.salt2.SALT2Like`-like object with a callable interface and training dataset.
        pars : dict
            Parameters for evaluating the model.
        snake : callable or None
            A regularization function applied to the parameters.

        Raises
        ------
        ValueError
            If the training dataset is missing or incompatible.
        TypeError
            If the model is not callable or if `snake` is not callable when provided.
        """
        # type checks
        if not callable(model):
            raise TypeError("The `model` must be a callable object.")
        if snake is not None and not callable(snake):
            raise TypeError("The `snake` must be a callable object or None.")

        # make sure there is a training dataset in the model
        if not hasattr(model, 'training_dataset'):
            raise ValueError("The `model` must have a `training_dataset` attribute.")

        self.model = model
        self.pars = pars
        self.snake = snake
        self.tds = model.training_dataset
        self.model_val = self.model(self.pars)
        self.snake_val = snake(pars) if snake is not None else np.zeros_like(self.model_val)
        y = self.tds.get_all_fluxes()
        ey = np.sqrt(self.tds.get_all_fluxerr()**2 + self.snake_val)
        self.wres = (y - self.model_val) / ey

    def get_sn_partial_chi2(self, phot=True, spec=False):
        r"""
        Calculates the partial chi-squared (\(\chi^2\)) values for supernovae (SN).

        Parameters
        ----------
        phot : bool, optional
            If True, includes photometric data in the calculation. Default is True.
        spec : bool, optional
            If True, includes spectroscopic data in the calculation. Default is False.

        Returns
        -------
        ndarray
            An array of \(\chi^2\) values normalized per supernova
            (indexed by `tds.sn_data.sn_index`, i.e. the continuous
            SN indexes maintained by the `TrainingDatset`)
        """
        nsn = len(self.tds.sn_data.sn_set)
        num = np.zeros(nsn)
        den = np.zeros_like(num)
        if phot:
            sn_index = self.tds.lc_data.sn_index
            offset = len(sn_index)
            num += np.bincount(sn_index, weights=self.wres[:offset]**2,
                               minlength=nsn)
            den += np.bincount(sn_index, minlength=nsn)
        if spec:
            sn_index = self.tds.spec_data.sn_index
            offset = len(sn_index)
            num += np.bincount(sn_index, weights=self.wres[offset:]**2,
                               minlength=nsn)
            den += np.bincount(sn_index, minlength=nsn)
        return num / den

    def get_lc_partial_chi2(self):
        r"""
        Calculates the partial chi-squared (\(\chi^2\)) values for light curves (LC).

        Returns
        -------
        ndarray
            An array of \(\chi^2\) values normalized per light curve, indexed
            as a function of `tds.lc_data.lc_index`, i.e. the continuous
            light curve index maintained by the `TrainingDataset`
        """
        lc_index = self.tds.lc_data.lc_index
        offset = len(lc_index)
        num = np.bincount(lc_index, weights=self.wres[:offset]**2)
        den = np.bincount(lc_index)
        return num / den

    def get_spec_partial_chi2(self):
        r"""
        Calculates the partial chi-squared (\(\chi^2\)) values for spectra.

        Returns
        -------
        ndarray
            An array of \(\chi^2\) values normalized per spectrum, indexed
            as a function of `tds.spec_data.spec_index`, i.e. the unique
            continuous spectrum index maintained by the `TrainingDataset`.
        """
        spec_index = self.tds.spec_data.spec_index
        offset = len(self.tds.lc_data) if self.tds.lc_data is not None else 0
        num = np.bincount(spec_index, weights=self.wres[offset:]**2)
        den = np.bincount(spec_index)
        return num / den


class TrainingCycle:
    """Template for a training step.
    """
    def __init__(self, model, pars, **kwargs):
        """Generic constructor
        """
        # we keep a handle on the initial model, tds and pars
        # passed to the class
        self.initial_model = model
        self.initial_pars = pars
        self.initial_tds = model.training_dataset

        # these are the actual model and tds operated by the class. By default,
        # they are just handles on the initial model and tds passed to the
        # constructor. If any of these have to be changed, then, they need to be
        # duplicated in the constructor of the actual class
        self.model = model
        self.tds = model.training_dataset

        # trainings generally differ by these
        self.snake = None
        self.static_snake = None
        self.cons = None
        self.regularization = None

        self.compute_covmat = kwargs.get('compute_covmat', False)

    def _sort_sne_by_chi2(self, phot=True, spec=True):
        """
        """
        chi2 = Chi2(self.model, self.pars, self.snake)
        c = chi2.get_sn_partial_chi2(phot=phot, spec=spec)
        i = np.argsort(c)
        return i, c

    def _sort_lcs_by_chi2(self):
        """
        """
        chi2 = Chi2(self.model, self.pars, self.snake)
        c = chi2.get_lc_partial_chi2()
        i = np.argsort(c)
        return i, c

    def _sort_spectra_by_chi2(self):
        """
        """
        chi2 = Chi2(self.model, self.pars, self.snake)
        c = chi2.get_spec_partial_chi2()
        i = np.argsort(c)
        return i, c

    def update_global_pars(self, blocks, pars):
        """update blocks of the parameter vector
        """
        for blk in blocks:
            self.pars[blk].full[:] = pars[blk].full

    def update_sn_pars(self, blocks, tds, pars):
        """Update blocks of the parameter vector that contain local (SN) parameters

        The model parameters may be divided in two classes: the global (model)
        parameters and local (SN-related) parameters. The structure of the local
        parameter blocks (i.e. which SN is stored at which index) may change if
        supernovae have been discarded or if the DataProxy has been re-indexed.
        """
        for blk in blocks:
            d = dict(zip(tds.sn_data.sn_set, pars[blk].full[tds.sn_data.sn_index]))
            self.pars[blk].full[:] = 0.
            for sn in self.tds.sn_data.sn_set:
                self.pars[blk].full[self.tds.sn_data.sn_map[sn]] = d[sn]

    def update_spec_block_pars(self, blocks, tds, pars, size):
        """Update blocks of the parameter vector
        """
        for blk in blocks:
            p = pars[blk].full
            spec_set = tds.spec_data.spec_set
            d = dict(zip(tds.spec_data.spec_set,
                         [p[i*size:(i+1)*size] for i in np.arange(len(spec_set))]))
            self.pars[blk].full[:] = 0.
            for spec in self.tds.spec_data.spec_set:
                i = self.tds.spec_data.spec_map[spec]
                self.pars[blk].full[i*size:(i+1)*size] = d[spec]

    def plot_lcs(self, sn_index=None, sn=None, which='worst_sne', nsn=3,
                 residuals=False, pulls=False, savefig=None):
        """Plot a selection of SN lightcurves
        """
        if sn_index is not None:
            selection = _to_list(sn_index)
            nsn = len(selection)
        elif sn is not None:
            to_plot = _to_list(sn)
            selection = [self.tds.sn_data.sn_map[i] for i in to_plot]
            nsn = len(selection)
        elif which is None:
            selection = np.random.choice(self.tds.sn_data.sn_index, nsn)
        elif 'sne' in which:
            sn_index, c = self._sort_sne_by_chi2(phot=True, spec=False)
            self.debug = [sn_index, c]
            if 'worst' in which:
                selection = sn_index[-nsn:][::-1].tolist()
            elif 'best' in which:
                selection = sn_index[:nsn].tolist()
            elif 'med' in which:
                selection = sn_index[int(nsn/2):int(nsn/2)+nsn].tolist()
        else:
            selection = np.random.choice(self.tds.sn_data.sn_index, nsn)

        nrows = int(np.floor(np.sqrt(nsn)))
        ncols = int(np.ceil(nsn / nrows))
        fig, axes = plt.subplots(figsize=(4*ncols, 4*nrows), nrows=nrows, ncols=ncols, sharex=True)
        for i,ax in enumerate(np.ravel(axes)):
            if i >= len(selection):
                break
            plotting.lightcurves.plot_sn_lightcurves_compact(
                self.model, self.pars, snake=self.snake,
                static_snake=self.static_snake,
                sn_index=selection[i],
                phase=True,
                residuals=residuals, pulls=pulls,
                ax=ax)

        if savefig is not None and isinstance(savefig, str):
            fig.savefig(savefig, bbox_inches='tight')

    def plot_spectra(self, sn_index=None, sn=None, spec_index=None, which='worst_spec',
                     nspec=3, residuals=False, pulls=False, savefig=None):
        """Plot a selection of spectra
        """
        if sn_index is not None:
            sn_index_selection = _to_list(sn_index)
            idx = np.isin(self.tds.spec_data.sn_index, sn_index_selection)
            spec_selection = np.unique(self.tds.spec_data.spec_index[idx])
            nspec = len(spec_selection)
        elif sn is not None:
            sn_selection = _to_list(sn)
            idx = np.isin(self.tds.spec_data.sn, sn_selection)
            spec_selection = np.unique(self.tds.spec_data.spec_index[idx])
            nspec = len(spec_selection)
        elif spec_index is not None:
            spec_selection = _to_list(spec_index)
        elif which is None:
            spec_selection = np.random.choice(self.tds.spec_data.spec_index, nspec)
        elif 'spec' in which:
            sn_index, c = self._sort_spectra_by_chi2()
            self.debug = [sn_index, c]
            if 'worst' in which:
                spec_selection = sn_index[-nspec:][::-1].tolist()
            elif 'best' in which:
                spec_selection = sn_index[:nspec].tolist()
            elif 'med' in which:
                spec_selection = sn_index[int(nspec/2):int(nspec/2)+nspec].tolist()
            else:
                spec_selection = np.random.choice(sn_index, nspec)

        nrows = int(np.floor(np.sqrt(nspec)))
        ncols = int(np.ceil(nspec / nrows))
        fig, axes = plt.subplots(figsize=(4*ncols, 4*nrows), nrows=nrows, ncols=ncols)
        for i,ax in enumerate(np.ravel(axes)):
            if i >= len(spec_selection):
                break
            plotting.spectra.plot_spectrum(
                self.model, self.pars, snake=self.snake,
                spec_index=spec_selection[i],
                residuals=residuals, pulls=pulls,
                ax=ax)

        if savefig is not None and isinstance(savefig, str):
            fig.savefig(savefig, bbox_inches='tight')

    def plot_pulls_per_band(self, savefig=None):
        """
        """
        plotting.lightcurves.plot_lc_pulls_per_band(self.tds,
                                                    self.model,
                                                    self.pars,
                                                    self.snake)

        if savefig is not None and isinstance(savfig, str):
            plt.savefig(savefig, bbox_inches='tight')

    def plot_model_comparison(self):
        """
        """
        pass

    def __call__(self):
        """
        """
        raise NotImplementedError('Base TrainingCycle.__call__ method is not implemented')

    def plot(self, output_dir=None):
        """
        """
        raise NotImplementedError('Base TrainingCycle.plot method is not implemented ')

    def save(self, output):
        """
        """
        assert isinstance(output, (pathlib.Path, str))
        output = pathlib.Path(output)
        if not output.parent.is_dir():
            output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, 'wb') as f:
            dill.dump(self, f)


class CleanDataset(TrainingCycle):
    """Initial dataset cleaning
    """
    def __init__(self, model, pars,
                 dr2_kwargs={'z_min':dict({"SNLS":0.2, "HSC":0.2, "snls":0.2, "hsc":0.2}),
                             'n_bands_min': 2,
                             'n_points_min': 5,
                             'spec_phase_range':(-20., 50.),
                             'spec_wavelength_range':(2000., 11000.)},
                 recalib_deg=3,
                 flag_catastrophic_outliers=False,
                 use_truth=False,
                 **kwargs):
        """
        """
        super().__init__(model, pars, **kwargs)
        self.tds = self.initial_tds.copy()
        self.tds.compress()
        self.model = self.initial_model.clone(self.tds)
        self.pars = self.model.init_pars(use_truth=use_truth)
        self.recalib_deg = recalib_deg
        self.use_truth = use_truth
        self.flag_catastrophic_outliers = flag_catastrophic_outliers
        self.dr2_kwargs = dr2_kwargs

    def __call__(self):
        """ Apply cuts
        """
        # nacl cuts : todo decide if it is of interest elsewhere
        lc, sp, spphot = salt2.SALT2Like.flag_out_of_range_datapoints(self.tds,
                                                                      update=True,
                                                                      compress=False)
        self._log('Out of Range', lc, sp, spphot)

        self.compress()
        self._recalib_and_clean_spectra()
        if self.flag_catastrophic_outliers:
            self._flag_outliers()
            self.compress()

        # build a minipets dataset
        if self.dr2_kwargs:
            from minipets import Dataset as PetsDataset
            pets_tds = PetsDataset.from_nacl(self.tds)
            pets_tds.filter_data(**self.dr2_kwargs)
            self.tds = pets_tds.get_tds()
        self.compress()
        self._update_spectrum_recalibration_pars()
        self.v = self.model(self.pars)

    def compress(self):
        logging.info('compressing and re-instantiating model and pars')
        self.tds.compress()
        self.model = self.model.clone(self.tds)
        self.pars = self.model.init_pars(use_truth=self.use_truth)

    def build_jacobian_matrix(self, rwl, spec_index, deg):
        n_meas = len(rwl)
        u_spec_index = np.unique(spec_index)
        n_spectra = len(u_spec_index)
        n_pars = n_spectra * (deg + 1)
        i, j, v = [], [], []
        for spidx in u_spec_index:
            idx = spec_index == spidx
            J = scipy.sparse.coo_matrix(np.vander(rwl[idx], deg+1))
            nz = np.nonzero(idx)[0]
            i.append(J.row + nz.min())
            offset = (deg+1) * spidx
            j.append(J.col + offset)
            v.append(J.data)

        i = np.hstack(i)
        j = np.hstack(j)
        v = np.hstack(v)
        return scipy.sparse.coo_matrix((v, (i,j)),
                                       shape=(n_meas, n_pars)).tocsr()

    def _recalib_and_clean_spectra(self, nsig=20, deg=None,
                                   update_tds=True,
                                   update_pars=True):
        """rough recalibration of the spectra
        """
        logging.info('recalib and clean spectra')
        tds = self.tds
        v = self.model(self.pars)

        if deg is None:
            try:
                deg = self.model.recal_func.deg
            except:
                deg = 0

        # clean the spectral data
        spec_offset = len(tds.lc_data)
        vv = v[spec_offset:]
        # low snr points
        zero_fluxerr = np.abs(tds.spec_data.fluxerr) <= 0.
        logging.info(f'ignoring {zero_fluxerr.sum()} points with buggy flux errs')
        model_is_zero = vv == 0.
        idx = (~zero_fluxerr) & (~model_is_zero)

        dp = DataProxy(tds.spec_data.nt[idx],
                       spec='spec', wavelength='wavelength',
                       flux='flux', fluxerr='fluxerr')
        dp.make_index('spec')
        dp.add_field('model_val', vv[idx])

        r = dp.flux / dp.model_val
        r_err = dp.fluxerr / dp.model_val
        w = 1. / r_err
        rwl = self.model.recal_func.reduced_wavelength(dp.wavelength)
        J = self.build_jacobian_matrix(rwl, dp.spec_index, deg=deg).tocoo()
        model = lm.LinearModel(J.row, J.col, J.data, name='recal')
        solver = lm.RobustLinearSolver(model, r, weights=1/r_err, verbose=True)
        p = solver.robust_solution(nsig=nsig)
        logging.info(f'{solver.bads.sum()} outliers detected at the level of {nsig} sigmas')

        self.solver = solver
        self.recalib_spec_dp = dp
        self.recalib_pars = p

        if update_tds:
            logging.info(f'update flags: {solver.bads.sum()} outliers flagged')
            self.tds.spec_data.valid[idx] &= ~solver.bads
        if update_pars:
            self._update_spectrum_recalibration_pars()

    def _update_spectrum_recalibration_pars(self):
        """
        """
        assert hasattr(self, 'recalib_pars') and hasattr(self, 'recalib_spec_dp'), \
            'no recalibration information available - check your dataflow'

        deg = self.recalib_deg
        tds = self.tds
        p = self.recalib_pars
        dp = self.recalib_spec_dp

        logging.info('updating SpectrumRecalibration parameters')
        for spec in dp.spec_set:
            try:
                i_dst = self.tds.spec_data.spec_map[spec]
                i_src = dp.spec_map[spec]
            except:
                logging.debug(f'spectrum {spec} removed from initial spec dataset')
                continue
            self.pars['SpectrumRecalibration'].full[i_dst*(deg+1):(i_dst+1)*(deg+1)] = p[i_src*(deg+1):(i_src+1)*(deg+1)]

    def _log(self, filter_name, lc_valid, spec_valid, specphot_valid):
        """log the cleaning stats
        """
        n_lc_oor = (~lc_valid).sum() if lc_valid is not None else None
        n_spec_oor = (~spec_valid).sum() if spec_valid is not None else None
        n_specphot_oor = (~specphot_valid).sum() if specphot_valid is not None else None
        n_lc = len(lc_valid) if lc_valid is not None else 0
        n_spec = len(spec_valid) if spec_valid is not None else 0
        n_specphot = len(specphot_valid) if specphot_valid is not None else 0
        logging.info(filter_name)
        if n_lc > 0:
            logging.info(f'Discarded: lc=       {n_lc_oor} ({100*n_lc_oor/n_lc:.2f}%)')
        if n_spec > 0:
            logging.info(f'Discarded: spec=     {n_spec_oor} ({100*n_spec_oor/n_spec:.2f}%)')
        if n_specphot > 0:
            logging.info(f'Discarded: specphot= {n_specphot_oor} ({100*n_specphot_oor/n_specphot:.2f}%)')

    def _flag_outliers(self, nsigs=500):
        """
        """
        chi2 = Chi2(self.model, self.pars, snake=self.snake)

        # photometric outliers
        lc_chi2_vs_sn_index = chi2.get_sn_partial_chi2(phot=True, spec=False)
        lc_chi2_med = np.median(lc_chi2_vs_sn_index)
        lc_chi2_mad = mad(lc_chi2_vs_sn_index)
        cut = lc_chi2_vs_sn_index > (lc_chi2_med + nsigs * lc_chi2_mad)
        logging.info(f'{cut.sum()} SNe discarded (catastrophic photometric outliers): {self.tds.sn_data.sn_set[cut]}')
        # self.tds.sn_data.valid[cut] = 0
        self.tds.kill_sne(self.tds.sn_data.sn_set[cut])

        # spectroscopic outliers
        spec_chi2_vs_spec_index = chi2.get_spec_partial_chi2()
        spec_chi2_med = np.median(spec_chi2_vs_spec_index)
        spec_chi2_mad = mad(spec_chi2_vs_spec_index)
        cut = np.argwhere(spec_chi2_vs_spec_index > (spec_chi2_med + nsigs * spec_chi2_mad)).flatten()
        logging.info(f'{len(cut)} spectra discarded (catastrophic spectroscopic outliers): {self.tds.spec_data.spec_set[cut]}')
        # idx = np.isin(self.tds.spec_data.spec_index, cut)
        #        self.tds.spec_data.valid[idx] = 0
        self.tds.kill_spectra(self.tds.spec_data.spec_set[cut])

        self.lc_chi2_vs_sn_index = lc_chi2_vs_sn_index
        self.lc_chi2_med = lc_chi2_med
        self.lc_chi2_mad = lc_chi2_mad

        self.spec_chi2_vs_spec_index = spec_chi2_vs_spec_index
        self.spec_chi2_med = spec_chi2_med
        self.spec_chi2_mad = spec_chi2_mad

    def _flag_spec_outliers(self):
        """
        """
        pass

    def plot(self, output_dir=None):
        """plot the dataset after cleaning
        """
        plotting.lightcurves.plot_phot_training_residuals(
            self.model, self.pars,
            title='CleanDataset: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_phot_chi2_phasespace(
            self.model, self.pars,
            title='CleanDataset: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_lc_partial_chi2(
            self.model, self.pars,
            output_dir=output_dir)
        plotting.spectra.plot_spec_training_residuals(
            self.model, self.pars,
            title='CleanDataset: spectroscopic data',
            output_dir=output_dir)
        plotting.spectra.plot_spec_chi2_phasespace(
            self.model, self.pars,
            title='CleanDataset: spectroscopic data',
            output_dir=output_dir)
        plotting.spectra.plot_spec_partial_chi2(
            self.model, self.pars,
            output_dir=output_dir)


class FitLightcurves(TrainingCycle):
    """Fits the light curves only (no spectra)
    """
    def __init__(self, model, pars, max_iter=100, **kw):
        """Constructor
        """
        super().__init__(model, pars, **kw)
        self.max_iter = max_iter
        self.lambda_init = kw.get('lambda_init', 1.E-12)
        self.tds = TrainingDataset(sne=self.initial_tds.sn_data.nt,
                                   lc_data=self.initial_tds.lc_data.nt,
                                   filterlib=self.initial_tds.filterlib,
                                   basis=self.initial_tds.basis)
        self.model = self.model.clone(self.tds)
        self.pars = pars.copy()

    def __call__(self):
        """
        """
        ll = LogLikelihood(self.model)
        self.loglikelihood = ll

        # initialize parameters
        for block_name in ll.pars._struct.slices:
            ll.pars[block_name].full[:] = self.pars[block_name].full

        ll.pars.fix()
        for block_name in ['X0', 'X1', 'c', 'tmax']:
            ll.pars[block_name].release()

        # Minimize the LogLikelihood
        minz = Minimizer(ll)
        p = minz.minimize_lm(ll.pars.free,
                             max_iter=self.max_iter,
                             dchi2_stop=1.E-2,
                             lamb=self.lambda_init,
                             diag_charge='marquardt_max')

        self.pars = ll.pars.copy()
        self.pars.full[:] = ll.pars.full[:]
        self.minimizer = minz
        try:
            self.covmat = self.minimizer.get_cov_matrix()[0]
        except:
            self.covmat = None

        if self.covmat is not None:
            ii = self.pars.indexof()
            ii = ii[ii>=0]
            npars = len(self.pars.full)
            cov = self.covmat.tocoo()
            self.full_covmat = coo_matrix((cov.data,
                                           (ii[cov.row], ii[cov.col])),
                                          shape=(npars, npars))
        else:
            self.full_covmat = None

    def plot(self, output_dir=None):
        """
        """
        plotting.lightcurves.plot_phot_training_residuals(
            self.model, self.pars,
            title='FitLightcurves: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_phot_chi2_phasespace(
            self.model, self.pars,
            title='FitLightCurves: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_lc_partial_chi2(
            self.model, self.pars,
            output_dir=output_dir)
        plotting.snpars.plot_sn_pars_vs_init(self.model, self.pars,
                                             covmat=self.covmat,
                                             output_dir=output_dir)
        plotting.snpars.plot_sn_pars_minus_init(self.model, self.pars,
                                                covmat=self.covmat,
                                                output_dir=output_dir)

        plotting.lightcurves.plot_lc_pulls_per_band(tds=self.tds,
                                                    model=self.model,
                                                    pars=self.pars,
                                                    snake=None,
                                                    output_dir=output_dir)


class FitSpectrumRecalibration(TrainingCycle):
    """Fits the spectrum recalibration polynomials
    """
    def __init__(self, model, pars, **kw):
        super().__init__(model, pars, **kw)
        self.tds = TrainingDataset(sne=self.initial_tds.sn_data.nt,
                                   spec_data=self.initial_tds.spec_data.nt,
                                   filterlib=self.initial_tds.filterlib)
        self.model = self.model.clone(self.tds)
        self.pars = pars.copy()
        self.lambda_init = kw.get('lambda_init', 1.E-12)

        # since the fit is now linear, it is better to rely on it
        # to recalibrate the spectra - _recalib_spectra() is very fragile.
        # recal = self._recalib_spectra()
        # self.pars['SpectrumRecalibration'].full[3::4] = np.log(recal)

    def _recalib_spectra(self):
        """
        """
        tds = self.tds
        v = self.model(self.pars)
        n_phot, n_spec, _ = self.tds.nb_meas(split_by_type=True)
        vv = v[n_phot:]

        ii = np.arange(len(vv))
        idx = np.abs(tds.spec_data.fluxerr / tds.spec_data.flux) < 1.
        zero_fluxerr = np.abs(tds.spec_data.fluxerr) <= 0.
        # logger.info(f'ignoring {zero_fluxerr.sum()} points with buggy flux errs')
        idx &= ~zero_fluxerr
        neg_flux = tds.spec_data.flux <= 0.
        idx &= ~neg_flux

        ii = vv[idx] == 0.
        r = np.abs(tds.spec_data.flux[idx][~ii] / vv[idx][~ii])
        r_err = tds.spec_data.fluxerr[idx][~ii] / np.abs(vv[idx][~ii])

        w = 1. / r_err**2
        n = np.bincount(tds.spec_data.spec_index[idx][~ii], weights=(w*r))
        d = np.bincount(tds.spec_data.spec_index[idx][~ii], weights=w)
        recal = n / d

        return recal


    def __call__(self):
        """
        """
        ll = LogLikelihood(self.model)
        self.loglikelihood = ll

        # initialize parameters
        for block_name in ll.pars._struct.slices:
            ll.pars[block_name].full[:] = self.pars[block_name].full

        ll.pars.fix()
        ll.pars['SpectrumRecalibration'].release()

        # minimize the LogLikelihood
        minz = Minimizer(ll)
        p = minz.minimize_lm(ll.pars.free,
                             max_iter=100,
                             dchi2_stop=1.E-2,
                             lamb=self.lambda_init,
                             diag_charge='marquardt_max')

        self.pars = ll.pars.copy()
        self.pars.full[:] = ll.pars.full[:]
        self.minimizer = minz

    def plot(self, output_dir=None):
        """
        """
        plotting.spectra.plot_spec_training_residuals(
            self.model, self.pars,
            title='FitSpectrumRecalibration: spectroscopic data',
            output_dir=output_dir)
        plotting.spectra.plot_spec_chi2_phasespace(
            self.model, self.pars,
            title='FitSpectrumRecalibration: spectroscopic data',
            output_dir=output_dir)
        plotting.spectra.plot_spec_partial_chi2(
            self.model, self.pars,
            output_dir=output_dir)


class FitGammaSNVarianceModel(TrainingCycle):
    """Fit a Local Error model on the data
    """
    def __init__(self, model, pars,
                 regul=None,
                 mu_reg=1.e-6,
                 max_iter=100, bins=(10,10),
                 **kw):
        super().__init__(model, pars, **kw)
        self.tds = self.initial_tds
        self.model = self.model.clone(self.initial_tds)
        self.regul = None
        self.mu_reg = mu_reg
        self.pars = pars.copy()
        self.max_iter = max_iter
        self.bins = bins
        self.lambda_init = kw.get('lambda_init', 1.E-12)
        self.snake = SNLocalErrorSnake2(self.model, bins=bins)
        self._default_priors()

    def _default_priors(self):
        ll = LogLikelihood(self.model,
                           variance_model=self.snake)

        if self.regul is None:
            self.regul = salt2.get_regularization_prior(self.model,
                                                        pars=ll.pars,
                                                        mu=self.mu_reg,
                                                        order=1,
                                                        check=True)
            ll = LogLikelihood(self.model, variance_model=self.snake,
                               reg=[self.regul])

        self.loglikelihood = self.ll = ll
        self.pars = ll.pars.copy()

    def __call__(self):
        """
        """
        ll = self.loglikelihood
        for block_name in ll.pars._struct.slices:
            if block_name in self.pars._struct.slices:
                ll.pars[block_name].full[:] = self.pars[block_name].full

        ll.pars.fix()
        # for block_name in ['X0', 'X1', 'c', 'tmax', 'gamma_sn', 'gamma_snake']:
        for block_name in self.pars._struct.slices: # ['gamma_sn', 'gamma_snake']:
            if 'gamma' in block_name:
                ll.pars[block_name].release()

        # now, we need to fix one parameter of the local error snake
        ll.pars['gamma_snake'].fix(self.snake.to_fix(4000., 0.), 1.)

        minz = Minimizer(ll)
        p = minz.minimize_lm(ll.pars.free, max_iter=self.max_iter,
                             lamb=self.lambda_init,
                             dchi2_stop=1.E-2,
                             diag_charge='marquardt_max',
                             accept=10., reject=5.)

        self.pars = ll.pars.copy()
        self.ll = ll
        self.minimizer = minz
        try:
            self.covmat = self.minimizer.get_cov_matrix()[0]
        except:
            self.covmat = None

    def plot(self, output_dir=None):
        """
        """
        plotting.lightcurves.plot_phot_training_residuals(
            self.model, self.pars,
            snake=self.snake,
            title='FitGammaSNVarianceModel: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_phot_chi2_phasespace(
            self.model, self.pars,
            snake=self.snake,
            title='FitGammaSNVarianceModel: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_lc_partial_chi2(
            self.model, self.pars,
            snake=self.snake,
            output_dir=output_dir)

        if self.tds.spec_data is not None:
            plotting.spectra.plot_spec_training_residuals(
                self.model, self.pars,
                snake=self.snake,
                title='FitGammaSNVarianceModel: spectroscopic data',
                output_dir=output_dir)
            plotting.spectra.plot_spec_chi2_phasespace(
                self.model, self.pars,
                snake=self.snake,
                title='FitGammaSNVarianceModel: spectroscopic data',
                output_dir=output_dir)
            plotting.spectra.plot_spec_partial_chi2(
                self.model, self.pars,
                snake=self.snake,
                output_dir=output_dir)
            try:
                plotting.snake.plot_gamma_sn_like_error_snake(
                    self.snake, self.pars,
                    output_dir=output_dir)
            except:
                logging.warning('unable to plot the error snake')
        plotting.snpars.plot_sn_pars_minus_init(
            self.model, self.pars, covmat=self.covmat,
            output_dir=output_dir)


class FitSimpleVarianceModel(TrainingCycle):
    """Fit a Local Error model on the data
    """
    def __init__(self, model, pars,
                 regul=None,
                 mu_reg=1.e-6,
                 max_iter=100,
                 **kw):
        super().__init__(model, pars, **kw)
        self.tds = self.initial_tds
        self.model = self.model.clone(self.initial_tds)
        self.regul = None
        self.mu_reg = mu_reg
        self.pars = pars.copy()
        self.max_iter = max_iter
        self.lambda_init = kw.get('lambda_init', 1.E-12)
        self.snake = SimpleErrorSnake(self.model)
        self.init_pars = pars
        self._default_priors()

    def _default_priors(self):
        ll = LogLikelihood(self.model,
                           variance_model=self.snake)

        if self.regul is None:
            self.regul = salt2.get_regularization_prior(self.model,
                                                        pars=ll.pars,
                                                        mu=self.mu_reg,
                                                        order=1,
                                                        check=True)
            ll = LogLikelihood(self.model, variance_model=self.snake,
                               reg=[self.regul])

        self.loglikelihood = self.ll = ll
        self.pars = ll.pars.copy()
        for blk in self.pars._struct.slices:
            if blk in self.init_pars._struct.slices:
                self.pars[blk].full[:] = self.init_pars[blk].full

    def __call__(self):
        """
        """
        ll = self.loglikelihood
        for block_name in ll.pars._struct.slices:
            if block_name in self.pars._struct.slices:
                ll.pars[block_name].full[:] = self.pars[block_name].full

        ll.pars.fix()
        # for block_name in ['X0', 'X1', 'c', 'tmax', 'gamma_sn', 'gamma_snake']:
        for block_name in ll.pars._struct.slices: # ['gamma_sn', 'gamma_snake']:
            if 'gamma' in block_name:
                ll.pars[block_name].release()

        minz = Minimizer(ll)
        p = minz.minimize_lm(ll.pars.free, max_iter=self.max_iter,
                             lamb=self.lambda_init,
                             dchi2_stop=1.E-2,
                             diag_charge='marquardt_max',
                             accept=10., reject=5.)

        self.pars = ll.pars.copy()
        self.ll = ll
        self.minimizer = minz
        try:
            self.covmat = self.minimizer.get_cov_matrix()[0]
        except:
            self.covmat = None

    def plot(self, output_dir=None):
        """
        """
        plotting.lightcurves.plot_phot_training_residuals(
            self.model, self.pars,
            snake=self.snake,
            title='FitGammaSNVarianceModel: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_phot_chi2_phasespace(
            self.model, self.pars,
            snake=self.snake,
            title='FitGammaSNVarianceModel: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_lc_partial_chi2(
            self.model, self.pars,
            snake=self.snake,
            output_dir=output_dir)

        if self.tds.spec_data is not None:
            plotting.spectra.plot_spec_training_residuals(
                self.model, self.pars,
                snake=self.snake,
                title='FitGammaSNVarianceModel: spectroscopic data',
                output_dir=output_dir)
            plotting.spectra.plot_spec_chi2_phasespace(
                self.model, self.pars,
                snake=self.snake,
                title='FitGammaSNVarianceModel: spectroscopic data',
                output_dir=output_dir)
            plotting.spectra.plot_spec_partial_chi2(
                self.model, self.pars,
                snake=self.snake,
                output_dir=output_dir)


class FitModel(TrainingCycle):
    """
    """
    def __init__(self, model, pars,
                 snake=None, cons=None, regul=None,
                 error_pedestal=None,
                 solve_cons=True,
                 max_iter=100, mu_cons=1.E6, mu_reg=1.E-6, Mb=-19.5,
                 bins=(5,5),
                 solve_constraints=False,
                 **kw):
        """
        """
        super().__init__(model, pars, **kw)
        self.model = model
        self.pars = pars.copy()
        self.snake = snake # if snake is not None else SNLocalErrorSnake2(self.model, bins=bins)
        # TODO: rename error pedestal -> static snake
        self.error_pedestal = error_pedestal
        self.static_snake = error_pedestal
        self.cons = cons
        self.regul = regul
        self.max_iter = max_iter
        self.mu_cons = mu_cons
        self.mu_reg = mu_reg
        self.Mb = Mb
        self.solve_constraints = solve_constraints
        self.lambda_init = kw.get('lambda_init', 1.E-12)
        self.compute_covmat = kw.get('compute_covmat', True)
        self.covmat = None
        self.priors = None
        self._default_priors()

    def _default_priors(self):
        # instantiate default constraints if none passed to the class
        if self.cons is None:
            #            self.cons = salt2.get_constraint_prior(self.model,
            #                                                   linear=True,
            #                                                   mu=self.mu_cons,
            #                                                   Mb=self.Mb,
            #                                                   check=True)
            self.cons = nacl_linear_constraints(self.model,
                                                mu=self.mu_cons,
                                                Mb=self.Mb,
                                                dm15=1.)

        ll = LogLikelihood(self.model,
                           variance_model=self.snake,
                           cons=[self.cons],
                           reg=[self.regul],
                           priors=self.priors)

        # instantiate default regularization if none passed to the class
        if self.regul is None:
            # argh, we need to instantiate a default LogLikelihood
            # just to get the final structure of the parameter vector
            # we probably should implement a LogLikelihood class method
            # which does that
            # now that we have it, can instantiate a priori
            self.regul = salt2.get_regularization_prior(self.model,
                                                        pars=ll.pars,
                                                        mu=self.mu_reg,
                                                        order=0,
                                                        check=True)
        self.pars = ll.pars.copy()

    def __call__(self, max_iter=None):
        """
        """
        # initialize the error pedestal
        # if self.static_snake is not None:
        #     error_pedestal = self.static_snake(self.pars)
        # else:
        #     error_pedestal = 0.

        # final log-likelihood
        ll = LogLikelihood(self.model,
                           variance_model=self.snake,
                           error_pedestal=self.error_pedestal,
                           cons=[self.cons],
                           reg=[self.regul],
                           priors=self.priors)
        self.ll = self.loglikelihood = ll

        for block_name in ll.pars._struct.slices:
            if block_name in self.pars._struct.slices:
                ll.pars[block_name].full[:] = self.pars[block_name].full
#        ll.pars.release()
#        ll.pars['gamma_sn'].fix()
#        ll.pars['gamma_snake'].fix()

        if self.solve_constraints:
            pp = salt2.constraints.solve_constraints(self.cons, ll.pars)
            ll.pars.full[:] = pp.full

        minz = Minimizer(ll)
        max_iter = max_iter if max_iter is not None else self.max_iter
        p = minz.minimize_lm(ll.pars.free, max_iter=max_iter,
                             lamb=self.lambda_init,
                             dchi2_stop=1.E-2,
                             accept=10., reject=5,
                             diag_charge='marquardt_max')

        self.pars = ll.pars.copy()
        self.minimizer = minz

        if self.compute_covmat:
            try:
                self.covmat = self.minimizer.get_cov_matrix()[0]
            except:
                logging.error('unable to compute the fit covmat')
                self.covmat = None

    def plot(self,
             output_dir=None,
             use_truth=False,
             sn_index=False,
             plot_regul=True,
             plot_model=True):
        """
        """
        plotting.lightcurves.plot_phot_training_residuals(
            self.model, self.pars, snake=self.snake,
            title='FitModel: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_phot_chi2_phasespace(
            self.model, self.pars, snake=self.snake,
            title='FitModel: photometric data',
            output_dir=output_dir)
        plotting.lightcurves.plot_lc_partial_chi2(
            self.model, self.pars, snake=self.snake,
            output_dir=output_dir)

        plotting.spectra.plot_spec_training_residuals(
            self.model, self.pars, snake=self.snake,
            title='FitModel: spectroscopic data',
            output_dir=output_dir)
        plotting.spectra.plot_spec_chi2_phasespace(
            self.model, self.pars, snake=self.snake,
            title='FitModel: spectroscopic data',
            output_dir=output_dir)
        plotting.spectra.plot_spec_partial_chi2(
            self.model, self.pars, snake=self.snake,
            output_dir=output_dir)

        if self.snake is not None:
            try:
                plotting.snake.plot_gamma_sn_like_error_snake(
                    self.snake, self.pars,
                    output_dir=output_dir)
            except:
                logging.warning('unable to plot the error snake')

        plotting.snpars.plot_sn_pars_minus_init(
            self.model, self.pars, covmat=self.covmat,
            output_dir=output_dir,
            sn_index=sn_index,
            use_truth=use_truth)

        plotting.lightcurves.plot_lc_pulls_per_band(tds=self.tds,
                                                    model=self.model,
                                                    pars=self.pars,
                                                    snake=self.snake,
                                                    output_dir=output_dir)
        if plot_model:
            self.plot_model(output_dir=output_dir)

        if plot_regul:
            self.plot_regul(output_dir=output_dir)

    def plot_regul(self, output_dir=None):
        _, _ = plotting.model.plot_dmodel(self, output_dir=output_dir)
        _, _ = plotting.model.plot_regularization_grid(self, output_dir=output_dir)

        plotting.model.plot_regularization_map(self.model,
                                               self.pars,
                                               self.tds,
                                               output_dir=output_dir)

    def plot_model(self, output_dir=None):
        plotting.model.plot_model_at_phase(
            self.model, self.pars, phase=0, output_dir=output_dir)

        plotting.model.plot_model_at_phase(
            self.model, self.pars, phase=15, output_dir=output_dir)

        plotting.model.plot_model_at_phase(
            self.model, self.pars, phase=30, output_dir=output_dir)

        plotting.model.plot_model_at_phase(
            self.model, self.pars, phase=-10, output_dir=output_dir)

        plotting.model.plot_color_law(
            self.model, self.pars, output_dir=output_dir)

        plotting.model.plot_model_comparison(
            self.model, self.pars, output_dir=output_dir)
        
        
    def save(self, output, edris_output=True):
        """
        """
        super().save(output)

        # Mahmoud's original EDRIS interface
        #
        # optional because it forces a covmat computation which takes time and
        # is useless for example in the pretrain phase.
        if edris_output:
            output_dir = pathlib.Path(output).parent
            columns = {
                'x0': 'x0_init',
                'x1': 'x1_init',
                'c': 'c_init',
                'tmax': 'tmax_init'
                }
            if 'name' not in self.tds.sn_data.nt.dtype.names:
                columns['sn'] = 'name'
            sn_data = pandas.DataFrame(data=self.tds.sn_data.nt).rename(
                columns=columns)
            
            sn_index = self.tds.sn_data.sn_index
            sn_data['x0'] = self.pars['X0'].full[sn_index]
            sn_data['x1'] = self.pars['X1'].full[sn_index]
            sn_data['c'] = self.pars['c'].full[sn_index]
            sn_data['tmax'] = self.pars['tmax'].full[sn_index]
            sn_data.to_parquet(output_dir / 'nacl_sn_pars.parquet')

            # SN parameter covmat
            covmat = self.covmat 
            nsn = len(self.pars['X0'].full)
            covblock = covmat[:4*nsn,:4*nsn]
            ii = np.hstack([sn_index + i*nsn for i in range(4)])
            reordered_cov_block = covblock[:, ii][ii]
            np.save(output_dir / 'nacl_sn_pars_cov.npy', reordered_cov_block.todense())


class FitVarianceModel(TrainingCycle):
    def __init__(self, model, pars, **kw):
        super().__init__(model, pars)
        self.pars.fix()


class Distillate:

    def __init__(self):
        self.cycle = cycle
        self.pars = pars

class NaClAlchemy:

    def __init__(self, cycles):
        self.cycles = cycles
        self.distillates = []

    def distill(self):
        for c in self.cycles:
            self.distillates.append(c.fit())

    def control_plots(self):
        pass



        # phase range (photometric data)
        # tmax = np.zeros(len(self.tds.sn_data))
        # tmax[self.tds.sn_data.sn_index] = self.tds.sn_data.tmax
        # phot_tmax = tmax[self.tds.lc_data.sn_index]
        # phase = (self.tds.lc_data.mjd - phot_tmax) / (1. + self.tds.lc_data.z)

        # idx = (phase<self.model.phase_range[0]) | (phase>self.model.phase_range[1])
        # logging.info(f'removing {idx.sum()} photometric points outside phase range')
        # self.tds.lc_data.valid[idx] = 0

        # # phase range (spectra)
        # spec_tmax = tmax[self.tds.spec_data.sn_index]
        # phase = (self.tds.spec_data.mjd - spec_tmax) / (1. + self.tds.spec_data.z)
        # idx = (phase<self.model.phase_range[0]) | (phase>self.model.phase_range[1])
        # logging.info(f'removing {idx.sum()} spectroscopic points outside phase range')
        # self.tds.spec_data.valid[idx] = 0

        # # we need to determine, for each spectrum, the i_basis_min and i_basis_max
        # b_bins = np.arange(-0.5, self.tds.spec_data.i_basis.max() + 1.5, 1)
        # s_bins = np.arange(-0.5, self.tds.spec_data.spec_index.max() + 1.5, 1)
        # h, _, _ = np.histogram2d(self.tds.spec_data.i_basis, self.tds.spec_data.spec_index, bins=(b_bins, s_bins))
        # bb = np.arange(0, self.tds.spec_data.i_basis.max() + 1, 1)
        # ss = np.arange(0, self.tds.spec_data.spec_index.max() + 1, 1)
        # bb, ss = np.meshgrid(bb, ss)
        # u = bb * h.T
        # mb = ma.masked_array(u, mask=u==0.)
        # b_min, b_max = np.array(np.min(mb, axis=1)), np.array(np.max(mb, axis=1))
        # to_kill  = np.array(b_min).astype(int)[self.tds.spec_data.spec_index] == self.tds.spec_data.i_basis
        # to_kill |= np.array(b_max).astype(int)[self.tds.spec_data.spec_index] == self.tds.spec_data.i_basis

        # logging.info(f'removing {np.sum(to_kill)} spectroscopic points outside wavelength range')
        # self.tds.spec_data.valid[to_kill] = 0


        # n_phot, n_spec, n_spectrophot = self.tds.nb_meas(split_by_type=1)
        # if n_phot < 0:
        #     return
        # v = self.model(self.pars)
        # fig, axes = pl.subplots(figsize=(12,12), nrows=2, ncols=2)
        # fig.suptitle('CleanDataset: photometric_data after cleaning')
        # x = np.arange(n_phot)
        # flux = self.tds.lc_data.flux
        # fluxerr = self.tds.lc_data.fluxerr
        # res = self.tds.lc_data.flux-v[:n_phot]
        # wres = (self.tds.lc_data.flux-v[:n_phot]) / self.tds.lc_data.fluxerr
        # ii = np.argsort(self.tds.lc_data.z)
        # ii = np.arange(len(self.tds.lc_data.z))
        # axes[0,0].errorbar(x, res[ii], yerr=fluxerr[ii], ls='', marker=',', color='gray')
        # axes[0,0].scatter(x, res[ii], c=self.tds.lc_data.z[ii], s=2, zorder=100, norm='log')
        # axes[0,0].set_ylabel('residuals')

        # axes[1,0].plot(x, wres[ii], ls='', marker=',', color='gray')
        # axes[1,0].scatter(x, wres[ii], c=self.tds.lc_data.z[ii], s=2, zorder=100, norm='log')
        # axes[1,0].set_xlabel('meas index')
        # axes[1,0].set_ylabel('pulls')

        # phase = (self.tds.lc_data.mjd - self.pars['tmax'].full[self.tds.lc_data.sn_index]) / (1. + self.tds.lc_data.z)
        # # phase = self.tds.lc_data.mjd
        # axes[0,1].errorbar(phase[ii], res[ii], yerr=fluxerr[ii], ls='', color='gray', marker='.')
        # axes[0,1].scatter(phase[ii], res[ii], c=self.tds.lc_data.z[ii], s=2, zorder=100, norm='log')
        # axes[0,1].set_ylabel('residuals')

        # axes[1,1].plot(phase[ii], wres[ii], ls='', color='gray', marker='.')
        # axes[1,1].scatter(phase[ii], wres[ii], c=self.tds.lc_data.z[ii], s=2, zorder=100, norm='log')
        # axes[1,1].set_xlabel('phase [days]')
        # axes[1,1].set_ylabel('pulls')

        # self.res = res
        # self.wres = wres



# class FitModelOnly(TrainingCycle):
#     """
#     """
#     def __init__(self, model, pars,
#                  snake=None, regul=None, cons=None,
#                  max_iter=100, mu_cons=1.E6, mu_reg=1.E-6, Mb=-19.5,
#                  bins=(5,5),
#                  solve_constraints=True):
#         """
#         """
#         super().__init__(model, pars)
#         self.model = model
#         self.pars = pars.copy()
#         self.snake = snake if snake is not None else SNLocalErrorSnake2(self.model, bins=bins)
#         self.cons = cons
#         self.regul = regul
#         self.max_iter = max_iter
#         self.mu_cons = mu_cons
#         self.mu_reg = mu_reg
#         self.Mb = Mb
#         self.solve_constraints = solve_constraints
#         self.priors = None

#     def _default_priors(self):
#         # instantiate default constraints if none passed to the class
#         if self.cons is None:
#             self.cons = salt2.get_constraint_prior(self.model,
#                                                    linear=True,
#                                                    mu=self.mu_cons,
#                                                    Mb=self.Mb,
#                                                    check=True)

#         # instantiate default regularization if none passed to the class
#         if self.regul is None:
#             # argh, we need to instantiate a default LogLikelihood
#             # just to get the final structure of the parameter vector
#             # we probably should implement a LogLikelihood class method
#             # which does that
#             ll = LogLikelihood(self.model,
#                                variance_model=self.snake,
#                                cons=[self.cons],
#                                reg=[self.regul],
#                                priors=self.priors)
#             # now that we have it, can instantiate a priori
#             self.regul = salt2.get_regularization_prior(self.model,
#                                                         pars=ll.pars,
#                                                         mu=self.mu_reg,
#                                                         order=1,
#                                                         check=True)

#     def __call__(self):
#         """
#         """
#         self._default_priors()

#         # final log-likelihood
#         ll = LogLikelihood(self.model,
#                            variance_model=self.snake,
#                            cons=[self.cons],
#                            reg=[self.regul],
#                            priors=self.priors)

#         for block_name in ll.pars._struct.slices:
#             if block_name in self.pars._struct.slices:
#                 ll.pars[block_name].full[:] = self.pars[block_name].full
#         ll.pars.release()

#         if self.solve_constraints:
#             pp = salt2.constraints.solve_constraints(self.cons, ll.pars)
#             ll.pars.full[:] = pp.full

#         for block_name in ['M0', 'M1', 'CL']:
#             ll.pars[block_name].release()

#         minz = Minimizer(ll)
#         p = minz.minimize_lm(ll.pars.free, max_iter=self.max_iter,
#                              lamb=1.E-6,
#                              dchi2_stop=1.E-2,
#                              diag_charge='marquardt_max',
#                              accept=10., reject=5.)

#         self.pars = ll.pars.copy()
#         self.minimizer = minz

#     def plot(self):
#         self.v, self.res, self.wres = _plot_photometric_data(self.model, self.pars,
#                                                              title='FitModelOnly : photometric data')
#         self.v, self.res, self.wres = _plot_spec_data(self.model, self.pars,
#                                                       title='FitModelOnly : spectroscopic data')
#         plot_phot_chi2_phasespace(self.model, self.pars, snake=self.snake,
#                                   title='FitModelOnly : photometric data')
#         plot_spec_chi2_phasespace(self.model, self.pars,
#                                   title='FitModelOnly : spectroscopic data')








    # def _flag_low_snr_datapoints(self, update=True, **kwargs):
    #     """Flag datapoints with a ridiculously low snr

    #     .. note:
    #        this is probably a bad idea. Un-used at the moment.
    #     """
    #     if self.tds.lc_data is not None:
    #         phot_snr = self.tds.lc_data.flux / self.tds.lc_data.fluxerr
    #         phot_min_snr = kwargs.get('phot_min_snr', self.phot_min_snr)
    #         phot_idx = phot_snr < phot_min_snr
    #         if update:
    #             self.tds.lc_data.valid[phot_idx] = 0
    #         phot_valid = (~phot_idx)
    #     else:
    #         phot_valid = None

    #     if self.tds.spec_data is not None:
    #         spec_snr = self.tds.spec_data.flux / self.tds.spec_data.fluxerr
    #         spec_min_snr = kwargs.get('spec_min_snr', self.spec_min_snr)
    #         spec_idx = spec_snr < spec_min_snr
    #         if update:
    #             self.tds.spec_data.valid[spec_idx] = 0
    #         spec_valid = (~spec_idx)
    #     else:
    #         spec_valid = None

    #     if self.tds.spectrophotometric_data is not None:
    #         spphot_snr = self.tds.spectrophotometric_data.flux / self.tds.spectrophotometric_data.fluxerr
    #         spphot_min_snr = kwargs.get('spphot_min_snr', self.spphot_min_snr)
    #         spphot_idx = spphot_snr < spphot_min_snr
    #         if update:
    #             self.tds.spectrophotometric_data.valid[spphot_idx] = 0
    #         spphot_valid = (~spphot_idx)
    #     else:
    #         spphot_valid = None

    #     return phot_valid, spec_valid, spphot_valid
