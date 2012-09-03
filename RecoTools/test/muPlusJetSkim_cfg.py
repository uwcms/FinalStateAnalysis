'''

Select ~good reconstructed mu+jet events.

Muon is isolated, pt > 20

At least one jet, not on top of the muon, with pt > 15.

'''

process = cms.Process("SKIM")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2012C/SingleMu/AOD/PromptReco-v1/000/198/230/0245B81C-BBC7-E111-8D0E-E0CB4E55365C.root'
    )
)

process.load("FinalStateAnalysis.RecoTools.triggerSkims_cfi")

process.muPlusJetSkim = cms.Path(process.muPlusJetSeq)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('skim.root'),
    outputCommands = cms.untracked.vstring('keep *_*_*_*',
                                           'drop *_*_*_SKIM'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents=cms.vstring("muPlusJetSkim")
    )
)

process.e = cms.EndPath(process.out)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))


# Tell the framework to shut up!
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 300
