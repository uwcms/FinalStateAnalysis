import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.RecoTools.electronIDMVAConfiguration_cfi import \
        electronMVAIDNOIPcfg

patElectronMVAIDEmbedder = cms.EDProducer(
    "PATElectronMVAIDEmbedder",
    electronMVAIDNOIPcfg,
    src = cms.InputTag("fixme"),
    ebRecHits = cms.InputTag("reducedEcalRecHitsEB"),
    eeRecHits = cms.InputTag("reducedEcalRecHitsEE"),
    userLabel = cms.string("MITID"),
)
