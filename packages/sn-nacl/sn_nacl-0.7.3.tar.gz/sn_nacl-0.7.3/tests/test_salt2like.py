import numpy as np
from nacl.dataset import TrainingDataset
from nacl.models import salt2
from lemaitre import bandpasses
import logging


def test_model():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    filterlib = bandpasses.get_filterlib()

    # Load the training data set
    tds = TrainingDataset.read_parquet("data/test_datasets/test_datasets_blind.parquet", filterlib=filterlib)

    model = salt2.get_model(tds)
    pars = model.init_pars()

    # to test the evaluation of the model and test the presence of inf, nan...
    v = model(pars)
    assert v is not None
    # assert the values of v are the ones we expect

    # to test the model derivatives
    v, J = model(pars, jac=True)
    assert v is not None
    assert J is not None
    # assert the values of v and J correspond to what we expect


# issue 20
def test_model_wl_basis_initialization():
    """
    """
    filterlib = bandpasses.get_filterlib()

    # Load the training data set
    tds = TrainingDataset.read_parquet(
        "data/test_datasets/test_datasets_blind.parquet",
        filterlib=filterlib)

    # instantiate a model with the tds, and make sure that
    # the model wavelength basis corresponds to the tds basis
    model = salt2.get_model(tds)
    check_tds_basis = np.allclose(model.basis.bx.grid, tds.basis.grid)
    check_tds_basis &= model.basis.bx.order == tds.basis.order
    assert check_tds_basis

    # even if we specify a wavelength basis for the model
    model = salt2.get_model(tds, wl_range=(2025., 9850.), basis_knots=(202, 20))
    check_tds_basis = np.allclose(model.basis.bx.grid, tds.basis.grid)
    check_tds_basis &= model.basis.bx.order == tds.basis.order
    assert check_tds_basis

    # now, remove the tds basis
    tds.basis = None
    wl_grid = np.linspace(2022., 12255., 250)
    model = salt2.get_model(tds, wl_grid=wl_grid)
    check_tds_basis = np.allclose(model.basis.bx.grid, wl_grid)
    check_tds_basis &= model.basis.bx.order == 4
    assert check_tds_basis


def test_model_cache():
    """Test the caching system implemented in the SALT2Like model
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    filterlib = bandpasses.get_filterlib()

    # Load the training data set
    tds = TrainingDataset.read_parquet("data/test_datasets/test_datasets_blind.parquet", filterlib=filterlib)

    # if we disable de cache, make sure that everything
    # is indeed recomputed
    model = salt2.get_model(tds, disable_cache=True)
    pars = model.init_pars()
    v = model(pars)
    assert model.cached is False
    vv = model(pars)
    assert model.cached is False
    assert np.allclose(v, vv)
    assert id(v) != id(vv)

    v, J = model(pars, jac=1)
    assert model.cached is False
    vv, JJ = model(pars, jac=1)
    assert model.cached is False
    assert np.allclose(v, vv)
    # what is super strange, is that J and JJ may be ordered differently
    D = J.todense() - JJ.todense()
    assert np.count_nonzero(D) == 0
    #    assert np.allclose(J.data, JJ.data)
    #    assert np.allclose(J.row, JJ.row)
    #    assert np.allclose(J.col, JJ.col)
    assert id(v) != id(vv)
    assert id(J) != id(JJ)

    # now, if we enable to cache, make sure that cache system works
    model = salt2.get_model(tds, disable_cache=False)
    pars = model.init_pars()
    v = model(pars)
    assert model.cached is False
    vv = model(pars)
    assert model.cached is True
    assert np.allclose(v, vv)
    assert id(v) == id(vv)

    # this time we want the jacobian
    # which, at this point, is not stored in the cache
    v, J = model(pars, jac=1)
    assert model.cached is False
    vv, JJ = model(pars, jac=1)
    assert model.cached is True
    assert np.allclose(v, vv)
    assert np.allclose(J.data, JJ.data)
    assert id(v) == id(vv)

    # change the parameter vector a little
    pars.full[222] += 1.E-6
    vvv = model(pars)
    assert model.cached is False
