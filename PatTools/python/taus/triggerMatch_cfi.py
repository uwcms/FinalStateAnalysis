import FWCore.ParameterSet.Config as cms

preTriggeredPatTaus = cms.EDProducer(
    "PATTauTriggerMatcher",
    src = cms.InputTag("fixme"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltFilterDoubleIsoPFTau20Trk5LeadTrack5IsolationL1HLTMatched'),
        cms.InputTag('hltFilterDoubleIsoPFTau35Trk5LeadTrack5IsolationL1HLTMatched')
    ),
    pdgId = cms.int32(0)
)

triggeredPatTaus = cms.EDProducer(
    "PATTauTriggerMatcher",
    src = cms.InputTag("fixme"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltOverlapFilterIsoMu15IsoPFTau15'),
        cms.InputTag('hltOverlapFilterIsoMu15IsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoMu15MediumIsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoMu15TightIsoPFTau20'),
        cms.InputTag('hltOverlapFilterMu15IsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoMu12IsoPFTau10'),
        cms.InputTag('hltOverlapFilterIsoEle15IsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle15IsoPFTau15'),
        cms.InputTag('hltOverlapFilterIsoEle15TightIsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle18MediumIsoPFTau20'),
        cms.InputTag('hltOverlapFilterIsoEle20MediumIsoPFTau20'),
        cms.InputTag('hltFilterDoubleIsoPFTau20Trk5LeadTrack5IsolationL1HLTMatched'),
        cms.InputTag('hltPFTauMediumIso20TrackMediumIso'),
        cms.InputTag('hltPFTau15TrackLooseIso'),
        cms.InputTag('hltPFTau20TrackLooseIso'),
        cms.InputTag('hltPFTauTightIso20TrackTightIso'),
    ),
    pdgId = cms.int32(15)
)
