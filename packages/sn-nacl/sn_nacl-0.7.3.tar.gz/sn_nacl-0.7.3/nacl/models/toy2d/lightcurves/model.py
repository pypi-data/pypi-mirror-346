import numpy as np
import scipy.sparse as sparse
from saltworks import FitParameters
from bbf.bspline import BSpline
from bbf import bspline


class Model:
    """A more realistic 2D lightcurve model
    """

    def __init__(self, data, grid_x1=None, grid_x2=None):
        self.data = data
        self.nsn = len(data.sn_map)
        if grid_x1 is not None:
            self.grid_x1 = grid_x1
            self.grid_x2 = grid_x2
        else:
            self.grid_x1 = np.linspace(self.data.x1.min() - 5., self.data.x1.max() + 5., 25)
            self.grid_x2 = np.linspace(self.data.x2.min() - 5., self.data.x2.max() + 5., 25)
        self.basis = bspline.BSpline2D(self.grid_x1, self.grid_x2, x_order=4, y_order=4)


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

        dx1 = self.data.x1 - tmax
        dx2 = self.data.x2 - tmax
        ph1 = (1. + stretch) * dx1
        ph2 = (1. + stretch) * dx2
        #P1, P2 = np.meshgrid(ph1.to_numpy(), ph2.to_numpy())
        #J = self.basis.eval(P1.ravel(), P2.ravel())
        J = self.basis.eval(ph1.to_numpy(), ph2.to_numpy())
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
        J_dmodel1, J_dmodel2 = self.basis.gradient(ph1.to_numpy(), ph2.to_numpy())
        dmod1 = J_dmodel1 @ pars['theta'].full
        dmod2 = J_dmodel2 @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * (dmod1 * dx1 + dmod2 * dx2))

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * (dmod1 + dmod2) * (1. + stretch))

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
        
        
class ModelwithCalibScatter:
    """A more realistic 2D lightcurve model
    """

    def __init__(self, data, grid_x1=None, grid_x2=None):
        self.data = data
        self.nsn = len(data.sn_map)
        self.nbands = len(self.data.band_set)
        if grid_x1 is not None:
            self.grid_x1 = grid_x1
            self.grid_x2 = grid_x2
        else:
            self.grid_x1 = np.linspace(self.data.x1.min() - 5., self.data.x1.max() + 5., 25)
            self.grid_x2 = np.linspace(self.data.x2.min() - 5., self.data.x2.max() + 5., 25)
        self.basis = bspline.BSpline2D(self.grid_x1, self.grid_x2, x_order=4, y_order=4)


    def get_struct(self):
        return [('x0', self.nsn), ('stretch', self.nsn), ('tmax', self.nsn),
                ('theta', len(self.basis)),
                ('eta', self.nbands)]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.uniform(-1., 1., len(self.basis))
        pars['x0'].full[:] = np.ones(self.nsn)
        pars['stretch'].full[:] = np.zeros(self.nsn)
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
        
        #colorscatter
        cal = 1. + pars['eta'].full[self.data.band_index]

        dx1 = self.data.x1 - tmax
        dx2 = self.data.x2 - tmax
        ph1 = (1. + stretch) * dx1
        ph2 = (1. + stretch) * dx2
        #P1, P2 = np.meshgrid(ph1.to_numpy(), ph2.to_numpy())
        #J = self.basis.eval(P1.ravel(), P2.ravel())
        J = self.basis.eval(ph1.to_numpy(), ph2.to_numpy())
        mod = J @ pars['theta'].full
        vals = x0 * mod * cal

        if not jac:
            return vals

        # model derivatives
        N = len(vals)
        i = np.arange(N)
        ii, jj, data = [], [], []
        # dmodel_dx0
        ii.append(i)
        jj.append(np.full(N, pars['x0'].indexof(self.data.sn_index)))
        data.append(mod * cal)

        # dmodel_dstretch
        J_dmodel1, J_dmodel2 = self.basis.gradient(ph1.to_numpy(), ph2.to_numpy())
        dmod1 = J_dmodel1 @ pars['theta'].full
        dmod2 = J_dmodel2 @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * (dmod1 * dx1 + dmod2 * dx2) * cal)

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * (dmod1 + dmod2) * (1. + stretch) * cal)

        # dmodel_dtheta
        ii.append(J.row)
        jj.append(pars['theta'].indexof(J.col))
        data.append(x0[J.row] * J.data * cal[J.row])
        
        # dmodel_deta
        ii.append(i)
        jj.append(pars['eta'].indexof(self.data.band_index))
        data.append(x0 * mod)

        # build the matrix
        i = np.hstack(ii)
        j = np.hstack(jj)
        data = np.hstack(data)
        idx = j>=0

        n_free_pars = len(pars.free)
        J = sparse.coo_matrix((data[idx], (i[idx], j[idx])), shape=(N,n_free_pars))

        return vals, J
        
class LightCurve2DCalibScatter:
    """A more realistic 2D lightcurve model with calibration errors and a color parameter
    """

    def __init__(self, data, grid_x1=None, grid_x2=None, pivot_wl=5000.):
        self.data = data
        self.nsn = len(data.sn_map)
        self.nbands = len(self.data.band_set)
        self.pivot_wl = pivot_wl
        if grid_x1 is not None:
            self.grid_x1 = grid_x1
            self.grid_x2 = grid_x2
        else:
            self.grid_x1 = np.linspace(self.data.x1.min() - 5., self.data.x1.max() + 5., 25)
            self.grid_x2 = np.linspace(self.data.x2.min() - 5., self.data.x2.max() + 5., 25)
        self.basis = bspline.BSpline2D(self.grid_x1, self.grid_x2, x_order=4, y_order=4)


    def get_struct(self):
        return [('x0', self.nsn), ('stretch', self.nsn), 
                ('tmax', self.nsn), ('color', self.nsn),
                ('theta', len(self.basis)),
                ('eta', self.nbands)]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.uniform(-1., 1., len(self.basis))
        pars['x0'].full[:] = np.ones(self.nsn)
        pars['stretch'].full[:] = np.zeros(self.nsn)
        pars['tmax'].full[:] = 0.
        pars['color'].full[:] = 0.
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
        zz = self.data.zz
        # rather simple color law - just for tests
        dwl = ((self.data.wl - self.pivot_wl) / self.pivot_wl).to_numpy()
        cl = 1. + pars['color'].full[self.data.sn_index] * dwl
        
        #colorscatter
        cal = 1. + pars['eta'].full[self.data.band_index]

        dx1 = self.data.x1 - tmax
        dx2 = self.data.x2 - tmax
        ph1 = (1. + stretch) * dx1 / zz
        ph2 = (1. + stretch) * dx2 / zz
        #P1, P2 = np.meshgrid(ph1.to_numpy(), ph2.to_numpy())
        #J = self.basis.eval(P1.ravel(), P2.ravel())
        J = self.basis.eval(ph1.to_numpy(), ph2.to_numpy())
        mod = J @ pars['theta'].full
        vals = x0 * mod * cal * cl

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
        J_dmodel1, J_dmodel2 = self.basis.gradient(ph1.to_numpy(), ph2.to_numpy())
        dmod1 = J_dmodel1 @ pars['theta'].full
        dmod2 = J_dmodel2 @ pars['theta'].full
        ii.append(i)
        jj.append(pars['stretch'].indexof(self.data.sn_index))
        data.append(x0 * (dmod1 * dx1 + dmod2 * dx2) * cl * cal / zz)
        
        # dmodel_dcolor
        ii.append(i)
        jj.append(pars['color'].indexof(self.data.sn_index))
        data.append(x0 * mod * dwl * cal)

        # dmodel_dtmax
        ii.append(i)
        jj.append(pars['tmax'].indexof(self.data.sn_index))
        data.append(-x0 * (dmod1 + dmod2) * (1. + stretch) * cl * cal / zz)

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
