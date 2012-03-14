'''

CFG file to make all Higgs ntuples

You can turn off different ntuples by passing option=0 using one of:

    makeH2Tau (em, et, and mt)
    makeTNP (ee & mm)
    makeTrilepton (emt, mmt, eet, emm, mmm)
    makeQuad (a bunch)

'''

import FWCore.ParameterSet.Config as cms

process = cms.Process("TrileptonNtuple")

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
    puScenario='S4',
    saveSkim=0,
    reportEvery=100,
    makeH2Tau=1,
    makeTNP=1,
    makeTrilepton=1,
    makeQuad=1,
)

options.outputFile="higgs.root"
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

process.schedule = cms.Schedule(
)

from FinalStateAnalysis.Higgs.tnp_ntuples_cfi import add_tnp_ntuples
from FinalStateAnalysis.Higgs.h2tau_ntuples_cfi import add_h2tau_ntuples
from FinalStateAnalysis.Higgs.trilepton_ntuples_cfi import add_trilepton_ntuples
from FinalStateAnalysis.Higgs.quad_ntuples_cfi import add_quad_ntuples

if options.makeH2Tau:
    add_h2tau_ntuples(process, process.schedule)

if options.makeTNP:
    add_tnp_ntuples(process, process.schedule)

if options.makeTrilepton:
    add_trilepton_ntuples(process, process.schedule)

if options.makeQuad:
    add_quad_ntuples(process, process.schedule)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
