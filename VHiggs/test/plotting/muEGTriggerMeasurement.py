'''

Code to measure the MuEG trigger efficiency

'''

import copy
import logging
import os
import re
import sys

import ROOT
import FinalStateAnalysis.PatTools.data as data_tool

# Logging options
logging.basicConfig(filename='muEGTriggerMeasurement.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("muEG")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)

ROOT.gROOT.SetBatch(True)

# Select Z->mu+e events
selections = [
    'ElectronCharge*Muon2Charge < 0',
    'Electron_EBtag < 3.3',
    'Muon2DZ < 0.2',
    'ElectronDZ < 0.2',
    'Electron_MissingHits < 0.5',
    'Electron_hasConversion < 0.5',
    'Electron_EID_MITID > 0.5',
    'Electron_ERelIso < 0.3',

    'Muon2Pt > 25',
    'Muon2AbsEta < 2.1',
    'Muon2_MtToMET < 40',
    'Muon2_MuID_WWID > 0.5',
    'Muon2_MuRelIso < 0.1',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'IsoMus_HLT > 0.5',
]

samples, plotter = data_tool.build_data(
    'Mu', '2011-12-10-v1-MuonTP', 'scratch_results',
    4684, ['MuEG', 'DoubleMu', 'EM'], count='em/skimCounter')

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
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

plotter.register_tree(
    'all',
    '/em/final/Ntuple',
    'ElectronPt',
    ' && '.join(selections),
    w = 'pu2011AB',
    binning = [100, 0, 100],
    include = ['*'],
    #exclude = fr_info['exclude'],
)

stack = plotter.build_stack(
    '/em/final/Ntuple:all',
    include = ['*'],
    exclude = ['*data*'],
    title = 'Mu-E mass',
    show_overflows = True,
    rebin = 2,
)

data = plotter.get_histogram(
    'data_SingleMu',
    '/em/final/Ntuple:all',
    show_overflows = True,
    rebin = 2,
)

stack.Draw()
stack.GetXaxis().SetTitle('Mu-E mass')
data.Draw("pe, same")
#legend.Draw()
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

saveplot('all_denominator')

plotter.register_tree(
    'passed',
    '/em/final/Ntuple',
    'ElectronPt',
    ' && '.join(selections + ['Mu17Ele8All_HLT > 0.5']),
    w = 'pu2011AB',
    binning = [100, 0, 100],
    include = ['*'],
    #exclude = fr_info['exclude'],
)

stack = plotter.build_stack(
    '/em/final/Ntuple:passed',
    include = ['*'],
    exclude = ['*data*'],
    title = 'Mu-E mass',
    show_overflows = True,
    rebin = 2,
)

data = plotter.get_histogram(
    'data_SingleMu',
    '/em/final/Ntuple:passed',
    show_overflows = True,
    rebin = 2,
)

stack.Draw()
stack.GetXaxis().SetTitle('Mu-E mass')
data.Draw("pe, same")
#legend.Draw()
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

saveplot('all_numerator')
