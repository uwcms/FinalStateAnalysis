import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
)

options.outputFile="tnp.root"
options.parseArguments()

process = cms.Process("TauTNP")

# Input in FWLITE mode
process.fwliteInput = cms.PSet(fileNames = cms.vstring(options.inputFiles))
# Input in FWK mode
process.source = cms.Source(
    "PoolSource", fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
)

plots_filename = options.outputFile.replace('.root', '.plots.root')
process.fwliteOutput = cms.PSet(fileName = cms.string(options.outputFile))

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

from FinalStateAnalysis.TagAndProbe.selectionTauTNP_cfi import selections as selectionsMT
from FinalStateAnalysis.TagAndProbe.selectionTauTNP_cfi import plots as plotsMT

process.mt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(1).pt'),
            take = cms.uint32(5),
            plot = plotsMT,
        ),
        selections = selectionsMT,
    )
)
