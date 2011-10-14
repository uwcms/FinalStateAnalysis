import FWCore.ParameterSet.Config as cms

# Embed VBTF ID
patMuonsEmbedWWId = cms.EDProducer(
    "PATMuonIdEmbedder",
    src = cms.InputTag("patMuonsLoosePFIsoEmbedded06"),
    userIntLabel = cms.string("WWID"),
    beamSpotSource = cms.InputTag("offlineBeamSpot"),
    vertexSource = cms.InputTag("selectedPrimaryVertex"),
)
