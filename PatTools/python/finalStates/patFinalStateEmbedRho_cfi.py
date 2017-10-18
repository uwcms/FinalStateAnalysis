import FWCore.ParameterSet.Config as cms

patEmbedRho = cms.EDProducer(
    "PATFinalStateFloatEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("kt6PFJets", "rho"),
    name = cms.string("rho"),
)
