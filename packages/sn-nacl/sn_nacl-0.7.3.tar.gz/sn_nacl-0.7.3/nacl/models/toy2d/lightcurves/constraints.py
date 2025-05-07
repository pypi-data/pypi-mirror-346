"""Constraints
"""

import numpy as np
from scipy import sparse
from nacl.models.toy1d.lightcurves.constraints import LinearConstraint, ConstraintSet
from scipy.sparse import coo_matrix, dok_matrix



class MaxLcAtPhase(LinearConstraint):

    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase

    def init_h_matrix(self, pars):
        J = self.model.basis.eval(np.array([self.phase]), np.array([self.phase])).tocoo()
        pp = pars.copy()
        pp.release()
        N = len(J.col)
        i = np.full(N, 0)
        j = pp['theta'].indexof(J.col)
        # idx = j>=0
        npars = len(pp.full)
        J = sparse.coo_matrix((J.data, (i, j)), shape=(1, npars))
        return J

    # def max_lc_at_phase(model, rhs, phase=0.):
    #     """
    #     """
    #     J =  model.basis.eval(np.array([phase])).toarray()
    #     return LinearConstraint(J, rhs)

class DMaxLcAtPhase1(LinearConstraint):

    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase

    def init_h_matrix(self, pars):
        J, _ = self.model.basis.gradient(np.array([self.phase]), np.array([self.phase]))
        J = J.tocoo()
        pp = pars.copy()
        pp.release()
        N = len(J.col)
        i = np.full(N, 0)
        j = pp['theta'].indexof(J.col)
        npars = len(pp.full)
        J = sparse.coo_matrix((J.data, (i, j)), shape=(1, npars))
        return J

class DMaxLcAtPhase2(LinearConstraint):

    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase

    def init_h_matrix(self, pars):
        _, J = self.model.basis.gradient(np.array([self.phase]), np.array([self.phase]))
        J = J.tocoo()
        pp = pars.copy()
        pp.release()
        N = len(J.col)
        i = np.full(N, 0)
        j = pp['theta'].indexof(J.col)
        npars = len(pp.full)
        J = sparse.coo_matrix((J.data, (i, j)), shape=(1, npars))
        return J

class MeanColor(LinearConstraint):

    def __init__(self, model, rhs):
        super().__init__(model, rhs)

    def init_h_matrix(self, pars):
        nsn = len(pars['x0'].full)
        npars = len(pars.full)
        j = pars['color'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = np.full(nsn, 1./nsn)
        idx = j >= 0
        J = sparse.coo_matrix((v[idx], (i[idx], j[idx])), shape=(1, npars))

        return J

def cons(model, mu=1.E6, color=False):
    """
    """
    #    m0 = max_lc_at_phase(model, 0., phase=0.)
    #    dm0 = dmax_lc_at_phase(model, 0., phase=0.)
    m0 = MaxLcAtPhase(model, 1., 0.)
    dm0_1 = DMaxLcAtPhase1(model, 0., 0.)
    dm0_2 = DMaxLcAtPhase2(model, 0., 0.)
    if not color:
        return ConstraintSet([m0, dm0_1, dm0_2], mu=mu)
    else:
        c0 = MeanColor(model, 0.)
        return ConstraintSet([m0, dm0_1, dm0_2, c0], mu=mu)
