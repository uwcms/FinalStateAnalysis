import FWCore.ParameterSet.Config as cms

lumiProducer = cms.EDProducer(
    "MCLumiProducer",
    trigSrc = cms.InputTag("patTriggerEvent"),
    xSec = cms.double(-1),
    xSecErr = cms.double(0.0)
)
