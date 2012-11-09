import FWCore.ParameterSet.Config as cms

'''

Skims for various UW analysis


'''

# So we can get the list of valid paths from the cfg.
skimConfig = cms.PSet(
    paths = cms.vstring()
)

from FinalStateAnalysis.RecoTools.zzSkim_cff import goodVertex,muons4skim,electrons4skim,leptons4skim,dileptons4skim,skim2010,skim40NoOF,skimNoOS,zzSkim 
skimConfig.paths.append("zzSkim")

# Single muon for Wjets
singleMuSelector = cms.EDFilter(
    "MuonSelector",
    src = cms.InputTag('muons'),
    cut = cms.string(
        "(isGlobalMuon) & abs(eta) < 2.4 & pt > 19.0"),
    filter = cms.bool(True)
)
singleMuPath = cms.Path(singleMuSelector)
skimConfig.paths.append("singleMuPath")

singleElecSelector = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag('gsfElectrons'),
    cut = cms.string(
        "abs(eta) < 2.5 & pt > 25.0"),
    filter = cms.bool(True)
)
singleElecPath = cms.Path(singleElecSelector)
skimConfig.paths.append("singleElecPath")

# Mu+Tau for H2Tau
mu14MuSelector = cms.EDFilter(
    "MuonSelector",
    src = cms.InputTag('muons'),
    cut = cms.string(
        "(isGlobalMuon) & abs(eta) < 2.4 & pt > 14.0"),
    filter = cms.bool(True)
)
tau18JetSelector = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("ak5PFJets"),
    cut = cms.string("abs(eta) < 2.3 & pt > 18.0"),
    filter = cms.bool(True)
)
muTauPath = cms.Path(mu14MuSelector + tau18JetSelector)
skimConfig.paths.append("muTauPath")

# E+Tau for H2Tau
e17Selector = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag("gsfElectrons"),
    cut = cms.string("abs(eta) < 2.5 & pt > 17"),
    filter = cms.bool(True),
)
eTauPath = cms.Path(e17Selector + tau18JetSelector)
skimConfig.paths.append("eTauPath")

# DoubleE for ZZ, VH, and HZG
e8Selector = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag("gsfElectrons"),
    cut = cms.string("abs(eta) < 2.5 & pt > 8"),
    filter = cms.bool(False),
)
twoElectronsAbove8 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("e8Selector"),
    minNumber = cms.uint32(2)
)
doubleEPath = cms.Path(e17Selector + e8Selector + twoElectronsAbove8)
skimConfig.paths.append("doubleEPath")

# DoubleMu for ZZ, VH and HZG
mu17Selector = cms.EDFilter(
    "MuonSelector",
    src = cms.InputTag("muons"),
    cut = cms.string("abs(eta) < 2.4 & pt > 17"),
    filter = cms.bool(True),
)
mu8Selector = cms.EDFilter(
    "MuonSelector",
    src = cms.InputTag("muons"),
    cut = cms.string("abs(eta) < 2.4 & pt > 8"),
    filter = cms.bool(False),
)
twoMuonsAbove8 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("mu8Selector"),
    minNumber = cms.uint32(2)
)
doubleMuPath = cms.Path(mu17Selector + mu8Selector + twoMuonsAbove8)
skimConfig.paths.append("doubleMuPath")

# MuEG 17-8
oneElectronAbove8 = twoElectronsAbove8.clone(minNumber = cms.uint32(1))
mu17e8Path = cms.Path(mu17Selector + e8Selector + oneElectronAbove8)
skimConfig.paths.append("mu17e8Path")

# MuEG 8-17
oneMuonAbove8 = twoMuonsAbove8.clone(minNumber = cms.uint32(1))
mu8e17Path = cms.Path(e17Selector + mu8Selector + oneMuonAbove8)
skimConfig.paths.append("mu8e17Path")

#diphoton skims ;-)
pho15Selector = cms.EDFilter(
    "PhotonSelector",
    src = cms.InputTag("photons"),
    cut = cms.string("abs(eta) < 3.0 & pt > 15"),
    filter=cms.bool(False)
)
twoPhotonsAbove15 = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("pho15Selector"),
    minNumber = cms.uint32(2)
)
pho20Selector = cms.EDFilter(
    "PhotonSelector",
    src = cms.InputTag("photons"),
    cut = cms.string("abs(eta) < 3.0 & pt > 20"),
    filter=cms.bool(True)
)

diPho15Path = cms.Path(pho20Selector + pho15Selector + twoPhotonsAbove15)
skimConfig.paths.append("pho15Pho20Path")


