
import numpy as np
from scipy.sparse import coo_matrix
from saltworks import FitParameters
from bbf import bspline



class Model:
    """A 2D spline description of 2D data

    Encpsulating the spline evaluation in a model, like that
    allows to easily fix parameters, use the nacl minimizer,
    with regularization penalties.
    """
    def __init__(self, x0, x1, grid_x0=None, grid_x1=None, order=4):
        self.x0 = x0
        self.x1 = x1
        self.grid_x0 = grid_x0
        self.grid_x1 = grid_x1
        self.basis = bspline.BSpline2D(grid_x0, grid_x1, x_order=order, y_order=order)
        X0, X1 = np.meshgrid(x0, x1)
        self.J = self.basis.eval(X0.ravel(), X1.ravel())

    def get_struct(self):
        return [('theta', len(self.basis))]

    def init_pars(self, pars=None):
        if pars is None:
            pars = FitParameters(self.get_struct())
        n = len(pars['theta'].full)
        pars['theta'].full[:] = np.random.rand(n)
        return pars

    def __call__(self, pars, jac=False):
        """
        """
        vals = self.J @ pars['theta'].full
        if not jac:
            return vals

        j = pars.indexof(self.J.col)
        idx = j>=0

        N = self.J.shape[0]
        n_free_pars = len(pars.free)
        JJ = coo_matrix((self.J.data[idx], (self.J.row[idx], j[idx])), shape=(N,n_free_pars))
        return vals, JJ
