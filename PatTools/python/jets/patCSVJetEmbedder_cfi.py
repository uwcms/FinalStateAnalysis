import FWCore.ParameterSet.Config as cms

# Embed SSV b-tag information into a PAT Jet

patCSVJetEmbedder = cms.EDProducer(
    "PATCSVJetEmbedder",
    src = cms.InputTag("fixme")
)
