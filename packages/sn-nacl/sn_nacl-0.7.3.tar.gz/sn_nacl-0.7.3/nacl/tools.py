#!/usr/bin/env python3

import sys

import dill
import glob
import logging
from argparse import ArgumentParser
import pathlib

import numpy as np
import matplotlib
import pylab as pl
import pandas as pd

from lemaitre import bandpasses
from .dataset import TrainingDataset
from .models import salt2
from .models.salt2 import constraints
from .models.salt2 import variancemodels
from .train import TrainSALT2Like
from . import alchemy
from . import plotting


def load_tds(path='DC1_tests/DC1_snake/DC1_0_batch999/DC1_0_batch_999.parquet'):
    """
    """
    path = pathlib.Path(path)
    if path.is_dir():
        # TODO: it would be great to have this logic directly in the TrainingDataset code
        print(path.joinpath('*.sn.parquet'))
        sn_index_file = glob.glob(str(path.joinpath('*.sn.parquet')))
        assert len(sn_index_file) ==1, f'unable to identify the TrainingDataset unique sn index: {sn_index_file}'
        sn_index_file = pathlib.Path(sn_index_file[0])
        print(sn_index_file)
        input_path = sn_index_file.with_name(sn_index_file.stem.split('.')[0]).with_suffix('.parquet')
        print(input_path)
    else:
        input_path = path

    fl = bandpasses.get_filterlib(rebuild=False)
    tds = TrainingDataset.read_parquet(input_path, filterlib=fl)
    return tds


def clean_tds(tds):
    """
    """

class NaClTrainer:
    def __init__(self,
                 tds_directory,
                 output_directory):
        """
        """
        self.tds = load_tds(tds_directory)
        self.output_dir = output_directory
        if type(self.output_dir) == str:
            self.output_dir = pathlib.Path(self.output_dir)
        # create a generic model
        nacl_dust = salt2.DustExtinction()
        self.model_initial = salt2.SALT2Like(self.tds,
                                    phase_grid=np.linspace(-50, 100., 30),
                                    dust_extinction_model=nacl_dust.CCM89_dust())
        self.pars_initial = self.model_initial.init_pars()

    def clean(self):
        # create a cleaned dataset
        logging.info('new alchemy')
        self.clean = alchemy.CleanDataset(self.model_initial, self.pars_initial,
                                        spec_phase_range=(-20., 50.),
                                        flag_catastrophic_outliers=True)
        self.clean()
        
    def lc_fit(self):
        self.lcfit = alchemy.FitLightcurves(self.clean.model, self.clean.pars)
        self.lcfit()

        output = self.output_dir.joinpath('1_lcfit')
        self.lcfit.plot(output_dir=output)
        self.lcfit.save(output.joinpath('distillate.pkl'))
        
    def spec_recal(self):
        self.specfit = alchemy.FitSpectrumRecalibration(self.clean.model, self.clean.pars)
        self.specfit()

        output = self.output_dir.joinpath('2_specfit')
        self.specfit.plot(output_dir=output)
        self.specfit.save(output.joinpath('distillate.pkl'))
        
    def model_init_fit(self):
        self.fm = alchemy.FitModel(self.clean.model, self.clean.pars, mu_reg=1.E-0, mu_cons=1.E6, compute_covmat=False)
        for blk in ['X0', 'X1', 'c', 'tmax']:
            self.fm.pars[blk].full[:] = self.lcfit.pars[blk].full
        self.fm.pars['SpectrumRecalibration'].full[:] = self.specfit.pars['SpectrumRecalibration'].full

        self.fm.pars.fix()
        for blk in ['X0', 'X1', 'c', 'tmax']:
            self.fm.pars[blk].release()
        self.fm.pars['M0'].release()
        self.fm.pars['M1'].release()
        self.fm.pars['CL'].release()
        self.fm.pars['SpectrumRecalibration'].release()
        self.fm(max_iter=10)

        output = self.output_dir.joinpath('3_pretrain')
        self.fm.plot(output_dir=output)
        self.fm.save(output.joinpath('distillate.pkl'))
        
    def error_snake_simple(self):
        self.gsn = alchemy.FitSimpleVarianceModel(self.fm.model, self.fm.pars)
        for blk in ['X0', 'X1', 'c', 'tmax']:
            self.gsn.pars[blk].full[:] = self.fm.pars[blk].full
        self.gsn.pars['SpectrumRecalibration'].full[:] = self.fm.pars['SpectrumRecalibration'].full
        self.gsn()

        output = self.output_dir.joinpath('4_snake')
        self.gsn.plot(output_dir=output)
        self.gsn.save(output.joinpath('distillate.pkl'))
        
    def full_model(self, max_iter=15):
        self.fm2 = alchemy.FitModel(self.gsn.model, self.gsn.pars, mu_reg=1.E-0, mu_cons=1.E6, snake=self.gsn.snake)
        for blk in ['X0', 'X1', 'c', 'tmax', 'M0', 'M1', 'CL']:
            self.fm2.pars[blk].full[:] = self.gsn.pars[blk].full
        self.fm2.pars['SpectrumRecalibration'].full[:] = self.gsn.pars['SpectrumRecalibration'].full
        self.fm2.pars['gamma'].full[:] = self.gsn.pars['gamma'].full
        self.fm2.pars.release()
        self.fm2(max_iter=max_iter)

        output = self.output_dir.joinpath('5_full')
        self.fm2.plot(output_dir=output)
        self.fm2.save(output.joinpath('distillate.pkl'))
        
    def __call__(self, save_edris=False):
        """
        """
        self.clean()
        self.lc_fit()
        self.spec_recal()
        self.model_init_fit()
        self.error_snake_simple()
        self.full_model(max_iter=30)
        if save_edris:
            sn_data = pd.DataFrame(data=self.fm2.tds.sn_data.nt)
            sn_data = sn_data.rename(columns={
                'x0': 'x0_init',
                'x1': 'x1_init',
                'c': 'c_init',
                'tmax': 'tmax_init'})

            sn_index = self.fm2.tds.sn_data.sn_index
            sn_data = sn_data.assign(x0=self.fm2.pars['X0'].full[sn_index])
            sn_data = sn_data.assign(x1=self.fm2.pars['X1'].full[sn_index])
            sn_data = sn_data.assign(c=self.fm2.pars['c'].full[sn_index])
            sn_data = sn_data.assign(t0=self.fm2.pars['tmax'].full[sn_index])
            if 'name' not in sn_data.keys():
                sn_data = sn_data.rename(columns={'sn':'name'})
            sn_data.to_parquet(str(self.output_dir) + '/output_params' + '.parquet')
            
            cov_mat = self.fm2.covmat
            cov_reduced = cov_mat[
                :4 * len(self.fm2.tds.sn_data),
                :4 * len(self.fm.tds.sn_data)]
            iii = np.hstack(
                [sn_index + i * len(self.fm2.tds.sn_data) for i in range(4)])
            cov_reduced = cov_reduced[:, iii][iii]
            covmatrix_file = str(self.output_dir) + '/output_cov' + '.npy'
            np.save(covmatrix_file, cov_reduced.toarray())
                 

if __name__ == '__main__':

    parser = ArgumentParser(description='A command line tool to perform a NaCl training (experimental)')
    parser.add_argument('-O', '--output-dir',
                        type=pathlib.Path,
                        help='output directory')
    parser.add_argument('-i', '--interactive',
                        default=False,
                        action='store_true',
                        help='where plots should be interactive or not')
    parser.add_argument('input_tds',
                        type=pathlib.Path,
                        help='input training dataset')
    args = parser.parse_args()

    # interactive plots ?
    if args.interactive:
        pl.ion()
        matplotlib.use('TkAgg')
    else:
        pl.ioff()
        matplotlib.use('Agg')

    # load the dataset
    tds = load_tds(args.input_tds)

    # prepare an output directory
    output_dir = args.output_dir
    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    nacl_trainer = NaClTrainer(args.input_tds, args.output_dir)
    nacl_trainer()
    
    # create a generic model
    #nacl_dust = salt2.DustExtinction()
    #model = salt2.SALT2Like(tds,
    #                        phase_grid=np.linspace(-50, 100., 30),
    #                        dust_extinction_model=nacl_dust.CCM89_dust())
    #pars = model.init_pars()

    # create a cleaned dataset
    #logging.info('new alchemy')
    #clean = alchemy.CleanDataset(model, pars,
    #                             spec_phase_range=(-15., 45.),
    #                             flag_catastrophic_outliers=True)
    #clean()

    # fit the light curves only. No error model. No spectra
    #if True:
    #    lcfit = alchemy.FitLightcurves(clean.model, clean.pars)
    #    lcfit()

    #    output = output_dir.joinpath('1_lcfit')
    #    lcfit.plot(output_dir=output)
    #    lcfit.save(output.joinpath('distillate.pkl'))

    # fit the spectrum recalibration only
    #if True:
    #    specfit = alchemy.FitSpectrumRecalibration(clean.model, clean.pars)
    #    specfit()

    #    output = output_dir.joinpath('2_specfit')
    #    specfit.plot(output_dir=output)
    #    specfit.save(output.joinpath('distillate.pkl'))

    # now, fit the full model, no error pedestal
    #if True:
    #    fm = alchemy.FitModel(clean.model, clean.pars, mu_reg=1.E-6, mu_cons=1.E6)
    #    for blk in ['X0', 'X1', 'c', 'tmax']:
    #        fm.pars[blk].full[:] = lcfit.pars[blk].full
    #    fm.pars['SpectrumRecalibration'].full[:] = specfit.pars['SpectrumRecalibration'].full

    #    fm.pars.fix()
    #    for blk in ['X0', 'X1', 'c', 'tmax']:
    #        fm.pars[blk].release()
    #    fm.pars['M0'].release()
    #    fm.pars['M1'].release()
    #    fm.pars['CL'].release()
    #    fm.pars['SpectrumRecalibration'].release()
    #    fm(max_iter=10)

    #    output = output_dir.joinpath('3_pretrain')
    #    fm.plot(output_dir=output)
    #    fm.save(output.joinpath('distillate.pkl'))

    # fit the light curves only with a Local error model
    #if True:
        # gsn = alchemy.FitGammaSNVarianceModel(clean.model, pars=clean.pars, bins=(5,5))
    #    gsn = alchemy.FitSimpleVarianceModel(fm.model, fm.pars)
    #    for blk in ['X0', 'X1', 'c', 'tmax']:
    #        gsn.pars[blk].full[:] = fm.pars[blk].full
    #    gsn.pars['SpectrumRecalibration'].full[:] = fm.pars['SpectrumRecalibration'].full
    #    gsn()

    #    output = output_dir.joinpath('4_snake')
    #    gsn.plot(output_dir=output)
    #    gsn.save(output.joinpath('distillate.pkl'))

    #if True:
    #    # now, fit the full model, error snake
    #    fm2 = alchemy.FitModel(gsn.model, gsn.pars, mu_reg=1.E-6, mu_cons=1.E6, snake=gsn.snake)
    #    for blk in ['X0', 'X1', 'c', 'tmax', 'M0', 'M1', 'CL']:
    #        fm2.pars[blk].full[:] = gsn.pars[blk].full
    #    fm2.pars['SpectrumRecalibration'].full[:] = gsn.pars['SpectrumRecalibration'].full
    #    fm2.pars.release()
    #    fm2(max_iter=15)

    #    output = output_dir.joinpath('5_full')
    #    fm2.plot(output_dir=output)
    #    fm2.save(output.joinpath('distillate.pkl'))


    # if False:
    #     # now, fit the full model
    #     # snake = variancemodels.SNLocalErrorSnake2(fm.model, bins=(5,5))
    #     snake = variancemodels.SimpleErrorSnake(fm.model)
    #     fm3 = alchemy.FitModel(fm2.model, fm2.pars, snake=snake) # , error_pedestal=error_pedestal)
    #     for blk in ['X0', 'X1', 'c', 'tmax']:
    #         fm3.pars[blk].full[:] = fm2.pars[blk].full
    #         #        fm2.pars['gamma_sn'].full[:] = 0.05
    #     fm3.pars['gamma_snake'].full[:] = 0.05
    #     fm3.pars['SpectrumRecalibration'].full[:] = fm2.pars['SpectrumRecalibration'].full
    #     fm3.pars['M0'].full[:] = fm2.pars['M0'].full
    #     fm3.pars['M1'].full[:] = fm2.pars['M1'].full
    #     fm3.pars['CL'].full[:] = fm2.pars['CL'].full
    #     fm3.pars.release()
    #     # fm2(max_iter=50)
