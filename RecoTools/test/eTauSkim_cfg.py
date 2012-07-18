'''

Select ~good reconstructed e-tau events.

'''

process = cms.Process("SKIM")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2011B/TauPlusX/AOD/PromptReco-v1/000/175/832/9E5E5FA4-35DD-E011-9C06-003048D2C020.root'
    )
)

process.load("FinalStateAnalysis.RecoTools.triggerSkims_cfi")

process.eTauSkim = cms.Path(process.eTauSkimSeq)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('skim.root'),
    outputCommands = cms.untracked.vstring('keep *_*_*_*',
                                           'drop *_*_*_SKIM'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents=cms.vstring("eTauSkim")
    )
)

process.e = cms.EndPath(process.out)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
