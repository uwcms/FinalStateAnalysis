import FWCore.ParameterSet.Config as cms

patElectronsEmbedJetInfo = cms.EDProducer(
    "PATElectronJetInfoEmbedder",
    src = cms.InputTag("fixme"),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag("selectedPatJets"),
    maxDeltaR = cms.double(0.5),
)
