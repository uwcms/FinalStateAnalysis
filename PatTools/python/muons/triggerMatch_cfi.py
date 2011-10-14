import FWCore.ParameterSet.Config as cms

triggeredPatMuons = cms.EDProducer(
    "PATMuonTriggerMatcher",
    src = cms.InputTag("fixme"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltSingleMuIsoL3IsoFiltered12','','HLT'),
        cms.InputTag('hltSingleMuIsoL3IsoFiltered15','','HLT'),
        cms.InputTag('hltSingleMuIsoL3IsoFiltered24','','HLT'),
        cms.InputTag('hltDiMuonL3PreFiltered8','','HLT'),
        cms.InputTag('hltDiMuonL3PreFiltered7','','HLT'),
        cms.InputTag('hltOverlapFilterIsoMu15IsoPFTau15','','HLT'),
        cms.InputTag('hltL1Mu3EG5L3Filtered17','','HLT'),
        cms.InputTag('hltL1MuOpenEG5L3Filtered8','','HLT'),
        cms.InputTag('hltOverlapFilterIsoMu12IsoPFTau10','','HLT')
    ),
    pdgId = cms.int32(13)
)
