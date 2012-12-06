import FWCore.ParameterSet.Config as cms

# Embed WWID ID
patMuonsEmbedWWId = cms.EDProducer(
    "PATMuonIdEmbedder",
    src = cms.InputTag("patMuonsLoosePFIsoEmbedded06"),
    userIntLabel = cms.string("WWID"),
    beamSpotSource = cms.InputTag("offlineBeamSpot"),
    vertexSource = cms.InputTag("selectedPrimaryVertex"),
)

## HZG Muon Id Variant for 2011 Data
patMuonsEmbedHZG2011 = cms.EDProducer(
    "PATMuonIdEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string("HZG2011"),
    beamSpotSource = cms.InputTag("offlineBeamSpot"),
    vertexSource = cms.InputTag("selectedPrimaryVertex"),
    applyGlobalMuonPromptTight = cms.bool(False),
    applyAllArbitrated = cms.bool(False),
    use2012IDVariables = cms.bool(True),
    usePFMuonReq = cms.bool(False),
    IPtrackType = cms.string("innerTrack"),
    IPrefType = cms.string("vertex"),
    maxIPxy = cms.double(0.2),
    maxIPz  = cms.double(1e3),
    minTkLayersWithMeasurement = cms.uint32(9)
)

## HZG Muon Id Variant for 2012 Data
patMuonsEmbedHZG2012 = cms.EDProducer(
    "PATMuonIdEmbedder",
    src = cms.InputTag("fixme"),
    userIntLabel = cms.string("HZG2012"),
    beamSpotSource = cms.InputTag("offlineBeamSpot"),
    vertexSource = cms.InputTag("selectedPrimaryVertex"),
    applyGlobalMuonPromptTight = cms.bool(False),
    applyAllArbitrated = cms.bool(False),
    use2012IDVariables = cms.bool(True),
    usePFMuonReq = cms.bool(True),
    IPtrackType = cms.string("innerTrack"),
    IPrefType = cms.string("vertex"),
    maxIPxy = cms.double(0.2),
    maxIPz  = cms.double(0.5),
    minTkLayersWithMeasurement = cms.uint32(6)   
)

# Embed Mike's version of the WWID cuts
patMuonsEmbedWWId2011 = cms.EDProducer(
    "PATMuonIdEmbedder",
    src = cms.InputTag("patMuonsLoosePFIsoEmbedded06"),
    userIntLabel = cms.string("WWID2011"),
    beamSpotSource = cms.InputTag("offlineBeamSpot"),
    vertexSource = cms.InputTag("selectedPrimaryVertex"),
    maxIPxy = cms.double(0.045),
    minTrackerHits = cms.uint32(11),
    maxIPz = cms.double(0.2),
)

patVBTFMuonMatch = cms.EDProducer(
    "PATVBTFMuonEmbedder", #Saves the case where muon is matched to a PF Muon
    src = cms.InputTag("fixme"),
    maxDxDy=cms.double(0.2),
    maxChi2=cms.double(10.),
    minTrackerHits=cms.int32(10),
    minPixelHits=cms.int32(1),
    minMuonHits = cms.int32(1),
    minMatches  = cms.int32(2),
    maxResol      = cms.double(0.1)
)



