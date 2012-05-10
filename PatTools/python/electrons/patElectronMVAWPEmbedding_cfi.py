'''

Embed working point cuts into pat::Electrons

See: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#Object_ID_AN1

'''
import FWCore.ParameterSet.Config as cms

patElectronMVAIDWPEmbedding = cms.EDProducer(
    "PATElectronWorkingPointEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string('mvaidwp'),
    categories = cms.VPSet(
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) < 0.8'),
            cut = cms.string('electronID("mvaNonTrigV0") > 0.925')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 0.8 & abs(eta) < 1.479'),
            cut = cms.string('electronID("mvaNonTrigV0") > 0.915')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 1.479'),
            cut = cms.string('electronID("mvaNonTrigV0") > 0.965')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) < 0.8'),
            cut = cms.string('electronID("mvaNonTrigV0") > 0.905')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 0.8 & abs(eta) < 1.479'),
            cut = cms.string('electronID("mvaNonTrigV0") > 0.955')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 1.479'),
            cut = cms.string('electronID("mvaNonTrigV0") > 0.975')
        ),
    )
)

patElectronMVAIsoWPEmbedding = cms.EDProducer(
    "PATElectronWorkingPointEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string('mvaisowp'),
    categories = cms.VPSet(
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) < 0.8'),
            cut = cms.string('userFloat("isomva") > 0.815')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 0.8 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.785')
        ),
        cms.PSet(
            category = cms.string('pt < 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.825')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) < 0.8'),
            cut = cms.string('userFloat("isomva") > 0.805')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 0.8 & abs(eta) < 1.479'),
            cut = cms.string('userFloat("isomva") > 0.815')
        ),
        cms.PSet(
            category = cms.string('pt >= 20 & abs(eta) >= 1.479'),
            cut = cms.string('userFloat("isomva") > 0.705')
        ),
    )
)
