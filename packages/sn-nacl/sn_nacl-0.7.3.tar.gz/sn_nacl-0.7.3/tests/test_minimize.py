import logging
import numpy as np

logging.basicConfig(level=logging.INFO)

from nacl.models.toy2d import lightcurves as lc2d
from nacl.models.toy2d import spline as spl2d
from nacl.loglikelihood import LogLikelihood
from nacl.minimize import Minimizer


def test_spline():
    """ Use a 2D toy model to test the spline fit.
    """
    gen = spl2d.ToyDataGenerator(n0=50,n1=50, b0_size=25, b1_size=25)
    gen.generate()
    model = spl2d.Model(gen.x0, gen.x1, gen.basis.bx.grid, gen.basis.by.grid, order=4)
    nj = 25
    reg = spl2d.Regularization(nj, block_name='theta', mu0=1., mu2=1.)
    ll = LogLikelihood(model, reg=[reg], data=gen.get_data())
    minz = Minimizer(ll)
    p_init = ll.pars.copy()
    p_init['theta'].full[:] = np.random.rand(len(p_init['theta'].full))
    r = minz.minimize_lm(p_init=p_init.free, lamb=1.E-6)
    assert r["status"] == 'converged' # at least
    return minz

def gen_lc2d():
    """ Return toy 2d lc data.
    """
    nbands = 3
    gen = lc2d.ToyModelGenerator(nbands=nbands)
    dp = gen.generate()
    return dp

def test_lc2d(dp=None, diag_charge='marquardt_lmax'):
    """ Use a 2D toy model to test the lc fit.
    """
    if dp is None:
        dp = gen_lc2d()

    gamma_init = 0.05
    model = lc2d.LightCurve2DCalibScatter(dp)
    reg = lc2d.Regularization(block_name='theta')
    cons = lc2d.cons(model, mu=1.E6, color='True')
    snake = lc2d.SimpleErrorSnake(model)
    #V_calib = np.diag(np.full(nbands, 0.005**2))
    #calib_prior = lc2d.CalibPrior(V_calib)
    ll = LogLikelihood(model,
                       reg=[reg],
                       cons=[cons],
                       #priors=[calib_prior],
                       data=dp)

    # fit initialization
    for block_name in ['x0', 'stretch', 'color', 'tmax']:
        ll.pars[block_name].full[:] = dp.sample[block_name]
        ll.pars[block_name].fix()
        for block_name in ['x0', 'stretch', 'color', 'tmax', 'eta']:
            ll.pars[block_name].release()

    # first fit with model only
    minz = Minimizer(ll)
    r = minz.minimize_lm(p_init=ll.pars.free, lamb=1.E-6, dchi2=10., max_iter=10)

    # second fit, with model and error modelfull
    ll = LogLikelihood(model,
                       variance_model=snake,
                       reg=[reg],
                       cons=[cons],
                       #priors=[calib_prior],
                       data=dp)
    for block_name in ['x0', 'tmax', 'stretch', 'color', 'theta']:
        ll.pars[block_name].full[:] = r['pars'][block_name].full[:]
    ll.pars['gamma'].full[:] = gamma_init

    minz = Minimizer(ll)
    r = minz.minimize_lm(p_init=ll.pars.free,
                         lamb=1.E-6,
                         max_iter=150,
                         diag_charge=diag_charge)
    assert r["status"] == 'converged' # at least
    return minz

if __name__ == "__main__":

    dp = gen_lc2d()
    _minz = []
    lst_opt = ['levenberg', 'marquardt', 'marquardt_max', 'marquardt_lmax']
    for diag_charge in lst_opt:
        _m = test_lc2d(dp=dp, diag_charge=diag_charge)
        _m.plot()
        _minz.append(_m)

    for _m, option in zip(_minz, lst_opt):
        _l = _m.get_log()
        print(option)
        print(f"number of iteration: {len(_l)} number of attempts: {_l['attempts'].sum()} "
              f"last chi2 {_l['main_chi2'].iloc[-1]:.1f} "
              f"delta_chi2 {_l['dchi2'].iloc[-1]:.1e} "
              f"delta_pars {_l['ldpars'].iloc[-1]:.1e}")
