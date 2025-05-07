"""
"""

import sys
import logging

import numpy as np
from scipy.interpolate import interp1d
from scipy import sparse
import matplotlib.pyplot as plt

from sksparse import cholmod

import pandas

from saltworks.plottools import binplot
from saltworks.robuststat import mad
from saltworks import linearmodels
from bbf.bspline import integ
from nacl.dataset import TrainingDataset

logger = logging.getLogger(__name__)


class SpectrumProjector:
    """Utility class to project a collection of spectra onto a BSpline basis

    Spectra in a typical NaCl training dataset have a higher resolution than the
    model itself (typically from ~ 1 \AA to 25 \AA w.r.t 50\AA for NaCl). To
    help make the training tractable, the spectra are projected on the model
    basis beforehand. This class does precisely that.

    .. note::
       this implementation is the most up to date. Use this one unless
       you know what you are doing.

    """

    class Projection:
        """Holds the result of projecting a single spectrum onto the basis.
        """
        def __init__(self, projector, slc, proj_coeffs, solver, proj_coeff_errs=None, beta=None):
            """Initialize a projection object.
            """
            self.projector = projector
            self.slc = slc
            self.wl_basis = projector.wl_basis
            self.basis_restframe_wavelength = integ(self.wl_basis, n=1) / integ(self.wl_basis, n=0)
            self.proj_coeffs = proj_coeffs
            self.solver = solver
            self.proj_coeff_errs = proj_coeff_errs
            self.beta = beta
            self.model = solver.model
            self.model_vals = self.model(self.proj_coeffs)
            self.i_basis = np.arange(len(self.wl_basis))
            self.default_selection = np.ones_like(self.proj_coeffs).astype(bool)

        @property
        def res(self):
            return self.projector.flux[self.slc] - self.model_vals

        @property
        def wres(self):
            return (self.projector.flux[self.slc] - self.model_vals) / self.projector.fluxerr[self.slc]

        @property
        def restframe_wavelength(self):
            return self.projector.restframe_wavelength[self.slc]

        @property
        def flux(self):
            return self.projector.flux[self.slc]

        @property
        def fluxerr(self):
            return self.projector.fluxerr[self.slc]

        @property
        def chi2(self):
            return self.solver.chi2

        @property
        def npars(self):
            # return self.solver.ndof()
            AA = self.solver.A.tocoo()
            npars = len(np.unique(AA.col))
            return npars

        @property
        def nmeas(self):
            return len(self.flux)

        @property
        def ndof(self):
            return self.nmeas - self.npars

        @property
        def rchi2(self):
            return self.chi2 / self.ndof

        @property
        def bads(self):
            return self.solver.bads

        @property
        def z(self):
            return self.projector.spec_data.z[self.slc].iloc[0]

        @property
        def sn(self):
            return self.projector.spec_data.sn[self.slc].iloc[0]

        @property
        def spec(self):
            return self.projector.spec_data.spec[self.slc].iloc[0]

        @property
        def mjd(self):
            return self.projector.spec_data.mjd[self.slc].iloc[0]

        @property
        def median_restframe_dwl(self):
            return np.median(np.diff(self.projector.restframe_wavelength[self.slc]))

        @property
        def median_dwl(self):
            return np.median(np.diff(self.projector.spec_data.wavelength[self.slc]))

        @property
        def fluxerr_variability(self):
            fluxerr = self.fluxerr
            iqr = np.percentile(fluxerr, 75) - np.percentile(fluxerr, 25)
            return iqr / np.median(fluxerr)

        @property
        def exptime(self):
            return self.projector.spec_data.exptime[self.slc].iloc[0]

        def get_projected_spectrum(self, **kw):
            """Return a DataFrame containing projected spectrum data.
            """
            n = len(self.wl_basis)
            d = pandas.DataFrame({
                'sn': self.sn,
                'spec': self.spec,
                'mjd': self.mjd,
                'z': self.z,
                'valid': np.ones(n).astype(int),
                'exptime': self.exptime,
                'wavelength': self.basis_restframe_wavelength * (1. + self.z),
                'restframe_wavelength': self.basis_restframe_wavelength,
                'i_basis': self.i_basis,
                'flux': self.proj_coeffs,
                'fluxerr': self.proj_coeff_errs,
                'chi2': self.chi2,
                'ndof': self.ndof,
                'median_restframe_dwl': self.median_restframe_dwl,
                'median_dwl': self.median_dwl,
                'fluxerr_variability': self.fluxerr_variability})
            return d

        def plot(self):
            """Plot observed flux, model fit, residuals, and projected spectrum
            """
            restframe_wavelength = self.restframe_wavelength
            flux = self.flux
            fluxerr = self.fluxerr
            model_vals = self.model_vals

            # main plotting part: if we have a model
            fig, axes = plt.subplots(nrows=4, ncols=1,
                                     figsize=(8,10),
                                     sharex=True)
            fig.suptitle(f'spec: {self.spec}')

            # main spectrum
            axes[0].errorbar(restframe_wavelength,
                             flux,
                             yerr=fluxerr,
                             ls='', marker='.', color='blue')
            # axes[0].errorbar(self.x[bads], self.y[bads],
            #                  yerr=self.yerr[bads],
            #                  ls='', marker='x', color='red')
            axes[0].plot(restframe_wavelength,
                         model_vals,
                         ls='--', color='r', zorder=100)
            axes[0].set_ylabel('flux')

            # plot the residuals
            axes[1].errorbar(restframe_wavelength,
                             flux-model_vals,
                             yerr=fluxerr,
                             ls='', marker='.', color='blue')
            # axes[1].errorbar(self.x[bads], self.y[bads]-self.model_vals[bads],
            #                  yerr=self.yerr[bads],
            #                  ls='', marker='x', color='red')
            axes[1].set_ylabel('residuals')

            # weighted residuals and binned weighted residuals
            axes[2].plot(restframe_wavelength,
                         (flux-model_vals)/fluxerr,
                         ls='', marker='.', color='blue')
            axes[2].set_ylabel('wres')

            binplot(restframe_wavelength,
                    (flux-model_vals)/fluxerr,
                    nbins=20, data=None, ax=axes[2], color='r', marker='o')
            axes[2].set_xlabel(r'$\lambda [\AA]$')
            plt.subplots_adjust(hspace=0.05)

            # compressed spectrum
            axes[3].errorbar(restframe_wavelength,
                             flux,
                             fluxerr,
                             ls='', marker='.', color='gray')
            idx = self.proj_coeffs != 0.
            axes[3].errorbar(self.basis_restframe_wavelength[idx],
                             self.proj_coeffs[idx],
                             yerr=self.proj_coeff_errs[idx],
                             ls='', marker='.', color='red')

    def __init__(self, spec_data, wl_basis, **kw):
        """Initialize the SpectrumProjector with data and basis.
        """
        self.wl_basis = wl_basis
        self.beta = kw.get('beta', 1.E-8)

        cut = self._select_data(spec_data)
        spec_data = spec_data[~cut]

        self.spec_data = spec_data.sort_values(['spec', 'wavelength']).reset_index(drop=True)
        self.spec = self.spec_data.spec.to_numpy()
        self.flux = self.spec_data.flux.to_numpy()
        self.fluxerr = self.spec_data.fluxerr.to_numpy()
        self.wavelength = self.spec_data.wavelength.to_numpy()
        self.restframe_wavelength = self.wavelength / (1. + self.spec_data.z).to_numpy()

        # just for our records
        self.spec_data_bads = spec_data[cut]

        # unique_specs, start_indices = np.unique(np.column_stack((self.spec, spec_indexes)), axis=0, return_index=True)
        unique_specs, start_indices = np.unique(self.spec, return_index=True)
        end_indices = np.r_[start_indices[1:], len(self.spec)]
        self.slices = [slice(b,e) for b,e in zip(start_indices, end_indices)]
        spec = [self.spec[s][0] for s in self.slices]
        self.slice_dict = dict(zip(spec, self.slices))

    def _select_data(self, spec_data):
        """Identifies and removes invalid measurements.

        Filters out NaNs, infs, non-positive errors, and wavelengths outside the
        basis range.

        Parameters
        ----------
        spec_data : pandas.DataFrame
            The input spectral data.

        Returns
        -------
        cut : np.ndarray
            Boolean mask for removed rows.
        """
        nan_idx = np.isnan(spec_data.flux) | np.isnan(spec_data.fluxerr)
        inf_idx = np.isinf(spec_data.flux) | np.isinf(spec_data.fluxerr)
        neg_fluxerr_idx = spec_data.fluxerr <= 0.
        wl_min, wl_max = self.wl_basis.grid.min(), self.wl_basis.grid.max()
        restframe_wavelength = spec_data.wavelength / (1. + spec_data.z)
        out_of_range_idx = (restframe_wavelength < wl_min) | (restframe_wavelength > wl_max)

        # TODO: add detection of gaps in spectra. If gaps greater than some threshold,
        # remove the spectrum entirely

        self.select_stats = {'nan': nan_idx.sum(),
                             'inf': inf_idx.sum(),
                             'negative_errs': neg_fluxerr_idx.sum(),
                             'out_of_range': out_of_range_idx.sum()}
        cut = nan_idx | inf_idx | neg_fluxerr_idx | out_of_range_idx
        logger.info(f'{cut.sum()} measurements removed.')
        if cut.sum() > 0:
            logger.info(f'nan:{nan_idx.sum()} inf:{inf_idx.sum()} negerr:{neg_fluxerr_idx.sum()} oorng:{out_of_range_idx.sum()}')

        return cut

    def _one_fit(self, slc, **kw):
        """Projects one spectrum onto the basis using a robust linear solver.

        Parameters
        ----------
        slc : slice
            Slice of the spectrum in the dataset.
        beta : float, optional
            Regularization parameter.
        compute_covmat_diag : bool, optional
            Whether to compute the diagonal of the covariance matrix.
        rescale : bool, optional
            Whether to rescale flux values.
        initial_error_pedestal : float, optional
            Additive error to flux uncertainty.
        show_log : bool, optional
            Show detailed logging.

        Returns
        -------
        proj : SpectrumProjector.Projection
            The result of the projection.
        """
        spec = self.spec[slc][0]
        restframe_wavelength = self.restframe_wavelength[slc]
        flux = self.flux[slc]
        fluxerr = self.fluxerr[slc]

        beta = kw.get('beta', self.beta)
        show_log = kw.get('show_log', False)
        default_logging_level = logging.getLogger().level
        compute_covmat_diag = kw.get('compute_covmat_diag', False)

        # rescale the fluxes
        rescale = kw.get('rescale', True)
        scale = 1. / np.median(np.abs(flux)) if rescale else 1.
        flux *= scale
        fluxerr *= scale

        # initial error pedestal ?
        initial_error_pedestal = kw.get('initial_error_pedestal', 0.)
        fluxerr = np.sqrt(fluxerr**2 + (initial_error_pedestal*flux)**2)
        w = 1. / fluxerr

        # model
        J = self.wl_basis.eval(restframe_wavelength)

        # add a fake point in J so that the correct dimensions of
        # J are taken into account in linearmodels.LinearModel

        model, solver, coeffs = None, None, None
        try:
            _row = np.hstack((J.row, [0]))
            _col = np.hstack((J.col, [len(self.wl_basis)-1]))
            _data = np.hstack((J.data, [0.]))
            _J = sparse.coo_matrix((_data, (_row, _col)), shape=J.shape)
            model = linearmodels.LinearModel(_J.row, _J.col, _J.data)
            if show_log:
                logging.getLogger().setLevel(logging.DEBUG)
            solver = linearmodels.RobustLinearSolver(model, flux,
                                                     weights=w,
                                                     beta=self.beta)
            coeffs = solver.robust_solution(nsig=4.)
            if show_log:
                logging.getLogger().setLevel(default_logging_level)

        except:
            logger.error(f'unable to fit spectrum: {spec}')
            logger.error(f'{sys.exc_info()}')
            return None

        # if requested, invert the hessian and return its diagonal
        if compute_covmat_diag:
            from scipy.sparse.linalg import splu
            n = len(self.wl_basis)
            N = len(w)
            W = sparse.dia_matrix((w, 0), shape=(N,N))
            H = J.T @ W @ J
            H = sparse.csc_matrix(H + 1.E-12 * sparse.eye(H.shape[0]))
            lu = splu(H)
            I = np.eye(H.shape[0])
            covmat_diag = np.array([lu.solve(I[:, i])[i] for i in range(H.shape[0])])
        else:
            covmat_diag = np.zeros(len(self.wl_basis))

        proj = SpectrumProjector.Projection(self, slc, coeffs, solver, np.sqrt(covmat_diag))
        proj.J = J

        return proj

    def process(self, **kw):
        """Projects all spectra and returns a compressed (unfiltered) representation

        Parameters
        ----------
        **kw : dict
            Optional arguments for `_one_fit`.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing compressed spectra (projected coefficients).
        """
        from tqdm import tqdm
        ret = []
        for spec in tqdm(self.slice_dict):
            r = self._one_fit(self.slice_dict[spec], compute_covmat_diag=True, **kw)
            if r is not None:
                ret.append(r.get_projected_spectrum())
        ret = pandas.concat(ret)

        return ret

    def filter_compressed_spectra(self, compressed_spectra, **kw):
        """Filters projected spectra based on DoF and flux error variability.

        Parameters
        ----------
        compressed_spectra : pandas.DataFrame
            The output of `process()`.
        min_ndof : int, optional
            Minimum number of degrees of freedom. Default is 10.
        max_fluxerr_variability : float, optional
            Maximum allowed flux error variability. Default is 10.

        Returns
        -------
        pandas.DataFrame
            Filtered compressed spectra.
        """
        cs = compressed_spectra

        # remove the coefficients outside the spectrum range
        zero_fluxes = (cs.flux == 0.)

        # remove the spectra with less than 10 ndof
        min_ndof_limit = kw.get('min_ndof', 10)
        ndof_cut = (cs.ndof < min_ndof_limit)
        removed = np.unique(cs[ndof_cut].spec)
        print(f'removed {len(removed)} spectra because less than {min_ndof_limit} dof')
        print(f'you may want to inspect: {removed}')

        # remove the spectra with a very large fluxerr variability
        fluxerr_variability_limit = kw.get('max_fluxerr_variability', 10.)
        fluxerr_variability_cut = (cs.fluxerr_variability > fluxerr_variability_limit)
        removed = np.unique(cs[fluxerr_variability_cut].spec)
        print(f'removed {len(removed)} spectra because exceeded fluxerr variability limit ({fluxerr_variability_limit})')
        print(f'you may want to inspect: {removed}')

        idx = (~zero_fluxes) & (~ndof_cut) & (~fluxerr_variability_cut)

        return compressed_spectra[idx]

    def control_plots(self, compressed_spectra):
        """Diagnostic plots from compressed spectra.

        Parameters
        ----------
        compressed_spectra : pandas.DataFrame
            Compressed spectra as output by `process()`.
        """
        df = compressed_spectra[['z', 'chi2', 'ndof', 'median_restframe_dwl', 'fluxerr_variability']].drop_duplicates()

        plt.figure()
        plt.plot(df.z, df.chi2/df.ndof, 'r.')
        plt.xlabel(r'$z$')
        plt.ylabel(r'$\chi^2 / ndof$')
        plt.title('compression chi2')

        plt.figure()
        plt.hist(df.chi2/df.ndof, bins=100)
        plt.xlabel(r'$\chi^2 / ndof$')
        plt.title('compression chi2')

        plt.figure()
        plt.scatter(df.median_restframe_dwl, df.chi2/df.ndof, c=df.z, s=5)
        plt.xlabel(r'$\delta\lambda [\AA]$')
        plt.ylabel(r'$\chi^2 / ndof$')

        plt.figure()
        plt.hist(df.fluxerr_variability, bins=100)
        plt.xlabel('fluxerr variability')

    def compress_and_plot(self, slc=None, spec=None):
        """Projects and plots a specific spectrum.

        Parameters
        ----------
        slc : slice, optional
            Slice of the spectrum in the dataset.
        spec : str, optional
            Spectrum ID.
        """
        slc = slc if slc is not None else self.slice_dict.get(spec, None)
        r = self._one_fit(slc, compute_covmat_diag=True)
        r.plot()

    def plot(self, slc=None, spec=None):
        """Plot observed flux for a given spectrum.

        Parameters
        ----------
        slc : slice, optional
            Slice of the spectrum in the dataset.
        spec : str, optional
            Spectrum ID.
        """
        slc = slc if slc is not None else self.slice_dict.get(spec, None)
        if slc is None:
            logger.error(f'unable to plot spectrum: slc={slc} spec={spec}')
        fig, axes = plt.subplots(nrows=1, ncols=1,
                                 figsize=(8,6))
        fig.suptitle(f'spec: {spec}')
        axes.errorbar(restframe_wavelength, flux,
                      yerr=fluxerr,
                      ls='', marker='.', color='blue')


class Spec:
    """A utility class to project a spectrum on a basis

    .. note:: this is the first projection class written for NaCl. It is slow
       and does not reject outliers. Kept for debugging purposes. Will be
       deprecated in a near future.
    """
    class FitResults:
        pass

    def __init__(self, tds, spec, basis,
                 error_eval_bin_width=50.,
                 beta=1.E-8):
        self.tds = tds
        self.spec = spec
        self.basis = basis
        self.error_eval_bin_width = error_eval_bin_width
        self.beta = beta
        if tds.spec_data != None:
            tds_spec_data = tds.spec_data
        else:
            tds_spec_data = tds.spectrophotometric_data
            self.tds_spec_data = tds_spec_data
            idx = self.idx = tds_spec_data.spec == spec

        for field in ['sn', 'mjd', 'valid', 'spec', 'exptime', 'z']:
            setattr(self, field, self._check_field(field))
            sn = tds_spec_data.sn[idx]
            assert np.all(np.equal(sn, sn[0]))

        self.wl = tds_spec_data.wavelength[idx]
        self.restframe_wl = self.wl / (1. + self.z)
        self.flux = tds_spec_data.flux[idx]
        self.fluxerr = tds_spec_data.fluxerr[idx]

        # # cut the NaN's
        # self.cut = np.isnan(self.flux) | (self.fluxerr < 0) | np.isnan(self.fluxerr)
        # if self.cut.sum() > 0:
        #     logger.warning(f'{self.cut.sum()} measurement detected with negative of nan uncertainties')

        # # cut the NaN's
        # self.cut = np.isnan(self.flux) | (self.fluxerr < 0) | np.isnan(self.fluxerr)
        # if self.cut.sum() > 0:
        #     logger.warning(f'{self.cut.sum()} measurement detected with negative of nan uncertainties')

        # wl_min, wl_max = basis.grid.min(), basis.grid.max()
        # # print(wl_min, wl_max, self.restframe_wl.min(), self.restframe_wl.max())
        # cut = (self.restframe_wl<wl_min) | (self.restframe_wl>wl_max)
        # if cut.sum() > 0:
        #     logger.info(f'{self.cut.sum()} outside basis range')
        # self.cut &= cut

        self.cut = self._select_data()

        self.fitres = []

    def _select_data(self):
        """the spectral data generally needs to be cleaned.
        """
        # remove the NaN's
        nan_idx = np.isnan(self.flux) | np.isnan(self.fluxerr)

        # some errors are negative
        # we don't cut the data - we resset them temporarily to 1.
        negflxerr_idx = self.fluxerr < 0.
        self.fluxerr[negflxerr_idx] = 1.

        # some data points are zeros
        zero_idx = (self.flux == 0.) | (self.fluxerr == 0.)

        # finally, get rid of all the data that is outside
        # the (restframe) basis wavelength rage
        wl_min, wl_max = self.basis.grid.min(), self.basis.grid.max()
        out_of_range_idx = (self.restframe_wl < wl_min) | (self.restframe_wl > wl_max)

        self.select_stats = {'nan': nan_idx.sum(),
                             'negative_errs': negflxerr_idx.sum(),
                             'zero_flux_or_err': zero_idx.sum(),
                             'out_of_range': out_of_range_idx.sum()}

        cut = nan_idx | zero_idx | out_of_range_idx
        logger.info(f'{self.sn}: {cut.sum()} measurement removed.')
        if cut.sum() > 0:
            logger.info(f'nan:{nan_idx.sum()} zflx:{zero_idx.sum()} oorng: {out_of_range_idx.sum()}')

        return cut

    def _check_field(self, name):
        """
        """
        try:
            s = np.unique(self.tds_spec_data.nt[self.idx][name])
        except:
            s = np.unique(self.tds_spec_data.__dict__[name][self.idx])
            assert len(s) == 1
        return s[0]

    def fit(self, x, y, yerr, beta=None):
        """
        """
        N = len(x)
        assert (len(y) == N) and (len(yerr) == N)
        if beta is None:
            beta = self.beta

        J = self.basis.eval(x)
        w = 1. / yerr
        W = sparse.dia_matrix((w**2, 0), shape=(N,N))
        H = J.T @ W @ J
        fact = cholmod.cholesky(H.tocsc(), beta=beta)

        r = Spec.FitResults()
        r.coeffs = fact(J.T @ W @ y)
        r.res = (y - J @ r.coeffs)
        r.wres = (y - J @ r.coeffs) * w
        r.chi2 = (r.wres**2).sum()
        r.ndof = (len(y) - len(r.coeffs))
        r.rchi2 = r.chi2 / r.ndof
        r.basis = self.basis
        #try:
        HH = H.todense() + np.diag(np.full(len(r.coeffs), 1.E-20))
        r.coeffs_cov = np.linalg.inv(HH)
        r.coeffs_err = np.sqrt(np.array(r.coeffs_cov.diagonal()).squeeze())
        r.i = np.arange(len(r.coeffs))
        r.selection = r.coeffs_err < 0.5/beta

            # r.coeffs_err = np.sqrt(scipy.sparse.linalg.inv(H).diagonal())
            #except:
            #    r.coeffs_err = np.zeros_like(r.coeffs)

        return r

    def recompute_error_model(self, wl, res, nbins=10):
        """
        """
        #       nbins = int((wl.max() - wl.min()) / bin_width)
        x, y, yerr = binplot(wl, res, nbins=nbins, scale=False, noplot=True)
        self.error_model = interp1d(x, yerr, kind='linear', fill_value=(yerr[0], yerr[-1]), bounds_error=False)
        self.x_err, self.y_err = x, yerr
        return self.error_model

    def flag_residuals(self):
        """
        """
        pass

    def process(self):
        """
        """
        rwl = self.restframe_wl[~self.cut]
        flx = self.flux[~self.cut]
        flxerr = self.fluxerr[~self.cut]

        if len(rwl) == 0:
            logger.error(f'{self.sn} no data')
            return None

        # re-eval errors
        r = self.fit(rwl, flx, flxerr)
        error_model = self.recompute_error_model(rwl, r.res, nbins=10)
        self.fitres.append(r)

        # re-fit with recomputed errors
        model_flxerr = error_model(self.restframe_wl)
        if np.any(model_flxerr <= 0.):
            logger.error(f'{self.sn}: unable to recompute an error model')
            self.estimated_fluxerr = model_flxerr
            return None

        r = self.fit(rwl, flx, model_flxerr[~self.cut])
        self.fitres.append(r)

        # # bin spectrum
        # r = self.fit(self.wl, self.flux, fluxerr, order=1, bin_width=self.bin_width)
        # self.fitres.append(r)

        self.estimated_fluxerr = model_flxerr

    def get_projected_spectrum(self):
        """
        """
        if len(self.fitres) != 2:
            return None

        r = self.fitres[1]
        idx = r.selection
        wl = integ(r.basis, n=1) / integ(r.basis, n=0)
        # wl = wl[r.selection]
        N = idx.sum()

        d = np.zeros(N, self.tds_spec_data.nt.dtype)
        d['sn'] = self.sn
        d['spec'] = self.spec
        d['mjd'] = self.mjd
        # d['z'] = self.z
        d['valid'] = self.valid
        d['exptime'] = self.exptime
        d['wavelength'] = wl[idx]
        d['i_basis'] = r.i[idx]
        d['flux'] = r.coeffs[idx]
        d['fluxerr'] = r.coeffs_err[idx]
        return d

    def plot(self):
        """
        """
        try:
            r = self.fitres[1]
        except:
            logger.warning('problem with the fit: showing initial fit')
            try:
                r = self.fitres[0]
            except:
                r = None
                logger.warning('problem with the fit: no fit available')

        fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(8,8), sharex=False)

        fig.suptitle(f'SN{self.sn} z={self.z} mjd={self.mjd}')

        # the original spectrum (with re-estimated errors and the fit)
        axes[0].errorbar(self.restframe_wl[~self.cut], self.flux[~self.cut], yerr=self.estimated_fluxerr[~self.cut],
                         ls='', marker='.', label='orig')
        wl_min, wl_max = self.restframe_wl.min(), self.restframe_wl.max()

        if r is not None:
            wl = np.linspace(wl_min, wl_max, 1000)
            J = self.basis.eval(wl)
            axes[0].plot(wl, J @ r.coeffs, 'r-', zorder=1000)
            axes[0].set_ylabel('spectrum')

        # the residuals
        if r is not None:
            axes[1].errorbar(self.restframe_wl[~self.cut], r.res, yerr=self.estimated_fluxerr[~self.cut],
                             ls='', marker='.', color='b')
            axes[1].set_ylabel('residuals')

            axes[2].plot(self.x_err, self.y_err, 'bo')
            xx = np.linspace(self.restframe_wl.min(), self.restframe_wl.max(), 100)
            axes[2].plot(xx, self.error_model(xx), 'r-')
            axes[2].set_ylabel('error model')

        # axes[3].shared_x_axes.remove(axes[3])
        if r is not None:
            axes[3].plot(r.i, r.coeffs,
                         color='gray', marker='.', alpha=0.5, ls='')
            axes[3].errorbar(r.i[r.selection], r.coeffs[r.selection], yerr=r.coeffs_err[r.selection],
                             ls='', marker='.')
            y = r.coeffs[r.selection]
            ym, ys = np.median(y), mad(y)
            axes[3].set_ylim((ym-3*ys, ym+3*ys))
            axes[3].set_ylabel('projection')


def clean_and_project_spectra(tds, basis, **kw):
    r"""Spectrum compression function

    This function loops over all the spectra contained in the `TrainingDataset`
    and projects each of them on the basis specified in argument. The
    compression is performed by the `Spec` class, which fits a function of the
    form :math:`\sum_i \theta_i B_i(\lambda)` on the spectra.


    .. note: this is the first version of the spectrum projection / compression
        code. It is slow and does not reject outliers. Likely to be deprecated
        in a near future.

    """
    nsn_max = kw.get('test_nsn_max', None)
    #spec_data = tds.spec_data
    if tds.spec_data is not None:
        spec_data = tds.spec_data
    else:
        spec_data = tds.spectrophotometric_data
        l = []
        with_errors = []
        z = spec_data.z
    for i, spec in enumerate(spec_data.spec_set):
        s = Spec(tds, spec, basis)
        logger.info(f'processing {s.sn} {spec}')
        try:
            s.process()
            p = s.get_projected_spectrum()
        except:
            logger.error(f'unable to process: {s.sn}')
            logger.error(f'{sys.exc_info()}')
            p = None
        if p is None:
            with_errors.append(s)
            continue
        l.append(p)
        if nsn_max is not None and i >= nsn_max:
            break
    return l, with_errors


class ProjFitResults:
    """This is a faster projection class. Fit all spectra on the basis at once.

    .. note:
       this class is very vulnerable to bad data (holes in the spectra,
       not enough points ..) Will be deprecated in a near future.

    """
    def __init__(self, spec_index, spec_data, wl_basis,
                 x, y, yerr, solver, solution,
                 **kw):
        """A collection of spectra projected on a wavelength basis
        """
        self.spec_index = spec_index
        self.spec_data = spec_data
        self.wl_basis = wl_basis
        self.x = x
        self.y = y
        self.yerr = yerr
        self.solver = solver
        self.theta = solution
        self.model_vals = self.solver.model(self.theta)
        self.bads = self.solver.bads
        self.scales = kw.get("scales", np.ones((len(y))))
        self.uncertainty_scales = kw.get("uncertainty_scales", np.ones((len(y))))

    @property
    def res(self):
        """
        Compute and return residuals: data - model
        """
        return self.y - self.model_vals

    @property
    def wres(self):
        """
        Compute and return weighted residuals: (data - model) / error.
        """
        return (self.y - self.model_vals) / self.yerr

    @property
    def chi2(self):
        index = self.spec_index[~self.bads]
        ngood = np.bincount(self.spec_index, ~self.bads)
        return np.bincount(index, weights=self.wres[~self.bads] ** 2) / (ngood - 1)
    
    @property
    def compressed_spec_coeffs(self):
        """
        Calculate compressed spectral coefficients from the fit.
        """
        # I really do not understand why I had written this ...
        # jacobian of the model
        # J = self.solver.model.A
        # this should not be necessary...
        # b = np.bincount(J.col, minlength=J.shape[1])
        # jmax = np.argwhere(np.abs(b) > 0.).ravel().max() + 1
        # cc = np.zeros(J.shape[1])
        # cc[:jmax] = self.theta
        return self.theta

    @property
    def compressed_spec_coeffs_errors(self):
        """"
        Estimate errors on compressed spectral coefficients.
        """
        # This matrix below is J . W^{1/2}
        C = self.solver.A.tocoo()
        H = C.T @ C
        H = H + 1.E-12 * sparse.eye(H.shape[0])
        n = len(self.wl_basis)
        n_spec = H.shape[0] / n
        assert n_spec.is_integer()
        n_spec = int(n_spec)
        d = []
        for i in range(n_spec):
            s = slice(i*n, (i+1)*n)
            U = H[s,s].tocsc()
            d.append(sparse.linalg.inv(U).diagonal())
            errs = np.hstack(d)
        return np.sqrt(errs)

    @property
    def compressed_spectra(self):
        """
        Return projected spectra as a Pandas DataFrame, computing if necessary.
        """
        if not hasattr(self, '_compressed_spectra'):
            self._compressed_spectra = self.get_projected_spectra(drop_n_first_last=2,
                                                                  max_bads=25)
        return self._compressed_spectra

    @classmethod
    def _drop_n_first_last_samples(cls, df, n):
        if n <= 0:
            logger.warning(f'drop_n_first_last_samples: negative n={n}')
            return df
        def trim(group):
            non_zero = group[group.flux != 0.]
            if len(non_zero) < n:
                return pandas.DataFrame()
            cut = non_zero.iloc[n:-n]
            return group.loc[cut.index]
        return df.groupby('spec', group_keys=False).apply(trim)

    # @classmethod
    # def _hack_first_last_errors(cls, df, n, fact=5.):
    #     if n <= 0:
    #         logger.warning(f'hack_first_last_errors: n<0')
    #         return df
    #     def rescale(group):
    #         group = group.copy()
    #         if len(group) < n:
    #             group.loc[:, 'fluxerr'] *= fact
    #         else:
    #             group.loc[group.index[:n], 'fluxerr'] *= fact
    #             group.loc[group.index[-n:], 'fluxerr'] *= fact
    #         return group
    #     return df.groupby('spec', group_keys=False).apply(rescale)

    @classmethod
    def _hack_first_last_errors(cls, df, n, fact=5.):
        if n <= 0:
            logger.warning(f'hack_first_last_errors: n<0')
            return df
        def rescale(group):
            if len(group) < n:
                group.loc[:, 'fluxerr'] *= fact
            else:
                group.loc[group.index[:n], 'fluxerr'] *= fact
                group.loc[group.index[-n:], 'fluxerr'] *= fact
            return group
        return df.groupby('spec', group_keys=False).apply(rescale)

    def _nbads_per_spectrum(self):
        """
        """
        r = np.bincount(self.spec_index, self.solver.bads)
        return r

    def get_projected_spectra(self, drop_n_first_last=2, max_bads=5,
                              max_restframe_wavelength_gap=40.,
                              hack_first_last_errors=5,
                              rescale_final_uncertainties=1.):
        """
        Compute and return projected spectra, optionally excluding edge samples.
        """
        wl = integ(self.wl_basis, n=1) / integ(self.wl_basis, n=0)
        spec_length = len(self.wl_basis)
        n_spec = len(np.unique(self.spec_index))
        N = spec_length * n_spec
        i_basis = np.arange(len(self.wl_basis))

        df = pandas.DataFrame({'spec_index': self.spec_index,
                               'sn': self.spec_data.sn,
                               'mjd': self.spec_data.mjd,
                               'spec': self.spec_data.spec,
                               'z': self.spec_data.z,
                               'resolution': self.spec_data.groupby('spec').wavelength.transform(lambda x: x.diff().median()),
                               'scales':self.scales,
                               'uncertainty_scales':self.uncertainty_scales*rescale_final_uncertainties,
                               })
        # restframe wavelength resolution
        df['restframe_wavelength'] = self.spec_data.wavelength / (1. + self.spec_data.z)
        df['restframe_resolution'] = df.groupby('spec').restframe_wavelength.transform(lambda x: x.diff().median())
        df['max_restframe_wavelength_gap'] = df.groupby('spec').restframe_wavelength.transform(lambda x: x.diff().max())

        by_spec_index = df.groupby('spec_index').first().sort_index()
        self.by_spec_index = by_spec_index # for debugging purposes, just in case

        df = pandas.DataFrame({
            'sn': by_spec_index.sn.repeat(spec_length).to_numpy(),
            'spec': by_spec_index.spec.repeat(spec_length).to_numpy(),
            'spec_index': np.arange(n_spec).repeat(spec_length),
            'mjd': by_spec_index.mjd.repeat(spec_length).to_numpy(),
            'z': by_spec_index.z.repeat(spec_length).to_numpy(),
            'valid': 1,
            'exptime': 0.,
            'wavelength': np.tile(wl, n_spec),
            'i_basis': np.tile(i_basis, n_spec),
            'flux': self.compressed_spec_coeffs,
            'fluxerr': self.compressed_spec_coeffs_errors * rescale_final_uncertainties,
            'resolution': by_spec_index.resolution.repeat(spec_length).to_numpy(),
            'restframe_resolution': by_spec_index.restframe_resolution.repeat(spec_length).to_numpy(),
            'scales':by_spec_index.scales.repeat(spec_length).to_numpy(),
            'uncertainty_scales':by_spec_index.uncertainty_scales.repeat(spec_length).to_numpy(),
            'chi2': self.chi2.repeat(spec_length),
            })

        if drop_n_first_last:
            df = self._drop_n_first_last_samples(df, n=drop_n_first_last)

        if hack_first_last_errors:
            df = self._hack_first_last_errors(df, n=hack_first_last_errors, fact=5.)

        if max_bads is not None:
            c = self._nbads_per_spectrum()
            to_remove = np.argwhere(c > max_bads).flatten()
            logger.info(f'removing {len(to_remove)} spectra with too many bads: {to_remove}')
            df = df.loc[~df.spec_index.isin(to_remove)]

        if max_restframe_wavelength_gap is not None:
            to_remove = by_spec_index[by_spec_index.max_restframe_wavelength_gap > max_restframe_wavelength_gap].spec.unique()
            logger.info(f'removing {len(to_remove)} spectra with gaps larger than {max_restframe_wavelength_gap}')
            logger.info(f'you may want to inspect: {to_remove}')
            df = df.loc[~df.spec.isin(to_remove)]

        idx = df.fluxerr.isna() | np.isinf(df.fluxerr)
        if any(idx):
            logger.info(f'removing {idx.sum()} spectral points with fluxerr=nan/inf')
            df = df.loc[~idx]

        return df

    def plot_spectrum(self, spec_index):
        """
        Plot observed flux, model fit, residuals, and projected spectra.
        """
        fig, axes = plt.subplots(nrows=4, ncols=1,
                                 figsize=(8,10),
                                 sharex=True)
        fig.suptitle(f'spec: {spec_index}')
        if spec_index is not None:
            idx = (self.spec_index == spec_index) & ~self.bads
            bads = (self.spec_index == spec_index) & self.bads
        else:
            idx = ~self.bads
            bads = self.bads

        axes[0].errorbar(self.x[idx], self.y[idx],
                         yerr=self.yerr[idx],
                         ls='', marker='.', color='blue')
        axes[0].errorbar(self.x[bads], self.y[bads],
                         yerr=self.yerr[bads],
                         ls='', marker='x', color='red')
        axes[0].plot(self.x[idx], self.model_vals[idx],
                     ls='--', color='r', zorder=100)
        axes[0].set_ylabel('flux')

        axes[1].errorbar(self.x[idx], self.y[idx]-self.model_vals[idx],
                         yerr=self.yerr[idx],
                         ls='', marker='.', color='blue')
        axes[1].errorbar(self.x[bads], self.y[bads]-self.model_vals[bads],
                         yerr=self.yerr[bads],
                         ls='', marker='x', color='red')
        axes[1].set_ylabel('residuals')

        axes[2].plot(self.x[idx], (self.y[idx]-self.model_vals[idx])/self.yerr[idx],
                     ls='', marker='.', color='blue')
        axes[2].set_ylabel('wres')
        binplot(self.x[idx], (self.y[idx]-self.model_vals[idx])/self.yerr[idx],
                nbins=20, data=None, ax=axes[2], color='r', marker='o')
        axes[2].set_xlabel(r'$\lambda [\AA]$')
        plt.subplots_adjust(hspace=0.05)

        axes[3].errorbar(self.x[idx], self.y[idx],
                         yerr=self.yerr[idx],
                         ls='', marker='.', color='gray')
        cs = self.compressed_spectra
        idx = cs.spec_index == spec_index
        axes[3].errorbar(self.compressed_spectra.wavelength[idx],
                         self.compressed_spectra.flux[idx],
                         yerr=self.compressed_spectra.fluxerr[idx],
                         ls='', marker='.', color='red')

    def plot_fit(self):
        """
        Plot observed flux, model fit, residuals, and projected spectra.
        """
        fig, axes = plt.subplots(nrows=2, ncols=1,
                                 figsize=(8,10),
                                 sharex=True)
        fig.suptitle(f'spectrum projection fit')
        idx = ~self.bads
        bads = self.bads

        axes[0].plot(self.x[idx], self.y[idx]-self.model_vals[idx],
                     #yerr=self.yerr[idx],
                     ls='', marker=',', color='blue')
        axes[0].errorbar(self.x[bads], self.y[bads]-self.model_vals[bads],
                         yerr=self.yerr[bads],
                         ls='', marker='x', color='red')
        axes[0].set_ylabel('residuals')

        axes[1].plot(self.x[idx], (self.y[idx]-self.model_vals[idx])/self.yerr[idx],
                     ls='', marker=',', color='blue')
        axes[1].set_ylabel('wres')
        #        binplot(self.x[idx], (self.y[idx]-self.model_vals[idx])/self.yerr[idx],
        #                nbins=20, data=None, ax=axes[2], color='r', marker='o')
        axes[1].set_xlabel(r'$\lambda [\AA]$')
        plt.subplots_adjust(hspace=0.05)

    def plot(self, spec_index=None):
        if spec_index is not None:
            self.plot_spectrum(spec_index)
        else:
            self.plot_fit()


class SpecProjector:

    def __init__(self, sn_data, spec_data, wl_basis,
                 **kw):
        """A utility class to project a collection of spectra on a wavelength basis

        This class cleans the spectral dataset, removing invalid measurements
        and then projects all the spectra on the wavelength basis at once. The
        projection is implemented as a robust linear fit of the spectral data on
        the basis.

        """
        self.sn_data = sn_data
        self.spec_data = spec_data
        self.wl_basis = wl_basis
        self.error_eval_bin_width = kw.get('error_eval_bin_width', 50.)
        self.beta = kw.get('beta', 1.E-8)
        restframe_wavelength = spec_data.wavelength / (1. + spec_data.z)
        self.restframe_wavelength = restframe_wavelength.to_numpy()
        self.flux = spec_data.flux.to_numpy()
        self.fluxerr = spec_data.fluxerr.to_numpy()
        self.cut = self._select_data()

    def _select_data(self):
        """
        Identify and remove invalid measurements (NaN, Inf, negative, or out-of-range values).
        """
        nan_idx = np.isnan(self.flux) | np.isnan(self.fluxerr)
        inf_idx = np.isinf(self.flux) | np.isinf(self.fluxerr)
        neg_fluxerr_idx = self.fluxerr <= 0.
        # strange_fluxerr = (self.fluxerr < 1.E-25) | (self.fluxerr > 1.E-5)
        wl_min, wl_max = self.wl_basis.grid.min(), self.wl_basis.grid.max()
        out_of_range_idx = (self.restframe_wavelength < wl_min) | (self.restframe_wavelength > wl_max)

        # TODO: add detection of gaps in spectra. If gaps greater than some threshold,
        # remove the spectrum entirely


        self.select_stats = {'nan': nan_idx.sum(),
                             'inf': inf_idx.sum(),
                             'negative_errs': neg_fluxerr_idx.sum(),
                             # 'strange_errs': strange_fluxerr.sum(),
                             'out_of_range': out_of_range_idx.sum()}
        # cut = nan_idx | inf_idx | neg_fluxerr_idx | strange_fluxerr | out_of_range_idx
        cut = nan_idx | inf_idx | neg_fluxerr_idx | out_of_range_idx
        logger.info(f'{cut.sum()} measurements removed.')
        if cut.sum() > 0:
            logger.info(f'nan:{nan_idx.sum()} inf:{inf_idx.sum()} negerr:{neg_fluxerr_idx.sum()} oorng:{out_of_range_idx.sum()}')

        return cut

    def _rescale_spectra(self, spec_index, flux):
        """
        Compute uncertainty scaling factors based on standard deviation of residuals.
        """
        scales = pandas.DataFrame({'spec': spec_index,
                                   'flux': np.abs(flux)}).groupby('spec').median().to_numpy().squeeze()
        return 1. / np.abs(scales[spec_index])

    #    def _rescale_uncertainties(self, spec_index, wres, bads):
    #        scales = pandas.DataFrame({'spec': spec_index[~bads],
    #                                   'wres': wres[~bads]}).groupby('spec').std().to_numpy().squeeze()
    #        # scales = pandas.DataFrame({'spec': spec_index[~bads], 'wres': wres[~bads]}).groupby('spec')['wres'].apply(lambda x: 1.4826 * np.median(np.abs(x - np.median(x)))).to_numpy().squeeze()
    #        return np.abs(scales[spec_index])

    def _rescale_uncertainties(self, spec_index, wres, bads,
                               wavelength=None, deg=None,
                               nbins_wl=10):
        """rescale the initial uncertainties
        """
        wl_bins = np.linspace(self.wl_basis.grid.min(),
                              self.wl_basis.grid.max(),
                              nbins_wl+1)
        spec_index_bins = np.arange(-0.5, spec_index.max()+1., 1.)
        h, _, _ = np.histogram2d(self.spec_data.wavelength[~self.cut],
                                 spec_index,
                                 weights=wres**2,
                                 bins=(wl_bins, spec_index_bins))
        n, _, _ = np.histogram2d(self.spec_data.wavelength[~self.cut],
                                 spec_index,
                                 bins=(wl_bins, spec_index_bins))
        with np.errstate(divide='ignore', invalid='ignore'):
            chi2 = h/n
            self.chi2 = chi2

        if deg is None and wavelength is None:
            # shortcut to get 1 chi2 per spectrum for now
            chi2_mean = np.nanmean(chi2, axis=0)
            scales = np.sqrt(chi2_mean)
            return scales[spec_index]

        # fitting a polynomial scale for each spectrum
        x_fit = 0.5 * (wl_bins[1:] + wl_bins[:-1])
        def fit_column(y):
            mask = ~np.isnan(y)
            if mask.sum() < deg + 1:
                return np.full(deg + 1, np.nan)
            return np.polyfit(x_fit[mask], y[mask], deg)
        coeffs = np.apply_along_axis(fit_column, axis=0, arr=chi2)

        c = coeffs[:, spec_index]
        return np.polyval(c, wavelength)

    def get_spec_index(self, spec_data):
        spec_index, _ = pandas.factorize(spec_data.spec)
        return spec_index

    def fit(self, beta=None, rescale=True,
            # global_flux_scale=None,
            initial_error_pedestal=0.005):
        """
        Perform a robust linear fit to the projected spectra and return the results.

        .. note::
           The initial error pedestal is highly beneficial. Experience shows that,
           even with mock data, we need to slightly inflate the uncertainties,
           especially when projecting rapidly varying spectral features onto a low-resolution basis.
        """
        if beta is None:
            beta = self.beta

        # total number of measurements
        N = (~self.cut).sum()

        # select measurements
        spec_data = self.spec_data[~self.cut]
        restframe_wavelength = self.restframe_wavelength[~self.cut]
        flux = spec_data.flux.to_numpy()
        fluxerr = spec_data.fluxerr.to_numpy()
        
        # one single index for the spectra
        spec_index, _ = pandas.factorize(spec_data.spec)
        n_spectra = len(np.unique(spec_index))

        if rescale:
            scales = self._rescale_spectra(spec_index, flux)
            flux *= scales
            fluxerr *= scales
            if initial_error_pedestal is not None:
                fluxerr = np.sqrt(fluxerr**2 + (initial_error_pedestal*flux)**2)
        # elif global_flux_scale is not None:
        #     flux *= global_flux_scale
        #     fluxerr *= global_flux_scale
        #                if not np.all(scales > 0.):
        #                    return spec_index, restframe_wavelength, flux, fluxerr, scales

        # build the fit matrix, build a model from it
        # and perform an initial (robust) fit
        J = self.wl_basis.eval(restframe_wavelength)
        col = spec_index[J.row] * J.shape[1] + J.col
        JJ = sparse.coo_matrix((J.data, (J.row, col)),
                               shape=(J.shape[0],
                                      J.shape[1] * n_spectra))
        w = 1. / fluxerr
        try:
            model = linearmodels.LinearModel(JJ.row, JJ.col, JJ.data)
            default_logging_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.DEBUG)
            solver = linearmodels.RobustLinearSolver(model, flux,
                                                     weights=w,
                                                     beta=self.beta)
            coeffs = solver.robust_solution(nsig=4.)
            logging.getLogger().setLevel(default_logging_level)
        except:
            logger.error(f'unable to fit (1/2)')
            logger.error(f'{sys.exc_info()}')
            return JJ

        # rescale the uncertainties and refit
        wres = w * (flux - model(coeffs))
        uncertainty_scales = self._rescale_uncertainties(spec_index, wres, solver.bads)
        logger.info(f'uncertainty_scales: {uncertainty_scales}')
        logger.info(f'{uncertainty_scales.min()} {uncertainty_scales.max()} {np.isnan(uncertainty_scales).sum()}')
        fluxerr *= uncertainty_scales
        w = 1. / fluxerr
        try:
            model = linearmodels.LinearModel(JJ.row, JJ.col, JJ.data)
            default_logging_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.DEBUG)
            solver = linearmodels.RobustLinearSolver(model, flux,
                                                     weights=w,
                                                     beta=self.beta)
            coeffs = solver.robust_solution(nsig=4.)
            logging.getLogger().setLevel(default_logging_level)
        except:
            logger.error(f'unable to fit (2/2)')
            logger.error(f'{sys.exc_info()}')
            return JJ


        # gather the fit results and return them
        r = ProjFitResults(spec_index, spec_data, self.wl_basis,
                           restframe_wavelength, flux, fluxerr,
                           solver, coeffs, scales=scales,
                           uncertainty_scales=uncertainty_scales)

        #        r.J = J
        #        r.JJ = JJ
        #r.uncertainty_scales = uncertainty_scales
        self.spec_index = spec_index
        self.coeffs = coeffs
        self.wres = wres
        self.bads = solver.bads

        return r

    def plot(self):
        """
        Visualize the results of the spectral projection and fit.
        """
        pass
