import FWCore.ParameterSet.Config as cms

patJetEmbedSystematics = cms.EDProducer(
    "PATJetSystematicsEmbedder",
    src = cms.InputTag("fixme"),
    corrLabel = cms.string("AK5PF"),
    unclusteredEnergyScale = cms.double(0.1),
)
