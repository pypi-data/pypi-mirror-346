"""NaCl SALT2Like error models
"""

import logging

import numpy as np
import numpy.polynomial.polynomial as nppol
from scipy import sparse

from bbf.bspline import BSpline2D, integ
from nacl.sparseutils import CooMatrixBuff2

try:
    from sksparse.cholmod import cholesky_AAt
except ImportError:
    from scikits.sparse.cholmod import cholesky_AAt


logger = logging.getLogger(__name__)


class SimpleErrorSnake:
    r"""
    A simplistic error snake model with a single parameter.

    This model represents the variance as a function of the model values:

    .. math::
        V = g^2 \cdot \text{model}^2

    where `g` is a parameter representing the scaling factor.

    Parameters
    ----------
    model : object
        The model used for evaluation.
    """
    def __init__(self, model):
        """
        Constructor.

        Parameters
        ----------
        model : object
            The model used for evaluation.
        """
        self.model = model
        self.training_dataset = model.training_dataset

    def clone(self, model, **kw):
        return self.__class__(model)

    def get_struct(self):
        """
        Get the block structure of the part of the parameter vector used to evaluate the model

        Returns
        -------
        list of tuple
            List containing the block structure of the parameter vector.
            Each item contains the block name and size.
        """
        return [("gamma", 1)]

    def init_pars(self, pars):
        """
        Initialize the blocks of the parameter vector which are specific to this class.

        Parameters
        ----------
        pars : `nacl.fitparameters.FitParameters`
            Parameters object to be initialized.
        """
        pars['gamma'].full[:] = 0.01

    def __call__(self, pars, jac=False):
        """
        Evaluate the variance model and optionally its Jacobian.

        Parameters
        ----------
        pars : object
            Parameters object containing the model parameters.
        jac : bool, optional
            If True, compute and return the Jacobian matrix. Default is False.

        Returns
        -------
        var : numpy.ndarray
            Array of variances.
        J : scipy.sparse.coo_matrix, optional
            Jacobian matrix, returned if `jac` is True.
        """
        v, J = None, None
        if jac:
            v, J = self.model(pars, jac=True)
        else:
            v = self.model(pars, jac=False)
        N = len(v)
        g = pars['gamma'].full[0]
        var = np.full(N, g**2 * v**2)

        if not jac:
            return var

        J = J.tocoo()

        n_free_pars = len(pars.free)
        i = [J.row]
        j = [J.col]
        data = [2. * g**2 * v[J.row] * J.data]
        i.append(np.arange(N))
        j.append(np.full(N, pars['gamma'].indexof(np.zeros(N).astype(int))))
        data.append(2. * g * v**2)

        i = np.hstack(i)
        j = np.hstack(j)
        data = np.hstack(data)

        idx = j >= 0
        J = sparse.coo_matrix((data[idx], (i[idx], j[idx])),
                              shape=(N, n_free_pars))

        return var, J


class LocalErrorSnake:
    r"""
    Error snake variance as a function of phase and wavelength

    This model represents the variance as a combination of a fixed error term and a model-dependent error term:

    .. math::
        V(\lambda, p) = \sigma_{Err}^2 + \sigma_{\mathrm{Mod}}^2(\lambda, p)

    where:

    .. math::
        \sigma_{\mathrm{Mod}}^{spec} &= g(\lambda, p) \times \phi_{\mathrm{spec}}(p, \lambda)\ \ (\mathrm{spectra}) \\
        \sigma_{\mathrm{Mod}}^{phot} &= g(\lambda, p) \times \phi_{\mathrm{phot}}(p, \lambda)\ \ (\mathrm{photometric})

    :math:`\gamma(\lambda, p)` is a global surface describing the spectral residual of a 2D spline surface defined on the same ranges as the corresponding model.
    """
    def __init__(self, model, bins=(10, 10), order=4):
        """Constructor

        Parameters
        ----------
        model : object
            The model used for evaluation.
        bins : tuple of int, optional
            The number of bins for the phase and wavelength grids (default is (10, 10)).
        order : int, optional
            The order of the B-spline (default is 4).
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.order = order

        # instantiate a basis
        ph_bins, wl_bins = bins
        phase_grid = np.linspace(model.basis.by.range[0], model.basis.by.range[-1], ph_bins)
        wl_grid = np.linspace(model.basis.bx.range[0], model.basis.bx.range[-1], wl_bins)
        self.basis = BSpline2D(wl_grid, phase_grid, x_order=order, y_order=order)

    def clone(self, model, **kw):
        ret = self.__class__(model,
                             bins=kw.get('bins', self.bins),
                             order=kw.get('order', self.order))
        return ret

    def get_struct(self):
        """
        Get the block structure of the part of the parameter vector used to evaluate the model.

        Returns
        -------
        list of tuple
            List containing the block structure of the parameter vector.
            Each item contains the block name and size.
        """
        return [('gamma', len(self.basis))]

    def init_pars(self, pars):
        """
        Initialize the blocks of the parameter vector which are specific to this class.

        Parameters
        ----------
        pars : `nacl.fitparameters.FitParameters`
            Parameters object to be (partially) initialized.
        """
        pars['gamma'].full[:] = 0.01

    def __call__(self, pars, jac=False):
        """
        Evaluate the variance model and optionally its Jacobian.

        Parameters
        ----------
        pars : object
            Parameters object containing the model parameters.
        jac : bool, optional
            If True, compute and return the Jacobian matrix. Default is False.

        Returns
        -------
        var : numpy.ndarray
            Array of variances.
        J : scipy.sparse.coo_matrix, optional
            Jacobian matrix, returned if `jac` is True.
        """
        # too bad we need to call the model again here...
        # let's see whether we could cache this call
        if jac:
            flux, Jm = self.model(pars, jac=True)
        else:
            flux = self.model(pars, jac=False)
            Jm = None

        tds = self.training_dataset
        zz = tds.lc_data.z
        tmax = pars['tmax'].full[tds.lc_data.sn_index]
        wl = tds.lc_data.wavelength / (1. + zz)
        phase = (tds.lc_data.mjd - tmax) / (1. + zz)
        Jv = self.basis.eval(wl, phase)

        g = np.zeros(len(tds))
        g[:len(tds.lc_data)] = np.exp(Jv @ pars['gamma'].full)
        v = g * flux**2
        if not jac:
            return v

        # derivatives
        N = len(tds)
        n_free_pars = len(pars.free)
        buff = CooMatrixBuff2((N, n_free_pars))

        # d_gamma
        buff.append(Jv.row,
                    pars['gamma'].indexof(Jv.col),
                    g[Jv.row] * Jv.data * flux[Jv.row]**2)

        # d_dpars
        buff.append(Jm.row,
                    Jm.col,
                    2. * g[Jm.row] * flux[Jm.row] * Jm.data)

        J = buff.tocoo()

        return v, J



class SNLambdaErrorSnake:
    """
    A model to evaluate the variance as a function of wavelength for supernovae.

    This model includes a polynomial dependency on the wavelength for the error calculation.
    """
    def __init__(self, model, deg=3):
        """
        Constructor.

        Parameters
        ----------
        model : object
            The model used for evaluation.
        deg : int, optional
            The degree of the polynomial used for the wavelength dependency (default is 3).
        """
        self.model = model
        self.training_dataset = self.model.training_dataset
        self.deg = deg

        #pre construction of the vandermonde matrix
        lc_data = self.training_dataset.lc_data
        restframe_wl = lc_data.wavelength / (1. + lc_data.z)
        r_wl = np.zeros(len(self.training_dataset))
        r_wl[:len(lc_data)] = restframe_wl
        self.vander_matrix = self.get_vander_matrix(r_wl)

    def clone(self, model, **kw):
        ret = self.__class__(model,
                             order=kw.get('deg', self.deg))
        return ret


    def get_struct(self):
        """
        Get the block structure of the part of the parameter vector relevant for model evaluation.

        Returns
        -------
        list of tuple
            List containing the block structure of the parameter vector.
            Each item contains the block name and size.
        """
        nsn = len(self.training_dataset.sn_data.sn_set)
        npars = self.deg # deg + 1 - 1 constraint
        return [('gamma_sn', nsn), ('gamma_snake', npars)]

    def init_pars(self, pars):
        """
        Initialize the blocks of the parameter vector which are specific to this class.

        Parameters
        ----------
        pars : `nacl.fitparameters.FitParameters`
            Parameters object to be (partially) initialized.
        """
        pars['gamma_sn'].full[:] = 0.01
        pars['gamma_snake'].full[:] = 0.

    def _reduce(self, restframe_wl):
        """
        Map the restframe wavelength to a standardized range (close to [-1,1])

        This is done mostly to improve the conditioning of the polynomial fit.

        Parameters
        ----------
        restframe_wl : numpy.ndarray
            Array of restframe wavelengths.

        Returns
        -------
        numpy.ndarray
            Reduced wavelengths.
        """
        return (restframe_wl-4500.) / (9000. - 2000.)

    def get_vander_matrix(self, restframe_wl):
        """
        Get the Vandermonde matrix for the reduced wavelengths.

        Parameters
        ----------
        restframe_wl : numpy.ndarray
            Array of restframe wavelengths.

        Returns
        -------
        numpy.ndarray
            Vandermonde matrix for the polynomial fit.
        """
        reduced_wl = self._reduce(restframe_wl)
        vander_mat = np.vander(reduced_wl, self.deg, increasing = False)
        return vander_mat

    def __call__(self, pars, jac=False):
        """
        Evaluate the variance model and optionally its Jacobian.

        Parameters
        ----------
        pars : object
            Parameters object containing the model parameters.
        jac : bool, optional
            If True, compute and return the Jacobian matrix. Default is False.

        Returns
        -------
        variance : numpy.ndarray
            Array of variances.
        J : scipy.sparse.coo_matrix, optional
            Jacobian matrix, returned if `jac` is True.
        """
        if jac:
            flux, Jm = self.model(pars, jac=True)
        else:
            flux = self.model(pars, jac=False)
            Jm = None

        tds = self.training_dataset
        zz = tds.lc_data.z
        restframe_wl = tds.lc_data.wavelength / (1. + zz)
        reduced_wl = self._reduce(restframe_wl)
        snake = np.zeros(len(tds))
        snake[:len(tds.lc_data)] = np.exp(np.polyval(pars['gamma_snake'].full, reduced_wl))

        g = np.zeros(len(tds))
        g[:len(tds.lc_data)] = pars['gamma_sn'].full[tds.lc_data.sn_index]
        variance = g**2 * snake * flux**2

        if not jac:
            return variance

        # derivatives
        N = len(tds)
        n_free_pars = len(pars.free)
        buff = CooMatrixBuff2((N, n_free_pars))

        # d_gamma = 2 * snake * g_i * flux**2
        buff.append(tds.lc_data.row,
                    pars['gamma_sn'].indexof(tds.lc_data.sn_index),
                    2 * snake[tds.lc_data.row] * g[tds.lc_data.row] * flux[tds.lc_data.row]**2)

        # d_snake = g**2 * flux**2 * reduced_wl ** i * snake
        data_d_snake = sparse.coo_matrix(variance[:,np.newaxis] * self.vander_matrix[:,0:self.deg-1])
        row_d_snake = data_d_snake.row
        col_d_snake = pars['gamma_snake'].indexof(data_d_snake.col)
        buff.append(row_d_snake,
                    col_d_snake,
                    data_d_snake.data)

        # d_pars = 2 * snake * g**2 + flux * Jm
        buff.append(Jm.row,
                    Jm.col,
                    2. * g[Jm.row]**2 * snake[Jm.row] * flux[Jm.row] * Jm.data)

        J = buff.tocoo()

        return variance, J


class SNLocalErrorSnake:
    r"""
    Error snake variance model as a function of phase and wavelength.

    This model evaluates the variance using a combination of phase, wavelength,
    and a de-weighting factor for each supernova (SN) to capture SN variability.

    .. math::
        V(\lambda, p) = \sigma_{Err}^2 + \sigma_{\mathrm{Mod}}^2(\lambda,p) \times \sigma_{\mathrm{SN}}

    where:

    .. math::
        \sigma_{\mathrm{Mod}}^{spec} &= g(\lambda, p) \times \gamma_{\mathrm{SN}} \times \phi_{\mathrm{spec}}(p,\lambda) \ (\mathrm{spectra}) \\
        \sigma_{\mathrm{Mod}}^{phot} &= g(\lambda, p) \times \gamma_{\mathrm{SN}} \times \phi_{\mathrm{phot}}(p,\lambda) \ (\mathrm{photometric})

    :math:`\gamma(\lambda, p)` is a global surface describing the spectral residual
    of a 2D spline surface defined on the same ranges as the corresponding model.
    :math:`\gamma_{\mathrm{SN}}` is a de-weighting factor for each SN to capture SN variability.
    """
    def __init__(self, model, bins=(10, 10), order=4):
        """
        Constructor for the SNLocalErrorSnake class.

        Parameters
        ----------
        model : object
            The model used for evaluation.
        bins : tuple of int, optional
            Number of bins for phase and wavelength. Default is (10, 10).
        order : int, optional
            Order of the B-spline. Default is 4.
        """
        self.model = model
        self.training_dataset = model.training_dataset

        # instantiate a basis
        ph_bins, wl_bins = bins
        phase_grid = np.linspace(model.basis.by.range[0], model.basis.by.range[-1], ph_bins)
        wl_grid = np.linspace(model.basis.bx.range[0], model.basis.bx.range[-1], wl_bins)
        self.wl_grid = wl_grid
        self.phase_grid = phase_grid
        self.basis = BSpline2D(wl_grid, phase_grid, x_order=order, y_order=order)

    def clone(self, model, **kw):
        ret = self.__class__(model,
                             bins=kw.get('bins', self.bins),
                             order=kw.get('order', self.order))
        return ret

    def get_struct(self):
        """
        Get the block structure of the parameter vector used to evaluate the model.

        Returns
        -------
        list of tuple
            List containing the block structure of the parameter vector.
            Each item contains the block name and size.
        """
        nsn = len(self.training_dataset.sn_data.sn_set)
        return [('gamma_snake', len(self.basis)), ('gamma_sn', nsn)]

    def init_pars(self, pars):
        """
        Initialize the blocks of the parameter vector which are specific to this class.

        Parameters
        ----------
        pars : `nacl.fitparameters.FitParameters`
            Parameters object to be (partially) initialized.
        """

        # initiating at 5% error

        pars['gamma_sn'].full[:] = 1

        WL, P = np.meshgrid(self.wl_grid, self.phase_grid)
        Jm = self.basis.eval(WL.ravel(), P.ravel())

        pars['gamma_snake'].full[:] = np.linalg.pinv(Jm.toarray()) @ np.repeat(2*np.log(0.05), 100)

    def __call__(self, pars, jac=False):
        """
        Evaluate the variance model and optionally its derivatives.

        Parameters
        ----------
        pars : object
            Parameters object containing the model parameters.
        jac : bool, optional
            If True, compute and return the Jacobian matrix. Default is False.

        Returns
        -------
        v : numpy.ndarray
            Array of variances.
        J : scipy.sparse.coo_matrix, optional
            Jacobian matrix, returned if `jac` is True.
        """
        if jac:
            flux, Jm = self.model(pars, jac=True)
        else:
            flux = self.model(pars, jac=False)
            Jm = None

        tds = self.training_dataset
        zz = tds.lc_data.z
        tmax = pars['tmax'].full[tds.lc_data.sn_index]
        wl = tds.lc_data.wavelength / (1. + zz)
        phase = (tds.lc_data.mjd - tmax) / (1. + zz)
        Jv = self.basis.eval(wl, phase)

        # fixing phase edges parameters
        njx = len(self.basis.bx)
        nj = len(self.basis)
        cols_to_keep = np.arange(0, nj-njx-1, 1)

        #cols_full = np.arange(0, nj, 1)
        #b = np.array([0, njy -1])
        #c = np.arange(0, njy, 1)
        #a = c*njy
        #x = [b+i for i in a]
        #x = np.hstack(x)
        #cols_remove = np.isin(cols_full, x)
        #cols_to_keep = ~cols_remove

        mask = np.isin(Jv.col, cols_to_keep)

        filtered_data = Jv.data[mask]
        filtered_row = Jv.row[mask]
        filtered_col = Jv.col[mask]

        col_map = {old_col:new_col for new_col, old_col in enumerate(cols_to_keep)}
        filtered_col = np.array([ col_map[c] for c in filtered_col ])
        new_shape = (Jv.shape[0], len(cols_to_keep))
        Jv = sparse.coo_matrix( (filtered_data, (filtered_row, filtered_col)), shape=new_shape)

        #
        g_snake = np.zeros(len(tds))
        g_snake[:len(tds.lc_data)] = np.exp(Jv @ pars['gamma_snake'].full[:-njx-1])

        g_sn = np.zeros(len(tds))
        g_sn[:len(tds.lc_data)] = pars['gamma_sn'].full[tds.lc_data.sn_index]

        v = g_snake * g_sn**2 * flux**2
        if not jac:
            return v

        # derivatives
        N = len(tds)
        n_free_pars = len(pars.free)
        buff = CooMatrixBuff2((N, n_free_pars))

        # d_gamma_snake
        buff.append(Jv.row,
                    pars['gamma_snake'].indexof(Jv.col),
                    g_snake[Jv.row] * Jv.data * g_sn[Jv.row]**2 * flux[Jv.row]**2)

        # d_gamma_sn
        buff.append(tds.lc_data.row,
                    pars['gamma_sn'].indexof(tds.lc_data.sn_index),
                    2 * g_sn[tds.lc_data.row] * g_snake[tds.lc_data.row] * flux[tds.lc_data.row]**2)

        # d_dpars
        buff.append(Jm.row,
                    Jm.col,
                    2. * g_snake[Jm.row] * g_sn[Jm.row]**2 * flux[Jm.row] * Jm.data)

        J = buff.tocoo()

        return v, J


class SNLocalErrorSnake2:
    r"""A variation around SNLocalErrorSnake

    just to debug an issue in the fit - I think fixed parameters
    are not handled correctly
    """
    def __init__(self, model, bins=(10, 10), order=4):
        """
        Constructor for the SNLocalErrorSnake class.

        Parameters
        ----------
        model : object
            The model used for evaluation.
        bins : tuple of int, optional
            Number of bins for phase and wavelength. Default is (10, 10).
        order : int, optional
            Order of the B-spline. Default is 4.
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.bins = bins
        self.order = order

        # instantiate a basis
        ph_bins, wl_bins = bins
        phase_grid = np.linspace(model.basis.by.range[0], model.basis.by.range[-1], ph_bins)
        wl_grid = np.linspace(model.basis.bx.range[0], model.basis.bx.range[-1], wl_bins)
        self.wl_grid = wl_grid
        self.phase_grid = phase_grid
        self.basis = BSpline2D(wl_grid, phase_grid, x_order=order, y_order=order)

    def clone(self, model, **kw):
        ret = self.__class__(model,
                             bins=kw.get('bins', self.bins),
                             order=kw.get('order', self.order))
        return ret

    def get_struct(self):
        """
        Get the block structure of the parameter vector used to evaluate the model.

        Returns
        -------
        list of tuple
            List containing the block structure of the parameter vector.
            Each item contains the block name and size.
        """
        nsn = len(self.training_dataset.sn_data.sn_set)
        return [('gamma_snake', len(self.basis)), ('gamma_sn', nsn)]

    def init_pars(self, pars):
        """
        Initialize the blocks of the parameter vector which are specific to this class.

        Parameters
        ----------
        pars : `nacl.fitparameters.FitParameters`
            Parameters object to be (partially) initialized.
        """

        # initiating at 5% error

        pars['gamma_sn'].full[:] = 0.1
        pars['gamma_snake'].full[:] = 1.
        # WL, P = np.meshgrid(self.wl_grid, self.phase_grid)
        # Jm = self.basis.eval(WL.ravel(), P.ravel())
        # pars['gamma_snake'].full[:] = np.linalg.pinv(Jm.toarray()) @ np.repeat(2*np.log(0.05), 100)

    def to_fix(self, wl, phase):
        """return value

        .. todo:
           this should probably be a spline basis method
        """
        basis_wl = integ(self.basis.bx, n=1) / integ(self.basis.bx, n=0)
        i_wl = np.argmin(np.abs(basis_wl - wl))
        basis_ph = integ(self.basis.by, n=1) / integ(self.basis.by, n=0)
        j_ph = np.argmin(np.abs(basis_ph - phase))
        ii = j_ph * len(self.basis.bx) + i_wl
        return ii

    def __call__(self, pars, jac=False):
        """
        Evaluate the variance model and optionally its derivatives.

        Parameters
        ----------
        pars : object
            Parameters object containing the model parameters.
        jac : bool, optional
            If True, compute and return the Jacobian matrix. Default is False.

        Returns
        -------
        v : numpy.ndarray
            Array of variances.
        J : scipy.sparse.coo_matrix, optional
            Jacobian matrix, returned if `jac` is True.
        """
        if jac:
            flux, Jm = self.model(pars, jac=True)
        else:
            flux = self.model(pars, jac=False)
            Jm = None

        tds = self.training_dataset
        zz, tmax, wl, mjd = [], [], [], []
        for d in (tds.lc_data, tds.spec_data):
            if d is None:
                continue
            zz.append(d.z)
            tmax.append(pars['tmax'].full[d.sn_index])
            wl.append(d.wavelength)
            mjd.append(d.mjd)
        zz = np.hstack(zz)
        tmax = np.hstack(tmax)
        wl = np.hstack(wl)
        mjd = np.hstack(mjd)
        # zz = np.hstack(filter(ff, [tds.lc_data.z,
        #                           tds.spec_data.z]))
        # tmax = np.hstack([pars['tmax'].full[tds.lc_data.sn_index],
        #                  pars['tmax'].full[tds.spec_data.sn_index]])
        #
        # wl = np.hstack([tds.lc_data.wavelength,
        #                tds.spec_data.wavelength]) / (1. + zz)
        # mjd = np.hstack([tds.lc_data.mjd,
        #                 tds.spec_data.mjd])
        phase = (mjd-tmax) / (1. + zz)
        #phase = np.hstack([(tds.lc_data.mjd - tmax) / (1. + zz),
        #                   (tds.spec_data.mjd - tmax) / (1. + zz)])
        Jv = self.basis.eval(wl, phase)

        # photometric part
        g_sn = np.zeros(len(tds))
        if tds.lc_data is not None:
            g_sn[:len(tds.lc_data)] = pars['gamma_sn'].full[tds.lc_data.sn_index]

        # spectral part
        if tds.spec_data is not None:
            g_sn[len(tds.lc_data):] = pars['gamma_sn'].full[tds.spec_data.sn_index]

        #
        g_snake = np.zeros(len(tds))
        # g_snake[:len(tds.lc_data)] = Jv @ pars['gamma_snake'].full
        g_snake[:] = Jv @ pars['gamma_snake'].full


        v = g_snake * g_sn**2 * flux**2
        if not jac:
            return v

        # derivatives
        N = len(tds)
        n_free_pars = len(pars.free)
        buff = CooMatrixBuff2((N, n_free_pars))

        # d_gamma_sn
        buff.append(tds.lc_data.row,
                    pars['gamma_sn'].indexof(tds.lc_data.sn_index),
                    2 * g_sn[tds.lc_data.row] * g_snake[tds.lc_data.row] * flux[tds.lc_data.row]**2)
        if tds.spec_data is not None:
            buff.append(tds.spec_data.row,
                        pars['gamma_sn'].indexof(tds.spec_data.sn_index),
                        2 * g_sn[tds.spec_data.row] * g_snake[tds.spec_data.row] * flux[tds.spec_data.row]**2)

        # d_gamma_snake
        buff.append(Jv.row,
                    pars['gamma_snake'].indexof(Jv.col),
                    Jv.data * g_sn[Jv.row]**2 * flux[Jv.row]**2)

        # d_dpars
        buff.append(Jm.row,
                    Jm.col,
                    2. * g_snake[Jm.row] * g_sn[Jm.row]**2 * flux[Jm.row] * Jm.data)

        J = buff.tocoo()

        return v, J



class SimpleErrorSnake_:
    r"""Simple, 1 parameter error snake: :math:`\sigma_f = \sigma_m \times f`

    This is the simplest error snake possible. We add a pedestal variance,
    constant in magnitude (i.e. of the form :math:`\sigma_m \times flux` in
    flux).
    """

    def __init__(self, model):  # , var_pedestal=0.001):
        self.model = model
        self.training_dataset = self.model.training_dataset
        # self.var_pedestal = var_pedestal

    def get_struct(self):
        """
        """
        return [('sigma_snake', 1)]

    def __call__(self, pars, jac=False, model_flux=None, model_jac=None):
        """return the diagonal of the error snake variance + derivatives
        """
        mflux, mjac = None, None
        # if parameters are given, we need to re-evaluate the model
        if p is not None:
            if not jac:
                mflux = self.model(p)
            else:
                mflux, mjac = self.model(p, jac=True)
        # otherwise, we re-evaluate it only if it is necessary
        else:
            if not jac:
                mflux = model_flux if model_flux is not None else self.model(self.model.pars.free)
            else:
                if model_flux is not None and model_jac is not None:
                    mflux, mjac = model_flux, model_jac
                else:
                    mflux, mjac = self.model(self.model.pars.free, jac=True)

        # model parameters
        pars = self.model.pars
        sigma_m = self.model.pars['sigma_snake'].full[0]

        # evaluate the variance
        var = (sigma_m * mflux)**2

        # we should only apply it to the photometric measurements
        # nlc, _, _ = self.model.training_dataset.n

        # and return it if this is the only thing requested
        if not jac:
            return var

        # derivatives
        n = len(self.model.pars.full)
        n_free = len(self.model.pars.free)
        N = self.training_dataset.nb_meas(valid_only=False)

        # dV / dsigma_snake
        i = np.arange(N).astype(int)
        j = np.full(N, pars['sigma_snake'].indexof())
        dVds = 2. * sigma_m * mflux**2
        idx = j>=0
        J_dVds = sparse.coo_matrix((dVds[idx], (i[idx],j[idx])), shape=(N,n_free))

        # dV/dbeta
        # mjac.data *= (2. * sigma_m**2 * mflux[mjac.row])
        J_dVdbeta = sparse.coo_matrix((mjac.data * 2. * sigma_m**2 * mflux[mjac.row],
                                (mjac.row, mjac.col)),
                                shape=mjac.shape)

        # i = np.hstack((i, mjac.row))
        # j = np.hstack((j, mjac.col))
        # v = np.hstack((dVds, mjac.data))
        # idx = j>=0
        # J = coo_matrix((v[idx], (i[idx],j[idx])), shape=(N, n_free))
        # J = J_dVds.tocsc() + J_dVdbeta.tocsc()
        J = J_dVds.tocoo() + J_dVdbeta.tocoo()

        return var, J

    def noise(self, p=None, **kwargs):
        """draw one realization of the error snake noise
        """
        var = self(p, jac=False, **kwargs)
        nlc, nsp, nphotspec = self.training_dataset.nb_meas(valid_only=False,
                                                            split_by_type=True)
        N = nlc + nsp + nphotspec
        n = np.zeros(N)
        # this error snake only applies to the photometric dataset
        n[:nlc] = np.random.normal(loc=0., scale=np.sqrt(var[:nlc]))
        return n


class CalibErrorModel:

    def __init__(self, model, calib_variance,
                 default_calib_variance=0.5**2):
        """Constructor

        Parameters
        ----------
        model : a NaCl model (e.g. SALT2Like)
            the underlying model
        calib_variance : float or pandas.DataFrame
            the calibration covariance matrix. It is either a float, if all
            bands have the same calibration variance (uncorrelated), or if all
            calibration uncertainties are uncorrelated, the diagonal of the
            covariance matrix, or the full covariance matrix.
        """
        self.model = model
        self.training_dataset = self.model.training_dataset
        self.calib_variance = calib_variance
        self.default_calib_variance = default_calib_variance
        self.inv_full_covmat = None
        self.sub_covmat = None

    def get_struct(self):
        nb_bands = self.training_dataset.nb_bands()
        return [('eta_calib', nb_bands)]
    def init_pars(self, pars):
        """
        """
        pars['eta_calib'].full[:] = 1.

    def build_covmat(self, pars,
                     calib_variance, bands=None,
                     default_calib_variance=0.5):
        """build a covmat (ordered to match the lc_data.band_index)

        Returns
        -------
        np.ndarray
            the re-ordered covmat
        """
        npars = len(pars.full)
        pfull = pars.copy()
        pfull.release()

        sz = len(pfull['eta_calib'].full)

        # if all bands have the same variance, that's easy
        if isinstance(calib_variance, float):
            nb_bands = self.training_dataset.nb_bands()
            i = pfull['eta_calib'].indexof()
            v = np.full(sz, 1./self.calib_variance)
            self.sub_covmat = np.diag(np.full(nb_bands, calib_variance))
            self.inv_full_covmat = sparse.coo_matrix((v, (i, i)), shape=(npars, npars)).tocsr()

        # otherwise, we may get a dict of the form {<band_name>: var, ...}
        # in which case it is also easy
        elif isinstance(calib_variance, dict):
            tds = self.model.training_dataset
            diag = []
            for bn in tds.lc_data.band_set:
                if bn not in calib_variance:
                    logger.warning(f'no calibration variance specified for band: {bn} -- will assign {default_calib_variance} by default')
                diag.append(calib_variance.get(bn, default_calib_variance))
            diag = np.array(diag)
            assert np.all(diag)
            i = pfull['eta_calib'].indexof()
            self.sub_covmat = np.diag(diag)
            self.inv_full_covmat = sparse.coo_matrix((1./diag, (i,i)), shape=(npars, npars)).tocsr()

        # finally, we may get a real matrix, along with a dict that
        # specifies the indices to band mapping. Then, all we have
        # to do, is to make sure all the bands are here, fill out the blank
        # if necessary, and re-order it if necessary
        elif isinstance(calib_variance, tuple):
            covmat, bands  = calib_variance
            # extend band into a simple map
            band_map = dict([(y,x) for x,y in enumerate(bands)])

            # extend calib covmat with a defaut value
            nr,nc = covmat.shape
            assert nr == nc
            extended_covmat = np.zeros((nr+1,nc+1))
            extended_covmat[:nr,:nc] = covmat
            extended_covmat[nr,nr] = default_calib_variance
            #            print('extended_covmat: ', extended_covmat)
            # re-order covmat
            i = []
            for bn in self.model.training_dataset.lc_data.band_set:
                if bn not in bands:
                    logger.warning('no calibration variance specified for band: {bn} -- will assign {default_calib_variance} by default')
                    i.append(nr)
                else:
                    i.append(band_map[bn])
            ii,jj = np.meshgrid(i,i)
            reordered_covmat = extended_covmat[ii,jj]

            # invert the covmat
            w = np.linalg.inv(reordered_covmat)

            # and re-index it into a larger (n,n) matrix, where n = number of parameters
            nn, _ = w.shape
            ii, jj = np.mgrid[:nn,:nn]
            self.sub_covmat = reordered_covmat
            self.inv_full_covmat = sparse.coo_matrix((w.flatten(),
                                               (pfull['eta_calib'].indexof(ii.flatten()),
                                                pfull['eta_calib'].indexof(jj.flatten()))),
                                              shape=(npars, npars)).tocsr()
        else:
            raise ValueError(f"build_covmat(): don't know what to do with {calib_variance}")

    def __call__(self, pars, deriv=False):
        """evaluate the calib prior (and optionally its gradient and Hessian)
        """
        #        if p is not None:
        #            self.model.pars.free = p

        if self.sub_covmat is None or self.inv_full_covmat is None or self.inv_full_covmat.shape[0]!=pars.full.shape[0]:
            self.build_covmat(pars, self.calib_variance)

        pfull = pars.full
        prior = np.dot(pfull, (self.inv_full_covmat.dot(pfull)))
        if not deriv:
            return prior

        # TODO: add some sanity and change the sign in the LogLikelihood
        # so that can return grad and not -grad ...
        # TODO: I am here ! -> reduce size, depending on fixed parameters

        n = self.inv_full_covmat.shape[0]
        idx = pars.indexof(np.arange(n)) >= 0

        grad = 2. * (self.inv_full_covmat @ pfull)[idx]
        hess = 2. * self.inv_full_covmat[:,idx][idx,:]

        return prior, grad, hess

    def correction(self, pars, lcdata=None):
        """the multiplicative correction to apply to the photometric data

        Parameters
        ----------
        p: (ndarray), optional
          vector of free parameters
        lcdata: stff, optional
          something that has a band_index

        Returns:
          a ndarray with the corrections
        """
#        if p is not None:
#            self.model.pars.free = p
        if lcdata is None:
            lcdata = self.training_dataset.lc_data
        corr = 1. + pars['eta_calib'].full[lcdata.band_index]
        return corr

    def noise(self, pars):
        """the noise component, to apply to the photometric data
        """
        # if p is not None:
        #     self.model.pars.free = p

        lc_data = self.training_dataset.lc_data

        nphot, nsp, nspphot = self.training_dataset.nb_meas(valid_only=False,
                                                            split_by_type=True)
        scales = np.ones(nphot + nsp + nspphot)
        nb_bands = self.training_dataset.nb_bands()

        # covmat = self.build_covmat()
        L = np.linalg.cholesky(self.sub_covmat)
        dm = L @ np.random.normal(0., scale=1., size=nb_bands)
        # dm = [dm[self.band_map[i]] for i in range(len(self.bands))]
        scales[:nphot] = 1. + dm[lc_data.band_index]
        return scales # 1.+ dm[lc_data.band_index]


class ColorScatterModel:
    """An adaptation of the color scatter model developed by Guy Augarde
    """
    U_WAVELENGTH = 3650.88
    B_WAVELENGTH = 4302.57
    V_WAVELENGTH = 5428.55
    R_WAVELENGTH = 6418.01
    I_WAVELENGTH = 7968.34
    WAVELENGTH = {"U": U_WAVELENGTH, "B": B_WAVELENGTH, "V": V_WAVELENGTH,
                  "R": R_WAVELENGTH, "I": I_WAVELENGTH}

    def __init__(self, model):
        """Constructor
        """
        self.model = model
        self.training_dataset = model.training_dataset
        lc_data = self.training_dataset.lc_data
        restframe_wl = lc_data.wavelength / (1. + lc_data.z)
        self.reduced_restframe_wl = self.model.reduce(restframe_wl)

    def get_struct(self):
        """
        """
        nb_lightcurves = self.training_dataset.nb_lcs()
        return [('sigma_kappa', 3),
                ('kappa_color', nb_lightcurves)]

    def __call__(self, p=None, deriv=False):
        """return the color scatter prior, and (optionaly) its grad and hessian
        """
        pass

    def correction(self, pars):
        """return the multiplicative correction to be applied to the model
        """
        # if p is not None:
        #    self.model.pars.free = p
        tds = self.training_dataset
        corr = 1. + pars['kappa_color'].full[tds.lc_data.lc_index]
        return corr

    def noise(self, pars):
        """generate one realization of the noise -- to add directly to the data
        """
        # if p is not None:
        #     self.model.pars.free = p
        var = self.__call__(pars, jac=False)
        nn = np.random.normal(scale=np.sqrt(var), size=len(var))
        return 1. * nn[self.training_dataset.lc_data.lc_index]


class ColorScatter:
    r"""color scatter model

    To model the residual variability of the SNe color not described by the
    model, we allow the relative amplitude of each light curve to vary by a
    quantity :math:`(1+kappa)`:

    .. math::
        \phi_{phot}(p_0) = X_0 (1+z) (1+kappa) \int S(\lambda, p) T\left( \lambda \right) \frac{\lambda}{hc} d\lambda

    where :math:`\kappa` is an additional parameter, depending on the SN and the
    observation band.

    The variability of :math:`\kappa` is defined by a Gaussian prior, whose
    variance is a function of the wavelength restframe, and must be determined
    during the adjustment. In our model, this term is implemented by a
    polynomial of the wavelength restframe of the SN. For a light curve observed
    in a band :math:`X`, of average wavelength :math:`\lambda^X`, the
    corresponding variance is:

    .. math::
        \sigma_\kappa^2 = P\left(\frac{\lambda^X}{1+z}\right)

    where :math:`z` is redshift of the supernova and :math:`P` is a polynomial
    of the wavelength restframe. In practice, :math:`P` is implemented in terms
    of a reduced restframe wavelength: :math:`\lambda_{r}`

    Attributes
    ----------
    WL_REDUCED : numpy.array
        Reduced SN-restframe mean wavelength
    pars : nacl.lib.fitparameters.FitParameters
        Color scatter parameters
    """
    U_WAVELENGTH = 3650.88
    B_WAVELENGTH = 4302.57
    V_WAVELENGTH = 5428.55
    R_WAVELENGTH = 6418.01
    I_WAVELENGTH = 7968.34
    WAVELENGTH = {"U": U_WAVELENGTH, "B": B_WAVELENGTH, "V": V_WAVELENGTH,
                  "R": R_WAVELENGTH, "I": I_WAVELENGTH}

    def __init__(self, model): # wavelength_rest_reduced, sigma_kappa):
        """Constructor

        Parameters
        ----------
        wavelength_rest_reduced :
            Reduced SN-restframe mean wavelength
        sigma_kappa : numpy.array
            Color scatter parameter initialisation.
        """
        self.model = model
        self.training_dataset = model.training_dataset
        lc_data = self.training_dataset.lc_data
        restframe_wl = lc_data.wavelength / (1. + lc_data.z)
        _, ii = np.unique(lc_data.lc_index, return_index=True)
        ii.sort()
        self.reduced_restframe_wl = self.reduce(restframe_wl[ii])

    def reduce(self, wl):
        """
        """
        B_WL, V_WL = self.WAVELENGTH["B"], self.WAVELENGTH["V"]
        return (wl-B_WL)/(V_WL-B_WL)

    def get_struct(self):
        """
        """
        nb_lightcurves = self.training_dataset.nb_lcs()
        return [('sigma_kappa', 3),
                ('kappa_color', nb_lightcurves)]
    def init_pars(self, pars):
        """
        """
        pars['kappa_color'].full[:] = 1.E-6
        pars['sigma_kappa'].full[:] = 1.E-6
        pars['sigma_kappa'].full[0] = -4.

    def __call__(self, pars, deriv=False):
        r"""Return the color scatter variance (the :math:`V_\kappa` matrix)

        Parameters
        ----------
        p : np.ndarray
          free parameter vector

        Returns
        -------
        val : numpy.ndarray
            the diagonal of the color scatter variance matrix (used in the kappa prior)
        if jac:
            jacobian of the color scatter.
        """
        sigma_kappa = pars['sigma_kappa'].full
        kappa = pars['kappa_color'].full

        var = np.exp(nppol.Polynomial(sigma_kappa)(self.reduced_restframe_wl))

        # log det, penaly
        log_det = np.log(var).sum()
        quad_penalty = (kappa**2 / var).sum()
        penalty = log_det + quad_penalty

        if not deriv:
            return penalty

        # gradient w.r.t kappa
        N = len(pars.free)
        grad = np.zeros(N)
        j = pars['kappa_color'].indexof()
        idx = j>=0
        grad[j[idx]] = (2. * kappa / var)[idx]

        # gradient w.r.t sigma_kappa
        nk = len(pars['kappa_color'].full)
        ns = len(pars['sigma_kappa'].full)
        var = var.reshape(-1,1)
        kappa = kappa.reshape(-1,1)
        dq_ds = nppol.polyvander(self.reduced_restframe_wl, deg=2)
        tr_wdv =  np.sum(dq_ds, axis=0)
        kwdvwk = -np.sum(kappa**2 * dq_ds / var, axis=0)
        print(tr_wdv, kwdvwk)
        j = pars['sigma_kappa'].indexof()
        idx = j >= 0
        # check the signs
        grad[j[idx]] = -1*(-tr_wdv - kwdvwk)[idx]

        # hessian w.r.t kappa
        i, j, val = [], [], []
        m = sparse.coo_matrix(np.diag(2. / var.flatten()), shape=(nk,nk))
        i.append(pars['kappa_color'].indexof(m.row))
        j.append(pars['kappa_color'].indexof(m.col))
        val.append(m.data)

        # hessian: kappa-sigma_kappa block
        m = sparse.coo_matrix(-2. * kappa * dq_ds / var, shape=(nk,ns)) # was -2
        i.append(pars['kappa_color'].indexof(m.row))
        j.append(pars['sigma_kappa'].indexof(m.col))
        val.append(m.data)
        j.append(pars['kappa_color'].indexof(m.row))
        i.append(pars['sigma_kappa'].indexof(m.col))
        val.append(m.data)

        # hessian: sigma_kappa - sigma_kappa block
        dq = kappa * dq_ds / np.sqrt(var)
        # tr_wdvwdv = -4 * dq.T @ dq
        # dq = kappa**2 * dq_ds / sig
        kwdvwdvwk = dq.T @ dq
        m = sparse.coo_matrix(kwdvwdvwk, shape=(ns,ns))
        i.append(pars['sigma_kappa'].indexof(m.row))
        j.append(pars['sigma_kappa'].indexof(m.col))
        val.append(m.data)

        # encapsulate all that into the (much larger) parameter vector space
        i = np.hstack(i)
        j = np.hstack(j)
        val = np.hstack(val)
        idx = (i>=0) & (j>=0)
        n_free_pars = len(pars.free)
        hessian = sparse.coo_matrix((val[idx], (i[idx], j[idx])), shape=(n_free_pars, n_free_pars))

        return penalty, grad, hessian

    def correction(self, pars):
        """return the multiplicative correction to be applied to the model
        """
        corr = 1. + pars['kappa_color'].full[self.training_dataset.lc_data.lc_index]
        return corr

    def noise(self, pars):
        """generate one realization of the noise -- to add directly to the data
        """
        var = self.__call__(pars, jac=False)
        nn = np.random.normal(scale=np.sqrt(var), size=len(var))
        return nn[self.training_dataset.lc_data.lc_index]
