# Check rate of mu+ mu- tau_h- --> mu+ mu+ tau_h-

import logging
logging.basicConfig(
    filename='analysis.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("checkMuonCharge")
import analysis_cfg
import uncertainties
import ROOT
import os
import math
import FinalStateAnalysis.PatTools.data as data_tool

if __name__ == "__main__":
    log.info("Beginning analysis")
    ############################################################################
    ### Load the data ##########################################################
    ############################################################################
    int_lumi = analysis_cfg.INT_LUMI
    skips = ['DoubleEl', 'EM', 'DoubleMu']
    samples, plotter = data_tool.build_data(
        'VH', analysis_cfg.JOBID, 'scratch_results',
        int_lumi, skips, count='emt/skimCounter', unweighted=False)

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

    channel = analysis_cfg.cfg['emt']
    charge_cat_cfg = channel['charge_categories']['emu']

    object1_cfg = charge_cat_cfg['object1']
    object2_cfg = charge_cat_cfg['object2']
    object3_cfg = charge_cat_cfg['object3']

    cuts = channel['baseline'] \
            + charge_cat_cfg['selections']['final']['cuts'] \
            + object1_cfg['pass'] + object2_cfg['pass'] + object3_cfg['pass']

    # Always require the e + muon are the opposite sign
    cuts += ['ElecCharge*MuCharge < 0']

    # Now make two categories - where the lead muon can flip, and where the
    # subleading muon can flip.  This prevents counting cases where the charge
    # would become 3.
    e_can_flip = cuts + ['ElecCharge*TauCharge > 0']

    plotter.register_tree(
        'e_can_flip',
        '/emt/final/Ntuple',
        'ElecAbsEta',
        ' && '.join(e_can_flip),
        binning = [2, 0, 3],
        include = ['*data*', 'Zje*'],
    )

    flippable = plotter.get_histogram(
        'data_MuEG',
        '/emt/final/Ntuple:e_can_flip',
    )

    print flippable.Integral()
    print flippable.GetBinContent(1)
    print flippable.GetBinContent(2)

    obs_bar = uncertainties.ufloat((
        flippable.GetBinContent(1),
        math.sqrt(flippable.GetBinContent(1))))
    obs_end = uncertainties.ufloat((
        flippable.GetBinContent(2),
        math.sqrt(flippable.GetBinContent(2))))

    print obs_bar*0.003
    print obs_end*0.02
    print obs_bar*0.003 + obs_end*0.02

    flippable_mc = plotter.get_histogram(
        'Zjets',
        '/emt/final/Ntuple:e_can_flip',
    )

    print flippable_mc.Integral()
    print flippable_mc.GetBinContent(1)
    print flippable_mc.GetBinContent(2)

    print flippable_mc.Integral()
    print flippable_mc.GetBinContent(1)*0.003
    print flippable_mc.GetBinContent(2)*0.02


