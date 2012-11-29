'''

RECO-Level skims used to create trigger studies skims

Author: UW Folks

'''

import FWCore.ParameterSet.Config as cms

###############################################################################
# Mu + Jets skim
# ==========
# Require an isolated, identified muon with pt > 19
#
# DR 0.4 charged relative isolation less than 10%
#
###############################################################################

# Single muon
tightMuons = cms.EDFilter(
    "MuonRefSelector",
    src = cms.InputTag("muons"),
    cut = cms.string(
        "pt>20 && isGlobalMuon && isTrackerMuon && abs(eta)<2.5"
        " && globalTrack().normalizedChi2<10"
        " && globalTrack().hitPattern().numberOfValidMuonHits>0"
        " && globalTrack().hitPattern().numberOfValidPixelHits>0"
        " && numberOfMatchedStations>1"
        " && globalTrack().hitPattern().trackerLayersWithMeasurement>5"
        " && (pfIsolationR04().sumChargedHadronPt)/pt< 0.1"
    ),
    filter = cms.bool(True),
)

ak5PFJetsPt15 = cms.EDFilter(
    "PFJetSelector",
    src = cms.InputTag("ak5PFJets"),
    cut = cms.string("pt > 18"),
    filter = cms.bool(True),
)

jetsNotOverlappingMuons = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("ak5PFJetsPt15"),
    subtractSrc = cms.InputTag("tightMuons"),
    minDeltaR = cms.double(0.5),
    filter = cms.bool(True),
)

muMetAboveMt40 = cms.EDProducer(
    "CandViewShallowCloneCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string('sqrt((daughter(0).pt+daughter(1).pt)*(daughter(0).pt+daughter(1).pt)-pt*pt)>40'),
    decay = cms.string("tightMuons pfMet")
)

wToMuNuFilter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("muMetAboveMt40"),
    minNumber = cms.uint32(1)
)

muPlusJetSeq = cms.Sequence(tightMuons * ak5PFJetsPt15 * jetsNotOverlappingMuons * muMetAboveMt40 * wToMuNuFilter)

###############################################################################
# E-Tau skim
# ==========
# Require an identified electron with pt > 18, eta < 2.5.
#
###############################################################################

electrons18 = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag("gsfElectrons"),
    cut = cms.string('pt>18&&abs(eta)<2.5&&((isEB()&&abs(deltaEtaSuperClusterTrackAtVtx())<0.007&&abs(deltaPhiSuperClusterTrackAtVtx())<0.15)||(isEE()&&abs(deltaEtaSuperClusterTrackAtVtx())<0.009&&abs(deltaPhiSuperClusterTrackAtVtx())<0.10))'),
    filter = cms.bool(True)
)

isoElectrons18 = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag("electrons18"),
    cut = cms.string('pfIsolationVariables.chargedHadronIso()/pt()<0.2'),
    filter = cms.bool(True)
)

isoTaus18 = cms.EDFilter(
    "PFTauSelector",
    src = cms.InputTag("hpsPFTauProducer"),
    cut = cms.string("pt > 18 & abs(eta) < 2.5"),
    discriminators = cms.VPSet(
        cms.PSet(
            discriminator=cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"),
            selectionCut=cms.double(0.5)
        ),
        cms.PSet(
            discriminator=cms.InputTag("hpsPFTauDiscriminationByVLooseIsolation"),
            selectionCut=cms.double(0.5)
        ),
        cms.PSet(
            discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseMuonRejection"),
            selectionCut=cms.double(0.5)
        ),
        cms.PSet(
            discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseElectronRejection"),
            selectionCut=cms.double(0.5)
        ),
    ),
    filter = cms.bool(True)
)

eTauSkimSeq = cms.Sequence(electrons18 * isoElectrons18 * isoTaus18)

###############################################################################
# Ele + Jets skim
# ==========
# Require an isolated, identified electron with pt > 30, plus 1 Jet
###############################################################################

# Higher Pt Electron

isoElectrons30 = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag("isoelectrons18"),
    cut = cms.string('pt>30'),
    filter = cms.bool(True)
)

jetsNotOverlappingElectrons = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("ak5PFJetsPt15"),
    subtractSrc = cms.InputTag("isoElectrons18"),
    minDeltaR = cms.double(0.5),
    filter = cms.bool(True),
)

eleMetAboveMt40 = cms.EDProducer(
    "CandViewShallowCloneCombiner",
    checkCharge = cms.bool(False),
    cut = cms.string('sqrt((daughter(0).pt+daughter(1).pt)*(daughter(0).pt+daughter(1).pt)-pt*pt)>40'),
    decay = cms.string("isoElectrons30 pfMet")
)

wToENuFilter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("eleMetAboveMt40"),
    minNumber = cms.uint32(1)
)

elePlusJetSeq = cms.Sequence(electrons18 * isoElectrons18 *isoElectrons30 * ak5PFJetsPt15 * jetsNotOverlappingElectrons * eleMetAboveMt40 * wToENuFilter)
