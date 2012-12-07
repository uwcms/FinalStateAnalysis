'''

Skims for various UW analysis.  The OR of these skims is used when building the
PAT tuple.

Author: Bucky Badger, UW Madison


'''

import FWCore.ParameterSet.Config as cms
import os

# The list of active paths are defined here.
skimConfig = cms.PSet(
    paths=cms.vstring()
)

# Get the ZZ skim (4 lepton final states)
from FinalStateAnalysis.RecoTools.zzSkim_cff import \
    goodVertex, muons4skim, electrons4skim, leptons4skim, dileptons4skim, \
    skim2010, skim40NoOF, skimNoOS, zzSkim

# So flake8 doesn't complain about unused imported modules.
_USED = [goodVertex, muons4skim, electrons4skim, leptons4skim, dileptons4skim,
         skim2010, skim40NoOF, skimNoOS, zzSkim]

skimConfig.paths.append("zzSkim")

# Single muon for Wjets
singleMuSelector = cms.EDFilter(
    "MuonSelector",
    src=cms.InputTag('muons'),
    cut=cms.string(
        "(isGlobalMuon) & abs(eta) < 2.4 & pt > 19.0"),
    filter=cms.bool(True)
)
singleMuPath = cms.Path(singleMuSelector)
# Don't run the single mu path, only single mu + jet
#skimConfig.paths.append("singleMuPath")

# Make a version which additionally requires a jet.
jet15Selector = cms.EDFilter(
    "CandViewRefSelector",
    src=cms.InputTag("ak5PFJets"),
    cut=cms.string("abs(eta) < 2.5 & pt > 15"),
    filter=cms.bool(True),
)
jet15NotOverlappingSingleMu = cms.EDFilter(
    "PFJetViewOverlapSubtraction",
    src=cms.InputTag("jet15Selector"),
    subtractSrc=cms.InputTag("singleMuSelector"),
    minDeltaR=cms.double(0.3),
    filter=cms.bool(True),
)
singleMuPlusJetPath = cms.Path(
    singleMuSelector + jet15Selector + jet15NotOverlappingSingleMu)
skimConfig.paths.append("singleMuPlusJetPath")

# We use a 30 GeV for electrons in 2011 data (CMSSW 4)
single_electron_thresh = 30 if 'CMSSW_4' in os.environ['CMSSW_VERSION'] else 25

singleElecSelector = cms.EDFilter(
    "GsfElectronSelector",
    src=cms.InputTag('gsfElectrons'),
    cut=cms.string(
        "abs(eta) < 2.5 & pt > %0.0f" % single_electron_thresh),
    filter=cms.bool(True)
)
singleElecPath = cms.Path(singleElecSelector)
# Don't run the single e path either, just single e + jet
#skimConfig.paths.append("singleElecPath")

jet15NotOverlappingSingleElec = cms.EDFilter(
    "PFJetViewOverlapSubtraction",
    src=cms.InputTag("jet15Selector"),
    subtractSrc=cms.InputTag("singleElecSelector"),
    minDeltaR=cms.double(0.3),
    filter=cms.bool(True),
)
singleElecPlusJetPath = cms.Path(
    singleElecSelector + jet15Selector + jet15NotOverlappingSingleElec)
skimConfig.paths.append("singleElecPlusJetPath")

# Mu+Tau for H2Tau
mu14MuSelector = cms.EDFilter(
    "MuonSelector",
    src=cms.InputTag('muons'),
    cut=cms.string(
        "(isGlobalMuon) & abs(eta) < 2.4 & pt > 14.0"),
    filter=cms.bool(True)
)
tau18JetSelector = cms.EDFilter(
    "CandViewRefSelector",
    src=cms.InputTag("ak5PFJets"),
    cut=cms.string("abs(eta) < 2.3 & pt > 18.0"),
    filter=cms.bool(True)
)
# Make sure we don't count the muon as a jet
tau18JetsNotOverlappingMu14 = cms.EDFilter(
    "PFJetViewOverlapSubtraction",
    src=cms.InputTag("tau18JetSelector"),
    subtractSrc=cms.InputTag("mu14MuSelector"),
    minDeltaR=cms.double(0.3),
    filter=cms.bool(True)
)
muTauPath = cms.Path(mu14MuSelector +
                     tau18JetSelector + tau18JetsNotOverlappingMu14)
skimConfig.paths.append("muTauPath")

# E+Tau for H2Tau
e17Selector = cms.EDFilter(
    "GsfElectronSelector",
    src=cms.InputTag("gsfElectrons"),
    cut=cms.string("abs(eta) < 2.5 & pt > 17"),
    filter=cms.bool(True),
)
# Make sure we don't count the electron as a jet
tau18JetsNotOverlappingE17 = cms.EDFilter(
    "PFJetViewOverlapSubtraction",
    src=cms.InputTag("tau18JetSelector"),
    subtractSrc=cms.InputTag("e17Selector"),
    minDeltaR=cms.double(0.3),
    filter=cms.bool(True)
)
eTauPath = cms.Path(e17Selector +
                    tau18JetSelector + tau18JetsNotOverlappingE17)
skimConfig.paths.append("eTauPath")

# DoubleE for ZZ, VH, and HZG
e8Selector = cms.EDFilter(
    "GsfElectronSelector",
    src=cms.InputTag("gsfElectrons"),
    cut=cms.string("abs(eta) < 2.5 & pt > 8"),
    filter=cms.bool(False),
)
twoElectronsAbove8 = cms.EDFilter(
    "CandViewCountFilter",
    src=cms.InputTag("e8Selector"),
    minNumber=cms.uint32(2)
)
doubleEPath = cms.Path(e17Selector + e8Selector + twoElectronsAbove8)
skimConfig.paths.append("doubleEPath")

# DoubleMu for ZZ, VH and HZG
mu17Selector = cms.EDFilter(
    "MuonSelector",
    src=cms.InputTag("muons"),
    cut=cms.string("abs(eta) < 2.4 & pt > 17"),
    filter=cms.bool(True),
)
mu8Selector = cms.EDFilter(
    "MuonSelector",
    src=cms.InputTag("muons"),
    cut=cms.string("abs(eta) < 2.4 & pt > 8"),
    filter=cms.bool(False),
)
twoMuonsAbove8 = cms.EDFilter(
    "CandViewCountFilter",
    src=cms.InputTag("mu8Selector"),
    minNumber=cms.uint32(2)
)
doubleMuPath = cms.Path(mu17Selector + mu8Selector + twoMuonsAbove8)
skimConfig.paths.append("doubleMuPath")

# MuEG 17-8
oneElectronAbove8 = twoElectronsAbove8.clone(minNumber=cms.uint32(1))
mu17e8Path = cms.Path(mu17Selector + e8Selector + oneElectronAbove8)
skimConfig.paths.append("mu17e8Path")

# MuEG 8-17
oneMuonAbove8 = twoMuonsAbove8.clone(minNumber=cms.uint32(1))
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

pho15Pho20Path = cms.Path(pho20Selector + pho15Selector + twoPhotonsAbove15)
skimConfig.paths.append("pho15Pho20Path")


