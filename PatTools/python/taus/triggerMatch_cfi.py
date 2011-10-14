import FWCore.ParameterSet.Config as cms

triggeredPatTaus = cms.EDProducer(
    "PATTauTriggerMatcher",
    src = cms.InputTag("fixme"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltOverlapFilterIsoMu15IsoPFTau15','','HLT'),
        cms.InputTag('hltOverlapFilterIsoMu12IsoPFTau10','','HLT'),
        cms.InputTag('hltOverlapFilterIsoEle15IsoPFTau20','','HLT'),
        cms.InputTag('hltOverlapFilterIsoEle18IsoPFTau20','','HLT')
    ),
    pdgId = cms.int32(15)
)
