import numpy as np
import scipy.sparse as sparse
from saltworks import FitParameters
from bbf.bspline import BSpline


class SingleBandLightcurveModel1D:
    """A more realistic 1D lightcurve model
    """

    def __init__(self, data, grid=None):
        self.data = data
        self.nsn = len(data.sn_map)
        if grid is not None:
            self.grid = grid
        else:
            self.grid = np.linspace(self.data.x.min() - 5., self.data.x.max() + 5., 25)
        self.basis = bspline.BSpline(self.grid, order=4)


    def get_struct(self):
        return [('x0', self.nsn), ('stretch', self.nsn), ('tmax', self.nsn),
                ('theta', len(self.basis))]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.uniform(-1., 1., len(self.basis))
        pars['x0'].full[:] = np.ones(self.nsn)
        pars['stretch'].full[:] = np.zeros(self.nsn)
        pars['tmax'].full[:] = 0.
        return pars

    def __call__(self, pars, jac=False):
        """evaluate the model and (optionally) its derivatives

        Parameters
        ----------
        pars: (FitParameters)
          model parameter vector
        jac: (bool)
          whether to evaluate or not the jacobian

        Returns
        -------
        ndarray of floats if jac is False
        ndarray, sparse.csr_matrix: if jac is True
        """
        x0   = pars['x0'].full[self.data.sn_index]
        stretch = pars['stretch'].full[self.data.sn_index]
        tmax = pars['tmax'].full[self.data.sn_index]

        dx = self.data.x - tmax
        ph = (1. + stretch) * dx
        J = self.basis.eval(ph.to_numpy())
        mod = J @ pars['theta'].full
        vals = x0 * mod

        if not jac:
            return vals

        # model derivatives
        N = len(vals)
        i = np.arange(N)
        ii, jj, data = [], [], []
        # dmodel_dx0
        ii.append(i)
        jj.append(np.full(N, pars['x0'].indexof(self.data.sn_index)))
        data.append(mod)

        # dmodel_dstretch
        J_dmodel = self.basis.deriv(ph.to_numpy())
        dmod = J_dmodel @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * dmod * dx)

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * dmod * (1. + stretch))

        # dmodel_dtheta
        ii.append(J.row)
        jj.append(pars['theta'].indexof(J.col))
        data.append(x0[J.row] * J.data)

        # build the matrix
        i = np.hstack(ii)
        j = np.hstack(jj)
        data = np.hstack(data)
        idx = j>=0

        n_free_pars = len(pars.free)
        J = sparse.coo_matrix((data[idx], (i[idx], j[idx])), shape=(N,n_free_pars))

        return vals, J


class LightCurveModel1D:

    def __init__(self, data, grid=None, pivot_wl=5000.):
        """
        """
        self.data = data
        self.nsn = len(data.sn_map)
        self.pivot_wl = pivot_wl
        if grid is not None:
            self.grid = grid
        else:
            self.grid = np.linspace(self.data.x.min() - 5., self.data.x.max() + 5., 25)
        self.basis = bspline.BSpline(self.grid, order=4)


    def get_struct(self):
        return [('x0', self.nsn), ('stretch', self.nsn),
                ('color', self.nsn), ('tmax', self.nsn),
                ('theta', len(self.basis))]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.uniform(-1., 1., len(self.basis))
        pars['x0'].full[:] = 1.
        pars['stretch'].full[:] = 0.
        pars['color'].full[:] = 0.
        pars['tmax'].full[:] = 0.
        return pars

    def __call__(self, pars, jac=False):
        """evaluate the model and (optionally) its derivatives

        Parameters
        ----------
        pars: (FitParameters)
          model parameter vector
        jac: (bool)
          whether to evaluate or not the jacobian

        Returns
        -------
        ndarray of floats if jac is False
        ndarray, sparse.csr_matrix: if jac is True
        """
        x0   = pars['x0'].full[self.data.sn_index]
        stretch = pars['stretch'].full[self.data.sn_index]
        tmax = pars['tmax'].full[self.data.sn_index]

        # rather simple color law - just for tests
        dwl = ((self.data.wl - self.pivot_wl) / self.pivot_wl).to_numpy()
        cl = 1. + pars['color'].full[self.data.sn_index] * dwl

        dx = self.data.x - tmax
        ph = (1. + stretch) * dx
        J = self.basis.eval(ph.to_numpy())
        mod = J @ pars['theta'].full
        vals = x0 * mod * cl

        if not jac:
            return vals

        # model derivatives
        N = len(vals)
        i = np.arange(N)
        ii, jj, data = [], [], []

        # dmodel_dx0
        ii.append(i)
        jj.append(np.full(N, pars['x0'].indexof(self.data.sn_index)))
        data.append(mod * cl)

        # dmodel_dstretch
        J_dmodel = self.basis.deriv(ph.to_numpy())
        dmod = J_dmodel @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * dmod * dx * cl)

        # dmodel_dcolor
        ii.append(i)
        jj.append(pars['color'].indexof(self.data.sn_index))
        data.append(x0 * mod * dwl)

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * dmod * (1. + stretch) * cl)

        # dmodel_dtheta
        ii.append(J.row)
        jj.append(pars['theta'].indexof(J.col))
        data.append(x0[J.row] * J.data * cl[J.row])

        # build the matrix
        i = np.hstack(ii)
        j = np.hstack(jj)
        data = np.hstack(data)
        idx = j>=0

        n_free_pars = len(pars.free)
        J = sparse.coo_matrix((data[idx], (i[idx], j[idx])), shape=(N,n_free_pars))

        return vals, J


class LightCurveModel1DWithCalibScatter:

    def __init__(self, data, grid=None, pivot_wl=5000.):
        """
        """
        self.data = data
        self.nsn = len(data.sn_map)
        self.nbands = len(self.data.band_set)
        self.pivot_wl = pivot_wl
        if grid is not None:
            self.grid = grid
        else:
            self.grid = np.linspace(self.data.x.min() - 5., self.data.x.max() + 5., 25)
        self.basis = bspline.BSpline(self.grid, order=4)


    def get_struct(self):
        return [('x0', self.nsn), ('stretch', self.nsn),
                ('color', self.nsn), ('tmax', self.nsn),
                ('theta', len(self.basis)),
                ('eta', self.nbands)]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.uniform(-1., 1., len(self.basis))
        pars['x0'].full[:] = 1.
        pars['stretch'].full[:] = 0.
        pars['color'].full[:] = 0.
        pars['tmax'].full[:] = 0.
        pars['eta'].full[:] = 0.
        return pars

    def __call__(self, pars, jac=False):
        """evaluate the model and (optionally) its derivatives

        Parameters
        ----------
        pars: (FitParameters)
          model parameter vector
        jac: (bool)
          whether to evaluate or not the jacobian

        Returns
        -------
        ndarray of floats if jac is False
        ndarray, sparse.csr_matrix: if jac is True
        """
        x0   = pars['x0'].full[self.data.sn_index]
        stretch = pars['stretch'].full[self.data.sn_index]
        tmax = pars['tmax'].full[self.data.sn_index]

        # rather simple color law - just for tests
        dwl = ((self.data.wl - self.pivot_wl) / self.pivot_wl).to_numpy()
        cl = 1. + pars['color'].full[self.data.sn_index] * dwl

        # calibration scatter
        cal = 1. + pars['eta'].full[self.data.band_index]

        dx = self.data.x - tmax
        ph = (1. + stretch) * dx
        J = self.basis.eval(ph.to_numpy())
        mod = J @ pars['theta'].full
        vals = x0 * mod * cl * cal

        if not jac:
            return vals

        # model derivatives
        N = len(vals)
        i = np.arange(N)
        ii, jj, data = [], [], []

        # dmodel_dx0
        ii.append(i)
        jj.append(np.full(N, pars['x0'].indexof(self.data.sn_index)))
        data.append(mod * cl * cal)

        # dmodel_dstretch
        J_dmodel = self.basis.deriv(ph.to_numpy())
        dmod = J_dmodel @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * dmod * dx * cl * cal)

        # dmodel_dcolor
        ii.append(i)
        jj.append(pars['color'].indexof(self.data.sn_index))
        data.append(x0 * mod * dwl * cal)

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * dmod * (1. + stretch) * cl * cal)

        # dmodel_dtheta
        ii.append(J.row)
        jj.append(pars['theta'].indexof(J.col))
        data.append(x0[J.row] * J.data * cl[J.row] * cal[J.row])

        # dmodel_deta
        ii.append(i)
        jj.append(pars['eta'].indexof(self.data.band_index))
        data.append(x0 * mod * cl)

        # build the matrix
        i = np.hstack(ii)
        j = np.hstack(jj)
        data = np.hstack(data)
        idx = j>=0

        n_free_pars = len(pars.free)
        J = sparse.coo_matrix((data[idx], (i[idx], j[idx])), shape=(N,n_free_pars))

        return vals, J


class LightCurveModel1DWithCalibAndColorScatter:

    def __init__(self, data, grid=None, pivot_wl=5000.):
        """
        """
        self.data = data
        self.nsn = len(data.sn_map)
        self.nbands = len(self.data.band_set)
        self.pivot_wl = pivot_wl
        if grid is not None:
            self.grid = grid
        else:
            self.grid = np.linspace(self.data.x.min() - 5., self.data.x.max() + 5., 25)
        self.basis = bspline.BSpline(self.grid, order=4)


    def get_struct(self):
        return [('x0', self.nsn), ('stretch', self.nsn),
                ('color', self.nsn), ('tmax', self.nsn),
                ('theta', len(self.basis)),
                ('eta', self.nbands),
                ('kappa', self.nsn * self.nbands)]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.uniform(-1., 1., len(self.basis))
        pars['x0'].full[:] = 1.
        pars['stretch'].full[:] = 0.
        pars['color'].full[:] = 0.
        pars['tmax'].full[:] = 0.
        pars['eta'].full[:] = 0.
        pars['kappa'].full[:] = 0.
        return pars

    def __call__(self, pars, jac=False):
        """evaluate the model and (optionally) its derivatives

        Parameters
        ----------
        pars: (FitParameters)
          model parameter vector
        jac: (bool)
          whether to evaluate or not the jacobian

        Returns
        -------
        ndarray of floats if jac is False
        ndarray, sparse.csr_matrix: if jac is True
        """
        x0   = pars['x0'].full[self.data.sn_index]
        stretch = pars['stretch'].full[self.data.sn_index]
        tmax = pars['tmax'].full[self.data.sn_index]

        # rather simple color law - just for tests
        dwl = ((self.data.wl - self.pivot_wl) / self.pivot_wl).to_numpy()
        cl = 1. + pars['color'].full[self.data.sn_index] * dwl

        # calibration scatter
        cal = 1. + pars['eta'].full[self.data.band_index]

        # color scatter
        csc = 1. + pars['kappa'].full[self.data.sn_band_index]

        dx = self.data.x - tmax
        ph = (1. + stretch) * dx
        J = self.basis.eval(ph.to_numpy())
        mod = J @ pars['theta'].full
        vals = x0 * mod * cl * cal * csc

        if not jac:
            return vals

        # model derivatives
        N = len(vals)
        i = np.arange(N)
        ii, jj, data = [], [], []

        # dmodel_dx0
        ii.append(i)
        jj.append(np.full(N, pars['x0'].indexof(self.data.sn_index)))
        data.append(mod * cl * cal * csc)

        # dmodel_dstretch
        J_dmodel = self.basis.deriv(ph.to_numpy())
        dmod = J_dmodel @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * dmod * dx * cl * cal * csc)

        # dmodel_dcolor
        ii.append(i)
        jj.append(pars['color'].indexof(self.data.sn_index))
        data.append(x0 * mod * dwl * cal * csc)

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * dmod * (1. + stretch) * cl * cal * csc)

        # dmodel_dtheta
        ii.append(J.row)
        jj.append(pars['theta'].indexof(J.col))
        data.append(x0[J.row] * J.data * cl[J.row] * cal[J.row] * csc[J.row])

        # dmodel_deta
        ii.append(i)
        jj.append(pars['eta'].indexof(self.data.band_index))
        data.append(x0 * mod * cl * csc)

        # dmodel_dkappa
        ii.append(i)
        jj.append(pars['kappa'].indexof(self.data.sn_band_index))
        data.append(x0 * mod * cl * cal)

        # build the matrix
        i = np.hstack(ii)
        j = np.hstack(jj)
        data = np.hstack(data)
        idx = j>=0

        n_free_pars = len(pars.free)
        J = sparse.coo_matrix((data[idx], (i[idx], j[idx])), shape=(N,n_free_pars))

        return vals, J
