import numpy as np
from scipy import sparse
from scipy.sparse import coo_matrix, dok_matrix


class Constraint:
    """Generic contraint
    """

    def __init__(self, model, rhs):  # , pars_struct=None):
        """
        """
        self.model = model
        self.rhs = rhs
        # if pars_struct:
        #     self.pars_struct = pars_struct
        # else:
        #     self.pars_struct = self.model.pars.copy()
        #     self.pars_struct.release()

    def __call__(self, p=None, deriv=False):
        pass


class LinearConstraint(Constraint):
    """Generic linear contraints
    """
    def __init__(self, model, rhs):
        """
        """
        super().__init__(model, rhs)
        self.h_matrix = None
        self.rhs = rhs

    def init_h_matrix(self, pars):
        raise NotImplementedError()

    def init_pars(self, pars):
        """
        """
        self.h_matrix = self.init_h_matrix(pars)

    def __call__(self, pars, deriv=False):
        """evaluate the constraint
        """
        if self.h_matrix is None:
            self.h_matrix = self.init_h_matrix(pars)

        cons = self.h_matrix @ pars.full - self.rhs
        cons = float(cons)
        if not deriv:
            return cons
        return cons, self.h_matrix, None


class ConstraintSet:
    """Combine a series of constraints (linear or not)

    This class combines a set of constraints and produces a (quadratic)
    penality, added to the Log Likelihood. Compute the gradient and the hessian
    of this penality if required.
    """

    def __init__(self, constraints, mu=1.E10):
        """constructor
        """
        # self.model = model
        self.constraints = constraints
        self.mu = mu

    def init_pars(self, pars):
        """
        """
        for c in self.constraints:
            c.init_pars(pars)

    def __call__(self, pars, deriv=False):
        """evaluate the penality
        """
        npars = len(pars.full)

        pen = 0.
        # if no derivatives specified, return the sum of the quadratic
        # penalities associated with each constraint
        if not deriv:
            for cons in self.constraints:
                pen += cons(pars, deriv=False)**2
            return self.mu * float(pen)

        # otherwise, compute and return the gradient and hessian
        # along with the quadratic penality
        grad = coo_matrix(([], ([], [])), shape=(1,npars))
        hess = coo_matrix(([], ([],[])), shape=(npars,npars))
        for cons in self.constraints:
            # p=None, because self.model.pars was just updated
            c, dc, d2c = cons(pars, deriv=True)
            pen  += c**2
            # we have restored the true grad convention (-2 -> +2)
            grad += +2. * float(c) * dc
            hess += +2. * dc.T.dot(dc)
            if d2c is not None:
                hess += 2. * c * d2c

        # fixed parameters ?
        idx = pars.indexof() >= 0
        pen = float(pen)
        grad = np.array(grad[:,idx].todense()).squeeze()
        hess = hess[:,idx][idx,:]

        return self.mu * pen, self.mu * grad, self.mu * hess

    def get_rhs(self):
        return np.array([c.rhs for c in self.constraints])





class MaxLcAtPhase(LinearConstraint):

    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase

    def init_h_matrix(self, pars):
        J = self.model.basis.eval(np.array([self.phase])).tocoo()
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

class DMaxLcAtPhase(LinearConstraint):

    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase

    def init_h_matrix(self, pars):
        J = self.model.basis.deriv(np.array([self.phase])).tocoo()
        pp = pars.copy()
        pp.release()
        N = len(J.col)
        i = np.full(N, 0)
        j = pp['theta'].indexof(J.col)
        npars = len(pp.full)
        J = sparse.coo_matrix((J.data, (i, j)), shape=(1, npars))
        return J

class MeanStretch(LinearConstraint):
    # Not the constraint i want but worth testing
    def __init__(self, model, rhs):
        super().__init__(model, rhs)
        
    def init_h_matrix(self, pars):
        nsn = len(pars['x0'].full)
        npars = len(pars.full)
        j = pars['stretch'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = np.full(nsn, 1./nsn)
        idx = j >= 0
        J = sparse.coo_matrix((v[idx], (i[idx], j[idx])), shape=(1, npars))

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

def cons(model, mu=1.E6, s=False):
    """
    """
    #    m0 = max_lc_at_phase(model, 0., phase=0.)
    #    dm0 = dmax_lc_at_phase(model, 0., phase=0.)
    m0 = MaxLcAtPhase(model, 1., 0.)
    dm0 = DMaxLcAtPhase(model, 0., 0.)
    if not s:
        return ConstraintSet([m0, dm0], mu=mu)
    else:
        s0 = MeanStretch(model, 0.)
        c0 = MeanColor(model, 0.)
        return ConstraintSet([m0, dm0, s0, c0], mu=mu)
