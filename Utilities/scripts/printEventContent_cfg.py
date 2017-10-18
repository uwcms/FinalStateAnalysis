#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing

process = cms.Process("USER")
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing

options = TauVarParsing.TauVarParsing()

options.parseArguments()

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")

process.p = cms.Path(process.printEventContent)

process.schedule = cms.Schedule(
    process.p
)
