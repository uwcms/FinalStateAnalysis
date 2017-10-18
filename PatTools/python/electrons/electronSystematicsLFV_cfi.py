import FWCore.ParameterSet.Config as cms


electronSystematicsLFV = cms.EDProducer(
    "PATElectronSystematicsEmbedderLFV",
    calibratedElectrons = cms.InputTag("slimmedElectrons"),
    uncalibratedElectrons = cms.InputTag("slimmedElectrons"),
    recHitCollectionEB = cms.InputTag("reducedEgamma","reducedEBRecHits"),
    recHitCollectionEE = cms.InputTag("reducedEgamma","reducedEERecHits"),

    #correctionfile name right now is hardcoded to MORIOND corrrection filename
)
