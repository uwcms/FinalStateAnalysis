'''

RECO-Level skims used to create trigger studies skims

Author: UW Folks

'''

import FWCore.ParameterSet.Config as cms


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
