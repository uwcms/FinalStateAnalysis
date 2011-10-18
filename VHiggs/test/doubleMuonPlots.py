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
samples, plotter = build_data('2011-10-17-v2-WHAnalyze', 'scratch_results', 2140, skips)

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

def saveplot(filename):
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'doubleMu', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'doubleMu',
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

# Using only the tau pt
plotter.register_tree(
    'ZmumuTauPt',
    '/mmt/final/Ntuple',
    'TauPt',
    zmm_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*', '*DoubleMu*'],
)

plotter.register_tree(
    'ZmumuTauPtHPSLoose',
    '/mmt/final/Ntuple',
    'TauPt',
    zmm_passesHPS_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['Zj*', '*DoubleMu*'],
)

#print plotter.computed_hists
stack = plotter.build_stack(
    '/mmt/final/Ntuple:ZmumuTauJetPt',
    include = ['Zj*',],title = 'Tau Jet p_{T} in Z#mu#mu events',
    rebin = 2, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZmumuTauJetPt',
    rebin = 2, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Tau Jet p_{T}")
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
legend.Draw()
saveplot("tauJetPt")

#print plotter.computed_hists
stack = plotter.build_stack(
    '/mmt/final/Ntuple:ZmumuTauJetPtHPSLoose',
    include = ['Zj*',], title = 'Tau Jet p_{T} in Z#mu#mu events (ID passed)',
    rebin = 2, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZmumuTauJetPtHPSLoose',
    rebin = 2, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Tau Jet p_{T}")
data.Draw("pe,same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
legend.Draw()
saveplot("tauJetPtHPSLoose")

numerator = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZmumuTauJetPtHPSLoose',)

denominator = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZmumuTauJetPt',)

tau_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
jetpt_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
jetpt_fit_func.SetParameter(0, 0.02)
jetpt_fit_func.SetParameter(1, 1.87)
jetpt_fit_func.SetParameter(2, -9.62806e-02)
jetpt_fit_func.SetLineColor(ROOT.EColor.kRed)

fit_result = tau_fake_rate.Fit(jetpt_fit_func)
jetPtFR = "(%f + %f*exp(%f*TauJetPt))" % (jetpt_fit_func.GetParameter(0),
                                              jetpt_fit_func.GetParameter(1),
                                              jetpt_fit_func.GetParameter(2))
jetPtWeight= "((%s)/(1-%s))" % (jetPtFR, jetPtFR)

tau_fake_rate.Draw("ape")
tau_fake_rate.GetHistogram().SetTitle("Tau Iso. Fake Rate vs. Jet p_{T}")
tau_fake_rate.GetHistogram().GetXaxis().SetTitle("Tau Jet p_{T}")
saveplot("tauFakeRateJetPt")

numerator = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZmumuTauPtHPSLoose',)

denominator = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZmumuTauPt',)

tau_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
#fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
fit_func = jetpt_fit_func.Clone()
fit_result = tau_fake_rate.Fit(fit_func)
tauPtFR = "(%f + %f*exp(%f*TauPt))" % (fit_func.GetParameter(0),
                                           fit_func.GetParameter(1),
                                           fit_func.GetParameter(2))
tauPtWeight= "((%s)/(1-%s))" % (tauPtFR, tauPtFR)

tau_fake_rate.Draw("ape")
tau_fake_rate.GetHistogram().SetTitle("Tau Iso. Fake Rate vs. p_{T}")
tau_fake_rate.GetHistogram().GetXaxis().SetTitle("Tau p_{T}")
print fit_result
saveplot("tauFakeRatePt")

###############################################################################
#### QCD validation plots #####################################################
###############################################################################


qcd_selection = (
    'Muon1Pt > 15 && Muon2Pt > 9 && Muon1AbsEta < 2.1 && Muon2AbsEta < 2.1'
    ' && Muon1_MuRelIso > 0.3 && Muon2_MuRelIso > 0.3'
    ' && Muon1Charge*Muon2Charge > 0'
    ' && ( (run < 1.5 && DoubleMu7_HLT > 0.5) ||'
    '   (run > 160430 && run < 165088 && DoubleMu7_HLT > 0.5) || '
    '   (run >= 165088 && Mu13Mu8_HLT) )'
)

qcd_selection_trg = qcd_selection
qcd_selection_hpsloose = qcd_selection + ' && Tau_LooseHPS > 0.5'
qcd_selection_hpsloose_trg = qcd_selection_trg + ' && Tau_LooseHPS > 0.5'

plotter.register_tree(
    'QCDTauJetPtHPSLoose',
    '/mmt/final/Ntuple',
    'TauJetPt',
    qcd_selection_hpsloose,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*',],
    exclude = ['*data*'],
)

# Now w/ trigger
plotter.register_tree(
    'QCDTauJetPtHPSLoose',
    '/mmt/final/Ntuple',
    'TauJetPt',
    qcd_selection_hpsloose_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*data*',],
)

plotter.register_tree(
    'QCDTauJetPt',
    '/mmt/final/Ntuple',
    'TauJetPt',
    qcd_selection,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*',],
    exclude = ['*data*'],
)
# Now w/ trigger
plotter.register_tree(
    'QCDTauJetPt',
    '/mmt/final/Ntuple',
    'TauJetPt',
    qcd_selection_trg,
    w = 'puWeight',
    binning = [100, 0, 200],
    include = ['*data*',],
)

stack = plotter.build_stack(
    '/mmt/final/Ntuple:QCDTauJetPt',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Tau jet p_{T} in SS QCD dimuon events 2.1 fb^{-1}',
    rebin = 5, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:QCDTauJetPt',
    rebin = 5, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Tau Jet p_{T}")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = ['*'],
    exclude = ['data*', '*VH*', 'WW', 'WZ', 'ZZ']
)
sm_legend.Draw()

saveplot("qcd_tauJetPt")

numerator = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:QCDTauJetPtHPSLoose',
    rebin = 5, show_overflows=True,
)

denominator = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:QCDTauJetPt',
    rebin = 5, show_overflows=True,
)

qcd_fake_rate = ROOT.TGraphAsymmErrors(numerator.th1, denominator.th1)
qcd_fake_rate.Draw("ape")
qcd_fake_rate.GetHistogram().GetXaxis().SetTitle("Tau Jet p_{T}")
qcd_fake_rate.GetHistogram().SetTitle("Tau iso. fake rate in QCD SS dimuon events")
jetpt_fit_func.SetLineColor(ROOT.EColor.kRed)
jetpt_fit_func.Draw("same")
saveplot("qcd_tauJetPt_fakerate")

###############################################################################
#### QCD control plots   ######################################################
###############################################################################

plotter.register_tree(
    'QCDNBjets',
    '/mmt/final/Ntuple',
    'NBjetsPt20_Nbjets',
    qcd_selection,
    w = 'puWeight',
    binning = [10, -0.5, 9.5],
    include = ['*',],
)

stack = plotter.build_stack(
    '/mmt/final/Ntuple:QCDNBjets',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Num. b-jets in QCD events',
    rebin = 1, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:QCDNBjets',
    rebin = 1, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("N bjets")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend.Draw()

saveplot("qcd_nBjets")

###############################################################################
#### Debug discrepancy plots
###############################################################################

# Same as Z selection, but no iso requirement on second leg
loose_Z_selection = (
    'Muon1Pt > 15 && Muon2Pt > 9 && Muon1AbsEta < 2.1 && Muon2AbsEta < 2.1'
    ' && Muon1_MuRelIso < 0.3 && '
    ' ( (run < 1.5 && DoubleMu7_HLT > 0.5) ||'
    '   (run > 160430 && run < 165088 && DoubleMu7_HLT > 0.5) || '
    '   (run >= 165088 && Mu13Mu8_HLT) )'
    ' && Leg1Leg2_Mass < 100 && Leg1Leg2_Mass > 80'
    ' && Muon1Charge*Muon2Charge < 0'
)

plotter.register_tree(
    'ZLeg2Iso',
    '/mmt/final/Ntuple',
    'Muon2_MuRelIso',
    loose_Z_selection,
    w = 'puWeight',
    binning = [100, 0, 0.5],
    include = ['*',],
)

stack = plotter.build_stack(
    '/mmt/final/Ntuple:ZLeg2Iso',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Rel. Iso. for subleading muon',
    rebin = 1, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:ZLeg2Iso',
    rebin = 1, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Rel. Iso.")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend.Draw()

saveplot("looseZ_relIso")

plotter.register_tree(
    'LooseZMass',
    '/mmt/final/Ntuple',
    'Leg1Leg2_Mass',
    loose_Z_selection,
    w = 'puWeight',
    binning = [120, 60, 120],
    include = ['*',],
)

stack = plotter.build_stack(
    '/mmt/final/Ntuple:LooseZMass',
    include = ['*',],
    exclude = ['*data*'],
    title = 'Mass',
    rebin = 1, show_overflows=True,
)

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:LooseZMass',
    rebin = 1, show_overflows=True,
)

stack.Draw()
stack.GetXaxis().SetTitle("Rel. Iso.")
data.Draw("pe, same")
stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)

sm_legend.Draw()

saveplot("looseZ_mass")

###############################################################################
#### Signal region plots ######################################################
###############################################################################

mc_legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = ['*'],
    exclude = ['data*', 'VH*']
)

for var, label, title, binning in [
    ('Leg1Leg2_Mass', 'DiMuonMass', 'M_{#mu#mu}', [100, 0, 200],),
    ('Leg2Leg3_Mass', 'MuTauMass', 'M_{#mu#tau}', [100, 0, 200],),
    ('Leg1_MtToMET', 'Leg1MtToMET', 'M_{T} #mu(1)-#tau', [100, 0, 200],),
    ('Leg2_MtToMET', 'Leg2MtToMET', 'M_{T} #mu(2)-#tau', [100, 0, 200],),
    ('TMath::Prob(vtxChi2,vtxNDOF)', 'vtxChi2Prob', 'Vertex #chi^{2} Prob', [1000, 0, 1.0],),
    ('vtxChi2/vtxNDOF', 'vtxChi2NODF', 'Vertex #chi^{2}/NODF', [100, 0, 30],),
    ('METPt', 'MET', 'MET', [100, 0, 200]),
    ('FinalState_Ht', 'HT', 'H_{T}', [100, 0, 200]),
    #('NBjetsPt20_Nbjets', 'Nbjets', 'N_{bjets}', [10, -0.5, 9.5]),
    #('NIsoMuonsPt5_Nmuons', 'NisoMuons', 'N_{mu}', [10, -0.5, 9.5])
]:
    plotter.register_tree(
        'SS%s' % label,
        '/mmt/final/Ntuple',
        var,
        ss_dimuon_selection,
        w = 'puWeight',
        binning = binning,
        include = ['Zj*', '*DoubleMu*', '*'],
    )

    stack = plotter.build_stack(
        '/mmt/final/Ntuple:SS%s' % label,
        include = ['*'],
        exclude = ['data*'],
        rebin = 5, show_overflows=True,
        title = 'SS Dimuon + jet events',
    )

    data = plotter.get_histogram(
        'data_DoubleMu', '/mmt/final/Ntuple:SS%s' % label,
        rebin = 5, show_overflows=True,
    )

    stack.Draw()
    data.Draw("pe,same")
    stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
    mc_legend.Draw()
    saveplot("ss_%s" % label)


    ss_fr_signal_selection = (
        ss_dimuon_selection
        #+ ' && NBjetsPt20_Nbjets < 1' \
        #+ ' && NIsoMuonsPt5_Nmuons < 1' \
        + ' && FinalState_Ht > 80'
    )

    plotter.register_tree(
        'SS%sWVetos' % label,
        '/mmt/final/Ntuple',
        var,
        ss_fr_signal_selection,
        w = 'puWeight',
        binning = binning,
        include = ['Zj*', '*DoubleMu*', '*'],
    )

    stack = plotter.build_stack(
        '/mmt/final/Ntuple:SS%sWVetos' % label,
        include = ['*'],
        exclude = ['data*'],
        rebin = 5, show_overflows=True,
        title = 'SS Dimoun + jet events 2.1 fb^{-1}',
    )

    data_wvetos = plotter.get_histogram(
        'data_DoubleMu', '/mmt/final/Ntuple:SS%sWVetos' % label,
        rebin = 5, show_overflows=True,
    )

    stack.Draw()
    stack.GetXaxis().SetTitle(title)
    data_wvetos.Draw("pe,same")
    stack.SetMaximum(max(stack.GetMaximum(), data_wvetos.GetMaximum())*1.1)
    mc_legend.Draw()
    saveplot("ss_%s_wvetos" % label)

    ss_signal_selection = ss_fr_signal_selection + ' && Tau_LooseHPS > 0.5'

    plotter.register_tree(
        'SS%sFinal' % label,
        '/mmt/final/Ntuple',
        var,
        ss_signal_selection,
        w = 'puWeight',
        binning = binning,
        include = ['Zj*', '*DoubleMu*', '*'],
    )

    stack = plotter.build_stack(
        '/mmt/final/Ntuple:SS%sFinal' % label,
        include = ['*'],
        exclude = ['data*'],
        rebin = 10, show_overflows=True,
        title = "Final #mu#mu#tau events 2.1 fb^{-1}",
    )

    data = plotter.get_histogram(
        'data_DoubleMu', '/mmt/final/Ntuple:SS%sFinal' % label,
        rebin = 10, show_overflows=True,
    )

    stack.Draw()
    stack.GetXaxis().SetTitle(title)
    data.Draw("pe,same")
    stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.1)
    mc_legend.Draw()
    saveplot("ss_%s_final" %label)

    ss_fr_signal_selection_weighted = "(%s && Tau_LooseHPS < 0.5)*(%s)" % (
        ss_fr_signal_selection, jetPtWeight)

    plotter.register_tree(
        'SS%sWeighted' % label,
        '/mmt/final/Ntuple',
        var,
        ss_fr_signal_selection_weighted,
        w = 'puWeight',
        binning = binning,
        include = ['*DoubleMu*', 'WZ', 'ZZ'],
    )

    print "about to get"

    data = plotter.get_histogram(
        'data_DoubleMu', '/mmt/final/Ntuple:SS%sFinal' % label,
        rebin = 10, show_overflows=True,
    )

    data_fr = plotter.get_histogram(
        'data_DoubleMu', '/mmt/final/Ntuple:SS%sWeighted' % label,
        rebin = 10, show_overflows=True,
    )
    print "correcting"
    # These two contribute to the fake rate, so we need to correct for them
    wz_final = plotter.get_histogram(
        'WZ', '/mmt/final/Ntuple:SS%sFinal' % label,
        rebin = 10, show_overflows=True,
    )
    wz_fr = plotter.get_histogram(
        'WZ', '/mmt/final/Ntuple:SS%sWeighted' % label,
        rebin = 10, show_overflows=True,
    )
    wz_corrected = wz_final - wz_fr

    zz_final = plotter.get_histogram(
        'ZZ', '/mmt/final/Ntuple:SS%sFinal' % label,
        rebin = 10, show_overflows=True,
    )
    zz_fr = plotter.get_histogram(
        'ZZ', '/mmt/final/Ntuple:SS%sWeighted' % label,
        rebin = 10, show_overflows=True,
    )
    zz_corrected = zz_final - zz_fr

    print "correcting"


    stack = ROOT.THStack("FR_predictions", "Final #mu#mu#tau selections 2.1 fb^{-1}")
    stack.Add(zz_corrected.th1, 'hist')
    stack.Add(wz_corrected.th1, 'hist')
    styling.apply_style(data_fr, **samplestyles.SAMPLE_STYLES['ztt'])
    stack.Add(data_fr.th1, 'hist')

    signal = plotter.get_histogram(
        'VH115', '/mmt/final/Ntuple:SS%sFinal' % label,
        rebin = 10, show_overflows=True,
    )
    signal = signal * 5
    #signal.SetFillColor(0)
    signal.SetLineWidth(2)
    stack.Add(signal.th1, 'hist')

    stack.Draw()
    #signal.Draw("same,hist")
    data.Draw('pe,same')
    stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)
    stack.GetXaxis().SetTitle(title)

    legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
    legend.AddEntry(zz_corrected.th1, "ZZ", 'lf')
    legend.AddEntry(wz_corrected.th1, "WZ", 'lf')
    legend.AddEntry(data_fr.th1, "Fakes", 'lf')
    legend.AddEntry(signal.th1, "VH(115) #times 5", 'lf')
    legend.SetFillStyle(0)
    legend.Draw()

    #data_fr.Draw('hist, same')
    saveplot("ss_%s_final_wfr" % label)


    print label
    n_data_for_fr = data_wvetos.Integral() - data.Integral()
    #print "data pre fr", data_wvetos.Integral() - data.Integral()
    print "Data & ", "%0.2f" % data.Integral(), "\pm", "%0.2f" % math.sqrt(data.Integral()), "\\\\"
    print "WZ &", "%0.2f" % wz_corrected.Integral(), "\\\\"
    print "ZZ &", "%0.2f" % zz_corrected.Integral(), "\\\\"
    print "Fakes &", "%0.2f" % data_fr.Integral(), "\pm", \
            "%0.2f" % (math.sqrt(n_data_for_fr)*data_fr.Integral()/n_data_for_fr), "\\\\"
    print "VH(115)", "%0.2f" % (signal.Integral()/5), "\\\\"


    data_for_fr_int = data_wvetos.Integral() - data.Integral()
    data_int = data.Integral()
    wz_int = wz_corrected.Integral()
    zz_int = zz_corrected.Integral()
    bkg_int = data_fr.Integral()
    signal_int = signal.Integral()
    print "tau pt FR:", tauPtFR
    print "jet pt FR:", jetPtFR



##### BUILD DATA CARD

#label = 'vtxChi2NODF'
label = 'MuTauMass'

data = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:SS%sFinal' % label,
    rebin = 10, show_overflows=True,
)

data_wvetos = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:SS%sWVetos' % label,
    rebin = 5, show_overflows=True,
)

data_fr = plotter.get_histogram(
    'data_DoubleMu', '/mmt/final/Ntuple:SS%sWeighted' % label,
    rebin = 10, show_overflows=True,
)
# These two contribute to the fake rate, so we need to correct for them
wz_final = plotter.get_histogram(
    'WZ', '/mmt/final/Ntuple:SS%sFinal' % label,
    rebin = 10, show_overflows=True,
)
wz_fr = plotter.get_histogram(
    'WZ', '/mmt/final/Ntuple:SS%sWeighted' % label,
    rebin = 10, show_overflows=True,
)
wz_corrected = wz_final - wz_fr

zz_final = plotter.get_histogram(
    'ZZ', '/mmt/final/Ntuple:SS%sFinal' % label,
    rebin = 10, show_overflows=True,
)
zz_fr = plotter.get_histogram(
    'ZZ', '/mmt/final/Ntuple:SS%sWeighted' % label,
    rebin = 10, show_overflows=True,
)
zz_corrected = zz_final - zz_fr


print "Writing data card"
output = ROOT.TFile("mmt_shapes.root", 'RECREATE')

for mass in [110, 115, 120, 125]:
    channel_dir = output.mkdir("mmt_%i" % mass)
    channel_dir.cd()
    data.Write("data_obs")
    data_fr.Write("fakes")
    data_wvetos.Write("ext_data_unweighted")
    wz_corrected.Write("wz")
    zz_corrected.Write("zz")

    signal = plotter.get_histogram(
        'VH%s' % mass, '/mmt/final/Ntuple:SS%sFinal' % label,
        rebin = 10, show_overflows=True,
    )
    signal.Write("signal")


