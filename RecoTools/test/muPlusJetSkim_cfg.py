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
        '/store/data/Run2012B/SingleMu/AOD/PromptReco-v1/000/193/840/5693C530-1E9C-E111-9230-002481E0D646.root'
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
