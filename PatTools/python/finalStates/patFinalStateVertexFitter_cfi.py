import FWCore.ParameterSet.Config as cms

patFinalStateVertexFitter = cms.EDProducer(
    "PATFinalStateVertexFitter",
    src = cms.InputTag("fixme"),
    # If disabled, do nothing.  Allows to run even without tracks.
    enable = cms.bool(True),
)
