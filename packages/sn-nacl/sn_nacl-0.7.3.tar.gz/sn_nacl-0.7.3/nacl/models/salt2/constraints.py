r"""This module implements the constraints that are needed to train a
nacl.model.SALT2Like model on a dataset.

At variance with the original SALT2 work and with what is described in Guy
Augarde's thesis, we have made a special effort to implement constraints which
are linear.

The contraints are implemented as quadratic penalties that are added to the
:math:`\chi^2`. These penalities are typically of the form:

.. math ::
    (f(\theta) - \alpha)^2

where :math:`f(\theta)` is a function of the parameters, and :math:`\alpha`
is a number.

Since there are several constraints, it is convenient to express them in vector
form:

.. math ::
    (\vec{F}(\theta) - \vec{\alpha})^T \cdot (\vec{F}(\theta) - \vec{\alpha})
"""

import numpy as np
from scipy.sparse import coo_matrix, dok_matrix
from bbf import SNMagSys

class AllParametersFixedError(Exception): pass


def solve_constraints(cons, pars):
    """
    Solve the linearized constraints for the given parameter vector.

    This function linearizes the constraints provided by `cons` and solves
    for the parameter adjustments needed to satisfy these constraints.

    Parameters
    ----------
    cons : Constraints
        The constraints object containing the linearized constraints and the right-hand side values.
    pars : FitParameters
        The parameters object containing the current values of the parameters.

    Returns
    -------
    FitParameters
        The adjusted free parameters that satisfy the constraints.

    Notes
    -----
    The function uses QR decomposition to solve the linear system of equations formed by the constraints.
    """
    H = cons.get_linearized_constraints(pars)
    rhs = cons.get_rhs()
    Q,R = np.linalg.qr(H.T)
    dx = np.linalg.solve(R.T, rhs - H @ pars.full)
    dx = np.array(Q.dot(dx)).squeeze()

    pp = pars.copy()
    pp.full[:] += dx

    return pp


def ab_flux_at_10Mpc(Mb=-19.5):
    """
    Calculate the AB flux at a distance of 10 Megaparsecs.

    Parameters
    ----------
    Mb : float, optional
        The absolute magnitude in the B-band (default is -19.5).

    Notes
    -----
    The formula used is `10**(-0.4 * (30 + Mb))`, where 30 is the distance modulus
    for 10 Megaparsecs.
    """
    return 10**(-0.4 * (30+Mb))


class Constraint:
    """
    Represents a constraint in the NaCl optimization problem.

    This class is used to define and apply constraints to the parameters
    of a model during optimization.
    """
    def __init__(self, model, rhs):
        """
        Initialize the Constraint class.

        Parameters
        ----------
        model : object
            The model to which the constraints are applied.
        rhs : numpy.array
            The right-hand side of the constraint equations.
        """
        self.model = model
        self.rhs = rhs

    def __call__(self, p=None, deriv=False):
        """
        Evaluate the constraint function or its derivative.

        Parameters
        ----------
        p : numpy.array, optional
            The parameters at which to evaluate the constraint (default is None).
        deriv : bool, optional
            If True, return the derivative of the constraint (default is False).

        Returns
        -------
        None
            This method should be implemented in a subclass to return the constraint
            value or its derivative.

        Notes
        -----
        This is a placeholder method and must be overridden in subclasses
        to implement specific constraint logic.
        """
        pass

    def get_linearized_constraint(self, pars):
        """
        Compute the linearized version of the constraint for the given parameters.

        Parameters
        ----------
        pars : FitParameters
            The current parameters for which the linearized constraint will be computed.

        Returns
        -------
        None
            This method should be implemented in a subclass to return the constraint
            value or its derivative.


        Raises
        ------
        NotImplementedError
            This method is intended to be implemented by subclasses that
            define specific constraints.
        """
        raise NotImplementedError


class LinearConstraint(Constraint):
    """
    Generic linear constraints for a model.

    This class represents linear constraints applied to a model's parameters,
    ensuring that certain conditions are met during optimization.

    Parameters
    ----------
    model : object
        The model to which the constraints are applied.
    rhs : numpy.array
        The right-hand side of the constraint equations.

    """
    def __init__(self, model, rhs, h_matrix=None):
        """
        Initialize the LinearConstraint class.

        Parameters
        ----------
        model : SALT2Like model
            The model to which the constraints are applied.
        rhs : numpy.array
            The right-hand side of the constraint equations.
        """
        super().__init__(model, rhs)
        self.h_matrix = h_matrix
        self.rhs = rhs

    def init_h_matrix(self, pars):
        """
        Initialize the H matrix based on the parameters.

        This method should be implemented by subclasses.

        Parameters
        ----------
        pars : FitParameters
            The parameters used to initialize the H matrix.
        """
        raise NotImplementedError()

    def init_pars(self, pars):
        """
        Initialize the constraint with the given parameters.

        Parameters
        ----------
        pars : FitParameters
            The parameters used to initialize the constraint.
        """
        self.h_matrix = self.init_h_matrix(pars)

    def __call__(self, pars, deriv=False):
        """
        Evaluate the constraint and optionally its derivatives.

        Parameters
        ----------
        pars : FitParameters
            The parameters at which to evaluate the constraint.
        deriv : bool, optional
            If True, return the derivative of the constraint (default is False).

        Returns
        -------
        float
            The value of the constraint.
        tuple
            If deriv is True, returns a tuple containing the constraint value, the H matrix, and None.
        """
        if self.h_matrix is None:
            self.h_matrix = self.init_h_matrix(pars)

        cons = self.h_matrix @ pars.full - self.rhs
        cons = float(cons)
        if not deriv:
            return cons
        return cons, self.h_matrix, None

    def get_linearized_constraint(self, pars):
        """
        Return the linearized constraint matrix for the given parameters.

        This method computes and returns the linear constraint matrix H at the
        current set of parameters, which is used to linearize the constraints
        during optimization.

        Parameters
        ----------
        pars : FitParameters
            The current parameters used to compute the linearized constraint.

        Returns
        -------
        numpy.array
            The linearized constraint matrix H, converted to a dense matrix if it is sparse.
        """
        h = self.init_h_matrix(pars)
        return np.array(h.todense())


class ConstraintSet:
    """
    Combines a series of constraints (linear or non-linear) for a model.

    This class manages a set of constraints, typically applied to the parameters
    of a model during optimization. It computes a quadratic penalty term that is
    added to the log-likelihood to enforce the constraints. If needed, the class
    can also compute the gradient and Hessian of the penalty to be used in
    gradient-based optimization methods.

    Parameters
    ----------
    constraints : list of `Constraint`s
        A list of constraint objects (either linear or non-linear) that are applied
        to the model parameters.
    mu : float, optional
        A penalty scaling factor. It controls the strength of the penalty applied for
        constraint violations. Default is 1.E10.
    """

    def __init__(self, constraints, mu=1.E10):
        """
        Initialize the ConstraintSet class with a set of constraints and a penalty
        scaling factor.

        Parameters
        ----------
        constraints : list of `Constraint`
            A list of constraints to apply to the model's parameters.
        mu : float, optional
            A penalty scaling factor that dictates the importance of constraint satisfaction
            during optimization. Default is 1.E10.

        """
        # self.model = model
        self.constraints = constraints
        self.mu = mu

    def init_pars(self, pars):
        """
        Initialize the constraints with the given parameters.

        This method initializes each constraint in the set with the current parameter values.

        Parameters
        ----------
        pars : FitParameters
            The current set of parameters for the model, which are used to initialize
            the constraints.
        """
        for c in self.constraints:
            c.init_pars(pars)

    def __call__(self, pars, deriv=False):
        """Evaluate the penalty associated with the constraints, optionally computing
        its gradient and Hessian.

        This method calculates the quadratic penalty from the constraints. If
        `deriv=True`, it also computes the gradient and Hessian of the penalty
        with respect to the parameters.

        Parameters
        ----------
        pars : FitParameters
            The current parameter values at which the penalty and its derivatives (if requested) are evaluated.
        deriv : bool, optional
            If True, the method returns the gradient and Hessian of the penalty in addition to the penalty value.
            Default is False.

        Returns
        -------
        float
            The total quadratic penalty associated with the constraints.
        tuple
            If `deriv=True`, returns a tuple containing:
                - The penalty value.
                - The gradient of the penalty with respect to the parameters.
                - The Hessian matrix of the penalty.
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
        """
        Get the right-hand side (rhs) values for all the constraints.

        This method retrieves the rhs values from each constraint in the set.

        Returns
        -------
        numpy.array
            An array containing the right-hand side values for each constraint.
        """
        return np.array([c.rhs for c in self.constraints])

    def get_linearized_constraints(self, pars):
        """
        Retrieve the linearized form of all constraints.

        This method returns the linearized constraint matrix (H) for the set of
        constraints, which is useful for solving linear constraint systems
        during optimization.

        Parameters
        ----------
        pars : FitParameters
            The current parameter values used to compute the linearized constraints.

        Returns
        -------
        numpy.array
            A stacked matrix of the linearized constraints for all constraints in the set.
        """
        return np.vstack([c.get_linearized_constraint(pars) for c in self.constraints])


class int_M0_at_phase_cons(LinearConstraint):
    """constraint on the integral of the M0 surface at peak

    This function builds a linear constraint on the M0 parameters.

    .. note:: at this stage, the constraints are a function of the *full*
       parameter vector, not just the free parameters.
    """
    def __init__(self, model, rhs, phase, band):
        super().__init__(model, rhs)
        self.phase = phase
        self.band = band

    def init_h_matrix(self, pars):
        J_phase = self.model.basis.by.eval(np.array([self.phase])).toarray()
        pp = pars.copy()
        pp.release()
        gram_dot_filter = self.model.get_gram_dot_filter(self.band)
        C = coo_matrix(np.outer(J_phase, gram_dot_filter).ravel())
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        i = np.full(len(C.col), 0)
        j = pp['M0'].indexof(C.col)
        M = coo_matrix((C.data, (i, j)), shape=(1, npars))
        M.data *= (self.model.norm / self.model.int_ab_spec)
        return M


class int_dM0_at_phase_cons(LinearConstraint):
    """constraint on the integral of the phase derivatives of M0 at peak
    """
    def __init__(self, model, rhs, phase, band):
        super().__init__(model, rhs)
        self.phase = phase
        self.band = band

    def init_h_matrix(self, pars):
        J_dphase = self.model.basis.by.deriv(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter(self.band)
        C = coo_matrix(np.outer(J_dphase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['M0'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data # / self.model.int_M0_phase_0 # (1.E5 * self.model.int_ab_spec)
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        M.data *= (self.model.norm)
        return M


class int_M1_at_phase_cons(LinearConstraint):
    """constraint on the integral of the M1 surface at peak
    """
    def __init__(self, model, rhs, phase, band):
        super().__init__(model, rhs)
        self.phase = phase
        self.band = band

    def init_h_matrix(self, pars):
        J_phase = self.model.basis.by.eval(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter(self.band)
        C = coo_matrix(np.outer(J_phase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['M1'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data   #/ model.int_M0_phase_0
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        M.data *= self.model.norm
        return M


class int_dM1_at_phase_cons(LinearConstraint):
    """constraint on the integral of the phase derivatives of M1 at peak
    """
    def __init__(self, model, rhs, phase, band):
        super().__init__(model, rhs)
        self.phase = phase
        self.band = band

    def init_h_matrix(self, pars):
        J_dphase = self.model.basis.by.deriv(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter(self.band)
        C = coo_matrix(np.outer(J_dphase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['M1'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data  # / model.int_M0_phase_0
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        M.data *= self.model.norm
        return M

class int_diff_dm_at_phase_cons(LinearConstraint):
    """Constraint on the differential Dm15 of a SN of x1=1.
    """
    def __init__(self, model, rhs, phase, band, diff_dm15=0.162):
        super().__init__(model, rhs)
        self.phase = phase
        self.band = band
        self.diff_dm15 = diff_dm15

    def init_h_matrix(self, pars):
        J_phase = self.model.basis.by.eval(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter(self.band)
        C = coo_matrix(np.outer(J_phase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()

        npars = len(pp.full)
        j = pp['M0'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data
        idx = j >= 0
        V0 = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        V0.data *= self.model.norm

        j = pp['M1'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data
        idx = j >= 0
        V1 = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        V1.data *= self.model.norm

        alpha = 10**(0.4 * self.diff_dm15)

        return (1.-alpha) * V0 + V1



class dm15_cons(LinearConstraint):
    r"""Constraint on the decay rate of the model

    the :math:`\Delta m_{15}` was historically as the difference between peak
    magnitude in the restframe :math:`B` band and the restframe :math:`B` band
    magnitude 15 restframe days later.

    This class allows us to constrain the flux ratio in a given restframe band
    between peak and some other (restframe) phase.
    """
    def __init__(self, model, rhs, phase, band, alpha, x1=0.):
        super().__init__(model, rhs)
        self.phase = phase
        self.band = band
        self.alpha = alpha
        self.x1 = x1

    def init_h_matrix(self, pars):
        J_0 = self.model.basis.by.eval(np.array([0.])).toarray()
        J_phase = self.model.basis.by.eval(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter(self.band)
        C_0 = coo_matrix(np.outer(J_0, gram_dot_filter).ravel())
        C_phase = coo_matrix(np.outer(J_phase, gram_dot_filter).ravel())
        #
        pp = pars.copy()
        pp.release()
        npars = len(pp.full)

        MM = []
        for C in [C_0, C_phase]:
            for surface in ['M0', 'M1']:
                j = pp[surface].indexof(C.col)
                i = np.full(len(C.col), 0)
                v = C.data   #/ model.int_M0_phase_0
                idx = j >= 0
                M = coo_matrix((v[idx], (i[idx], j[idx])),
                               shape=(1, npars))
                M.data *= self.model.norm
                MM.append(M)

        return MM[0] + self.x1 * MM[1] - self.alpha * (MM[2] + self.x1 * MM[3])


class mean_col_cons(LinearConstraint):
    """constraint on the mean of the color parameters
    """
    def __init__(self, model, rhs):
        super().__init__(model, rhs)

    def init_h_matrix(self, pars):
        nsn = len(pars['X0'].full)
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['c'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = np.full(nsn, 1./nsn)
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])), shape=(1, npars))
        return M


class mean_x1_cons(LinearConstraint):
    """constraint on the mean of the x1 parameters
    """
    def __init__(self, model, rhs):
        super().__init__(model, rhs)

    def init_h_matrix(self, pars):
        nsn = len(pars['X0'].full)
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['X1'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = np.full(nsn, 1./nsn)
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                       shape=(1, npars))
        return M


class x1_var_cons(Constraint):

    def __init__(self, model, rhs):
        self.model = model
        self.rhs = rhs

    def __call__(self, pars, deriv=False):
        """
        """
        # if p is not None:
        #     self.model.pars.free = p.free

        # CHECK: do we need all_pars_released, or just self.model.pars ?
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full) # len(self.model.all_pars_released.full)
        nsn = len(pp['X0'].full)

        # constraint function: h(X1) = \sum_i X1**2
        cons = (pp['X1'].full**2).sum() / nsn  # pp or pars ?
        if not deriv:
            return cons

        # first derivatives of h
        pars.full[:] = 0.
        j = pars['X1'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = pars['X1'].full
        idx = j >= 0
        J = coo_matrix((v[idx], (i[idx], j[idx])), shape=(1, npars)) # was +1

        # second derivatives of h
        i = pars['X1'].indexof(np.arange(nsn))
        v = np.full(nsn, 2./nsn)
        idx = j >= 0
        H = coo_matrix((v[idx], (i[idx], i[idx])), shape=(npars, npars))

        return cons, J, H


def salt2like_linear_constraints(model, mu=1.E6, Mb=-19.5, dm15=1.): # was 0.96
    """
    """
    # TODO: cleanup normalization scheme and color band names
    B = model.normalization_band_name

    m0_0 = int_M0_at_phase_cons(model, 14381300.77605067, phase=0., band=B) # ab_flux_at_10Mpc(Mb=Mb),
    dm0_0 = int_dM0_at_phase_cons(model, 0., phase=0., band=B)
    m1_0 = int_M1_at_phase_cons(model, 0., phase=0., band=B)
    m1_15 = int_M1_at_phase_cons(model, dm15, phase=15., band=B)  # rhs was 0.96
    # dm1 = int_dM1_at_phase_cons(model, 0.)
    col = mean_col_cons(model, 0.)
    x1  = mean_x1_cons(model, 0.)
    # x1_var = x1_var_cons(model, 1.)

    return ConstraintSet([m0_0, dm0_0, m1_0, m1_15, col, x1], mu=mu)


def nacl_linear_constraints(model, mu=1.E6, Mb=-19.5, dm15=1., magsys='AB'):
    """
    """
    # TODO: cleanup normalization scheme and color band names
    B = model.normalization_band_name
    V = model.color_band_names[1]

    # The model has a peak at phase 0 in the restframe B-band
    # and we fix the peak value
    m0_0_B  = int_M0_at_phase_cons(model, 14381300.77605067, phase=0., band=B) # ab_flux_at_10Mpc(Mb=Mb)
    dm0_0_B = int_dM0_at_phase_cons(model, 0., phase=0., band=B)
    m1_0_B  = int_M1_at_phase_cons(model, 0., phase=0., band=B)
    dm1_0_B = int_dM1_at_phase_cons(model, 0., phase=0., band=B)

    # The model has a fixed Dm15 in the restframe B-band
    rhs = 10**(-0.4 * dm15) * 14381300.77605067
    # rhs = 5.25774e+06 # temporary rhs
    m0_15_B = int_M0_at_phase_cons(model, rhs, phase=15., band=B)
    # m1_15_B = int_M1_at_phase_cons(model, 0., phase=15., band=B)  # rhs was 0.96
    diff_dm15 = int_diff_dm_at_phase_cons(model, 0., phase=15, band=B, diff_dm15=0.162)

    # The standard supernova has a restframe B-V color of zero
    ms = SNMagSys(model.filter_db, magsys)
    zp_B = ms.get_zp(model.color_band_names[0])
    zp_V = ms.get_zp(model.color_band_names[1])
    scale = 10**(0.4 * (zp_B-zp_V)) # should be minus
    m0_0_V = int_M0_at_phase_cons(model, 14381300.77605067 * scale, phase=0., band=V) # temporary rhs

    return ConstraintSet(
        [m0_0_B, dm0_0_B, m1_0_B, dm1_0_B, m0_15_B, diff_dm15, m0_0_V],
        mu=mu)


def salt24like_linear_constraints(model, pars, mu=1.E9, Mb=-19.5):
    """
    purely linear constraints, on the global model, derived from SALT2.4

    The goal of this constraint set is to test the global constraint strategy.
    """
    B = model.normalization_band_name
    V = model.color_band_names[1]

    # The model has a peak at phase 0 in the restframe B-band
    # and we fix the peak value
    m0_0_B = int_M0_at_phase_cons(model, 0, phase=0., band=B)
    m0_0_B_val = m0_0_B(pars)

    m1_0_B = int_M1_at_phase_cons(model, 0., phase=0., band=B)
    m1_0_B_val = m1_0_B(pars)

    # dm0_0_B = int_dM0_at_phase_cons(model, 0., phase=0., band=B)
    # dm0_0_B_val = dm0_0_B(pars)

    # dm1_0_B = constraints.int_dM0_at_phase_cons(model, 0., phase=0., band=B)

    # The model has a fixed Dm15 in the restframe B-band
    m0_15_B = int_M0_at_phase_cons(model, 0., phase=15., band=B)
    m0_15_B_val = m0_15_B(pars)

    m1_15_B = int_M1_at_phase_cons(model, 0., phase=15., band=B)  # rhs was 0.96
    m1_15_B_val = m1_15_B(pars)

    # The standard supernova has a restframe B-V color of zero
    m0_0_V = int_M0_at_phase_cons(model, 0., phase=0., band=V)
    m0_0_V_val = m0_0_V(pars)

    alpha = m0_0_B_val / m0_15_B_val
    beta = (m0_0_B_val + m1_0_B_val) / (m0_15_B_val + m1_15_B_val)
    cons = ConstraintSet(
        [int_M0_at_phase_cons(model, m0_0_B_val, phase=0., band=B),
         int_M1_at_phase_cons(model,         0., phase=0., band=B),
         int_dM0_at_phase_cons(model,        0., phase=0., band=B),
         dm15_cons(model, 0., phase=15., band=B, alpha=2.735, x1=0.),
         dm15_cons(model, 0., phase=15., band=B, alpha=2.357,  x1=1.),
         int_M0_at_phase_cons(model, m0_0_V_val, phase=0., band=V)],
        mu=mu)

    return cons


def salt2like_classical_constraints(model, mu=1.E6, Mb=-19.5):
    """
    """
    # m0_0 = int_M0_at_phase_cons(model, ab_flux_at_10Mpc(Mb=Mb), phase=0.)
    m0_0 = int_M0_at_phase_cons(model, 14381300.77605067, phase=0.)
    dm0_0 = int_dM0_at_phase_cons(model, 0., phase=0.)
    m1_0 = int_M1_at_phase_cons(model, 0., phase=0.)
    dm1 = int_dM1_at_phase_cons(model, 0.)
    col = mean_col_cons(model, 0.)
    x1  = mean_x1_cons(model, 0.)
    x1_var = x1_var_cons(model, 1.)

    return ConstraintSet(
        [m0_0, dm0_0, m1_0, dm1, col, x1, x1_var],
        mu=mu)
