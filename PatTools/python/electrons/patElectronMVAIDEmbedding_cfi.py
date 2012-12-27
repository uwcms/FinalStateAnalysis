import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.PatTools.electrons.electronIDMVAConfiguration_cfi \
        import electronMVAIDNOIPcfg, electronMVAIDTrig2012

patElectronMVAIDEmbedder = cms.EDProducer(
    "PATElectronMVAIDEmbedder",
    electronMVAIDNOIPcfg,
    src = cms.InputTag("fixme"),
    ebRecHits = cms.InputTag("reducedEcalRecHitsEB"),
    eeRecHits = cms.InputTag("reducedEcalRecHitsEE"),
    srcVertices = cms.InputTag("selectedPrimaryVertex"),
    maxDZ = cms.double(0.2),
    maxDB = cms.double(0.045),
)

patElectronMVAIDEmbedder2012 = cms.EDProducer(
    "PATElectronMVAIDEmbedder",
    electronMVAIDTrig2012,
    src = cms.InputTag("fixme"),
    ebRecHits = cms.InputTag("reducedEcalRecHitsEB"),
    eeRecHits = cms.InputTag("reducedEcalRecHitsEE"),
    srcVertices = cms.InputTag("selectedPrimaryVertex"),
    maxDZ = cms.double(1e3),
    maxDB = cms.double(1e3),
)
