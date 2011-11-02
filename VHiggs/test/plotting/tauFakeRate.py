import ROOT
import os
import sys
import glob
import logging
import math
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles

logging.basicConfig(filename='example.log',level=logging.DEBUG)
log = logging.getLogger("plotting")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.WARNING
log.addHandler(h1)

logging.getLogger("AnalysisPlotter").addHandler(h1)

h2 = logging.StreamHandler(sys.stderr)
h2.level = logging.DEBUG
logging.getLogger("ROOTCache").addHandler(h2)

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetStyle("Plain")
#ROOT.gStyle.SetOptFit(11111)

from data import build_data
#samples, plotter = build_data('2011-10-03-v4-WHAnalyze', 'scratch', 1249, skips)
skips =['QCD', 'TauPlusX', '2011B', 'SingleMu', 'inbetween', 'DoubleEl', 'v4']
#samples, plotter = build_data('2011-10-05-v1-WHAnalyze', 'scratch_results', 1249, skips)
skips =['EM', 'MuPt5', 'TauPlusX', '2011B_PromptReco_v1_b', 'SingleMu', 'MuEG', 'DoubleEl', '2011B', 'MuHad']
samples, plotter = build_data('2011-10-25-WHReSkim', 'scratch_results', 2140, skips)

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

def saveplot(filename):
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'tauFakeRate', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'tauFakeRate',
                               filename + '_log' + filetype))

# We only really care about Z+jets in the OS case
os_include = ['Zj*', 'Wp*', 'data*DoubleMu*']

legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = os_include,
    drawopt='lf')

base_dimuon_selection = (
    'Muon1Pt > 15 && Muon2Pt > 9 && Muon1AbsEta < 2.1 && Muon2AbsEta < 2.1'
    ' && Muon1_MuRelIso < 0.3 && Muon2_MuRelIso < 0.3 && '
    ' ( (run < 1.5 && DoubleMu7_HLT > 0.5) ||'
    '   (run > 160430 && run < 165088 && DoubleMu7_HLT > 0.5) || '
    '   (run >= 165088 && Mu13Mu8_HLT) )'
)

ss_dimuon_selection = base_dimuon_selection + '&& Muon1Charge*Muon2Charge > 0'
os_dimuon_selection = base_dimuon_selection + '&& Muon1Charge*Muon2Charge < 0'
os_dimuon_selection_trg = os_dimuon_selection

plotter.register_tree(
    'SelectedDiMuonMass',
    '/mmt/final/Ntuple',
    'Leg1Leg2_Mass',
    os_dimuon_selection,
    w = 'puWeight',
    binning = [120, 60, 120],
    #include = ['Zj*', '*DoubleMu*'],
    include = ['Zj*', 'Wp*'],
)

plotter.register_tree(
    'SelectedDiMuonMass',
    '/mmt/final/Ntuple',
    'Leg1Leg2_Mass',
    os_dimuon_selection_trg,
    w = 'puWeight',
    binning = [120, 60, 120],
    include = ['*DoubleMu*'],
)

stack = plotter.build_stack(
    '/mmt/final/Ntuple:SelectedDiMuonMass',
    include = ['Zj*', 'Wp*'],
    title = "Dimuon mass in OS events 2.1 fb^{-1}",
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:SelectedDiMuonMass')

stack.Draw()
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
stack.GetXaxis().SetTitle("OS Dimuon + jet events 2.1 fb^{-1}")
legend.Draw()
saveplot("dimuon_mass")

zmm_selection = os_dimuon_selection + \
    ' && Leg1Leg2_Mass > 80 && Leg1Leg2_Mass < 100'
zmm_selection_trg = os_dimuon_selection_trg + \
    ' && Leg1Leg2_Mass > 80 && Leg1Leg2_Mass < 100'

plotter.register_tree(
    'ZmumuTauJetPt',
    '/mmt/final/Ntuple',
    'TauJetPt',
    zmm_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*'],
)

plotter.register_tree(
    'ZmumuTauJetPt',
    '/mmt/final/Ntuple',
    'TauJetPt',
    zmm_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*DoubleMu*'],
)


zmm_passesHPS_selection = zmm_selection + ' && Tau_LooseHPS'
zmm_passesHPS_selection_trg = zmm_selection_trg + ' && Tau_LooseHPS'

plotter.register_tree(
    'ZmumuTauJetPtHPSLoose',
    '/mmt/final/Ntuple',
    'TauJetPt',
    zmm_passesHPS_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*',],
)

plotter.register_tree(
    'ZmumuTauJetPtHPSLoose',
    '/mmt/final/Ntuple',
    'TauJetPt',
    zmm_passesHPS_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*DoubleMu*'],
)
