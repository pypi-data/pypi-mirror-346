import numpy as np
from scipy.sparse import coo_matrix
from saltworks import FitParameters
from bbf.bspline import BSpline


class Model:
    """A 1D spline description of 1D data

    Encpsulating the sline evaluation in a model, like that
    allows to easily fix parameters, use the nacl minimizer,
    with regularization penalties.
    """
    def __init__(self, x, grid=None, order=4):
        self.x = x
        self.grid = grid
        self.basis = bspline.BSpline(grid, order=4)
        self.J = self.basis.eval(self.x)

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
