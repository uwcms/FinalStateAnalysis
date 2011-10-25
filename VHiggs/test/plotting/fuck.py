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
    canvas.Print(os.path.join("plots", "fuck", filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", "fuck",
                               filename + '_log' + filetype))


legend = plotter.build_legend(
    '/mm/Muon2_Pt/Muon2_Pt',
    include = ['*'],
    drawopt='lf')


base_dimuon_selection = (
    'Muon1Pt > 15 && Muon2Pt > 9 && Muon1AbsEta < 2.1 && Muon2AbsEta < 2.1'
    ' && Muon1_MuRelIso > 0.3'
)

ss_dimuon_selection = base_dimuon_selection + '&& Muon1Charge*Muon2Charge > 0'
ss_dimuon_selection_iso = ss_dimuon_selection + ' && Muon2_MuRelIso < 0.3'

plotter.register_tree(
    'Muon2PtNoIso',
    '/mm/final/Ntuple',
    'Muon2Pt',
    ss_dimuon_selection,
    w = 'puWeight',
    binning = [25, 00, 250],
    #include = ['Zj*', '*DoubleMu*'],
    include = ['*'],
)

stack = plotter.build_stack(
    '/mm/final/Ntuple:Muon2PtNoIso',
    include = ['Zj*', 'Wp*'],
    title = "Muon p_{T} in tag anti-iso SS events 2.1 fb^{-1}",
)

data = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Muon2PtNoIso')

stack.Draw()
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
stack.GetXaxis().SetTitle("Muon p_{T}")
legend.Draw()
saveplot("muon2Pt")

plotter.register_tree(
    'Muon2PtIso',
    '/mm/final/Ntuple',
    'Muon2Pt',
    ss_dimuon_selection_iso,
    w = 'puWeight',
    binning = [25, 00, 250],
    #include = ['Zj*', '*DoubleMu*'],
    include = ['*'],
)

stack = plotter.build_stack(
    '/mm/final/Ntuple:Muon2PtIso',
    include = ['Zj*', 'Wp*'],
    title = "Muon p_{T} in tag anti-iso SS events 2.1 fb^{-1}",
)

data = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Muon2PtIso')

stack.Draw()
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
stack.GetXaxis().SetTitle("Muon p_{T}")
legend.Draw()
saveplot("muon2PtIso")

numerator = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Muon2PtIso')

denominator = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Muon2PtNoIso')

jet_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
jetpt_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 250)
jetpt_fit_func.SetParameter(0, 0.02)
jetpt_fit_func.SetParameter(1, 1.87)
jetpt_fit_func.SetParameter(2, -9.62806e-02)
jetpt_fit_func.SetLineColor(ROOT.EColor.kRed)

fit_result = jet_fake_rate.Fit(jetpt_fit_func)
jet_fake_rate.Draw("ape")
saveplot("muon_fr")

plotter.register_tree(
    'Jet2PtNoIso',
    '/mm/final/Ntuple',
    'Muon2Pt + Muon2Pt*Muon2_MuRelIso',
    ss_dimuon_selection,
    w = 'puWeight',
    binning = [25, 00, 250],
    #include = ['Zj*', '*DoubleMu*'],
    include = ['*'],
)

stack = plotter.build_stack(
    '/mm/final/Ntuple:Jet2PtNoIso',
    include = ['Zj*', 'Wp*'],
    title = "Jet p_{T} in tag anti-iso SS events 2.1 fb^{-1}",
)

data = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Jet2PtNoIso')

stack.Draw()
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
stack.GetXaxis().SetTitle("Muon p_{T}")
legend.Draw()
saveplot("muon2Pt")

plotter.register_tree(
    'Jet2PtIso',
    '/mm/final/Ntuple',
    'Muon2Pt + Muon2Pt*Muon2_MuRelIso',
    ss_dimuon_selection_iso,
    w = 'puWeight',
    binning = [25, 00, 250],
    #include = ['Zj*', '*DoubleMu*'],
    include = ['*'],
)

stack = plotter.build_stack(
    '/mm/final/Ntuple:Jet2PtIso',
    include = ['Zj*', 'Wp*'],
    title = "Jet p_{T} in tag anti-iso SS events 2.1 fb^{-1}",
)

data = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Jet2PtIso')

stack.Draw()
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
stack.GetXaxis().SetTitle("Muon p_{T}")
legend.Draw()
saveplot("muon2PtIso")

numerator = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Jet2PtIso')

denominator = plotter.get_histogram(
    'data_SingleMu', '/mm/final/Ntuple:Jet2PtNoIso')

jet_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
jetpt_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 250)
jetpt_fit_func.SetParameter(0, 0.02)
jetpt_fit_func.SetParameter(1, 1.87)
jetpt_fit_func.SetParameter(2, -9.62806e-02)
jetpt_fit_func.SetLineColor(ROOT.EColor.kRed)

fit_result = jet_fake_rate.Fit(jetpt_fit_func)
jet_fake_rate.Draw("ape")
saveplot("jet_fr")

print jetpt_fit_func.GetParameter(0)
print jetpt_fit_func.GetParameter(1)
print jetpt_fit_func.GetParameter(2)
