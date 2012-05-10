'''

Embed working point cuts into pat::Muons

See: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#Object_ID_AN1

'''
import FWCore.ParameterSet.Config as cms

patMuonMVAIsoWP1Embedding = cms.EDProducer(
    "PATMuonWorkingPointEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string('mvaisowp1'),
    categories = cms.VPSet(
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.922')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.929')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.921')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.9')
        ),
    )
)

patMuonMVAIsoWP2Embedding = cms.EDProducer(
    "PATMuonWorkingPointEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string('mvaisowp2'),
    categories = cms.VPSet(
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.91')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.91')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.897')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.864')
        ),
    )
)

patMuonMVAIsoWP3Embedding = cms.EDProducer(
    "PATMuonWorkingPointEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string('mvaisowp3'),
    categories = cms.VPSet(
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.957')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.96')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.981')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.971')
        ),
    )
)
