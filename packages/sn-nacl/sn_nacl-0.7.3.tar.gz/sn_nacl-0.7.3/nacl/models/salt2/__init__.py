"""The salt2 model
"""

import logging
import numpy as np

from .constraints import salt2like_linear_constraints, salt2like_classical_constraints, salt24like_linear_constraints, nacl_linear_constraints
from .regularizations import NaClSplineRegularization, NaClAdaptSplineRegularization
from .variancemodels import SimpleErrorSnake, CalibErrorModel, SNLambdaErrorSnake, LocalErrorSnake, SNLocalErrorSnake, ColorScatter
from .salt import SALT2Like
from .spectra import *
from .dust_extinction import DustExtinction


logger = logging.getLogger(__name__)


def wl_extend(n_wl = 200, min_wl = 2000., max_wl = 11000., step=30.):
    """
    Increases resolution in a defined region of wavelength.
    """
    #bad_zone = [(3500.,3800.),(5900.,6200.),(7700.,8300.)]
    reg_zone = (min_wl,max_wl)
    basis = np.linspace(reg_zone[0], reg_zone[1], n_wl)
    #for b in bad_zone:
    #    B = np.arange( b[0], b[1] + step, step )
    #    basis = np.append( basis, B )
    #    basis.sort()
    #    basis = np.unique(basis)
    return basis


def phase_extend(n_p = 20, min_p = -20., max_p = 50., step=1.):
    """
    Increases resolution in a defined region of wavelength.
    """
    #bad_zone = [(-20.,-15.),(40.,50.)]
    reg_zone = (min_p,max_p)
    basis = np.linspace(reg_zone[0], reg_zone[1], n_p)
    #for b in bad_zone:
    #    B = np.arange( b[0], b[1] + step, step )
    #    basis = np.append( basis, B )
    #    basis.sort()
    #    basis = np.unique(basis)
    return basis
phase_grid = phase_extend()
wl_grid = wl_extend(n_wl = 127, max_wl = 9000.)

def get_model(tds,
              # init_from_salt2_file='salt2.npz',
              **kwargs):
    """a general function to instantiate the model
    """
    ret = SALT2Like(tds, **kwargs)
    return ret

def get_constraint_prior(model, linear=True, mu=1.E6, Mb=-19.5, check=True):
    """instantiate a set of constraints to apply to the model parameters
    """
    cons = None
    if linear:
        pars = model.init_pars()
        cons = salt24like_linear_constraints(model, pars, mu=mu, Mb=Mb)
        # cons = nacl_linear_constraints(model, mu=mu, Mb=Mb)
    else:
        cons = salt2like_classical_constraints(model, mu=mu, Mb=Mb)
    # check active
    # if none active: return None
    return cons

def get_regularization_prior(model, pars, mu=1., order=1, check=True):
    """instantiate a regularization class
    """
    to_regularize = []
    for block_name in ['M0', 'M1', 'gamma_snake']:
        if block_name not in pars._struct.slices:
            continue
        if ((pars[block_name].indexof() >= 0).any()):
            to_regularize.append(block_name)
        else:
            logger.info(f'{block_name} has all pars fixed: no regularization needed')

    if check and len(to_regularize) == 0:
        return None

    return NaClAdaptSplineRegularization(
        model,
        pars,
        to_regularize=to_regularize,
        order=order,
        mu=mu)
    
    #return NaClAdaptSplineRegularization(
    #    model,
    #    pars,
    #    to_regularize=to_regularize,
    #    order=order,
    #    mu=mu)

def get_simple_snake_error(model):
    """instantiates a simple error snake model
    """
    variance_model = SimpleErrorSnake(model)
    return variance_model

def get_local_snake_error(model):
    """instantiates a local error snake model
    """
    variance_model = LocalErrorSnake(model)
    return variance_model

def get_sn_lambda_snake_error(model):
    """
    instantiates an error snake which is SN and wavelength dependent
    """
    variance_model = SNLambdaErrorSnake(model)
    return variance_model

def get_sn_local_snake_error(model):
    """
    """
    variance_model = SNLocalErrorSnake(model)
    return variance_model
