from nacl.dataset import TrainingDataset
from nacl.models import salt2
from nacl.train import TrainSALT2Like
from lemaitre import bandpasses

import pytest


def test_training(tmp_path):
    filterlib = bandpasses.get_filterlib()

    # Load the training data set
    tds = TrainingDataset.read_parquet(
        "data/test_datasets/test_datasets_blind.parquet",
        filterlib=filterlib)

    model = salt2.get_model(tds)
    # tds.plot_sample()
    # plt.show()

    pars = model.init_pars()
    # to test the evaluation of the model and test the presence of inf, nan...
    v = model(pars)
    assert v is not None

    # Initialisation of the trainer
    trainer = TrainSALT2Like(tds, variance_model='simple_snake')
    # trainer.plot_lc("ZTF17aadlxmv", numfit=None, plot_variance=True)
    # plt.show()

    # # Training
    # path = str(tmp_path / "lemaitre_nacl_tests")
    # trainer.train_salt2_model(save=True, path=path)

    # # Outputs
    # pars_trained = trainer.log[-1].pars
    # v_trained = trainer.log[-1].v  # evaluated model
    # # cov_matrix = trainer.log[-1].minz.get_cov_matrix()[0]

    # # Tests
    # assert pars_trained is not None
    # assert v_trained is not None
