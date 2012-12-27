import FWCore.ParameterSet.Config as cms

electronMVAIDNOIPcfg = cms.PSet(
    methodName = cms.string("NOIP"),
    Subdet0LowPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/Subdet0LowPt_NoIPInfo_BDTG.weights.xml.gz"
    ),
    Subdet1LowPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/Subdet1LowPt_NoIPInfo_BDTG.weights.xml.gz"
    ),
    Subdet2LowPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/Subdet2LowPt_NoIPInfo_BDTG.weights.xml.gz"
    ),
    Subdet0HighPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/Subdet0HighPt_NoIPInfo_BDTG.weights.xml.gz"
    ),
    Subdet1HighPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/Subdet1HighPt_NoIPInfo_BDTG.weights.xml.gz"
    ),
    Subdet2HighPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/Subdet2HighPt_NoIPInfo_BDTG.weights.xml.gz"
    ),
    mvaType = cms.uint32(1) # No IP infor
)

electronMVAIDTrig2012 = cms.PSet(
    methodName = cms.string("BDT"),
    Subdet0LowPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/ElectronIDMVA_Trig_V4_EtaBin0LowPt_V4_BDTG.weights.xml.gz"
    ),
    Subdet1LowPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/ElectronIDMVA_Trig_V4_EtaBin1LowPt_V4_BDTG.weights.xml.gz"
    ),
    Subdet2LowPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/ElectronIDMVA_Trig_V4_EtaBin2LowPt_V4_BDTG.weights.xml.gz"
    ),
    Subdet0HighPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/ElectronIDMVA_Trig_V4_EtaBin0HighPt_V4_BDTG.weights.xml.gz"
    ),
    Subdet1HighPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/ElectronIDMVA_Trig_V4_EtaBin1HighPt_V4_BDTG.weights.xml.gz"
    ),
    Subdet2HighPtWeights = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/ElectronMVAWeights/ElectronIDMVA_Trig_V4_EtaBin2HighPt_V4_BDTG.weights.xml.gz"
    ),
    mvaType = cms.uint32(3) # triggering electrons 2012
)
