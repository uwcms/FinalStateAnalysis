import FWCore.ParameterSet.Config as cms

patPhotonPFIsolation = cms.EDProducer(
    "PATPhotonPFIsolationEmbedder",
    src = cms.InputTag("fixme"),
    pfCollectionSrc = cms.InputTag("particleFlow"),    
    vtxSrc = cms.InputTag("offlinePrimaryVertices"),
    defaultVertex = cms.uint32(0), #set vertex embedded as default iso    
    userFloatPrefix = cms.string("pf"),
    coneSize = cms.double(0.3)
)
