import FWCore.ParameterSet.Config as cms

# Embed SSV b-tag information into a PAT Jet

patSSVJetEmbedder = cms.EDProducer(
    "PATSSVJetEmbedder",
    src = cms.InputTag("fixme")
)
