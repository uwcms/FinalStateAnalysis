import FWCore.ParameterSet.Config as cms

patJetEmbedSmear = cms.EDProducer(
    "PATJetSmearEmbedder",
    src = cms.InputTag("smear"),
    inputFileName = cms.FileInPath(
        "FinalStateAnalysis/PatTools/data/pfJetResolutionMCtoDataCorrLUT.root"),
    lutName = cms.string('pfJetResolutionMCtoDataCorrLUT'),
    smearBy = cms.double(1.0),
    srcGenJets = cms.InputTag("ak5GenJets"),
    dRmaxGenJetMatch = cms.double(0.3),
)
