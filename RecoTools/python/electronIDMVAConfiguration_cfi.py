import FWCore.ParameterSet.Config as cms

electronMVAIDNOIPcfg = cms.PSet(
    methodName = cms.string("NOIP"),
    Subdet0Pt10To20Weights = cms.FileInPath(
        "FinalStateAnalysis/RecoTools/data/ElectronMVAWeights/Subdet0LowPt_NoIPInfo_BDTG.weights.xml"
    ),
    Subdet1Pt10To20Weights = cms.FileInPath(
        "FinalStateAnalysis/RecoTools/data/ElectronMVAWeights/Subdet1LowPt_NoIPInfo_BDTG.weights.xml"
    ),
    Subdet2Pt10To20Weights = cms.FileInPath(
        "FinalStateAnalysis/RecoTools/data/ElectronMVAWeights/Subdet2LowPt_NoIPInfo_BDTG.weights.xml"
    ),
    Subdet0Pt20toInfWeights = cms.FileInPath(
        "FinalStateAnalysis/RecoTools/data/ElectronMVAWeights/Subdet0HighPt_NoIPInfo_BDTG.weights.xml"
    ),
    Subdet1Pt20toInfWeights = cms.FileInPath(
        "FinalStateAnalysis/RecoTools/data/ElectronMVAWeights/Subdet1HighPt_NoIPInfo_BDTG.weights.xml"
    ),
    Subdet2Pt20toInfWeights = cms.FileInPath(
        "FinalStateAnalysis/RecoTools/data/ElectronMVAWeights/Subdet2HighPt_NoIPInfo_BDTG.weights.xml"
    ),
    type = cms.uint32(1) # No IP infor
)
