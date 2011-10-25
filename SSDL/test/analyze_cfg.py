import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
)

options.outputFile="vhiggs.root"
options.parseArguments()

process = cms.Process("VHiggsAna2")

# Input in FWLITE mode
process.fwliteInput = cms.PSet(fileNames = cms.vstring(options.inputFiles))
# Input in FWK mode
process.source = cms.Source(
    "PoolSource", fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
)

plots_filename = options.outputFile.replace('.root', '.plots.root')
process.fwliteOutput = cms.PSet(fileName = cms.string(options.outputFile))
process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options.outputFile)
)

process.steering = cms.PSet(
    analyzers = cms.vstring(
        'mt',
    ),
    reportAfter = cms.uint32(1000),
    ignored_cuts = cms.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

# Common among all analyzers
process.common = cms.PSet(
    weights = cms.vstring(
        'weight("3bx_S42011A")'
    ),
    evtSrc = cms.InputTag("patFinalStateEventProducer"),
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),
)

process.steering.ignored_cuts = cms.vstring()

from FinalStateAnalysis.SSDL.selectionMT import selections as selectionsMT
from FinalStateAnalysis.SSDL.selectionMT import plots as plotsMT

process.mt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsMT,
        ),
        selections = selectionsMT,
    )
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("FinalStateAnalysis.RecoTools.eventCount_cfi")
process.count = cms.Path(process.eventCount)
process.schedule = cms.Schedule(process.count)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile.replace('.root', '.edm.root')),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring()
    ),
    outputCommands = cms.untracked.vstring('keep *')
)
process.end = cms.EndPath(process.out)

process.ProfilerService = cms.Service (
    "ProfilerService",
    firstEvent = cms.untracked.int32(3),
    lastEvent = cms.untracked.int32(12),
    paths = cms.untracked.vstring('emtPath')
)

# Build the filter selectors for skimming events.
for channel in process.steering.analyzers:
    # Build the filter
    filter = cms.EDFilter(
        "PATFinalStateAnalysisFilter",
        getattr(process, channel)
    )
    setattr(process, channel + "Filter", filter)
    path = cms.Path(filter)
    setattr(process, channel + "Path", path)
    process.schedule.append(path)
    process.out.SelectEvents.SelectEvents.append(channel + "Path")

process.schedule.append(process.end)
