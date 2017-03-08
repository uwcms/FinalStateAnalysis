import FWCore.ParameterSet.Config as cms


electronSystematicsLFV = cms.EDProducer(
    "PATElectronSystematicsEmbedderLFV",
    calibratedElectrons = cms.InputTag("slimmedElectrons"),
    uncalibratedElectrons = cms.InputTag("slimmedElectrons"),
    #correctionfile name right now is hardcoded to MORIOND corrrection filename
)
