'''

Code to measure the MuEG trigger efficiency

'''

import logging
import json
import os
import sys

import ROOT
import FinalStateAnalysis.PatTools.data as data_tool
import FinalStateAnalysis.Utilities.styling as styling

# Logging options
logging.basicConfig(filename='muEGTriggerMeasurement.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("muEG")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)

# Load the MC-DATA correction functions
log.info("Loading MC-DATA corrections")
ROOT.gROOT.ProcessLine('.L corrections.C++')

ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetHistTopMargin(0.0)

# Select Z->mu+e events
selections = [
    'Muon2Pt > 26',
    #'IsoMus_HLT > 0.5',
    'IsoMus_HLT > 0.5',
    'Muon2_MuRelIso < 0.1',
    'Electron_ERelIso < 0.3',
    'Muon2_MuID_WWID > 0.5',
    'Electron_EID_MITID > 0.5',

    'ElectronCharge*Muon2Charge < 0',
    'Electron_EBtag < 3.3',
    'abs(Muon2DZ) < 0.2',
    'abs(ElectronDZ) < 0.2',

    'Electron_MissingHits < 0.5',
    'Electron_hasConversion < 0.5',

    'Muon2AbsEta < 2.1',
    'Muon2_MtToMET < 40',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
]

samples, plotter = data_tool.build_data(
    'Mu', '2012-04-14-v1-MuonTP', 'scratch_results',
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


correction = '*'.join([
    'pu2011AB',
    'MuIso(Muon2Pt, Muon2AbsEta, run)',
    'MuID(Muon2Pt, Muon2AbsEta, run)',
    'EleIso(ElectronPt, ElectronAbsEta, run)',
    'EleID(ElectronPt, ElectronAbsEta, run)',
])

summary = {}

var = 'ElectronPt'
binning = [100, 0, 100]
rebin = 5

#var = 'IsoMus_HLTGroup'
#binning = [40, -1.5, 18.5],
#rebin = 2

log.info("Beginning selections...")
for eta_bin in eta_bins:
    label, eta_low, eta_high = eta_bin
    log.info("Selecting %s", label)
    eta_selection = ['ElectronAbsEta >= %f' % eta_low,
                     'ElectronAbsEta < %f' % eta_high]
    plotter.register_tree(
        'denom_' + label,
        '/em/final/Ntuple',
        var,
        ' && '.join(selections + eta_selection),
        w = correction,
        binning = binning,
        include = ['*'],
        #exclude = fr_info['exclude'],
    )

    plotter.register_tree(
        'num_' + label,
        '/em/final/Ntuple',
        var,
        ' && '.join(selections + eta_selection + ['Mu17Ele8All_HLT > 0.5']),
        w = correction,
        binning = binning,
        include = ['*'],
        #exclude = fr_info['exclude'],
    )

    log.info("building denom stack")
    stack_denom = plotter.build_stack(
        '/em/final/Ntuple:denom_' + label,
        include = ['*'],
        exclude = ['*data*'],
        title = 'Mu-E mass',
        show_overflows = True,
        rebin = rebin,
    )

    log.info("getting data histogram")
    data_denom = plotter.get_histogram(
        'data_SingleMu',
        '/em/final/Ntuple:denom_' + label,
        show_overflows = True,
        rebin = rebin,
    )

    #canvas.cd(1)
    log.info("drawing stack")
    stack_denom.Draw()
    stack_denom.GetXaxis().SetTitle('Electron p_{T}')
    data_denom.Draw("pe, same")
    #legend.Draw()
    cms_label1 = styling.cms_preliminary(4684)
    maximum = 1.5*stack_denom.GetHistogram().GetMaximum()
    stack_denom.SetMaximum(maximum)
    canvas.Update()

    saveplot('denom_versus_pt_%s' % label)

    log.info("building num stack")
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

    #canvas.cd(2)
    stack.Draw()
    stack.GetXaxis().SetTitle('Electron p_{T}')
    data.Draw("pe, same")
    cms_label2 = styling.cms_preliminary(4684)
    #legend.Draw()
    stack.SetMaximum(maximum)

    mc_legend = plotter.build_legend(
        '/em/skimCounter',
        include = ['*QCD*', '*Wjets*', '*ttjets*', '*Zjets*'],
        drawopt='lf',
        xlow = 0.6, ylow=0.5,)
    mc_legend.Draw()
    canvas.Update()

    saveplot('num_versus_pt_%s' % label)

    rebinning = [5, 10, 15, 20, 25, 30, 100]

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
        show_overflows = True).cloneAndRebin(rebinning)
    data_denom = plotter.get_histogram(
        'data_SingleMu', '/em/final/Ntuple:denom_' + label,
        show_overflows = True).cloneAndRebin(rebinning)

    mc_num = plotter.get_histogram(
        'Zjets', '/em/final/Ntuple:num_' + label,
        show_overflows = True).cloneAndRebin(rebinning)
    mc_denom = plotter.get_histogram(
        'Zjets', '/em/final/Ntuple:denom_' + label,
        show_overflows = True).cloneAndRebin(rebinning)

    data_eff = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
    mc_eff = ROOT.TGraphAsymmErrors(mc_num.th1, mc_denom.th1)
    canvas.cd(1)

    fit_func_str = "[0]*0.5*(1 + TMath::Erf([2]*(x - [1])))"

    data_fit_func = ROOT.TF1("data_fit_func", fit_func_str, 2)
    data_fit_func.SetParameter(0, 0.95)
    data_fit_func.SetParLimits(0, 0, 1)
    data_fit_func.SetParameter(1, 5)
    data_fit_func.SetParLimits(1, 0, 15)
    data_fit_func.SetParameter(2, 0.2)
    data_fit_func.SetParLimits(2, 0.0001, 0.5)

    mc_fit_func = ROOT.TF1("mc_fit_func",fit_func_str, 2)
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

    mc_fitted_func = fit_func_str
    data_fitted_func = fit_func_str

    for ipar in range(3):
        mc_fitted_func = mc_fitted_func.replace(
            '[%i]' % ipar, '%e' % mc_fit_func.GetParameter(ipar))
        data_fitted_func = data_fitted_func.replace(
            '[%i]' % ipar, '%e' % data_fit_func.GetParameter(ipar))

    # Write results to summary json file
    summary[label] = {
        'mc' : mc_fitted_func,
        'data' : data_fitted_func,
    }

with open('mueg_trig_correction_results.json', 'w') as summary_file:
    summary_file.write(json.dumps(summary, indent=2) + '\n')
