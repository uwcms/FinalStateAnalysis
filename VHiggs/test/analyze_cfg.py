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
        #'eee',
        'eem',
        'eet',
        'emm',
        'emt',
        #'ett',
        #'mmm',
        'mmt',
        #'mtt'
    ),
    reportAfter = cms.uint32(1000),
    ignored_cuts = cms.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

# Common among all analyzers
process.common = cms.PSet(
    weights = cms.VInputTag(
        cms.InputTag("lumiWeights", "3bx")
    ),
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),
)

process.steering.ignored_cuts = cms.vstring(
    "*_BJetVeto", "*RelIso*", "*Veto*", "*CombinedIsolation*"
)

from FinalStateAnalysis.VHiggs.selectionEEE import selections as selectionsEEE
from FinalStateAnalysis.VHiggs.selectionEEM import selections as selectionsEEM
from FinalStateAnalysis.VHiggs.selectionEET import selections as selectionsEET
from FinalStateAnalysis.VHiggs.selectionEMM import selections as selectionsEMM
from FinalStateAnalysis.VHiggs.selectionEMT import selections as selectionsEMT
from FinalStateAnalysis.VHiggs.selectionETT import selections as selectionsETT
from FinalStateAnalysis.VHiggs.selectionMMM import selections as selectionsMMM
from FinalStateAnalysis.VHiggs.selectionMMT import selections as selectionsMMT
from FinalStateAnalysis.VHiggs.selectionMTT import selections as selectionsMTT

from FinalStateAnalysis.VHiggs.selectionEEE import plots as plotsEEE
from FinalStateAnalysis.VHiggs.selectionEEM import plots as plotsEEM
from FinalStateAnalysis.VHiggs.selectionEET import plots as plotsEET
from FinalStateAnalysis.VHiggs.selectionEMM import plots as plotsEMM
from FinalStateAnalysis.VHiggs.selectionEMT import plots as plotsEMT
from FinalStateAnalysis.VHiggs.selectionETT import plots as plotsETT
from FinalStateAnalysis.VHiggs.selectionMMM import plots as plotsMMM
from FinalStateAnalysis.VHiggs.selectionMMT import plots as plotsMMT
from FinalStateAnalysis.VHiggs.selectionMTT import plots as plotsMTT

process.eee = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecElecElec'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            #plot = plotsEEE,
            plot = cms.PSet(histos=cms.VPSet()),
        ),
        selections = selectionsEEE
    )
)

process.eem = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecElecMu'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(1).pt'),
            take = cms.uint32(5),
            plot = plotsEEM,
        ),
        selections = selectionsEEM
    )
)

process.eet = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecElecTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsEET,
        ),
        selections = selectionsEET
    )
)

process.emm = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecMuMu'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsEMM,
        ),
        selections = selectionsEMM,
    )
)

process.emt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecMuTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsEMT,
        ),
        selections = selectionsEMT,
    )
)

process.ett = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecTauTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsETT,
        ),
        selections = selectionsETT,
    )
)

process.mmm = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuMuMu'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsMMM,
        ),
        selections = selectionsMMM,
    )
)

process.mmt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuMuTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsMMT,
        ),
        selections = selectionsMMT,
    )
)

process.mtt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuTauTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(5),
            plot = plotsMTT,
        ),
        selections = selectionsMTT,
    )
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("FinalStateAnalysis.RecoTools.eventCount_cfi")
process.count = cms.Path(process.eventCount)
process.schedule = cms.Schedule(process.count)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
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
