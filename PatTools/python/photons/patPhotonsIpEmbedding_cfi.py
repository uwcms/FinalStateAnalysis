import FWCore.ParameterSet.Config as cms

patElectronsEmbedIp = cms.EDProducer(
    "PATElectronIpEmbedder",
    src = cms.InputTag("fixme"),
    vtxSrc = cms.InputTag("selectedPrimaryVertex"),
)
