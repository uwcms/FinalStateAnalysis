import FWCore.ParameterSet.Config as cms

patTausEmbedIp = cms.EDProducer(
    "PATTauIpEmbedder",
    src = cms.InputTag("fixme"),
    vtxSrc = cms.InputTag("selectedPrimaryVertex"),
)
