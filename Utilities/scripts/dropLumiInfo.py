#!/usr/bin/env cmsRun

'''
Drops the stupid run and lumi information from skim files,
as it can be ~100MB in very tight skims.

Usage: ./dropLumiInfo.py inputFile=input_file outputFile=output_file

'''

import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')

options.parseArguments()

process = cms.Process("SlimLumi")
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring (options.inputFiles),
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32 (options.maxEvents)
)

process.Out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string (options.outputFile),
    outputCommands = cms.untracked.vstring(
        'keep *',
        'drop LumiDetails_lumiProducer_*_*',
        'drop LumiSummary_lumiProducer_*_*',
        'drop RunSummary_lumiProducer_*_*',
        'drop *_MEtoEDMConverter_*_*',
    )
)

process.end = cms.EndPath(process.Out)
