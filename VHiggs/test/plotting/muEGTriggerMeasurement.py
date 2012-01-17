'''

Code to measure the MuEG trigger efficiency

'''

import copy
import logging
import os
import re
import sys
import uncertainties

import ROOT
import FinalStateAnalysis.PatTools.data as data_tool
import FinalStateAnalysis.Utilities.Histo as Histo
import array

# Logging options
logging.basicConfig(filename='muEGTriggerMeasurement.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("muEG")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)

ROOT.gROOT.SetBatch(True)

# Select Z->mu+e events
selections = [
    'Muon2Pt > 25',
    'IsoMus_HLT > 0.5',
    'Muon2_MuRelIso < 0.1',
    'Electron_ERelIso < 0.3',
    'Muon2_MuID_WWID > 0.5',
    'Electron_EID_MITID > 0.5',

    'ElectronCharge*Muon2Charge < 0',
    'Electron_EBtag < 3.3',
    'Muon2DZ < 0.2',
    'ElectronDZ < 0.2',
    'Electron_MissingHits < 0.5',
    'Electron_hasConversion < 0.5',

    'Muon2AbsEta < 2.1',
    'Muon2_MtToMET < 40',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
]

samples, plotter = data_tool.build_data(
    'Mu', '2012-01-16-v1-MuonTP', 'scratch_results',
    4684, ['MuEG', 'DoubleMu', 'EM'], count='em/skimCounter')

canvas = ROOT.TCanvas("basdf", "aasdf", 1200, 600)
canvas.Divide(2)

def saveplot(filename):
    # Save the current canvas
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'muEGTrigger', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'muEGTrigger', filename + '_log' + filetype))

eta_bins = [
    ('barrel', 0, 1.44),
    ('trans', 1.44, 1.57),
    ('endcap', 1.57, 2.5),
]

rebin = 10

def get_yields(plotter, name, samples, binning):
    combined_histogram = None
    for sample in samples:
        sample_histo = plotter.get_histogram(
            sample, name, show_overflows=True)
        sample_histo.Sumw2()
        if combined_histogram is None:
            combined_histogram = Histo.Histo(sample_histo.th1)
        else:
            combined_histogram += sample_histo
    rebinned_histogram = combined_histogram.cloneAndRebin(binning)
    bin_boundaries = zip(binning[:-1], binning[1:])
    for start, end, in bin_boundaries:
        middle = start + (end - start)/2.
        yield (start, end, rebinned_histogram(middle),
               rebinned_histogram.GetBinError(rebinned_histogram.FindBin(middle)))

log.info("Beginning selections...")
for eta_bin in eta_bins:
    label, eta_low, eta_high = eta_bin
    log.info("Selecting %s", label)
    eta_selection = ['ElectronAbsEta >= %f' % eta_low,
                     'ElectronAbsEta < %f' % eta_high]
    plotter.register_tree(
        'denom_' + label,
        '/em/final/Ntuple',
        'ElectronPt',
        ' && '.join(selections + eta_selection),
        w = 'pu2011AB',
        binning = [100, 0, 100],
        include = ['*'],
        #exclude = fr_info['exclude'],
    )

    plotter.register_tree(
        'num_' + label,
        '/em/final/Ntuple',
        'ElectronPt',
        ' && '.join(selections + eta_selection + ['Mu17Ele8All_HLT > 0.5']),
        w = 'pu2011AB',
        binning = [100, 0, 100],
        include = ['*'],
        #exclude = fr_info['exclude'],
    )

    stack_denom = plotter.build_stack(
        '/em/final/Ntuple:denom_' + label,
        include = ['*'],
        exclude = ['*data*'],
        title = 'Mu-E mass',
        show_overflows = True,
        rebin = rebin,
    )

    data_denom = plotter.get_histogram(
        'data_SingleMu',
        '/em/final/Ntuple:denom_' + label,
        show_overflows = True,
        rebin = rebin,
    )

    canvas.cd(1)
    stack_denom.Draw()
    stack_denom.GetXaxis().SetTitle('Mu-E mass')
    data_denom.Draw("pe, same")
    #legend.Draw()
    stack_denom.SetMaximum(max(stack_denom.GetMaximum(), data_denom.GetMaximum())*1.5)

    stack = plotter.build_stack(
        '/em/final/Ntuple:num_' + label,
        include = ['*'],
        exclude = ['*data*'],
        title = 'Mu-E mass',
        show_overflows = True,
        rebin = rebin,
    )

    data = plotter.get_histogram(
        'data_SingleMu',
        '/em/final/Ntuple:num_' + label,
        show_overflows = True,
        rebin = rebin,
    )

    canvas.cd(2)
    stack.Draw()
    stack.GetXaxis().SetTitle('Mu-E mass')
    data.Draw("pe, same")
    #legend.Draw()
    stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

    saveplot('versus_pt_%s' % label)

    binning = [5, 10, 15, 20, 25, 30, 100]

    #data_num = list(get_yields(plotter, '/em/final/Ntuple:num_' + label,
                               #['data_SingleMu'], binning))
    #data_denom = list(get_yields(plotter, '/em/final/Ntuple:denom_' + label,
                                 #['data_SingleMu'], binning))

    #mc_samples = ['Zjets', 'Wjets', 'QCDMu', 'ttjets']
    #mc_num = list(get_yields(plotter, '/em/final/Ntuple:num_' + label,
                             #mc_samples, binning))
    #mc_denom = list(get_yields(plotter, '/em/final/Ntuple:denom_' + label,
                               #mc_samples, binning))


    data_num = plotter.get_histogram(
        'data_SingleMu', '/em/final/Ntuple:num_' + label,
        show_overflows = True).cloneAndRebin(binning)
    data_denom = plotter.get_histogram(
        'data_SingleMu', '/em/final/Ntuple:denom_' + label,
        show_overflows = True).cloneAndRebin(binning)

    mc_num = plotter.get_histogram(
        'Zjets', '/em/final/Ntuple:num_' + label,
        show_overflows = True).cloneAndRebin(binning)
    mc_denom = plotter.get_histogram(
        'Zjets', '/em/final/Ntuple:denom_' + label,
        show_overflows = True).cloneAndRebin(binning)

    data_eff = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
    mc_eff = ROOT.TGraphAsymmErrors(mc_num.th1, mc_denom.th1)
    canvas.cd(1)

    data_fit_func = ROOT.TF1(
        "data_fit_func", "[0]*0.5*(1 + TMath::Erf([2]*(x - [1])))", 2)
    data_fit_func.SetParameter(0, 0.95)
    data_fit_func.SetParLimits(0, 0, 1)
    data_fit_func.SetParameter(1, 5)
    data_fit_func.SetParLimits(1, 0, 15)
    data_fit_func.SetParameter(2, 0.2)
    data_fit_func.SetParLimits(2, 0.0001, 0.5)

    mc_fit_func = ROOT.TF1(
        "mc_fit_func", "[0]*0.5*(1 + TMath::Erf([2]*(x - [1])))", 2)
    mc_fit_func.SetParameter(0, 0.95)
    mc_fit_func.SetParLimits(0, 0, 1)
    mc_fit_func.SetParameter(1, 5)
    mc_fit_func.SetParLimits(1, 0, 15)
    mc_fit_func.SetParameter(2, 1./5)
    mc_fit_func.SetParLimits(2, 0.0001, 0.5)

    data_eff.Fit(data_fit_func)
    data_eff.Draw('ap')
    data_eff.GetHistogram().SetMaximum(1)
    data_eff.GetHistogram().SetMinimum(0.5)

    canvas.cd(2)
    mc_eff.Fit(mc_fit_func)
    mc_eff.Draw('ap')
    mc_eff.GetHistogram().SetMaximum(1)
    mc_eff.GetHistogram().SetMinimum(0.5)
    saveplot('efficiencies_%s' % label)
