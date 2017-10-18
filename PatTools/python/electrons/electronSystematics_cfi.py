import FWCore.ParameterSet.Config as cms

electronSystematics = cms.EDProducer(
    "PATElectronSystematicsEmbedder",
    src = cms.InputTag("slimmedelectrons"),
    nominal = cms.double(1.0),
    eScaleUp = cms.double(1.06),
    eScaleDown = cms.double(0.94),
)
