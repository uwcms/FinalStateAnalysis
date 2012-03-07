'''

Make Higgs2Tau ntuples (mu-tau, e-tau, e-mu)

'''

import FWCore.ParameterSet.Config as cms

process = cms.Process("TrileptonNtuple")

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
    puScenario='S4',
    saveSkim=0,
    reportEvery=100,
)

options.outputFile="h2tau.root"
options.parseArguments()

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
    #lumisToProcess = options.buildPoolSourceLumiMask()
)

if options.eventsToProcess:
    process.source.eventsToProcess = cms.untracked.VEventRange(
        options.eventsToProcess)

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options.outputFile)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

process.load("FinalStateAnalysis.Higgs.et_ntuple")
process.load("FinalStateAnalysis.Higgs.em_ntuple")
process.load("FinalStateAnalysis.Higgs.mt_ntuple")

process.etaupath = cms.Path(process.etau)
process.emupath = cms.Path(process.emu)
process.mutaupath = cms.Path(process.mutau)

process.schedule = cms.Schedule(
    process.etaupath,
    process.mutaupath,
    process.emupath,
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
