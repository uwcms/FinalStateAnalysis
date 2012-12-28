import FWCore.ParameterSet.Config as cms

patPhotonPHOSPHOREmbedder = cms.EDProducer(
    "PATPhotonPHOSPHOREmbedder",
    src = cms.InputTag("fixme"),
    year = cms.uint32(2011),
    isMC = cms.bool(False),
    r9Categories = cms.bool(True),    
    dataCard = cms.FileInPath("FinalStateAnalysis/PatTools/data/PHOSPHOR_NUMBERS_EXPFIT_ERRORS.txt")
)


