import ROOT
import os
import sys
import glob
import logging
import math
from EvanSoft.Utilities.AnalysisPlotter import styling,samplestyles

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
ROOT.gROOT.SetStyle("Plain")
#ROOT.gStyle.SetOptFit(11111)

from data import build_data
skips =['QCD', 'TauPlusX', '2011B', 'SingleMu', 'inbetween', 'DoubleEl', 'v4']
#samples, plotter = build_data('2011-10-03-v4-WHAnalyze', 'scratch', 1249, skips)
samples, plotter = build_data('2011-10-05-v1-WHAnalyze', 'scratch_results', 1249, skips)

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

def saveplot(filename):
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'emm', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'emm',
                               filename + '_log' + filetype))


base_dimuon_selection = \
        'Mu1Pt > 15 && Mu2Pt > 9 && Mu1AbsEta < 2.1 && Mu2AbsEta < 2.1' \
        ' && Mu1_MuRelIso < 0.3 && Mu2_MuRelIso < 0.1 && ElecPt > 10'

ss_dimuon_selection = base_dimuon_selection + '&& Mu1Charge*Mu2Charge > 0'
os_dimuon_selection = base_dimuon_selection + '&& Mu1Charge*Mu2Charge < 0'
os_dimuon_selection_trg = os_dimuon_selection + '&& Mu13Mu8_HLT > 0'
ss_dimuon_selection_trg = ss_dimuon_selection + '&& Mu13Mu8_HLT > 0'

zmm_selection = os_dimuon_selection + \
    ' && Leg1Leg2_Mass > 80 && Leg1Leg2_Mass < 100'
zmm_selection_trg = os_dimuon_selection_trg + \
    ' && Leg1Leg2_Mass > 80 && Leg1Leg2_Mass < 100'
zmm_passesRelIso_selection = zmm_selection + ' && Elec_ERelIso < 0.3'
zmm_passesRelIso_selection_trg = zmm_selection_trg + ' && Elec_ERelIso < 0.3'

plotter.register_tree(
    'ZmumuElecPt',
    '/emm/final/Ntuple',
    'ElecPt',
    zmm_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*'],
)
plotter.register_tree(
    'ZmumuElecPt',
    '/emm/final/Ntuple',
    'ElecPt',
    zmm_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*DoubleMu*'],
)

plotter.register_tree(
    'ZmumuElecPtRelIso',
    '/emm/final/Ntuple',
    'ElecPt',
    zmm_passesRelIso_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*',],
)

plotter.register_tree(
    'ZmumuElecPtRelIso',
    '/emm/final/Ntuple',
    'ElecPt',
    zmm_passesRelIso_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*DoubleMu*'],
)

stack = plotter.build_stack(
    '/emm/final/Ntuple:ZmumuElecPt',
    include = ['Zj*',],title = 'Electron p_{T} in Z#mu#mu events',
)
data = plotter.get_histogram(
    'data_DoubleMu', '/emm/final/Ntuple:ZmumuElecPt')

legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = ['*Zj*', '*DoubleMu*'],
    drawopt='lf')

stack.Draw()
stack.GetXaxis().SetTitle("Electron p_{T}")
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
legend.Draw()
saveplot("zmm_electronPt")

# The above doesn't work

qcd_selection = \
        'Mu1Pt > 15 && Mu2Pt > 9 && Mu1AbsEta < 2.1 && Mu2AbsEta < 2.1' \
        ' && Mu1_MuRelIso > 0.3 && Mu2_MuRelIso > 0.3'

qcd_selection_trg = \
        'Mu1Pt > 15 && Mu2Pt > 9 && Mu1AbsEta < 2.1 && Mu2AbsEta < 2.1' \
        ' && Mu1_MuRelIso > 0.3 && Mu2_MuRelIso > 0.3 && Mu13Mu8_HLT'

qcd_passesRelIso_selection = qcd_selection + ' && Elec_ERelIso < 0.3'
qcd_passesRelIso_selection_trg = qcd_selection_trg + ' && Elec_ERelIso < 0.3'

plotter.register_tree(
    'QCDElecPt',
    '/emm/final/Ntuple',
    'ElecPt',
    qcd_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*'],
)
plotter.register_tree(
    'QCDElecPt',
    '/emm/final/Ntuple',
    'ElecPt',
    qcd_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*DoubleMu*'],
)

plotter.register_tree(
    'QCDElecPtRelIso',
    '/emm/final/Ntuple',
    'ElecPt',
    qcd_passesRelIso_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*',],
)

plotter.register_tree(
    'QCDElecPtRelIso',
    '/emm/final/Ntuple',
    'ElecPt',
    qcd_passesRelIso_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*DoubleMu*'],
)

stack = plotter.build_stack(
    '/emm/final/Ntuple:QCDElecPt',
    include = ['Zj*',],title = 'Electron p_{T} in Z#mu#mu events',
)
data = plotter.get_histogram(
    'data_DoubleMu', '/emm/final/Ntuple:QCDElecPt')

legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = ['*Zj*', '*DoubleMu*'],
    drawopt='lf')

stack.Draw()
stack.GetXaxis().SetTitle("Electron p_{T}")
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
legend.Draw()
saveplot("qcd_electronPt")

numerator = plotter.get_histogram(
    'data_DoubleMu', '/emm/final/Ntuple:QCDElecPtRelIso',
    rebin = 10
)

denominator = plotter.get_histogram(
    'data_DoubleMu', '/emm/final/Ntuple:QCDElecPt',
    rebin = 10
)

e_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
jetpt_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
jetpt_fit_func.SetParameter(0, 0.02)
jetpt_fit_func.SetParameter(1, 1.87)
jetpt_fit_func.SetParameter(2, -9.62806e-02)
fit_result = e_fake_rate.Fit(jetpt_fit_func)
e_fake_rate.Draw("ape")
e_fake_rate.GetHistogram().SetTitle("Electron Iso. Fake Rate vs. electron p_{T}")
e_fake_rate.GetHistogram().GetXaxis().SetTitle("electron p_{T}")
saveplot("eFakeRate")

final_selection = ss_dimuon_selection + ' && Elec_ERelIso < 0.3'
final_selection_trg = ss_dimuon_selection_trg + ' && Elec_ERelIso < 0.3'

for var, label, title in [
    ('Leg1Leg2_Mass', 'EMuonMass', 'M_{e#mu}'),
    ('Leg2Leg3_Mass', 'MuMuMass', 'M_{#mu#mu}'),
    ('Leg1Leg3_Mass', 'EMuon2Mass', 'M_{e#mu}'),
    ('Leg1_MtToMET', 'Leg1MtToMET', 'M_{T} #mu(1)-#tau'),
    ('Leg2_MtToMET', 'Leg2MtToMET', 'M_{T} #mu(2)-#tau'),
    ('FinalState_Ht', 'HT', 'H_{T}'),
    ('NBjetsPt20_Nbjets', 'Nbjets', 'N_{bjets}') ]:

    plotter.register_tree(
        label,
        '/emm/final/Ntuple',
        var,
        final_selection,
        w = 'puWeight',
        binning = [100, 0, 200],
        include = ['*',],
    )

    plotter.register_tree(
        label,
        '/emm/final/Ntuple',
        var,
        final_selection_trg,
        w = 'puWeight',
        binning = [100, 0, 200],
        include = ['*DoubleMu*'],
    )

    stack = plotter.build_stack(
        '/emm/final/Ntuple:' + label,
        include = ['*',], exclude=['*data*'],title = title,
        rebin = 5
    )
    data = plotter.get_histogram(
        'data_DoubleMu', '/emm/final/Ntuple:' + label,
        rebin = 5
    )

    legend = plotter.build_legend(
        '/mmt/final/SS/finalState/Leg1Leg2_Mass',
        include = ['*', '*DoubleMu*'],
        drawopt='lf')

    stack.Draw()
    stack.GetXaxis().SetTitle(title)
    data.Draw("pe,same")
    stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
    stack.SetMinimum(1e-6)
    legend.Draw()
    saveplot("final_" + label)
