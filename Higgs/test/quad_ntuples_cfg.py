'''

Quad final state ntuples

'''

import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing

from FinalStateAnalysis.Higgs.quad_ntuples import make_ntuple

process = cms.Process("TrileptonNtuple")

options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
    puScenario='S4',
    saveSkim=0,
    reportEvery=100,
)

options.outputFile="quad_ntuples.root"
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

process.schedule = cms.Schedule()

final_states = [
    'eeem',
    'eeet',
    'eemm',
    'eemt',
    'eett',
    'emmm',
    'emmt',
    'mmmt',
    'mmtt',
]

for final_state in final_states:
    print "Building %s final state" % final_state
    # build ntuplizer
    analyzer = make_ntuple(final_state[0], final_state[1], final_state[2],
                           final_state[3])
    # Add to process
    setattr(process, final_state, analyzer)
    # Make a path
    p = cms.Path(analyzer)
    setattr(process, final_state + 'path', p)
    process.schedule.append(p)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
