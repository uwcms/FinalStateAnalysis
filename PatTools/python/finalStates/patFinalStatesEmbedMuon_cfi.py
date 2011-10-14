import FWCore.ParameterSet.Config as cms

patFinalStatesEmbedMuons = cms.EDProducer(
    "PATFinalStateOverlapEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("cleanPatMuons"),
    name = cms.string("extMuons"), # external taus
    minDeltaR = cms.double(0.3),
    maxDeltaR = cms.double(1e9),
    cut = cms.string(''),
)

