"""Variance models for the simple 1D light curve models


"""

import numpy as np
import scipy.sparse as sparse

class SimplePedestalModel:
    """Just a constant pedestal error added to the data
    """
    def __init__(self, model):
        self.model = model

    def get_struct(self):
        """model specific parameter blocks
        """
        return [("gamma", 1)]

    def init_pars(self, pars):
        pars['gamma'].full[:] = 1.

    def __call__(self, pars, jac=False):
        v, J = None, None
        if jac:
            v, J = self.model(pars, jac=True)
        else:
            v = self.model(pars, jac=False)
        N = len(v)
        g = pars['gamma'].full[0]
        var = np.full(N, g**2)

        if not jac:
            return var

        n_free_pars = len(pars.free)
        dvar = np.full(N, 2. * g)
        i = np.arange(N)
        j = pars['gamma'].indexof(np.zeros(N).astype(int))
        idx = j >= 0
        J = sparse.coo_matrix((dvar[idx], (i[idx], j[idx])),
                              shape=(N, n_free_pars))
        return var, J

class SimpleErrorSnake:

    def __init__(self, model):
        self.model = model

    def get_struct(self):
        return [("gamma", 1)]

    def init_pars(self, pars):
        pars['gamma'].full[:] = 0.01

    def __call__(self, pars, jac=False):
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
