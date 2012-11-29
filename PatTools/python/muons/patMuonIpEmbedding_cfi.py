import FWCore.ParameterSet.Config as cms

patMuonsEmbedIp = cms.EDProducer(
    "PATMuonIpEmbedder",
    src = cms.InputTag("fixme"),
    vtxSrc = cms.InputTag("selectedPrimaryVertex"),
)
