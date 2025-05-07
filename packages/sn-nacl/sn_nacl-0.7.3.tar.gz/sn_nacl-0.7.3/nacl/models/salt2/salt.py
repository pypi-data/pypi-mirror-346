"""Pure python reimplementation of the original salt2 model
"""

import functools
import logging

import numpy as np
import scipy.sparse
import sncosmo

try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt

from bbf import bspline, SNFilterSet, SNMagSys
from saltworks import FitParameters

from .colorlaw import ColorLaw
from .lightcurves import LightcurveEvalUnit
from .spectra import (
    CompressedSpectrumEvalUnit,
    CompressedSpectroPhotoEvalUnit,
    SpectrumEvalUnitFast
)
#   SpectrumRecalibrationPolynomials


logger = logging.getLogger(__name__)


class SALT2Like(object):
    r"""A re-implementation of the SALT2 model

    SALT2 is an empirical SN spectrophotometric model. This class provides a
    pure python re-implementation of SALT2 with a number of improvements.

    The SALT2 parametrization is defined as follows. In the SN restframe the
    absolute spectral density :math:`S(\lambda)` is:

    .. math::
        S(\lambda, \mathrm{p}) = X_0 \times \left[M_0(\lambda, \mathrm{p}) + X_1
           \times M_1(\lambda, \mathrm{p})\right]\ 10^{0.4 c CL(\lambda)}

    where :math:`\mathrm{p}` is the SN phase, i.e. the restframe time since SN
    peak luminosity:

    .. math::
        \mathrm{ph} = \frac{t_{MJD} - t_{max}}{1 + z}

    :math:`M_0`, :math:`M_1` are global surfaces describing the spectral
    evolution of the average SN and its principal variation, and
    :math:`CL(\lambda)` is a global "extinction correction" describing the color
    diversity of the SNIa family.

    :math:`(X_0, X_1, c)` are SN-dependent. :math:`X_0` is the amplitude of the
    "SN-frame B-band lightcurve" as inferred from the observer-frame fluxes.
    :math:`X_1` is the coordinate of the SN along :math:`M_1`. In practice, it
    quantifies the variations of the light curve width. :math:`c` is the SN
    color -- or more exactly, the SN color excess with respect to the average SN
    color.

    """

    def __init__(self, training_dataset,
                 phase_range=(-20., 50.),
                 wl_range=(2000., 11000.),
                 basis_knots=[200, 20],
                 filter_wl_range=(2000., 11000.),
                 basis_filter_knots=1500,
                 wl_grid=None, phase_grid=None,
                 spectrum_recal_degree=3,
                 normalization_band_name='swope2::b',
                 color_band_names=('swope2::b', 'swope2::v'),
                 disable_cache=False,
                 # color_law_out_of_the_integral=False,
                 dust_extinction_model=None,
                 compressed_spectra=True):
        """Constructor for the SALT2Like class

        Initializes the bases (phase, wavelength, filter), computes the Gram
        matrix, evaluates the color law on the effective wavelengths, and
        organizes the data into spectral/photometric computing units.

        Parameters
        ----------
        training_dataset : nacl.dataset.TrainingDataset
            The training dataset containing light curve and spectral data.
        phase_range : tuple of float, optional
            Nominal phase range of the model, by default (-20., 50.).
        wl_range : tuple of float, optional
            Nominal wavelength range of the model, by default (3000., 11000.).
        basis_knots : list of int, optional
            Number of wavelength and photometric knots, by default [200, 20].
        basis_filter_knots : int, optional
            Number of knots for the filter basis, by default, 1500.
        wl_grid : array-like, optional
            Grid of wavelengths, to be used for basis construction.
        phase_grid : array-like, optional
            Grid of phases, to be used for basis construction.
        spectrum_recal_degree : int, optional
            Degree of the spectrum recalibration polynomials, by default 3.
        normalization_band_name : str, optional
            Name of the band to be used for model normalization, by default swope2::b
        disable_cache : bool, optional
            If True, disable the caching system, by default False.
        """
        self.training_dataset = training_dataset
        self.lc_data = training_dataset.lc_data
        self.spectrum_recal_degree = spectrum_recal_degree
        self.delta_phase = 0. # check: do not remember what this is
        if self.training_dataset.lc_data is not None:
            self.bands = list(self.training_dataset.transmissions.keys())
        self.normalization_band_name = normalization_band_name
        self.color_band_names = color_band_names # used by the constraints
        self._compressed_spectra = compressed_spectra
        self.timing = []

        self.basis, self.gram, self.G2, self.L_eff = None, None, None, None
        self.val, self.jacobian_val, self.jacobian_i, self.jacobian_j = None, None, None, None
        self.polynome_color_law, self.jacobian_color_law = None, None

        # initialize model basis and model parameter vector
        # model component: bases, color law, and parameter vector
        self.basis = SALT2Like._init_bases(self.training_dataset,
                                           wl_grid, phase_grid,
                                           wl_range, phase_range,
                                           basis_knots)

        self.filter_basis = self._init_filter_basis(filter_wl_range,
                                                    basis_filter_knots,
                                                    order=4)

#        # Filter basis
#        self.filter_basis = self._init_filter_basis(filter_wl_range, basis_filter_knots,
#                                                    filter_basis_order)

        # filter database
        static_bands = set([self.normalization_band_name] + list(self.color_band_names))
        self.filter_db = self._init_filter_db(self.filter_basis, band_names=static_bands)

        # normalization parameter
        self.norm = self.normalization(pars=None, band_name=normalization_band_name,
                                       default_norm=1.01907246e-12)

        # grams
        self.init_grams_and_cc_grid()

        # dust
        self.dust_extinction_model = dust_extinction_model

        # color law
        self.color_law = ColorLaw()

        # and finally, prepare the computing units
        self.queue = self._init_eval_units()

        # cache system
        self.disable_cache = disable_cache
        self.cached = False
        self._cache = None

        # now that everything is initialized, store some global
        # basis properties which are used in other parts of the code
        self.phase_range = self.basis.by.grid.min(), self.basis.by.grid.max() # phase_range
        self.wl_range = self.basis.bx.grid.min(), self.basis.bx.grid.max() # wl_range
        self.wl_grid = self.basis.bx.grid
        self.phase_grid = self.basis.by.grid
        self.filter_wl_range = self.filter_basis.grid.min(), self.filter_basis.grid.max() # filter_wl_range
        self.n_wl, self.n_ph = len(self.basis.bx.grid), len(self.basis.by.grid) # basis_knots[0],  basis_knots[1]
        self.basis_knots = self.n_wl, self.n_ph # basis_knots
        self.basis_filter_knots = basis_filter_knots   # len(self.filter_basis)

        # tests whether all data points are within the model range.
        # if not, print a warning
        self._check_out_of_range_datapoints()

    def _init_filter_basis(self, filter_wl_range, basis_filter_knots, order=4):
        """
        """
        return bspline.BSpline(np.linspace(filter_wl_range[0],
                                           filter_wl_range[1],
                                           basis_filter_knots),
                               order=order)

    def _init_filter_db(self, filter_basis, band_names):
        """
        """
        filter_db = SNFilterSet(basis=filter_basis)
        for bn in band_names:
            if bn not in filter_db:
                filter_db.insert(bn, z=0.)
        return filter_db

    def _check_out_of_range_datapoints(self):
        """
        """
        valid = SALT2Like.flag_out_of_range_datapoints(self.training_dataset,
                                                       phase_range=self.phase_range,
                                                       wl_range=self.wl_range,
                                                       basis_knots=self.basis_knots,
                                                       basis_filter_knots=self.basis_filter_knots,
                                                       wl_grid=self.wl_grid,
                                                       phase_grid=self.phase_grid,
                                                       compress=False)
        n_out = list(map(lambda x: 0 if x is None else (~x).sum(), valid))
        if n_out[0] > 0:
            logger.warning(f'{n_out[0]} lc data points outside model definition range')
        if n_out[1] > 0:
            logger.warning(f'{n_out[1]} spec data points outside model definition range')
        if n_out[2] > 0:
            logger.warning(f'{n_out[2]} spectrophotometric data points outside model definition range')

    def clone(self, new_tds, **kwargs):
        """clone new model, same features, different tds
        """
        phase_range = kwargs.get('phase_range', self.phase_range)
        wl_range = kwargs.get('wl_range', self.wl_range)
        basis_knots = kwargs.get('basis_knots', self.basis_knots)
        filter_wl_range = kwargs.get('filter_wl_range', self.filter_wl_range)
        basis_filter_knots = kwargs.get('basis_filter_knots', self.basis_filter_knots)
        wl_grid = kwargs.get('wl_grid', self.wl_grid)
        phase_grid = kwargs.get('phase_grid', self.phase_grid)
        spectrum_recal_degree = kwargs.get('spectrum_recal_degree', self.spectrum_recal_degree)
        normalization_band_name = kwargs.get('normalization_band_name', self.normalization_band_name)
        color_band_names = kwargs.get('color_band_names', self.color_band_names)
        disable_cache = kwargs.get('disable_cache', self.disable_cache)
        dust_extinction_model = kwargs.get('dust_extinction_model', self.dust_extinction_model)
        return self.__class__(new_tds,
                              phase_range=phase_range,
                              wl_range=wl_range,
                              basis_knots=basis_knots,
                              filter_wl_range=filter_wl_range,
                              basis_filter_knots=basis_filter_knots,
                              wl_grid=wl_grid,
                              phase_grid=phase_grid,
                              spectrum_recal_degree=spectrum_recal_degree,
                              normalization_band_name=normalization_band_name,
                              color_band_names=color_band_names,
                              disable_cache=disable_cache,
                              dust_extinction_model=dust_extinction_model)

    @classmethod
    def flag_out_of_range_datapoints(cls, training_dataset,
                                     phase_range=(-20., 50.),
                                     wl_range=(2000., 11000.),
                                     basis_knots=[200, 20],
                                     basis_filter_knots=900,
                                     wl_grid=None, phase_grid=None,
                                     update=False,
                                     compress=False):
        """
        Flags data points in the training dataset that are out of the specified model phase and wavelength ranges.

        Parameters
        ----------
        training_dataset : TrainingDataset
            The training dataset containing lightcurves and/or spectral data
        phase_range : tuple of float, optional
            The valid range of phases (default is (-20., 50.)).
        wl_range : tuple of float, optional
            The valid range of wavelengths (default is (2000., 11000.)).
        basis_knots : list of int, optional
            The number of knots for the B-spline bases in wavelength and phase (default is [200, 20]).
        basis_filter_knots : int, optional
            The number of knots for the filter B-spline basis (default is 900).
        wl_grid : array-like, optional
            The wavelength grid for the model basis (default is None).
        phase_grid : array-like, optional
            The phase grid for the model basis (default is None).
        update : bool, optional
            If True, update the internal measurement `valid` flag (default is False)
        compress : bool, optional
            If True, compress the training dataset to exclude flagged data points (default is False).

        Returns
        -------
        tuple
            A tuple containing:
            - lc_valid (array-like or None): Boolean array indicating valid light curve data points.
            - spec_valid (array-like or None): Boolean array indicating valid spectral data points.
            - spectrophot_valid (array-like or None): Boolean array indicating valid spectrophotometric data points.

        Notes
        -----
        This method performs the following operations:
        1. Initializes model and filter bases using the provided grids and ranges.
        2. Calculates the valid phase and wavelength ranges from the model basis.
        3. Flags light curve data points that are outside the model's phase range.
        4. Flags spectral data points that are outside the model's phase and wavelength ranges.
        5. Flags spectrophotometric data points that are outside the model's phase and wavelength ranges.
        6. If `compress` is True, updates the training dataset to exclude flagged data points.

        Logging
        -------
        Logs the number of data points removed for each type (light curve, spectral, spectrophotometric).

        Examples
        --------
        >>> from nacl.dataset import TrainingDataset
        >>> from lemaitre import bandpasses
        >>> tds = TrainingDataset.read_parquet("data/test_datasets/test_datasets_blind.parquet")
        >>> lc_valid, spec_valid, spectrophot_valid = SALT2Like.flag_out_of_range_datapoints(tds, compress=True)
        """
        tds = training_dataset
        model_basis = cls._init_bases(tds, wl_grid, phase_grid,
                                      wl_range, phase_range, basis_knots)
        filter_basis = bspline.BSpline(np.linspace(wl_range[0], wl_range[1],
                                                   basis_filter_knots), order=4)
        filter_db = SNFilterSet(basis=filter_basis)

        # model phase range, model wavelength range
        ph_min, ph_max = model_basis.by.grid.min(), model_basis.by.grid.max()
        wl_min, wl_max = model_basis.bx.grid.min(), model_basis.bx.grid.max()

        tmax = np.zeros(len(tds.sn_data))
        tmax[tds.sn_data.sn_index] = tds.sn_data.tmax[:]

        if tds.lc_data is not None:
            # select the light curves for which the filters
            # overlap with the model definition range
            valid = {}
            for lc in tds.lc_db:
                tr = filter_db.insert(lc.band, lc.z)
                valid[lc.lc_index] = tr.valid
            # tr_data = [filter_db.insert(lc.band, lc.z) for lc in tds.lc_db]
            # valid = np.array([tr.valid for tr in tr_data])
            lc_valid = np.array([valid[lci] for lci in tds.lc_data.lc_index])
            # select the light curve data points which are
            # in the model phase range
            restframe_phase = (tds.lc_data.mjd - tmax[tds.lc_data.sn_index]) / (1. + tds.lc_data.z)
            lc_valid &= ((restframe_phase >= ph_min) & (restframe_phase <= ph_max))
            tds.restframe_phase = restframe_phase
            # logger.info(f' --> {(~((restframe_phase >= ph_min) & (restframe_phase <= ph_max))).sum()}')
            n_out = (~lc_valid).sum()
            if n_out > 0:
                logger.warning(f'{n_out} lc data points outside the model definition range')
        else:
            lc_valid = None

        if tds.spec_data is not None:
            # select the spectra which are in the model phase range
            # tmax = tds.sn_data.tmax[tds.spec_data.sn_index]
            restframe_phase = (tds.spec_data.mjd - tmax[tds.spec_data.sn_index]) / (1. + tds.spec_data.z)
            spec_valid = (restframe_phase >= ph_min) & (restframe_phase <= ph_max)
            # select the spectral points which are in the model spectral range
            restframe_wl = tds.spec_data.wavelength / (1. + tds.spec_data.z)
            spec_valid &= (restframe_wl >= wl_min) & (restframe_wl <= wl_max)
            n_out = (~spec_valid).sum()
            if n_out > 0:
                logger.warning(f'{n_out} spec data points outside the model definition range')
        else:
            spec_valid = None

        if tds.spectrophotometric_data is not None:
            # same cut, for the spectrophotometric data
            # tmax = tds.sn_data.tmax[tds.spectrophotometric_data.sn_index]
            restframe_phase = (tds.spectrophotometric_data.mjd - tmax[tds.spectrophotometric_data.sn_index]) / (1. + tds.spectrophotometric_data.z)
            spectrophot_valid = (restframe_phase >= ph_min) & (restframe_phase <= ph_max)
            restframe_wl = tds.spectrophotometric_data.wavelength / (1. + tds.spectrophotometric_data.z)
            spectrophot_valid &= (restframe_wl >= wl_min) & (restframe_wl <= wl_max)
            n_out = (~spectrophot_valid).sum()
            if n_out > 0:
                logger.warning(f'{n_out} spectrophot data points outside the model definition range')
        else:
            spectrophot_valid = None

        if update:
            if lc_valid is not None:
                tds.lc_data.valid &= lc_valid
            if spec_valid is not None:
                tds.spec_data.valid &= spec_valid
            if spectrophot_valid is not None:
                tds.spectrophotometric_data.valid &= spectrophot_valid

        if compress:
            if lc_valid is not None:
                tds.lc_data.valid &= lc_valid
                lc_valid = lc_valid[lc_valid]
            if spec_valid is not None:
                tds.spec_data.valid &= spec_valid
                spec_valid = spec_valid[spec_valid]
            if spectrophot_valid is not None:
                tds.spectrophotometric_data.valid &= spectrophot_valid
                spectrophot_valid = spectrophot_valid[spectrophot_valid]
            tds.compress()

        return (lc_valid, spec_valid, spectrophot_valid)

    def _get_from_cache(self, pars, jac=False):
        """
        Retrieve the cached model results and Jacobian matrix (if applicable).

        This method checks if the current parameter set matches the parameters
        stored in the cache. If they match, it retrieves the cached model results,
        and optionally, the Jacobian matrix.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            The current set of fit parameters.
        jac : bool, optional
            Flag indicating whether the Jacobian matrix is needed. Defaults to False.

        Returns
        -------
        tuple or None
            - If `jac` is False and the cache is valid, returns the cached model results (numpy.array).
            - If `jac` is True and the cache is valid, returns a tuple containing the cached model results and Jacobian matrix (numpy.array, scipy.sparse.csr_matrix).
            - If the cache is invalid or not present, returns None.

        Notes
        -----
        The cache is validated by comparing the current parameters (`pars.full`) with the cached parameters.
        If the parameters do not match, the cache is considered invalid and None is returned.
        """

        if self.disable_cache or not hasattr(self, '_cache') or self._cache is None:
            return None

        p, v, J = self._cache
        if len(pars.full) != len(p.full):
            return None
        # TODO: check fixed pars
        if np.array_equal(pars.full, p.full) and np.array_equal(pars.indexof(), p.indexof()):
            if not jac:
                return v
            else:
                if J is None:
                    return None
                return v, J
        return None

    def  _save_to_cache(self, pars, v, J=None):
        """
        Save the current model results and Jacobian matrix to the cache.

        This method stores the provided model results and optionally the Jacobian
        matrix in the cache along with the current parameter set. This allows for
        quick retrieval of these values in future computations if the parameters
        have not changed.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            The current set of fit parameters to be cached.
        v : numpy.array
            The model results to be cached.
        J : scipy.sparse.csr_matrix, optional
            The Jacobian matrix to be cached. Defaults to None.
        """
        if not self.disable_cache:
            self._cache = (pars.copy(), v, J)
        else:
            self._cache = None

    def get_gram_dot_filter(self, band_name=None):
        """Used by the integral constraints
        """
        key = band_name if band_name is not None else self.normalization_band_name
        coeffs = self.filter_db[key].tq
        return self.gram.dot(coeffs)

    def reduce(self, wl):
        return self.color_law.reduce(wl)

    def init_grams_and_cc_grid(self):
        r"""Compute the :math:`\Lambda^{\mathrm{eff}}_{\ell q}` matrix (see definition above) on which the color
        law is evaluated.

        .. math::
             \bar{\lambda}_{\ell q} = \frac{\int \lambda^2 B_\ell(\lambda) B_q(\lambda)
             d\lambda}{\int \lambda B_\ell(\lambda) B_q(\lambda) d\lambda}

        Compute de grammian of order one, :math:`G` and two :math:`G2` of the model :

        .. math::
            G = \int \lambda B_\ell(\lambda) B_q(\lambda) d\lambda \\
            G2 = \int \lambda^2 B_\ell(\lambda) B_q(\lambda) d\lambda


        .. note::
             this method will be moved to the main model class (since we may work
             with one single :math:`\Lambda^{\mathrm{eff}}` matrix in a near future).
        """
        self.gram = get_gram(0., self.basis.bx, self.filter_basis, lambda_power=1)
        self.G2 = get_gram(0., self.basis.bx, self.filter_basis, lambda_power=2)

        gram = self.gram.tocoo()
        gram2 = self.G2.tocoo()
        assert(~np.any(gram.row-gram2.row) and ~np.any(gram.col-gram2.col))
        l_eff = gram2.data / gram.data
        self.L_eff = scipy.sparse.coo_matrix((l_eff, (gram.row, gram.col)), shape=gram.shape)

    def get_struct(self):
        """return the structure of the fit parameter vector

        In practice, the fit parameter vector is larger than just the model
        parameters: it also contains the parameters of the error models (error
        snake, color scatter, calibration, see e.g. variancemodels.py). The
        instantiation of the final fit parameter vector cannot therefore be
        performed by the model itself. What the model can do, is to return the
        description of the fit parameter blocks it knows about.

        """
        # note : the model can be computed even for the invalid measurements
        # if they are still present in the dataset
        nb_sne = self.training_dataset.nb_sne(valid_only=False)
        # nb_spectra = self.training_dataset.nb_spectra()
        # nb_passbands = len(self.bands)
        # spec_recalibration_npars = self.recalibration_degree + 1
        # nb_lightcurves = self.training_dataset.nb_lcs(valid_only=False)
        d = [('X0',   nb_sne),
             ('X1',   nb_sne),
             ('c',  nb_sne),
             ('tmax', nb_sne),
             ('M0',   len(self.basis)),
             ('M1',   len(self.basis)),
             ('CL',  4)]
        if hasattr(self, 'recal_func'):
            d.extend(self.recal_func.get_struct())
            #        if self.training_dataset.spec_data is not None:
            #            d.append(('SpectrumRecalibration', spec_recalibration_npars.sum()))
        return d

    def init_pars(self, pars=None, model_name='salt2.4', version='2.4', use_truth=False):
        """
        Instantiate and initialize a fit parameter vector

        This method initializes the fit parameters for the SALT2 model. If no
        parameters are provided, it creates a new `FitParameters` object based
        on the model's structure. It then initializes the parameter vector. The
        SN-specific parameters are initialized from the `TrainingDataset` held
        by the model. The model-specific parameters (M0, M1, CL) are built from
        previous models (e.g. SALT2 or SALT3, retrieved from `sncosmo`)

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters, optional
            Existing fit parameters to initialize. If None, a new `FitParameters` object is created.
        model_name : str, optional
            The name of the model version to use for initialization, by default 'salt2.4'.
        version : str, optional
            The version of the model to use for initialization, by default '2.4'.

        Returns
        -------
        pars : nacl.fitparameters.FitParameters
            Initialized model parameters.

        Notes
        -----
        The model parameters are obtained from a projection of the SALT2/SALT3
        surfaces on the model basis. As the model basis may differ from the
        original SALT2/SALT3 bases, this initialization yields only an
        approximation of the original models.
        """
        if pars is None:
            pars = FitParameters(self.get_struct())

        self.init_model_pars(pars, model_name=model_name, version=version)
        self.init_from_training_dataset(pars, use_truth=use_truth)

        if 'SpectrumRecalibration' in pars._struct:
            self.recal_func.init_pars(pars)

        return pars

    def init_from_training_dataset(self, pars, use_truth=False):
        """Load initial SN parameters from the training dataset.

        This method initializes the SN-specific parameters (X0, X1, c, tmax)
        from the `TrainingDataset` held by the model.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            Fit parameters to be initialized.
        """
        sn_data = self.training_dataset.sn_data
        if use_truth:
            try:
                logging.warning('initializing model from simulation truth (if available)')
                pars['X0'].full[sn_data.sn_index] = sn_data.nt['x0_true']
                pars['X1'].full[sn_data.sn_index] = sn_data.nt['x1_true']
                pars['c'].full[sn_data.sn_index] = sn_data.nt['c_true']
                pars['tmax'].full[sn_data.sn_index] = sn_data.nt['tmax_true']
                return
            except:
                logging.warning("unable to use truth to initialize the SN parameters. Reverting to default")

        pars['X0'].full[sn_data.sn_index] = sn_data.x0
        pars['X1'].full[sn_data.sn_index] = sn_data.x1
        pars['c'].full[sn_data.sn_index] = sn_data.col
        pars['tmax'].full[sn_data.sn_index] = sn_data.tmax

    def init_model_pars(self, pars, model_name='salt2', version='2.4'):
        """Load and adapt the SALT2/SALT3 global surfaces and color law from `sncosmo`.

        This method loads the coefficients of the SALT2.4 surfaces and color
        law. The definition of the model spline bases may differ from the
        original definition of the SALT2/SALT3 bases; thus, the original
        surfaces are reprojected onto the model basis.

        Parameters
        ----------
        pars : nacl.lib.fitparameters.FitParameters
            Fit parameters to be initialized.
        model_name : str, optional
            The name of the model version to use for initialization, by default 'salt2'.
        version : str, optional
            The version of the model to use for initialization, by default '2.4'.
        """
        salt2_source = sncosmo.get_source('salt2', version='2.4')

        phase_grid = np.linspace(self.phase_range[0], self.phase_range[1], self.n_ph)
        wl_grid = np.linspace(self.wl_range[0], self.wl_range[1], self.n_wl)
        basis = bspline.BSpline2D(wl_grid, phase_grid, x_order=4, y_order=4)

        phase_salt = salt2_source._phase
        wl_salt = salt2_source._wave

        w, p = np.meshgrid(wl_salt, phase_salt)

        sncosmo_scale = salt2_source._SCALE_FACTOR
        salt2_m0 = salt2_source._model['M0'](phase_salt, wl_salt).ravel() / sncosmo_scale
        salt2_m1 = salt2_source._model['M1'](phase_salt, wl_salt).ravel() / sncosmo_scale
        salt2_cl = np.array(salt2_source._colorlaw_coeffs)[::-1]

        jac = self.basis.eval(w.ravel(), p.ravel()).tocsr()
        factor = cholesky_AAt(jac.T, beta=1.E-6)

        pars['M0'].full[:] = factor(jac.T * salt2_m0)
        pars['M1'].full[:] = factor(jac.T * salt2_m1)
        pars['CL'].full[:] = salt2_cl

    @classmethod
    def _init_bases(cls, tds, wl_grid=None, phase_grid=None,
                    wl_range=(2000., 11000.),
                    phase_range=(-20., 50.), basis_knots=(200,20)):
        """
        Instantiate model bases.

        This class method initializes the model bases using B-splines. If no
        wavelength or phase grid is provided, it creates default grids based
        on the specified ranges and number of knots.

        Parameters
        ----------
        wl_grid : array-like, optional
            User-provided grid in wavelength. If None, a default grid is created.
        phase_grid : array-like, optional
            User-provided grid in phase. If None, a default grid is created.
        wl_range : tuple, optional
            Wavelength range for the default grid, by default (2000., 11000.).
        phase_range : tuple, optional
            Phase range for the default grid, by default (-20., 50.).
        basis_knots : tuple, optional
            Number of knots in wavelength and phase, by default (200, 20).

        Returns
        -------
        bspline.BSpline2D
            The B-spline basis for the model.
        """
        # if the tds has already a wavelength basis, then, it probably means
        # that the spectra have been compressed on that basis. So, the model
        # must use it, no matter what is specified in the arguments (wl_range,
        # and basis_knots or wl_grid)
        if hasattr(tds, 'basis') and tds.basis is not None:
            # if a wl_grid is specified, warn the user that it won't be used
            if wl_grid is not None:
                logger.warning(f'grid {wl_grid.min()}:{wl_grid.max()}:{len(wl_grid)} ignored')
            wl_grid = tds.basis.grid
            x_order = tds.basis.order
            logger.info(f'using the TrainingDataset basis [{wl_grid.min()},{wl_grid.max()},{len(wl_grid)},order={x_order}]')

        if wl_grid is None:
            assert wl_range is not None and basis_knots is not None
            n_wl, n_ph = basis_knots
            logger.info('default regular grid in wavelength')
            wl_grid = np.linspace(wl_range[0], wl_range[1], n_wl)
        else:
            logger.info('user provided grid in wavelength')

        # for the phase, we use what is specified in the arguments.
        if phase_grid is None:
            assert phase_range is not None and basis_knots is not None
            n_wl, n_ph = basis_knots
            logger.info('default regular grid in phase')
            phase_grid = np.hstack([np.linspace(phase_range[0],
                                                phase_range[1],
                                                n_ph)])
        else:
            logger.info('user provided grid in phase')

        return bspline.BSpline2D(wl_grid, phase_grid,
                                 x_order=4, y_order=4)

    def normalization(self, pars=None, band_name='swope2::b', Mb=-19.5, magsys='AB',
                      default_norm=1.01907246e-12):
        """
        Model normalization.

        The SALT2Like normalization is set during training by the constraint
        on the integral of M0 at phase zero. By default, the model is not
        renormalized during evaluation.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters, optional
            Model parameters for normalization. If None, the default normalization is returned.
        band_name : str, optional
            The band used for normalization, by default 'swope2::b'.
        Mb : float, optional
            Absolute magnitude, by default -19.5.
        magsys : str, optional
            Magnitude system, by default 'AB'.
        default_norm : float, optional
            Default normalization value, by default 1.01907246e-12.

        Returns
        -------
        float
            The normalization factor.
        """
        default_norm = default_norm if default_norm is not None else 1.01907246e-12
        # tq, filter_basis = self.filter_db[band_name]
        passband_data = self.filter_db[band_name]

        # AB flux in the specified band
        ms = SNMagSys(self.filter_db, magsys)
        # zp = ms.ZeroPoint(self.filter_db.transmission_db[band_name])
        zp = ms.get_zp(band_name)
        self.int_ab_spec = 10**(0.4 * zp)

        # normalization quantities
        self.flux_at_10pc = np.power(10., -0.4 * (Mb-zp))
        self.flux_at_10Mpc = np.power(10., -0.4 * (Mb+30.-zp))

        if pars is None:
            return default_norm

        phase_eval = self.basis.by.eval(np.array([0. + self.delta_phase])).tocsr()
        gram = get_gram(z=0., model_basis=self.basis.bx,
                        filter_basis=passband_data.basis, lambda_power=1)
        surface_0 = pars['M0'].full.reshape(len(self.basis.by), -1)
        # evaluate the integral of the model in the specified band
        self.int_M0_phase_0 = phase_eval.dot(surface_0.dot(gram.dot(passband_data.tq)))

        return self.flux_at_10Mpc / self.int_M0_phase_0

    def renorm(self, pars, band_name='swope2::b', Mb=-19.5, magsys='AB'):
        """
        Adjust the model normalization.

        This method explicitly recomputes the normalization factor based on the
        provided parameters, band, magnitude, and magnitude system.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            Model parameters for normalization.
        band_name : str, optional
            The band used for normalization, by default 'swope2::b'.
        Mb : float, optional
            Absolute magnitude, by default -19.5.
        magsys : str, optional
            Magnitude system, by default 'AB'.

        Returns
        -------
        None
        """
        # explicitely recompute a normalization
        self.norm = self.normalization(pars, band_name, Mb, magsys,
                                       default_norm=None)

    def _init_eval_units(self):
        """
        Initialize the photometric and spectroscopic evaluation units.

        The actual evaluation of the model is delegated to specialized
        sub-units, which are called sequentially. These units are stored
        in a queue.

        Returns
        -------
        list
            List of initialized evaluation units.
        """
        queue = []
        if self.training_dataset.lc_data is not None:
            logger.info('initializing lightcurve eval unit')
            queue.append(LightcurveEvalUnit(self))
        if self.training_dataset.spec_data is not None:
            logger.info('initializing spectrum eval unit')
            if not self._compressed_spectra:
                queue.append(SpectrumEvalUnitFast(self,
                                                  spec_recal_degree=self.spectrum_recal_degree))
            else:
                queue.append(CompressedSpectrumEvalUnit(self,
                                                        spec_recal_degree=self.spectrum_recal_degree))
        if self.training_dataset.spectrophotometric_data is not None:
            logger.info('initializing spectrophotometric eval unit')
            if not self._compressed_spectra:
                raise "not implemented"
            queue.append(CompressedSpectroPhotoEvalUnit(self))
        return queue

    def precompute_color_law(self, cl_pars, jac=False):
        """
        Precompute the color law for the photometric data.

        Parameters
        ----------
        cl_pars : numpy.array or None
            Color law parameters.
        jac : bool, optional
            If True, computes and stores the Jacobian of the color law, by default False.

        Returns
        -------
        None
        """
        polynome_color_law, jacobian_color_law = \
            self.color_law(self.L_eff.data, cl_pars,
                           jac=jac)  # return_jacobian_as_coo_matrix=False)
        self.polynome_color_law = \
            scipy.sparse.csr_matrix((polynome_color_law,
                                     (self.L_eff.row, self.L_eff.col)),
                                    shape=self.L_eff.shape)
        if jac:
            self.jacobian_color_law = []
            _, n = jacobian_color_law.shape
            for i in range(n):
                jacobian_cl = \
                    scipy.sparse.csr_matrix((jacobian_color_law[:, i],
                                             (self.L_eff.row, self.L_eff.col)), shape=self.L_eff.shape)
                self.jacobian_color_law.append(jacobian_cl)

    def get_restframe_phases(self, pars, data):
        """
        Compute the rest-frame phases for a given dataset.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            Model parameters containing 'tmax'.
        data : object
            Dataset containing MJD and redshift information.

        Returns
        -------
        numpy.array
            Supernova rest-frame phases.
        """
        sn_index = data.sn_index
        tmax = pars['tmax'].full[sn_index]
        return (data.mjd - tmax) / (1.+data.z)

    def __call__(self, pars, jac=False): # , plotting=False, ilc_plot=None, spec_plot=False):
        """
        Evaluate the model for the given parameter set.

        This method evaluates the model by looping over the evaluation units
        and assembling the results into a single vector and, optionally, a
        single Jacobian matrix.

        Parameters
        ----------
        pars : numpy.array
            Vector containing the free parameters.
        jac : bool, optional
            If True, returns the Jacobian matrix, by default False.

        Returns
        -------
        numpy.array
            Model evaluation results.
        scipy.sparse.csr_matrix, optional
            Jacobian matrix if `jac` is True.
        """
        cached_res = self._get_from_cache(pars, jac=jac)
        if cached_res is not None:
            logger.debug('SALT2Like.__call__: returning cached result')
            self.cached = True
            return cached_res
        else:
            self.cached = False

        # self.clear_cache()
        # loop over the eval units
        res = [q(pars, jac) for q in self.queue]

        if not jac:
            model_val = np.add.reduce([r for r in res])
            self._save_to_cache(pars, model_val, None)
            return model_val

        model_val = np.add.reduce([r[0] for r in res])

        rows = np.hstack([r[1].row for r in res])
        cols = np.hstack([r[1].col for r in res])
        vals = np.hstack([r[1].data for r in res])

        idx = cols >= 0
        JJ = scipy.sparse.coo_matrix((vals[idx], (rows[idx], cols[idx])),
                                     shape=res[0][1].shape)

        self._save_to_cache(pars, model_val, JJ)
        return model_val, JJ

    @property
    def y(self):
        """
        Get all flux measurements from the training dataset.

        Returns
        -------
        numpy.array
            Array of all flux measurements.
        """
        return self.training_dataset.get_all_fluxes()

    @property
    def yerr(self):
        """
        Get all flux measurement errors from the training dataset.

        Returns
        -------
        numpy.array
            Array of all flux measurement errors.
        """
        return self.training_dataset.get_all_fluxerr()

    @property
    def bads(self):
        """
        Get boolean array flagging the bad data points from the training dataset.

        Returns
        -------
        numpy.array
            Array of indices of bad data points.
        """
        return self.training_dataset.get_bads()


@functools.cache
def get_gram(z, model_basis, filter_basis, lambda_power=1):
    """Calculate the grammian of to spline basis.

    The grammian :math:`G` of order :math:`N`, to basis :math:`B_0` (define on
    wavelength, in our case surfaces wavelength basis) and :math:`B_1` (define
    on SN-restframe wavelength, filter basis) is defined as:

    .. math::
        G = \\int \\lambda^N B_0(\\lambda) B_q(\\lambda (1+z)) d\\lambda

    Parameters
    -------
    z : numpy.array
        Vector containing the data redshift.
    model_basis : bbf.bspline.BSpline
        Wavelength basis.
    filter_basis : bbf.bspline.BSpline
        Filter basis defined common to all the bands.
    lambda_power : int
        Gramian order.

    Returns
    -------
    gram : scipy.sparse.csc_matrix
        Grammian

    """
    return bspline.lgram(
        model_basis,
        filter_basis,
        z=z,
        lambda_power=lambda_power).tocsc()
