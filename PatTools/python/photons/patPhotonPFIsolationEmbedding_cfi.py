import FWCore.ParameterSet.Config as cms

patPhotonPFIsolation = cms.EDProducer(
    "PATPhotonIsolationEmbedder",
    src = cms.InputTag("fixme"),
    pfCollectionSrc = cms.InputTag("particleFlow"),
    vtxSrc = cms.InputTag("offlinePrimaryVertices"),
    userFloatPrefix = cms.string("pf"),
    coneSize = cms.double(0.3)
)
