import FWCore.ParameterSet.Config as cms

patMuonsEmbedIp = cms.EDProducer(
    "PATMuonIpEmbedder",
    src = cms.InputTag("patMuonsEmbedWWId"),
    userFloatLabel = cms.string("vertexDXY"),
    vtxSrc = cms.InputTag("selectedPrimaryVertex"),
)
