import FWCore.ParameterSet.Config as cms

triggeredPatElectronsL = cms.EDProducer(
   "PATElectronTriggerMatcher",
   src = cms.InputTag("patElectrons"),
   trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
   filters = cms.VInputTag(
       cms.InputTag('hltEle17CaloIdLCaloIsoVLPixelMatchFilterDoubleEG125'),
       cms.InputTag('hltEle17CaloIdIsoEle8CaloIdIsoPixelMatchDoubleFilter'),
       cms.InputTag('hltEle17CaloIdLCaloIsoVLPixelMatchFilter'),
       cms.InputTag('hltEle8CaloIdLCaloIsoVLPixelMatchFilter'),
       cms.InputTag('hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter'),
       cms.InputTag('hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter'),
       cms.InputTag('hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter'),
       cms.InputTag('hltMu17Ele8CaloIdTPixelMatchFilter'),
   ),
   pdgId = cms.int32(0)
)

triggeredPatElectrons = cms.EDProducer(
    "PATElectronTriggerMatcher",
    src = cms.InputTag("triggeredPatElectronsL"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltEle15CaloIdVTTrkIdTCaloIsoTTrkIsoTTrackIsolFilter'),
        cms.InputTag('hltEle15CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilter'),
        cms.InputTag('hltEle18CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilter'),
        cms.InputTag('hltOverlapFilterIsoEle15IsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle15IsoPFTau15'),
        cms.InputTag('hltOverlapFilterIsoEle15TightIsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle18MediumIsoPFTau20'),
        cms.InputTag('hltEle17CaloIdVTCaloIsoVTTrkIdTTrkIsoVTSC8TrackIsolFilter'),
        cms.InputTag('hltEle17CaloIdVTCaloIsoVTTrkIdTTrkIsoVTEle8TrackIsolFilter'),
        cms.InputTag('hltEle17TightIdLooseIsoEle8TightIdLooseIsoTrackIsolFilter'),
        cms.InputTag('hltEle17TightIdLooseIsoEle8TightIdLooseIsoTrackIsolDoubleFilter'),
        cms.InputTag('hltEle20CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilterL1SingleEG18orL1SingleEG20'),
        cms.InputTag('hltEle32CaloIdTCaloIsoTTrkIdTTrkIsoTTrackIsoFilter'),
        cms.InputTag('hltEle32CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilter'),
        cms.InputTag('hltOverlapFilterIsoEle18TightIsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle18IsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle20MediumIsoPFTau20'),
    ),
    pdgId = cms.int32(11)
)
