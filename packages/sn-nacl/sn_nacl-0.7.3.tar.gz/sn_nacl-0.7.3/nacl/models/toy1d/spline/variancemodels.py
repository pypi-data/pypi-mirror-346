"""Error snake examples

"""


import numpy as np
from scipy import sparse


class SimplePedestalErrorModel:
    """Error snake variance

    A simple model: just a constant pedestal error added to the data
    """
    def __init__(self, model):
        """constructor
        """
        self.model = model

    def get_struct(self):
        """structure of the error model specific parameters
        """
        return [("gamma", 1)]

    def init_pars(self, pars):
        pars['gamma'].full[:] = 1.

    def __call__(self, pars, jac=False):
        """
        """
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

        # n_pars = len(pars.full)
        n_free_pars = len(pars.free)
        dvar = np.full(N, 2. * g)
        i = np.arange(N)
        j = pars['gamma'].indexof(np.zeros(N).astype(int))
        idx = j>=0
        J = sparse.coo_matrix((dvar[idx], (i[idx], j[idx])),
                              shape=(N,n_free_pars))

        return var, J


class ConstantErrorSnake:
    r"""Simplistic Error snake

    This model is slightly more complicated: the variance depends on the model value:

    ..math::
        \sigma = \gamma \times f(\lambda,p)
    """
    def __init__(self, model):
        pass

    def get_struct(self):
        return [('gamma', 1)]

    def __call__(self, p, jac=False):
        pass


class VariableErrorSnake:
    """Realistic Error Snake

    This model is even more complicated: the variance depends on the model value
    and varies as a function of math:`$x$`

    """
    def __init__(self, model, basis=None):
        pass

    def get_struct(self):
        pass

    def __call__(self, p, jac=False):
        pass
