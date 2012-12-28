import FWCore.ParameterSet.Config as cms

weightFileBase = "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/"
weightFiles = ["ElectronIDMVA_Trig_V4_EtaBin0LowPt_V4_BDTG.weights.xml.gz",
               "ElectronIDMVA_Trig_V4_EtaBin1LowPt_V4_BDTG.weights.xml.gz",
               "ElectronIDMVA_Trig_V4_EtaBin2LowPt_V4_BDTG.weights.xml.gz",
               "ElectronIDMVA_Trig_V4_EtaBin0HighPt_V4_BDTG.weights.xml.gz",
               "ElectronIDMVA_Trig_V4_EtaBin1HighPt_V4_BDTG.weights.xml.gz",
               "ElectronIDMVA_Trig_V4_EtaBin2HighPt_V4_BDTG.weights.xml.gz"]
fullNames = [weightFileBase+file for file in weightFiles]

mvaTrigIDISOV0 = cms.EDFilter(
    "ElectronIdMVAProducer",
    verbose = cms.untracked.bool(False),
    vertexTag = cms.InputTag('offlinePrimaryVertices'),
    electronTag = cms.InputTag('gsfElectrons'),
    reducedEBRecHitCollection = cms.InputTag('reducedEcalRecHitsEB'),
    reducedEERecHitCollection = cms.InputTag('reducedEcalRecHitsEE'),
    method = cms.string("BDT"),
    mvaWeightFile = cms.vstring(fullNames),
    isISISO=cms.untracked.bool(True),
    Trig = cms.bool(True),
)
