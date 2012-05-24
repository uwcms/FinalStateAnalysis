#!/usr/bin/env cmsRun

# Dump the trigger to STDOUT

import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

import os

options = VarParsing ('analysis')

# add a list of strings for events to process
options.register ('eventsToProcess',
                  '',
                  VarParsing.multiplicity.list,
                  VarParsing.varType.string,
                  "Events to process")

options.register ('process',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name")

options.register ('gt',
                  '%s' % os.environ['datagt'],
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Global Tag")

options.parseArguments()

process = cms.Process("DumpTrigger")
process.source = cms.Source (
    "PoolSource",
    fileNames = cms.untracked.vstring (options.inputFiles),
)

if options.eventsToProcess:
    process.source.eventsToProcess = \
            cms.untracked.VEventRange (options.eventsToProcess)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32 (options.maxEvents)
)

process.patTrigger = cms.EDProducer(
    "PATTriggerProducer",
    onlyStandAlone = cms.bool(False),
    processName = cms.string(options.process)
)

process.patTriggerEvent = cms.EDProducer(
    "PATTriggerEventProducer",
    processName = cms.string(options.process),
    patTriggerMatches = cms.VInputTag(),
)


process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
try:
    from Configuration.PyReleaseValidation.autoCond import autoCond
except ImportError:
    # Moved in 52X
    from Configuration.AlCA.autoCond import autoCond

process.GlobalTag.globaltag = options.gt


process.dumpTrigger = cms.EDAnalyzer(
    "DumpTriggerResults",
    src = cms.InputTag("patTriggerEvent"),
)

process.dump = cms.EDAnalyzer("EventContentAnalyzer")

process.p = cms.Path(
    process.patTrigger
    * process.patTriggerEvent
    #* process.dump
    * process.dumpTrigger
)
