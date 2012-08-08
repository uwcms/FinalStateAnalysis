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

muPlusJetSeq = cms.Sequence(tightMuons * ak5PFJetsPt15 * jetsNotOverlappingMuons)

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


