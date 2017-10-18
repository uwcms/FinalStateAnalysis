import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.PatTools.electrons.electronIDMVAConfiguration_cfi \
        import electronMVAIDNOIPcfg

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
