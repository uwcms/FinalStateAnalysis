import FWCore.ParameterSet.Config as cms

patPhotonPHOSPHOR2011Embedder = cms.EDProducer(
    "PATPhotonPHOSPHOREmbedder",
    src = cms.InputTag("fixme"),
    year = cms.uint32(2011),
    isMC = cms.bool(False),
    r9Categories = cms.bool(True),    
    dataCard = cms.FileInPath("PHOSPHOR_NUMBERS_EXPFIT_ERRORS.txt")
)

patPhotonPHOSPHOR2012Embedder = cms.EDProducer(
    "PATPhotonPHOSPHOREmbedder",
    src = cms.InputTag("fixme"),
    year = cms.uint32(2012),
    isMC = cms.bool(False),
    r9Categories = cms.bool(True),    
    dataCard = cms.FileInPath("PHOSPHOR_NUMBERS_EXPFIT_ERRORS.txt")
)
