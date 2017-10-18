import FWCore.ParameterSet.Config as cms

patMuonsEmbedJetInfo = cms.EDProducer(
    "PATMuonJetInfoEmbedder",
    src = cms.InputTag("fixme"),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag("selectedPatJets"),
    maxDeltaR = cms.double(0.5),
)
