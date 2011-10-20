import logging
import sys
import os
import glob

import ROOT
from FinalStateAnalysis.TagAndProbe.TNPFitter import TNPFitter

tnplog = logging.getLogger("TNPFitter")
tnplog.setLevel(logging.INFO)
h1 = logging.StreamHandler(sys.stderr)
h1.level = logging.INFO
tnplog.addHandler(h1)
print tnplog

canvas = ROOT.TCanvas("basdf", "aasdf", 1200, 600)
canvas.Divide(2)

mc_chain = ROOT.TChain("mm/final/Ntuple")
data_chain = ROOT.TChain("mm/final/Ntuple")

mc_path = os.path.join(
    os.environ['scratch_results'],
    '2011-10-17-v5-MuonTP-Zjets_M50-analyzeFinalStates', '*', '*.root')

data_path = os.path.join(
    os.environ['scratch_results'],
    '2011-10-17-v5-MuonTP-data_SingleMu_Run2011A_*', '*', '*.root')

for ifile, file in enumerate(glob.glob(mc_path)):
    if ifile > 20:
        break
    mc_chain.Add(file)

for ifile, file in enumerate(glob.glob(data_path)):
    data_chain.Add(file)

# Define variables
vars = [
    ROOT.RooRealVar("finalStateVisP4Mass", "M_{#mu#mu}", 70, 110, "GeV/c^{2}"),
    ROOT.RooRealVar("Muon2_hltSingleMuIsoL3IsoFiltered24", "Iso Mu 24", -2, 2),
    ROOT.RooRealVar("Muon2_hltDiMuonL3p5PreFiltered8", "Mu 8", -2, 2),
    ROOT.RooRealVar("Muon2_hltSingleMu13L3Filtered13", "Mu 8", -2, 2),
    ROOT.RooRealVar("Muon2_hltDiMuonL3PreFiltered7", "DoubleMu7", -2, 2),
    ROOT.RooRealVar("Muon2Pt", "Muon p_{T}", 0, 100, "GeV/c"),
    ROOT.RooRealVar("Muon2_MuRelIso", "Muon Rel. Iso.", 0, 10),
    ROOT.RooRealVar("Muon2_MuID_WWID", "Muon WW ID", -2, 2),
    ROOT.RooRealVar("Muon2GenPdgId", "Muon MC Match", -5, 20),
    ROOT.RooRealVar("puWeight", "PU Weight", 0, 5),
]
# We fit the dimuon mass
fit_var = vars[0]
pu_var = vars[-1]

mc_fitter = TNPFitter(mc_chain, vars)
data_fitter = TNPFitter(data_chain, vars)

# Define our shapes
pdf_config = [
    "Voigtian::signalPass(finalStateVisP4Mass, mean[90,80,100], width[2.495], sigma[3,0.01,20])",
    "Voigtian::signalFail(finalStateVisP4Mass, mean, width, sigma)",
    "Exponential::backgroundPass(finalStateVisP4Mass, lp[0,-5,5])",
    "Exponential::backgroundFail(finalStateVisP4Mass, lf[0,-5,5])",
]

# What we measure the triggers against
base_probe_selections = ['Muon2_MuRelIso < 0.3', 'Muon2_MuID_WWID > 0.5' ]
mc_probe_selections = [ 'Muon2GenPdgId > 12' ]

################################################################################
###  DATA-MC correction factor for DoubleMu7   #################################
################################################################################

#ws, result = fitter.fit(
    #fit_var,
    #base_probe_selections,
    #['Muon2_hltSingleMuIsoL3IsoFiltered24 > 0.5'],
    #['Muon2_hltSingleMuIsoL3IsoFiltered24 > -0.5', 'Muon2_hltSingleMuIsoL3IsoFiltered24 < 0.5'],
    #pdf_config,
#)

hlt_DoubleMu7_pass = ['Muon2_hltDiMuonL3PreFiltered7 > 0.5']
hlt_DoubleMu7_fail = ['Muon2_hltDiMuonL3PreFiltered7 > -0.5',
                      'Muon2_hltDiMuonL3PreFiltered7 < 0.5']

pt_bins = range(3, 30, 2)
data_trend = data_fitter.fit_trend(
    'Muon2Pt',
    pt_bins,
    fit_var,
    base_probe_selections,
    hlt_DoubleMu7_pass,
    hlt_DoubleMu7_fail,
    pdf_config,
)

pt_bins = range(3, 30, 1)
mc_trend = mc_fitter.mc_trend(
    'Muon2Pt',
    pt_bins,
    fit_var,
    ROOT.RooArgList(pu_var),
    mc_probe_selections,
    base_probe_selections,
    hlt_DoubleMu7_pass,
    hlt_DoubleMu7_fail,
)

canvas.cd(1)
data_graph = data_fitter.make_trend_graph(data_trend)
data_graph.Draw("ape")
data_turnon = data_fitter.fit_trend_graph(data_graph)
data_turnon.Draw('same')
canvas.SaveAs("doubleMu7_data.png")

canvas.cd(2)
mc_graph = mc_fitter.make_trend_graph(mc_trend)
mc_graph.Draw("ape")
mc_turnon = mc_fitter.fit_trend_graph(mc_graph)
mc_turnon.Draw('same')
canvas.SaveAs("doubleMu7_mc.png")

hlt_Mu13_pass = ['Muon2_hltSingleMu13L3Filtered13 > 0.5']
hlt_Mu13_fail = ['Muon2_hltSingleMu13L3Filtered13 > -0.5',
                      'Muon2_hltSingleMu13L3Filtered13 < 0.5']

pt_bins = range(3, 30, 2)
data_trend = data_fitter.fit_trend(
    'Muon2Pt',
    pt_bins,
    fit_var,
    base_probe_selections,
    hlt_Mu13_pass,
    hlt_Mu13_fail,
    pdf_config,
)
data_graph = data_fitter.make_trend_graph(data_trend)
data_graph.Draw("ape")
data_turnon = data_fitter.fit_trend_graph(data_graph)
data_turnon.Draw('same')
canvas.SaveAs("hltMu13.png")

#frame_pass = vars[0].frame()
#frame_fail = vars[0].frame()
#fail_data.plotOn(frame_fail)
#pdf_fail.plotOn(frame_fail)
#pdf_fail.plotOn(frame_fail, ROOT.RooFit.Components('backgroundFail'))

#pass_data.plotOn(frame_pass)
#pdf_pass.plotOn(frame_pass)
#pdf_pass.plotOn(frame_pass, ROOT.RooFit.Components('backgroundPass'))

#canvas.cd(1)
#frame_pass.Draw()
#canvas.cd(2)
#frame_fail.Draw()

#print result.floatParsFinal().find('efficiency')
