"""SALT2 model: spectral part


TODO: remove color law evaluation from SpectrumEvalUnitFast
TODO: rename SpectrumEvalUnitFast

"""
import time
import numpy as np
import scipy

from nacl.sparseutils import CooMatrixBuff2


class CompressedSpectrumEvalUnit(object):
    """
    Predicts the components of the projection of the spectra on the model basis.

    For large datasets, it is often more efficient to project the spectra onto
    the model basis (which has significantly lower resolution) prior to
    training, and fit the model to the projection coefficients instead of the
    high-resolution spectra.

    Parameters
    ----------
    model : nacl.models.salt.SALT2Like
        The model used for evaluation.
    spec_recal_degree : int, optional
        The degree of the polynomial for spectral recalibration (default is 3).
    """
    def __init__(self, model, spec_recal_degree=3):
        """
        Constructor.

        Parameters
        ----------
        model : nacl.models.salt.SALT2Like
            The model used for evaluation.
        spec_recal_degree : int, optional
            The degree of the polynomial for spectral recalibration (default is 3).
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.recal_func = SpectrumRecalibrationPolynomials(model, deg=spec_recal_degree)
        self.model.recal_func = self.recal_func

    def __call__(self, pars, jac=False):
        """
        Evaluate the model on all spectra.

        Parameters
        ----------
        pars : saltworks.FitParameters
            The model parameters.
        jac : bool, optional
            If True, compute and return the Jacobian matrix.

        Returns
        -------
        numpy.array
            Model evaluations.
        scipy.sparse.csr_matrix, optional
            Jacobian matrix if `jac` is True.
        """
        tds = self.training_dataset
        spec_index = tds.spec_db.spec_index
        mjd = tds.spec_db.mjd
        sn_index = tds.spec_db.sn_index
        z = tds.spec_db.z

        # restframe phases
        restframe_phase = (mjd - pars['tmax'].full[sn_index]) / (1. + z)
        phase_basis = self.model.basis.by
        J = phase_basis.eval(restframe_phase + self.model.delta_phase)

        # TODO: we use the wavelength field to store the spline basis number
        # this is not a great idea, I think. We should use wavelength to
        # store the spline function mean wavelength and add a new field to store
        # the basis function number
        i_basis = tds.spec_data.i_basis.astype(int)

        # predict the spectrum coefficients
        n_wl, n_ph = len(self.model.basis.bx), len(self.model.basis.by)
        M0 = pars['M0'].full.reshape(n_ph, n_wl)
        MM = J.dot(M0)
        V0 = MM[tds.spec_data.spec_index, i_basis]

        M1 = pars['M1'].full.reshape(n_ph, n_wl)
        MM = J.dot(M1)
        V1 = MM[tds.spec_data.spec_index, i_basis]

        # model parameters
        X1 = pars['X1'].full[tds.spec_data.sn_index]

        # recalibration parameters
        recal, Jr = self.recal_func(pars, jac=jac)
        # recal = np.exp(recal)

        zz = 1. + tds.spec_data.z
        pca = V0 + X1 * V1
        model_val = pca * recal / zz


        if not jac:
            v = np.zeros(len(self.training_dataset))
            # v[tds.spec_data.row] = self.model.norm * model_val
            v[tds.spec_data.row] = model_val
            return v

        # evaluate the derivatives
        N = len(tds)
        n_free_pars = len(pars.free)
        buff = CooMatrixBuff2((N, n_free_pars))


        # X0 does not appear in the spectral part model of the
        # dmdX0 = 0

        # dMdX1
        buff.append(tds.spec_data.row,
                    pars['X1'].indexof(tds.spec_data.sn_index),
                    V1 * recal / zz)

        # no color law (absorbed by recal)
        # dMdc = 0

        # dtmax
        # we can gain a little here, by not evaluating the gradient along the
        # wavelength (ddlambda)
        dJ = phase_basis.deriv(restframe_phase + self.model.delta_phase)
        dV0 = dJ.dot(M0)[tds.spec_data.spec_index, i_basis]
        dV1 = dJ.dot(M1)[tds.spec_data.spec_index, i_basis]
        buff.append(tds.spec_data.row,
                    pars['tmax'].indexof(tds.spec_data.sn_index),
                    -1. * (dV0 + X1 * dV1) * recal / zz**2)

        del dJ
        del dV0
        del dV1

        # dM0
        j = np.arange(n_ph)
        row = tds.spec_data.row.repeat(n_ph)
        tds_row = np.arange(len(tds.spec_data)).repeat(n_ph)
        spec_index = tds.spec_data.spec_index.repeat(n_ph)
        i_basis = tds.spec_data.i_basis.repeat(n_ph)
        l = np.tile(np.arange(n_ph), len(tds.spec_data))
        col = l * n_wl + i_basis # or maybe the other way around
        val = np.array(J.tocsr()[spec_index, l]).squeeze()

        buff.append(row,
                    pars['M0'].indexof(col),
                    val * recal[tds_row] / zz[tds_row])

        # dM1
        buff.append(row,
                    pars['M1'].indexof(col),
                    X1[tds_row] * val * recal[tds_row] / zz[tds_row])

        # dcl (color law)
        # no color law -> dMdcl = 0

        # dMdr (recalibration)
        assert Jr is not None
        # Jr = self.recal_func.jacobian
        Jr = Jr.tocoo()
        buff.append(tds.spec_data.row[Jr.row],
                    pars['SpectrumRecalibration'].indexof(Jr.col),
                    Jr.data * pca[Jr.row] / zz[Jr.row])
                    # Jr.data * recal[Jr.row] * pca[Jr.row] / zz[Jr.row])

        J = buff.tocoo()
        # J.data *= self.model.norm

        v = np.zeros(len(self.training_dataset))
        # v[tds.spec_data.row] = self.model.norm * model_val
        v[tds.spec_data.row] = model_val
        return v, J


class CompressedSpectroPhotoEvalUnit(object):
    """Predicts the spectrophotometric data projected on the model wavelength basis

    Spectrophotometric spectra, hence, no recalibration polynomials, but a color law.
    """
    def __init__(self, model):
        """Constructor.

        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.color_law = model.color_law

    def __call__(self, pars, jac=False):
        r"""Evaluate the model for a all spectra

        Parameters
        ----------
        pars : `saltworks.FitParameters`
            the model parameter vector
        jac : bool
            if True compute and return the jacobian matrix

        Returns
        -------
        val : numpy.array
            Model evaluations.
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix (if jac is true).
        """
        tds = self.training_dataset
        spec_index = tds.spectrophot_db.spec_index
        sn_index = tds.spectrophot_db.sn_index
        mjd = tds.spectrophot_db.mjd
        z = tds.spectrophot_db.z
        #self.model.renorm(pars)
        norm = self.model.norm
        #norm = 1.

        # restframe phases
        restframe_phase = (mjd - pars['tmax'].full[sn_index]) / (1. + z)
        phase_basis = self.model.basis.by
        J = phase_basis.eval(restframe_phase + self.model.delta_phase)

        # TODO: we use the wavelenth field to store the spline basis number. We
        # need to change that: use the wavelength column to store the spline
        # function mean wavelength, and add a new field to stire the basis
        # function id.
        i_basis = tds.spectrophotometric_data.i_basis.astype(int)

        # predict the projection coefficients (and not the original spectral fluxes)
        n_wl, n_ph = len(self.model.basis.bx), len(self.model.basis.by)
        M0 = pars['M0'].full.reshape(n_ph, n_wl)
        MM = J.dot(M0)
        V0 = MM[tds.spectrophotometric_data.spec_index, i_basis]

        M1 = pars['M1'].full.reshape(n_ph, n_wl)
        MM = J.dot(M1)
        V1 = MM[tds.spectrophotometric_data.spec_index, i_basis]

        # model parameters
        X0 = pars['X0'].full[tds.spectrophotometric_data.sn_index]
        X1 = pars['X1'].full[tds.spectrophotometric_data.sn_index]
        col = pars['c'].full[tds.spectrophotometric_data.sn_index]

        # color law
        cl_pars = pars['CL'].full
        cl_pol, J_cl_pol = self.color_law(tds.spectrophotometric_data.wavelength,
                                          cl_pars, jac=jac)
        cl = np.power(10., 0.4 * col * cl_pol)

        # norm
        norm = self.model.norm

        zz = 1. + tds.spectrophotometric_data.z
        #model_val = norm * X0 * (V0 + X1 * V1) * cl / zz
        model_val = X0 * (V0 + X1 * V1) * cl / zz

        if not jac:
            v = np.zeros(len(self.training_dataset))
            v[tds.spectrophotometric_data.row] = self.model.norm * model_val
            return v

        J_i, J_j, J_val = [], [], []

        # now, the derivatives
        # dMdX0
        J_i.append(tds.spectrophotometric_data.row)
        J_j.append(pars['X0'].indexof(tds.spectrophotometric_data.sn_index))
        J_val.append(norm * (V0 + X1 * V1) * cl / zz)

        # dMdX1
        J_i.append(tds.spectrophotometric_data.row)
        J_j.append(pars['X1'].indexof(tds.spectrophotometric_data.sn_index))
        J_val.append(norm * X0 * V1 * cl / zz)

        # dMdcol
        J_i.append(tds.spectrophotometric_data.row)
        J_j.append(pars['c'].indexof(tds.spectrophotometric_data.sn_index))
        J_val.append(norm * model_val * 0.4 * np.log(10.) * cl_pol)

        # dMdtmax
        dJ = phase_basis.deriv(restframe_phase + self.model.delta_phase)
        dV0 = dJ.dot(M0)[tds.spectrophotometric_data.spec_index, i_basis]
        dV1 = dJ.dot(M1)[tds.spectrophotometric_data.spec_index, i_basis]
        J_i.append(tds.spectrophotometric_data.row)
        J_j.append(pars['tmax'].indexof(tds.spectrophotometric_data.sn_index))
        J_val.append(-norm * X0 * (dV0 + X1 * dV1) * cl / zz**2)

        del dJ

        # dMdM0
        j = np.arange(n_ph)
        row = tds.spectrophotometric_data.row.repeat(n_ph)
        tds_row = np.arange(len(tds.spectrophotometric_data)).repeat(n_ph)
        spec_index = tds.spectrophotometric_data.spec_index.repeat(n_ph)
        i_basis = tds.spectrophotometric_data.i_basis.repeat(n_ph)
        l = np.tile(np.arange(n_ph), len(tds.spectrophotometric_data))
        col = l * n_wl + i_basis # or maybe the other way around
        val = np.array(J.tocsr()[spec_index, l]).squeeze()

        J_i.append(row)
        J_j.append(pars['M0'].indexof(col))
        J_val.append(norm * X0[tds_row] * val * cl[tds_row] / zz[tds_row])

        # dMdM1
        J_i.append(row)
        J_j.append(pars['M1'].indexof(col))
        J_val.append(norm * X0[tds_row] * X1[tds_row] * val * cl[tds_row] / zz[tds_row])

        # dMdcl
        col = pars['c'].full[tds.spectrophotometric_data.sn_index]
        JJ = scipy.sparse.coo_matrix(J_cl_pol)
        J_i.append(tds.spectrophotometric_data.row[JJ.row])
        J_j.append(pars['CL'].indexof(JJ.col))
        J_val.append(norm * model_val[JJ.row] * 0.4 * np.log(10) * col[JJ.row] * JJ.data)

        i = np.hstack(J_i)
        j = np.hstack(J_j)
        val = np.hstack(J_val)
        idx = j >= 0
        N = len(tds)
        n_free_pars = len(pars.free)
        JJ = scipy.sparse.coo_matrix((val[idx], (i[idx], j[idx])),
                                     shape=(N, n_free_pars))
        #JJ.data *= self.model.norm

        v = np.zeros(len(self.training_dataset))
        v[tds.spectrophotometric_data.row] = self.model.norm * model_val

        return v, JJ

# FIXME: not sure this one works well.
# TODO: write a series of tests
class SpectrumEvalUnitFast(object):
    r"""Evaluate the model for all SN spectra in the training dataset

    This class is one of the two type of "eval units". Given a chunk of the
    training dataset which corresponds the spectral observations, and given the
    :math:`(X_0, X_1, c, t_{max})` parameters of the SN, it computes the
    quantity:

    .. math::
         \frac{1}{1+z} \left[M_0\left(\frac{\lambda}{1+z}, \mathrm{p}\right) + X_1\ M_1\left(\frac{\lambda}{1+z},
         \mathrm{p}\right) \right]\ 10^{0.4\ c\ P(\frac{\lambda}{1+z})}\ s(\lambda_{rec})

    where
    .. math::
        M_{0|1}(\lambda, \mathrm{p}) = \sum_{k\ell} \theta_{k\ell} B_k(\mathrm{p}) B_l(\mathrm{\lambda})

    and
    .. math::
         \mathrm{p} = \frac{t - t_{max}}{1+z}

    and where :math:`R_s(\lambda)` is a polynomial correction which absorbs the
    wavelength-dependent large scale calibration errors affecting the spectrum.

    The evaluation reduces to a sparse matrix multiplication.

    """
    def __init__(self, model, spec_recal_degree=3):
        """Constructor.

        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        tds = model.training_dataset
        self.training_dataset = model.training_dataset
        self.spec_data = tds.spec_data
        self.model = model
        self.z = self.spec_data.z

        self.wl_basis_size = len(model.basis.bx)
        self.ph_basis_size = len(model.basis.by)

        # restframe wavelengths
        self.restframe_wl = self.spec_data.wavelength/(1.+self.z)
        self.recal_func = SpectrumRecalibrationPolynomials(model, deg=spec_recal_degree)
        self.model.recal_func = self.recal_func

    def __call__(self, pars, jac=False, debug_mode=False):
        r"""Evaluate the model on all spectra

        Parameters
        ----------
        jac : bool
            if True compute and return the jacobian matrix
        debug_mode : bool
            if true, just return the model components.

        Returns
        -------
        val : numpy.array
            model evaluations.
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix (if jac is true).
        """
        tds = self.training_dataset
        t0 = time.perf_counter()
        spec_data = self.training_dataset.spec_data
        sn_index = spec_data.sn_index
        basis = self.model.basis
        color_law = self.model.color_law

        # pars = self.model.pars
        M0 = pars['M0'].full
        M1 = pars['M1'].full
        cl_pars = pars['CL'].full

        # sn-related parameters
        x0, x1 = pars['X0'].full[sn_index], pars['X1'].full[sn_index]
        c, tmax = pars['c'].full[sn_index],  pars['tmax'].full[sn_index]

        # we need to re-evaluate the basis on the phases, since tmax changes
        restframe_phases = (spec_data.mjd-tmax)/(1.+self.z)
        jacobian = basis.eval(self.restframe_wl, restframe_phases + self.model.delta_phase).tocsr()

        # model components
        component_0 = jacobian.dot(M0)
        component_1 = jacobian.dot(M1)
        polynome_color_law, jacobian_color_law = \
            color_law(self.restframe_wl, cl_pars, jac=jac)
        color_law = np.power(10., 0.4*c*polynome_color_law)
        zz = 1. + self.z

        # recalibration polynomial
        # if we evaluate this, then recal_func must be instantiated
        # if self.recal_func is not None:
        assert self.recal_func is not None
        recal, jacobian_spec_rec = self.recal_func(pars, jac=jac)
        if jacobian_spec_rec is not None:
            jacobian_spec_rec = jacobian_spec_rec.tocoo()
            # don't know what to do with this
            # jacobian_spec_rec.data *= recal[jacobian_spec_rec.row]

        # recal = np.exp(recal)
        pca = (component_0 + x1 * component_1)
        model = pca * color_law * recal / zz

        if debug_mode:
            return component_0, component_1, color_law, recal, model

        #self.model.val.append(_model)
        if not jac:
            #self.model.timing.append(time.perf_counter()-t0)
            v = np.zeros(len(self.training_dataset))
            v[tds.spec_data.row] = self.model.norm * model
            return v
        else:
            raise "Not implemented"
        
        # jacobian = jacobian.tocoo()

        # # X0 does not appear in the spectral part of the model
        # # hence, dmdX0 = 0

        # # dMdX1
        # jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val
        # jacobian_i.append(spec_data.row)
        # jacobian_j.append(pars['X1'].indexof(sn_index))
        # jacobian_val.append(component_1 * color_law * recal / zz)

        # # dMdc
        # jacobian_i.append(spec_data.row)
        # jacobian_j.append(pars['c'].indexof(sn_index))
        # jacobian_val.append(model * 0.4 * np.log(10.) * polynome_color_law)

        # # dMdtmax
        # # we can gain a little here, by not evaluating the gradient along the wavelength (ddlambda)
        # _, deval_phase = self.model.basis.gradient(self.restframe_wl, restframe_phases + self.model.delta_phase)
        # deval_phase = deval_phase.tocsr()
        # jacobian_i.append(spec_data.row)
        # jacobian_j.append(pars['tmax'].indexof(sn_index))
        # jacobian_val.append(-1. * (deval_phase.dot(M0) + x1*deval_phase.dot(M1)) * color_law * recal / zz**2)

        # # dmdtheta_0
        # jacobian_i.append(spec_data.row[jacobian.row])
        # jacobian_j.append(pars['M0'].indexof(jacobian.col))
        # jacobian_val.append(jacobian.data * color_law[jacobian.row] * recal[jacobian.row] / zz[jacobian.row])

        # # dmdtheta_1
        # jacobian_i.append(spec_data.row[jacobian.row])
        # jacobian_j.append(pars['M1'].indexof(jacobian.col))
        # jacobian_val.append(x1[jacobian.row] * jacobian.data * color_law[jacobian.row] *
        #                     recal[jacobian.row] / zz[jacobian.row])

        # # dMdcl (color law)
        # jacobian_color_law = scipy.sparse.coo_matrix(jacobian_color_law)
        # jacobian_i.append(spec_data.row[jacobian_color_law.row])
        # jacobian_j.append(pars['CL'].indexof(jacobian_color_law.col))
        # jacobian_val.append(c[jacobian_color_law.row] * 0.4 * np.log(10.) * jacobian_color_law.data *
        #                     model[jacobian_color_law.row])

        # # dMdr (recalibration)
        # if jacobian_spec_rec is not None:
        #     jacobian_i.append(spec_data.row[jacobian_spec_rec.row])
        #     jacobian_j.append(pars['SpectrumRecalibration'].indexof(jacobian_spec_rec.col))
        #     jacobian_val.append(jacobian_spec_rec.data * (pca*color_law)[jacobian_spec_rec.row]/zz[jacobian_spec_rec.row])

        # if self.model.disable_cache:
        #     self.model.clear_cache()
        # self.model.timing.append(time.perf_counter()-t0)

        # return _model, 


class SpectroPhotoEvalUnit(object):
    """Evaluation of calibrated spectra
    """
    def __init__(self, tds, model):
        """Constructor.

        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.models.salt.SALT2Like
            Model.
        """
        self.training_dataset = tds
        self.data = tds.spectrophotometric_data
        self.model = model

        self.spec_index = self.data.spec_index
        self.sn_index = self.data.sn_index
        self.z = self.data.z

        # Look at that later
        self.color_law = model.color_law
        #        self.pars = model.pars
        self.basis = model.basis

        self.wl_basis_size = len(model.basis.bx)
        self.ph_basis_size = len(model.basis.by)

        # restframe wavelengths
        self.restframe_wl = self.data.wavelength/(1.+self.z)
        #        self.Jl = model.basis.bx.eval(self.restframe_wl).tocsr()

        # and we can connect directly to the global parameters
        #        self.M0 = model.pars['M0'].full
        #        self.M1 = model.pars['M1'].full
        #        self.cl_pars = model.pars['CL'].full

    def __call__(self, pars, jac=False, debug_mode=False):
        r"""Evaluate the model for a all spectra

        Parameters
        ----------
        jac : bool
            if True compute and return the jacobian matrix
        debug_mode : bool
            if true, just return the model components.

        Returns
        -------
        val : numpy.array
            Model evaluations.
        jacobian : scipy.sparse.csr_matrix
            Jacobian matrix (if jac is true).
        """

        t0 = time.perf_counter()

        # sn-related parameters
        x0, x1 = pars['X0'].full[self.sn_index], pars['X1'].full[self.sn_index]
        c, tmax = pars['c'].full[self.sn_index],  pars['tmax'].full[self.sn_index]
        # c, tmax = pars['c'].full[self.sn_index],  pars['tmax'].full[self.training_dataset.spectrophotometric_data.isn]

        # we need to re-evaluate the basis on the phases, since tmax changes
        restframe_phases = (self.data.mjd-tmax)/(1.+self.z)
        jacobian = self.basis.eval(self.restframe_wl, restframe_phases + self.model.delta_phase).tocsr()

        # norm
        norm = self.model.norm

        # model components
        component_0 = jacobian.dot(self.M0)
        component_1 = jacobian.dot(self.M1)

        polynome_color_law, jacobian_color_law = self.color_law(self.restframe_wl, self.cl_pars, jac=jac)
        color_law = np.power(10., 0.4*c*polynome_color_law)
        zz = 1. + self.z

        pca = (component_0 + x1 * component_1)
        model = x0 * norm * pca * color_law / zz

        if debug_mode:
            return component_0, component_1, color_law, recal, model

        self.model.val.append(model)
        if not jac:
            self.model.timing.append(time.perf_counter()-t0)
            return model

        jacobian = jacobian.tocoo()
        # jacobian_spec_rec = jacobian_spec_rec.tocoo()

        jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val
        jacobian_i.append(self.data.row)
        jacobian_j.append(pars['X0'].indexof(self.sn_index))
        # jacobian_val.append((component_0 + x1*component_1) * color_law * recal / zz)
        jacobian_val.append(norm * pca * color_law / zz)

        # dMdX1
        # jacobian_i, jacobian_j, jacobian_val = self.model.jacobian_i, self.model.jacobian_j, self.model.jacobian_val
        jacobian_i.append(self.data.row)
        jacobian_j.append(pars['X1'].indexof(self.sn_index))
        # jacobian_val.append(x0 * component_1 * color_law * recal / zz)
        jacobian_val.append(x0 * norm * component_1 * color_law / zz)

        # dMdc
        jacobian_i.append(self.data.row)
        jacobian_j.append(pars['c'].indexof(self.sn_index))
        jacobian_val.append(model * 0.4 * np.log(10.) * polynome_color_law)

        # dMdtmax
        # we can gain a little here, by not evaluating the gradient along the wavelength (ddlambda)
        _, deval_phase = self.model.basis.gradient(self.restframe_wl, restframe_phases + self.model.delta_phase)
        deval_phase = deval_phase.tocsr()
        jacobian_i.append(self.data.row)
        jacobian_j.append(pars['tmax'].indexof(self.sn_index))
        #jacobian_val.append(-1. *x0* (deval_phase.dot(self.M0) + x1*deval_phase.dot(self.M1)) * color_law * recal / zz**2)
        jacobian_val.append(-1. * x0 * norm * (deval_phase.dot(self.M0) + x1*deval_phase.dot(self.M1)) * color_law / zz**2)

        # dmdtheta_0
        jacobian_i.append(self.data.row[jacobian.row])
        jacobian_j.append(pars['M0'].indexof(jacobian.col))
        #jacobian_val.append(x0[jacobian.row] *jacobian.data * color_law[jacobian.row] * recal[jacobian.row] / zz[jacobian.row])
        jacobian_val.append(x0[jacobian.row] * norm * jacobian.data * color_law[jacobian.row] / zz[jacobian.row])

        # dmdtheta_1
        jacobian_i.append(self.data.row[jacobian.row])
        jacobian_j.append(pars['M1'].indexof(jacobian.col))
        #jacobian_val.append(x0[jacobian.row]*x1[jacobian.row] * jacobian.data * color_law[jacobian.row] *
        #                    recal[jacobian.row] / zz[jacobian.row])
        jacobian_val.append(x0[jacobian.row] * x1[jacobian.row] * norm *  jacobian.data * color_law[jacobian.row]/ zz[jacobian.row])

        # dMdcl (color law)
        jacobian_color_law = scipy.sparse.coo_matrix(jacobian_color_law)
        jacobian_i.append(self.data.row[jacobian_color_law.row])
        jacobian_j.append(pars['CL'].indexof(jacobian_color_law.col))
        jacobian_val.append(c[jacobian_color_law.row] * 0.4 * np.log(10.) * jacobian_color_law.data *
                            model[jacobian_color_law.row])

        if self.model.disable_cache:
            self.model.clear_cache()
        self.model.timing.append(time.perf_counter()-t0)


        return model


class SpectrumRecalibrationPolynomials:
    r"""A utility class to manage the recalibration polynomials

    The photometric calibration of spectra is generally affected by significant
    error modes at large wavelength scales. It is imperative to remove these
    error modes, while preserving the information provided by the spectra at
    small scales (spectral features)

    This is achieved during training by multiplying the spectral predictions of
    the model by a recalibration polynomial specific to each spectrum, function
    of the observation wavelength :math:`\lambda_o`, and of order :math:`N_s =
    3`, common to all spectra:

    .. math::
        s(\lambda_{rec}) = \sum_i^{N_s} s_i \lambda_{rec}^{N_s - i} %quad \mbox{and}
        \quad \lambda_{0} = \frac{\lambda - 5000}{9000 - 2700}

    with:

    .. math::
        \lambda_{rec} = \frac{2 (\lambda_o - \lambda_{max})}{\lambda_{max} - \lambda_{min}+1

    """
    def __init__(self, model, deg=3):
        """Constructor

        Parameters
        ----------
        tds : nacl.dataset.TrainingDataset
            Data set of photometric and spectroscopic observations.
        model : nacl.model.salt
            Model.
        pol_degrees : int or indexable structure
            Polynomial degree for each spectrum.
        """

        self.tds = model.training_dataset
        self.model = model
        self.deg = deg
        self.jacobian = None

        self.n_meas = len(self.tds.spec_data)
        n_spectra = len(self.tds.spec_db)
        self.n_pars = n_spectra * (self.deg + 1)
        self.jacobian = self.build_jacobian_matrix()

    def get_struct(self):
        """
        """
        d = [('SpectrumRecalibration', self.n_pars)]
        return d

    def init_pars(self, pars):
        """initialize the model parameters

        return a parameter vector initialized such that the recalibration
        polynomials are evaluated to 1 for each spectra.

        Returns
        -------
        initialized parameters : array_like of floats

        """
        # p = np.zeros(self.n)
        # o = np.cumsum(self.pol_degrees+1) - 1
        # p[o] = 1.
        # return p
        i = np.arange(self.deg, self.n_pars, self.deg+1)
        pars['SpectrumRecalibration'].full[:] = 0.
        pars['SpectrumRecalibration'].full[i] = 1.

    @classmethod
    def reduced_wavelength(cls, wl):
        """reduce the wl values to the [-1,1] interval
        """
        wl_min, wl_max = wl.min(), wl.max()
        a = 2. / (wl_max - wl_min)
        b = 1. - 2. * wl_max / (wl_max-wl_min)
        rwl = a * wl + b
        return rwl

    def build_jacobian_matrix(self):
        """build the matrix of derivatives

        .. note:: this implementation is slightly different from what Guy had
          originally produced. Same degree for all spectra, same wavelength
          range for all spectra. If need, we may re-introduce some more
          complexity in the the future. Hopefully, we won't have to.

        """
        i, j, v = [], [], []
        spec_data = self.tds.spec_data

        for spec_index in self.tds.spec_db.spec_index:
            idx = spec_data.spec_index == spec_index
            wl = spec_data.wavelength[idx]
            rwl = self.reduced_wavelength(wl)
            J = scipy.sparse.coo_matrix(np.vander(rwl, self.deg+1))
            nz = np.nonzero(idx)[0]
            i.append(J.row + nz.min())
            offset = (self.deg+1) * spec_index
            j.append(J.col + offset)
            v.append(J.data)

        i = np.hstack(i)
        j = np.hstack(j)
        v = np.hstack(v)
        return scipy.sparse.coo_matrix((v, (i,j)),
                                       shape=(self.n_meas, self.n_pars)).tocsr()

    def __call__(self, pars, jac=False):
        """Evaluate the recalibration polynomials

            Parameters
            ----------
            jac : bool
                If the jacobian is needed.

            Returns
            -------
            v : numpy.array
                Recalibration parameter evaluated.
            self.jacobian : None or scipy.sparse.coo_matrix
                Jacobian matrix of the recalibration polynomial functions.
            """
        p_full = pars['SpectrumRecalibration'].full
        v = self.jacobian.dot(p_full)
        if not jac:
            return v, None
        return v, self.jacobian
