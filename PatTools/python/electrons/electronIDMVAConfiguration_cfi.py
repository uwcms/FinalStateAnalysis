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
