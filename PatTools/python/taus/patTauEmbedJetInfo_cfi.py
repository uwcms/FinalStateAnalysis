import FWCore.ParameterSet.Config as cms

patTausEmbedJetInfo = cms.EDProducer(
    "PATTauJetInfoEmbedder",
    src = cms.InputTag("fixme"),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag("selectedPatJets"),
)
