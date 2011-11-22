import FWCore.ParameterSet.Config as cms

patMuonsEmbedIp = cms.EDProducer(
    "PATMuonIpEmbedder",
    src = cms.InputTag("patMuonsEmbedWWId"),
    vtxSrc = cms.InputTag("selectedPrimaryVertex"),
)
