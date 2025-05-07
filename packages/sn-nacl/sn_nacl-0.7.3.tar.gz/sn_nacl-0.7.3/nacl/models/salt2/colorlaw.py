"""SALT2 color-law
"""

import numpy as np


class ColorLaw:
    r"""Implementation of the SALT2 color law (version 1)

        The SALT2 color law describes the color diversity of SNeIa. In SALT 2.4, the
        color law is parametrized as follows:

        .. math::
            CL(\lambda;c) = 10^{0.4\ c \times P(\lambda_r)}

        where :math:`P(\lambda_r)` is a polynomial, such as :math:`P(\lambda_B) = 0`
        and :math:`P(\lambda_V) = 1`.

        This implies the following transformation :

        .. math::
            \lambda_r = \frac{\lambda-\lambda^B}{\lambda^V - \lambda^B}

        It is defined in the wavelength range :math:`2800 A < \lambda < 7000 A` and
        extrapolated with a linear function outside this interval.

        This class evaluates :math:`P(\lambda, \alpha_i)` and its derivatives
        :math:`\partial P/\partial \alpha_i` (which is the painful part).
    """
    WAVELENGTH = {"U": 3650.88, "B": 4302.57, "V": 5428.55, "R": 6418.01, "I": 7968.34}
    U_WAVELENGTH = 3650.88
    B_WAVELENGTH = 4302.57
    V_WAVELENGTH = 5428.55
    R_WAVELENGTH = 6418.01
    I_WAVELENGTH = 7968.34

    def __init__(self, wl_range=[2800, 7000]):
        """
        Constructor.

        Parameters
        ----------
        wl_range : array_like, optional
            Nominal wavelength range for the polynomial color law. Outside this
            range, the color law is extrapolated with degree-1 polynomials (default is [2800, 7000] Å).
        """
        assert (wl_range[0] < wl_range[1])
        self.min_lambda, self.max_lambda = wl_range

        self.min_reduced_lambda = self.reduce(self.min_lambda)
        self.max_reduced_lambda = self.reduce(self.max_lambda)
        self.pars = np.zeros(5)

    def reduce(self, wl):
        r"""
        Wavelength remapping.

        Defined as:

        .. math::
            \lambda_r = \frac{\lambda - \lambda_B}{\lambda_V - \lambda_B}

        Parameters
        ----------
        wl : array-like
            The input wavelengths in Angstroms.

        Returns
        -------
        reduced_wavelengths : array of floats
            The remapped wavelengths.

        """
        B_WL, V_WL = self.WAVELENGTH["B"], self.WAVELENGTH["V"]
        return (wl-B_WL)/(V_WL-B_WL)

    def __call__(self, wl, p, jac=False):  # return_jacobian_as_coo_matrix=False):
        r"""
        Evaluate the polynomial part of the color law.

        The full SALT2 color law is given by:

        .. math::
            CL(\lambda, c) = 10^{0.4\ c\ P(\lambda, \alpha_i)}

        with

       .. math::
           P(\lambda) = \left\{ \begin{split}
           P'(\bar\lambda_{UV}) \times (\bar\lambda - \bar\lambda_{UV}) + P(\bar\lambda_{UV})
           & \ \ \ \ \mathrm{if \lambda < \lambda_{UV}} \\
           \bar\lambda \times \left(\sum_{i=1}^4 \alpha_i \bar\lambda^i + 1 - \sum_{i=1}^4\alpha_i\right)
           & \ \ \ \ \mathrm{if \lambda_{UV} < \lambda < \lambda_{IR}} \\
           P'(\bar\lambda_{IR}) \times (\bar\lambda - \bar\lambda_{IR}) + P(\bar\lambda_{IR})
           & \ \ \ \ \mathrm{if \lambda > \lambda_{IR}} \\
           \end{split}\right.

       This function evaluates :math:`P(\lambda,\alpha_i)` along with its
       derivatives w.r.t. the :math:`\alpha_i`: :math:`\partial P / \partial \alpha_i`.

       Parameters
       ----------
       wl : ndarray of float
           Input wavelengths (in Angstroms).
       p : ndarray
           Color law parameters (i.e. the :math:`(\alpha_i)_{1\leq i \leq 4}`).
       jac : bool, optional
           Whether to return the Jacobian matrix (default is False).

       Returns
       -------
       cl : array-like of float
           The color law values.
       jacobian : numpy.array or scipy.sparse.csr_matrix
           The matrix of derivatives, if `jac` is True.
        """
        self.pars[0:4] = p
        self.pars[4] = 1 - p.sum()
        d_pars = np.polyder(self.pars)

        # nominal range
        rwl = self.reduce(np.asarray(wl))
        r = np.polyval(self.pars, rwl) * rwl

        # uv side (if necessary)
        idx_uv = rwl < self.min_reduced_lambda
        has_uv_data = idx_uv.sum() > 0
        if has_uv_data:
            val = np.polyval(self.pars, self.min_reduced_lambda)
            d_val = np.polyval(d_pars, self.min_reduced_lambda)
            self.pars_uv = np.asarray([d_val * self.min_reduced_lambda + val,
                                       val * self.min_reduced_lambda])
            r[idx_uv] = np.polyval(self.pars_uv, rwl[idx_uv]-self.min_reduced_lambda)

        # ir side
        idx_ir = rwl > self.max_reduced_lambda
        has_ir_data = idx_ir.sum() > 0
        if has_ir_data:
            val = np.polyval(self.pars, self.max_reduced_lambda)
            d_val = np.polyval(d_pars, self.max_reduced_lambda)
            self.pars_ir = np.asarray([d_val * self.max_reduced_lambda + val,
                                       val * self.max_reduced_lambda])
            r[idx_ir] = np.polyval(self.pars_ir, rwl[idx_ir]-self.max_reduced_lambda)

        if not jac:
            return r, None

        # the jacobian is unfortunately a dense matrix
        # (maybe we should try using splines)
        #
        # In the nominal wavelength range, it has the form:
        #
        #   [l_1**5-l_1   l_1**4-l1    l_1**3-l1  l_1**2-l1]
        #   [  ...          ...           ...       ...    ]
        #   [l_N**5-l_1   l_N**4-l1    l_N**3-l1  l_N**2-l1]
        #
        v = np.vander(rwl, 6)[:, 0:-2]
        jacobian = (v.T-rwl).T

        #
        # and in the extrapolation range, it has the form:
        #
        # J_ik = [dCL'/da_k(rwl-rwl_uv) + dCL/da_k]
        #
        # Granted, it's not very readable. But it should be fast enough
        if has_uv_data:
            l_uv = self.min_reduced_lambda
            j1_luv = (np.vander([l_uv], 6)[:, 0:-2].T - np.array([l_uv])).T
            j2_luv = np.vander([l_uv], 5)[:, 0:-1] * np.array([5., 4., 3., 2.]) - 1.
            n_uv = idx_uv.sum()
            jacobian[idx_uv] = j2_luv * (rwl[idx_uv]-l_uv).reshape(n_uv, -1) + j1_luv * np.ones(n_uv).reshape(n_uv, -1)

        if has_ir_data:
            l_ir = self.max_reduced_lambda
            j1_lir = (np.vander([l_ir], 6)[:, 0:-2].T - np.array([l_ir])).T
            j2_lir = np.vander([l_ir], 5)[:, 0:-1] * np.array([5., 4., 3., 2.]) - 1.
            n_ir = idx_ir.sum()
            jacobian[idx_ir] = j2_lir * (rwl[idx_ir]-l_ir).reshape(n_ir, -1) + j1_lir * np.ones(n_ir).reshape(n_ir, -1)

        # check for nan's and inf's
        if np.any(np.isnan(r)) or np.any(np.isinf(r)):
            raise ValueError('inf/nan values in color law')

        #
        # if return_jacobian_as_coo_matrix:
        #    jacobian = scipy.sparse.coo_matrix(jacobian)

        return r, jacobian



def check_grad(wl, color_law, p):
    """
    Check the gradient of the color law.

    This function evaluates the color law and its Jacobian, then numerically
    estimates the gradient for comparison.

    Parameters
    ----------
    wl : array-like
        Wavelengths at which to evaluate the color law.
    color_law : ColorLaw
        An instance of the ColorLaw class.
    p : array-like
        Parameters of the color law.

    Returns
    -------
    jacobian : numpy.array
        The analytical Jacobian matrix.
    numerical_grad : numpy.array
        The numerically estimated gradient.
    """
    v, jacobian = color_law(wl, p, jac=True)
    dx = 1.E-7
    pp = p.copy()
    df = []
    for i in range(len(pp)):
        pp[i] += dx
        vp, _ = color_law(wl, pp, jac=False)
        df.append((vp-v)/dx)
        pp[i] -= dx
    return jacobian, np.vstack(df).T
