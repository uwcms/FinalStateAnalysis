'''

CFG file to make all Higgs ntuples

You can turn off different ntuples by passing option=0 using one of:

    makeH2Tau (em, et, and mt)
    makeTNP (ee & mm)
    makeTrilepton (emt, mmt, eet, emm, mmm)
    makeQuad (a bunch for 2l2tau)
    make4L (eeee, eemm, mmmm)

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
    make4L=1,
    dump=0, # If one, dump process python to stdout
    rerunFSA=0, # If one, rebuild the PAT FSA events
    verbose=0, # If one print out the TimeReport
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

# If desired, apply a luminosity mask
if options.lumiMask:
    print "Applying LumiMask from", options.lumiMask
    process.source.lumisToProcess = options.buildPoolSourceLumiMask()

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options.outputFile)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

process.schedule = cms.Schedule(
)

# Check if we want to rerun creation of the FSA objects
if options.rerunFSA:
    print "Rebuilding FS composite objects"
    # Drop the input ones, just to make sure we aren't screwing anything up
    # fixme
    process.buildFSASeq = cms.Sequence()
    from FinalStateAnalysis.PatTools.patFinalStateProducers \
            import produce_final_states
    # Which collections are used to build the final states
    fs_daughter_inputs = {
        'electrons' : 'cleanPatElectrons',
        'muons' : 'cleanPatMuons',
        'taus' : 'cleanPatTaus',
        'jets' : 'selectedPatJets',
        'met' : 'systematicsMET',
    }
    # Eventually, set buildFSAEvent to False, currently working around bug
    # in pat tuples.
    produce_final_states(process, fs_daughter_inputs, [], process.buildFSASeq,
                         'puTagDoesntMatter', buildFSAEvent='eFix',
                         noTracks=True)
    process.buildFSAPath = cms.Path(process.buildFSASeq)
    process.schedule.append(process.buildFSAPath)

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
    add_quad_ntuples(process, process.schedule, do_zz=False, do_zh=True)

if options.make4L:
    add_quad_ntuples(process, process.schedule, do_zh=False, do_zz=True)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

if options.verbose:
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if options.dump:
    print process.dumpPython()
