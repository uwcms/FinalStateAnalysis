import FWCore.ParameterSet.Config as cms

finalStateMassResolutionEmbedder = cms.EDProducer(
    "PATFinalStateMassResolutionEmbedder",
    debug = cms.bool(False),
    src = cms.InputTag("fixme")
    )
