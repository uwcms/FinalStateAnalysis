import FWCore.ParameterSet.Config as cms

patFinalStateVertexFitter = cms.EDProducer(
    "PATFinalStateVertexFitter",
    src = cms.InputTag("fixme"),
)
