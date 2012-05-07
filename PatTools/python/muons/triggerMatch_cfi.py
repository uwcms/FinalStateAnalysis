import FWCore.ParameterSet.Config as cms

triggeredPatMuons = cms.EDProducer(
    "PATMuonTriggerMatcher",
    src = cms.InputTag("patMuons"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD"),
    filters = cms.VInputTag(
        cms.InputTag('hltSingleMuIsoL3IsoFiltered12'),
        cms.InputTag('hltSingleMuIsoL3IsoFiltered15'),
        cms.InputTag('hltSingleMuIsoL3IsoFiltered24'),
        cms.InputTag('hltDiMuonL3PreFiltered8'),
        cms.InputTag('hltDiMuonL3PreFiltered7'),
        cms.InputTag('hltOverlapFilterIsoMu15IsoPFTau15'),
        cms.InputTag('hltL1Mu3EG5L3Filtered17'),
        cms.InputTag('hltL1Mu7EG5L3MuFiltered17'),
        cms.InputTag('hltL1MuOpenEG12L3Filtered8'),
        cms.InputTag('hltL1MuOpenEG5L3Filtered8'),
        cms.InputTag('hltL1MuOpenEG8L3Filtered8'),
        cms.InputTag('hltL1Mu3EG5L3Filtered8'),
        cms.InputTag('hltOverlapFilterIsoMu12IsoPFTau10'),
        cms.InputTag('hltSingleMuIsoL3IsoFiltered17'),
        cms.InputTag('hltSingleMuL2QualIsoL3IsoFiltered17'),
        cms.InputTag('hltSingleMuL2QualIsoL3IsoFiltered24'),
        cms.InputTag('hltSingleMu13L3Filtered13'),
        cms.InputTag('hltSingleMuIsoL1s14L3IsoFiltered15eta2p1'),
        cms.InputTag('hltL3IsoL1sMu14Eta2p1L1f0L2f14QL2IsoL3f24L3IsoFiltered'),
        cms.InputTag('hltDiMuonL3p5PreFiltered8'),
        cms.InputTag('hltSingleMu13L3Filtered17'),
        cms.InputTag('hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f18QL3crIsoFiltered10'),
        cms.InputTag('hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoFiltered10'),
    ),
    pdgId = cms.int32(13)
)
