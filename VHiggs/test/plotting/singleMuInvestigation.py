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

skips =['EM', 'MuPt5', 'TauPlusX', 'W', '2011B_PromptReco_v1_b',
        'DoubleMu', 'MuEG', 'DoubleEl', '2011B', 'MuHad', 'VH', 'TT', 'ZZ',
        'Zbb', 'Zcc'
       ]

samples, plotter = build_data('2011-10-17-v5-MuonTP', 'scratch_results', 2140,
                              skips, count='mm/skimCounter')

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

def saveplot(filename):
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'singleMuZ', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'singleMuZ',
                               filename + '_log' + filetype))


legend = plotter.build_legend(
    '/mm/Muon2_Pt/Muon2_Pt',
    include = ['*'],
    drawopt='lf')


base_dimuon_selection = (
    'Muon1Pt > 15 && Muon2Pt > 9 && Muon1AbsEta < 2.1 && Muon2AbsEta < 2.1'
    ' && Muon1_MuRelIso < 0.3 && Muon2_MuRelIso < 0.3'
)

ss_dimuon_selection = base_dimuon_selection + '&& Muon1Charge*Muon2Charge > 0'
os_dimuon_selection = base_dimuon_selection + '&& Muon1Charge*Muon2Charge < 0'
os_dimuon_selection_trg = os_dimuon_selection

plotter.register_tree(
    'SelectedDiMuonMass',
    '/mm/final/Ntuple',
    'finalStateVisP4Mass',
    os_dimuon_selection,
    w = 'puWeight',
    binning = [120, 60, 120],
    #include = ['Zj*', '*DoubleMu*'],
    include = ['*'],
)

stack = plotter.build_stack(
    '/mm/final/Ntuple:SelectedDiMuonMass',
    include = ['Zj*', 'Wp*'],
    title = "Dimuon mass in OS events 2.1 fb^{-1}",
)

data = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:SelectedDiMuonMass')

stack.Draw()
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
stack.GetXaxis().SetTitle("OS Dimuon + jet events 2.1 fb^{-1}")
legend.Draw()
saveplot("dimuon_mass")

count_z = plotter.get_histogram(
    'Zjets', '/mm/skimCounter'
)

count_data = plotter.get_histogram(
    'data_SingleMu', '/mm/skimCounter'
)

print "Zjets skim count:", count_z.Integral()
print "data skim count:", count_data.Integral()

