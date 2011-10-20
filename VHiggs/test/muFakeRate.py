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
skips =['EM', 'MuPt5', 'TauPlusX', '2011B_PromptReco_v1_b', 'SingleMu', 'MuEG', 'DoubleEl', '2011B', 'MuHad']
#samples, plotter = build_data('2011-10-17-v2-WHAnalyze', 'scratch_results', 2140, skips)
samples, plotter = build_data('2011-10-20-v2-WHAnalyze', 'scratch_results', 2140, skips)

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

def saveplot(filename):
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'muFakeRate', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'muFakeRate',
                               filename + '_log' + filetype))

# We only really care about Z+jets in the OS case
os_include = ['Zj*', 'Wp*', 'data*DoubleMu*', '*WZ*', '*ZZ*']

legend = plotter.build_legend(
    '/mmm/final/SS/finalState/Leg1Leg2_Mass',
    include = os_include,
    drawopt='lf')

base_dimuon_selection = (
    'Muon1Pt > 15 && Muon2Pt > 9 && Muon1AbsEta < 2.1 && Muon2AbsEta < 2.4'
    ' && Muon1_MuRelIso < 0.15 && Muon2_MuRelIso < 0.15 && '
    ' Muon3Pt > 9 && '
    ' Muon1_MuID_WWID > 0.5 && '
    ' Muon2_MuID_WWID > 0.5 && '
    ' NIsoMuonsPt5_Nmuons < 1 && '
    ' NBjetsPt20_Nbjets < 1 && '
    ' Leg3_MtToMET < 40 && '
    ' Leg1Leg2_Mass > 70 && '
    ' Leg1Leg2_Mass < 110 && '
    ' ( (run < 1.5 && DoubleMu7_HLT > 0.5) ||'
    '   (run > 160430 && run < 165088 && DoubleMu7_HLT > 0.5) || '
    '   (run >= 165088 && Mu13Mu8_HLT) )'
)

os_dimuon_selection = base_dimuon_selection + '&& Muon1Charge*Muon2Charge < 0'
os_dimuon_selection_trg = os_dimuon_selection

###############################################################################
#### QCD validation plots #####################################################
###############################################################################

plotter.register_tree(
    'DiMuMass',
    '/mmm/final/Ntuple',
    'Leg1Leg2_Mass',
    os_dimuon_selection,
    w = 'puWeight',
    binning = [120, 70, 110],
    include = ['*',],
)

plotter.register_tree(
    'MuJetPt',
    '/mmm/final/Ntuple',
    'Muon3Pt + Muon3Pt*Muon3_MuRelIso',
    os_dimuon_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*',],
)

plotter.register_tree(
    'MuJetPtIso',
    '/mmm/final/Ntuple',
    'Muon3Pt + Muon3Pt*Muon3_MuRelIso',
    os_dimuon_selection + ' && Muon3_MuRelIso < 0.3 && Muon3_MuID_WWID',
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*',],
)

stack = plotter.build_stack(
    '/mmm/final/Ntuple:MuJetPt',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Muontron jet p_{T} in Z#mu#mu events 2.1 fb^{-1}',
    rebin = 5, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmm/final/Ntuple:MuJetPt',
    rebin = 5, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Mu Jet p_{T}")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = ['*'],
    exclude = ['data*', '*VH*',]
)
sm_legend.Draw()

saveplot("z_eJetPt")

stack = plotter.build_stack(
    '/mmm/final/Ntuple:MuJetPtIso',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Muontron jet p_{T} in Z#mu#mu events 2.1 fb^{-1}',
    rebin = 5, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmm/final/Ntuple:MuJetPtIso',
    rebin = 5, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Mu Jet p_{T}")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend.Draw()

saveplot("z_eJetPtIso")

stack = plotter.build_stack(
    '/mmm/final/Ntuple:DiMuMass',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Dimuon mass in Z#mu#mu events 2.1 fb^{-1}',
    rebin = 5, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmm/final/Ntuple:DiMuMass',
    rebin = 5, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("M_{#mu#mu} (GeV)")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend.Draw()

saveplot("z_MuMuMass")

numerator = plotter.get_histogram(
    'data_DoubleMu', '/mmm/final/Ntuple:MuJetPtIso',
    rebin = 5, show_overflows=True,
)

denominator = plotter.get_histogram(
    'data_DoubleMu', '/mmm/final/Ntuple:MuJetPt',
    rebin = 5, show_overflows=True,
)

qcd_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
qcd_fake_rate.Draw("ape")
qcd_fake_rate.GetHistogram().GetXaxis().SetTitle("Muon Jet p_{T}")
qcd_fake_rate.GetHistogram().SetTitle("Muon. iso. fake rate in Z#mu#mu events")
qcd_fake_rate.GetHistogram().SetMinimum(1e-3)
jetpt_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 250)
jetpt_fit_func.SetParameter(0, 0.0438)
jetpt_fit_func.SetParameter(1, 2.69)
jetpt_fit_func.SetParameter(2, -0.1)
jetpt_fit_func.SetLineColor(ROOT.EColor.kRed)
qcd_fake_rate.Fit(jetpt_fit_func)
jetpt_fit_func.Draw("same")
saveplot("z_muonJetPt_fr")

jetPtFR = "(%f + %f*exp(%f*(Muon3Pt + Muon3Pt*Muon3_MuRelIso)))" % (jetpt_fit_func.GetParameter(0),
                                          jetpt_fit_func.GetParameter(1),
                                          jetpt_fit_func.GetParameter(2))
jetPtWeight= "((%s)/(1-%s))" % (jetPtFR, jetPtFR)

print jetPtFR
print jetPtWeight
