"""SN light curve eval unit
"""

import logging

import numpy as np

# import numexpr as ne

logger = logging.getLogger(__name__)


try:
    from sparse_dot_mkl import gram_matrix_mkl, dot_product_mkl
except:
    logger.warning('module: `sparse_dot_mkl` not available')
else:
    logger.info('sparse_dot_mkl found. Building hessian should be faster.')

from bbf import magsys
from bbf import bspline

from nacl.sparseutils import kron_product_by_line, CooMatrixBuff, CooMatrixBuff2




class LightcurveEvalUnit:
    """The evaluation unit for light curves.

    This class evaluates all light curves present in the training dataset at
    once for increased efficiency.

    """
    def __init__(self, model, **kwargs):
        """
        Initialize the LightcurveEvalUnit.

        Parameters
        ----------
        model : object
            The main model object containing the training dataset.
        """
        self.model = model
        self.training_dataset = model.training_dataset
        self.gram = self.model.gram.todense()
        self.color_law = self.model.color_law

        nb_lightcurves = len(self.training_dataset.lc_db)
        filter_db_basis_size = len(model.filter_db.basis)
        F = np.zeros((nb_lightcurves, filter_db_basis_size))
        for lc in self.training_dataset.lc_db:
            # tqz, _ = self.model.filter_db.insert(lc.band, z=lc.z)
            tr_data = self.model.filter_db.insert(lc.band, z=lc.z)
            F[lc.lc_index, :] = tr_data.tq

        self.flux_scales = self.compute_flux_scales()
        self.flux_scales *= self.model.norm

        # filter projections
        self.filter_projections = (self.gram @ F.T).T
        self.original_meas_filter_projections = \
            self.filter_projections[self.training_dataset.lc_data.lc_index]

        # model spline basis mean wavelengths
        self.basis_wavelengths = bspline.integ(self.model.basis.bx, n=1) / bspline.integ(self.model.basis.bx)

        # Galactic dust extinction model
        self.galactic_extinction = self._precompute_galactic_extinction()
        if self.galactic_extinction is not None:
            self.meas_filter_projections = np.multiply(self.original_meas_filter_projections, self.galactic_extinction)
        else:
            self.meas_filter_projections = self.original_meas_filter_projections

    def _precompute_galactic_extinction(self):
        """Precompute the Galactic dust extinction for the supernovae in the dataset.

        This method evaluates the Galactic dust extinction model (if specified)
        and computes the extinction correction for the supernovae based on their
        redshift and Milky Way E(B-V) values. The extinction is calculated over
        the basis wavelengths of the model and is stored for use in correcting
        the photometric data.

        Returns:
        --------
        np.ndarray or None
           Returns an array of extinction corrections for the lightcurve data if
           the Galactic dust extinction model is specified. If no model is available,
           returns `None`.

        Notes:
        ------
        - The method first checks if the `dust_extinction_model` is specified in
          the model. If not, it logs a warning and exits without calculating
          extinction.
        - The extinction is evaluated over the wavelength grid corresponding to
          the basis functions of the model, and redshifted to the observer frame
          for each supernova. This forms a (N_sn x len(basis)) matrix by which we
          multiply the contracted Gram-Filter matrix.
        - The Milky Way E(B-V) values (`mwebv`) are taken from the training
          dataset for each supernova and are used to apply the extinction model.
        - The final extinction matrix is indexed by the supernova lightcurve
          data.

        Raises:
        -------
        - Logs a warning if no Galactic dust extinction model is specified.
        """
        if self.model.dust_extinction_model is None:
            logging.warning('No Galactic dust extinction model specified !')
            return None

        ext_model = self.model.dust_extinction_model
        tds = self.training_dataset

        # we evaluate the model on the basis wavelengths
        basis_wavelengths = bspline.integ(self.model.basis.bx, n=1) / bspline.integ(self.model.basis.bx)
        wl = basis_wavelengths * 1e-4 # in microns

        # compute the extinction matrix
        zz = 1. + tds.sn_data.z
        mwebv = tds.sn_data.nt['mwebv']
        obs_frame_wl = (wl[:,np.newaxis] * zz).T
        ext = np.array([ext_model.extinguish((1. / obs_frame_wl)[i,:], Ebv=mwebv[i]) for i in range(obs_frame_wl.shape[0])])

        return ext[tds.lc_data.isn]

    def compute_flux_scales(self):
        """Compute the flux scales for the training dataset.

        The flux scales are necessary to convert model fluxes to observed
        fluxes in units defined by the observer.

        Returns
        -------
        numpy.array
            Array of flux scales.

        Notes
        -----
        Here, we assume that all mags are in the AB mag system. This may not be true.
        This need to be corrected.

        """
        zp_scale = self.training_dataset.lc_data.zp_scale

        # also insert the filter at z = 0, needed to compute integrals of AB spectrum
        bands = np.unique(self.training_dataset.lc_db.band)
        for b in bands:
            self.model.filter_db.insert(b, z=0.)

        ms = magsys.SNMagSys(self.model.filter_db)
        int_AB_dict = dict(zip(bands, [10.**(0.4 * ms.get_zp(b.lower())) for b in bands]))
        int_AB = np.array([int_AB_dict[b] for b in self.training_dataset.lc_data.band])
        flux_scales = int_AB / zp_scale
        return flux_scales

    def __call__(self, pars, jac=False):
        """Evaluate the light curve model for a given set of parameters.

        Parameters
        ----------
        pars : nacl.fitparameters.FitParameters
            The current set of fit parameters.
        jac : bool, optional
            Whether to compute and return the Jacobian matrix. Defaults to False.

        Returns
        -------
        numpy.array
            Model flux values.
        scipy.sparse.coo_matrix, optional
            Jacobian matrix if `jac` is True.

        """
        lc_data = self.training_dataset.lc_data
        lc_db = self.training_dataset.lc_db

        wl_basis = self.model.basis.bx
        ph_basis = self.model.basis.by
        n_wl, n_ph = len(wl_basis), len(ph_basis)

        # pick matrix
        n_lc, n_meas = len(lc_db), len(lc_data)

        # phases
        zz = 1. + lc_data.z
        tmax = pars['tmax'].full[lc_data.sn_index]
        restframe_phases = (lc_data.mjd - tmax) / zz
        J_phase_sparse = ph_basis.eval(restframe_phases + self.model.delta_phase)
        J_phase = np.array(J_phase_sparse.todense())


        if 'eta_calib' in pars._struct.slices:
            calib_corr = 1. + pars['eta_calib'].full[lc_data.band_index]
        else:
            calib_corr = np.ones(len(lc_data.band_index))

        if 'kappa_color' in pars._struct.slices:
            cs_corr = 1. + pars['kappa_color'].full[lc_data.lc_index]
        else:
            cs_corr = np.ones(len(lc_data.lc_index))

        M0 = pars['M0'].full.reshape(n_ph, n_wl)
        M1 = pars['M1'].full.reshape(n_ph, n_wl)
        X0 = pars['X0'].full[lc_data.sn_index]
        X1 = pars['X1'].full[lc_data.sn_index]
        col = pars['c'].full[lc_data.sn_index]
        cl_pars = pars['CL'].full

        # if self.color_law_out_of_the_integral:
        #     # here, we decide to move it out of the integral
        #     # maybe we need to add a small correction
        #     restframe_wavelength = lc_data.wavelength / zz
        #     cl_pol, J_cl_pol = self.color_law(restframe_wavelength,
        #                                       cl_pars, jac=jac)
        #     cl = np.power(10., 0.4 * col * cl_pol)
        #     meas_filter_projections = self.meas_filter_projections
        #     # cl_pol, J_cl_pol = self.color_law(restframe_wavelength,
        #     #                                   cl_pars, jac=jac)
        #     # cl = np.power(10., 0.4 * col * cl_pol)
        # else:
        # here, we apply a first order correction in order to take into
        # account the filter deformation when the color law is steep
        #            C0_2 = np.array(M0.dot(self.meas_filter_projections_2.T))
        #            C0_2 = (J_phase * C0_2.T).sum(axis=1)
        #            C1_2 = np.array(M1.dot(self.meas_filter_projections_2.T))
        #            C1_2 = (J_phase * C1_2.T).sum(axis=1)
        #            pca2 = C0_2 + X1 * C1_2
        #            restframe_wavelength = pca2 / pca
        cl_pol, J_cl_pol = self.color_law(self.basis_wavelengths,
                                          cl_pars, jac=jac)
        nn, _ = self.meas_filter_projections.shape
        cl_pol = np.broadcast_to(cl_pol, (nn, len(cl_pol)))
        cc = col.reshape(-1, 1)
        cl = np.power(10., 0.4 * cc * cl_pol)
        meas_filter_projections = np.multiply(self.meas_filter_projections, cl)
        C0_ = np.array(M0.dot(meas_filter_projections.T))
        C0 = (J_phase * C0_.T).sum(axis=1)
        C1_ = np.array(M1.dot(meas_filter_projections.T))
        C1 = (J_phase * C1_.T).sum(axis=1)

        #        if self.color_law_out_of_the_integral:
        #            pca = (C0 + X1 * C1) * cl
        pca = (C0 + X1 * C1)

        # self.lc_data_wl_restframe_debug = lc_data.wavelength / zz
        # self.restframe_wavelength = restframe_wavelength

        model_val = X0 * pca * zz * calib_corr * cs_corr

        if not jac:
            v = np.zeros(len(self.training_dataset))
            v[lc_data.row] = self.flux_scales * model_val
            return v

        # jacobian
        N = len(self.training_dataset)
        n_free_pars = len(pars.free)

        # since the hstack is taking a lot of time and memory, we do things differently:
        # we allocate 3 large buffers for the jacobian i, j, vals, and we
        # update them in place.

        # estimated size of the derivatives
        logger.debug(' ... kron')
        K = kron_product_by_line(J_phase_sparse, meas_filter_projections)
        logger.debug(f'     -> done, K.nnz={K.nnz} nnz_real={(K.data != 0.).sum()} {len(K.row)}')

        estimated_size = 2 * K.nnz   # dMdM0 and dMdM1
        estimated_size += 6 * N      # local parameters (dMdX0, dMdX1, dMdcol, dMtmax, dMdeta, dMdkappa)
        nnz = len(J_cl_pol.nonzero()[0])
        estimated_size += nnz
        logger.debug(f'estimated size: {estimated_size}')

        buff = CooMatrixBuff2((N, n_free_pars)) # , estimated_size)
        self.K = K
        self.X0 = X0
        self.cl = cl
        self.calib_corr = calib_corr
        self.cs_corr = cs_corr
        self.zz = zz

        # we start with the largest derivatives: dMdM0 and dMdM1
        # dMdM0
        # we could write it as:
        # v_ = X0[K.row] * K.data * cl[K.row] * calib_corr[K.row] * cs_corr[K.row] * zz[K.row]
        # but it is slow. So, we re-arrange it as:
        i_ = lc_data.row[K.row]
        # v_ = X0 * cl * calib_corr * cs_corr * zz
        v_ = X0 * calib_corr * cs_corr * zz
        # vv_, dd_ = v_[K.row], K.data
        # v_ = ne.evaluate('vv_ * dd_')
        v_ = v_[K.row] * K.data
        buff.append(i_,
                    pars['M0'].indexof(K.col),
                    v_)

        # dMdM1
        # X1_ = X1[K.row]
        buff.append(lc_data.row[K.row],
                    pars['M1'].indexof(K.col),
                    v_ * X1[K.row])

        del K
        del i_
        del v_

        # dMdtmax
        phase_basis = self.model.basis.by
        dJ = np.array(phase_basis.deriv(restframe_phases + self.model.delta_phase).todense())
        dC0 = (dJ * C0_.T).sum(axis=1)
        dC1 = (dJ * C1_.T).sum(axis=1)
        # buff.append(lc_data.row,
        #             pars['tmax'].indexof(lc_data.sn_index),
        #             # ne.evaluate('-X0 * (dC0 + X1 * dC1) * cl * calib_corr * cs_corr'))
        #             -X0 * (dC0 + X1 * dC1) * cl * calib_corr * cs_corr)
        buff.append(lc_data.row,
                    pars['tmax'].indexof(lc_data.sn_index),
                    # ne.evaluate('-X0 * (dC0 + X1 * dC1) * cl * calib_corr * cs_corr'))
                    -X0 * (dC0 + X1 * dC1) * calib_corr * cs_corr)

        del dJ
        del C0_
        del C1_

        # dMdcl
        # this is where I am not super happy with this explicit loop
        # over the color law parameters
        _, n_cl_pars = J_cl_pol.shape
        for p in range(n_cl_pars):
            K = 0.4 * np.log(10.) * np.array(J_cl_pol[:,p]) * np.array(meas_filter_projections)
            dC0_ = M0.dot(K.T)
            dC0 = (J_phase * dC0_.T).sum(axis=1)
            dC1_ = M1.dot(K.T)
            dC1 = (J_phase * dC1_.T).sum(axis=1)
            model_val_dcl = X0 * zz * (dC0 + X1 * dC1) * col * calib_corr * cs_corr
            buff.append(lc_data.row,
                        np.full(len(lc_data.row), pars['CL'].indexof(p)),
                        model_val_dcl)

        # dMdX0
        buff.append(lc_data.row,
                    pars['X0'].indexof(lc_data.sn_index),
                    pca * zz * calib_corr * cs_corr)
                    # pca * cl * zz * calib_corr * cs_corr)

        # dMdX1
        buff.append(lc_data.row,
                    pars['X1'].indexof(lc_data.sn_index),
                    X0 * C1 * zz * calib_corr * cs_corr)
                    # X0 * C1 * cl * zz * calib_corr * cs_corr)

        # dMdcol
        d_meas_filter_projections = np.multiply(meas_filter_projections, 0.4 * np.log(10.) * cl_pol)
        C0__dcol = np.array(M0.dot(d_meas_filter_projections.T))
        C0_dcol = (J_phase * C0__dcol.T).sum(axis=1)
        C1__dcol = np.array(M1.dot(d_meas_filter_projections.T))
        C1_dcol = (J_phase * C1__dcol.T).sum(axis=1)
        pca_dcol = (C0_dcol + X1 * C1_dcol)
        model_val_dcol = X0 * pca_dcol * zz * calib_corr * cs_corr
        del C0__dcol
        del C0_dcol
        del C1__dcol
        del C1_dcol
        buff.append(
            lc_data.row,
            pars['c'].indexof(lc_data.sn_index),
            model_val_dcol)

        # dMdeta
        if 'eta_calib' in pars._struct:
            buff.append(lc_data.row,
                        pars['eta_calib'].indexof(lc_data.band_index),
                        X0 * pca * zz * cs_corr)
                        # X0 * pca * cl * zz * cs_corr)

        # dMkappa
        if 'kappa_color' in pars._struct:
            buff.append(lc_data.row,
                        pars['kappa_color'].indexof(lc_data.band_index),
                        X0 * pca * zz * calib_corr)
                        # X0 * pca * cl * zz * calib_corr)

        logger.debug(' -> tocoo()')
        J = buff.tocoo()
        del buff

        # multiply the data by the flux scales
        # to express fluxes in observer units
        J.data *= self.flux_scales[J.row]
        v = np.zeros(len(self.training_dataset))
        v[lc_data.row] = self.flux_scales * model_val

        return v, J
