import FWCore.ParameterSet.Config as cms

triggeredPatElectrons = cms.EDProducer(
    "PATElectronTriggerMatcher",
    src = cms.InputTag("patElectrons"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltEle15CaloIdVTTrkIdTCaloIsoTTrkIsoTTrackIsolFilter','','HLT'),
        cms.InputTag('hltEle18CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilter','','HLT'),
        cms.InputTag('hltOverlapFilterIsoEle15IsoPFTau20','','HLT'),
        cms.InputTag('hltEle17CaloIdVTCaloIsoVTTrkIdTTrkIsoVTSC8TrackIsolFilter','','HLT'),
        cms.InputTag('hltEle32CaloIdTCaloIsoTTrkIdTTrkIsoTTrackIsoFilter','','HLT'),
        cms.InputTag('hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter','','HLT'),
        cms.InputTag('hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter','','HLT'),
        cms.InputTag('hltOverlapFilterIsoEle18IsoPFTau20','','HLT')
    ),
    pdgId = cms.int32(11)
)
