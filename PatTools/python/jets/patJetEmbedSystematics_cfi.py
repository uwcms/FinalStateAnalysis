import FWCore.ParameterSet.Config as cms

patJetEmbedSystematics = cms.EDProducer(
    "PATJetSystematicsEmbedder",
    src = cms.InputTag("fixme"),
    corrLabel = cms.string("AK5PF"),
    unclusteredEnergyScale = cms.double(0.1),
)

patJetEmbedSystematicsFull = cms.EDProducer(
    "PATJetSystematicsEmbedderFull",
    srcPFJets = cms.InputTag("fixme"),
    srcPatJets = cms.InputTag("fixme"),
    corrLabel = cms.string("AK5PF"),
    unclusteredEnergyScale = cms.double(0.1),
)
