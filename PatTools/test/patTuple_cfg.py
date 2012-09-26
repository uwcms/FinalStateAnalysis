#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.cfgcleaner as cfgcleaner
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
from FinalStateAnalysis.Utilities.version import fsa_version, repo_status
import os
import time

options = TauVarParsing.TauVarParsing(
    xSec = -999.0,
    xSecErr = 0.0,
    skipEvents=0, # For debugging
    keepEverything=0,
    reportEvery=2000,
    puTag='unknown',
    verbose=0, # Print out summary table at end
    profile=0, # Enabling profiling
    keepAll=0, # Don't drop any event content
    # Used for the EGamma electron calibration
    # See https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaElectronEnergyScale
    dataset='Prompt',
	dumpCfg='', #used for crab
    clean = 1,
    embedded=0, # If running on embedded samples, set to 1
)

files = [
    "root://cmsxrootd.hep.wisc.edu//store/data/Run2012A/DoubleMu/AOD/PromptReco-v1/000/190/456/D0478E94-0681-E111-82A4-0019B9F72F97.root"
]
for file in files:
    options.inputFiles = file

options.parseArguments()

process = cms.Process("TUPLE")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
)
# If data, apply a luminosity mask
if not options.isMC and options.lumiMask:
    print "Applying LumiMask from", options.lumiMask
    process.source.lumisToProcess = options.buildPoolSourceLumiMask()

# Check if we only want to process a few events
if options.eventsToProcess:
    process.source.eventsToProcess = \
            cms.untracked.VEventRange(options.eventsToProcess)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

output_command = 'drop *'
if options.keepEverything:
    output_command = 'keep *'

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    # Drop per-event meta data from dropped objects
    dropMetaData = cms.untracked.string("ALL"),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('fixme')
    ),
    outputCommands = cms.untracked.vstring(output_command)
)

# Configure the pat tuple
import FinalStateAnalysis.PatTools.patTupleProduction as tuplizer
tuplize, output_commands = tuplizer.configurePatTuple(
    process, isMC=options.isMC, xSec=options.xSec, xSecErr=options.xSecErr,
    puTag=options.puTag, dataset=options.dataset,
    embedded=options.embedded,
)

if options.globalTag == "":
    raise RuntimeError("Global tag not specified!  Try sourcing environment.sh\n")

process.GlobalTag.globaltag = cms.string(options.globalTag)

# Count events at the beginning of the pat tuplization
process.load("FinalStateAnalysis.RecoTools.eventCount_cfi")
process.load("FinalStateAnalysis.RecoTools.dqmEventCount_cfi")

# Hack meta information about this PAT tuple in the provenance.
process.eventCount.uwMeta = cms.PSet(
    # The git commit
    commit = cms.string(fsa_version()),
    user = cms.string(os.environ['LOGNAME']),
    date = cms.string(time.strftime("%d %b %Y %H:%M:%S +0000", time.gmtime())),
)


process.schedule = cms.Schedule()

# Load all of our skim paths
process.load("FinalStateAnalysis.RecoTools.uwSkims_cfi")
# PAT tuplize all skim paths
for skim_path in process.skimConfig.paths:
    print "Building skim path:", skim_path
    the_path = getattr(process, skim_path)
    # Count every event, even the ones that fail the skim
    the_path.insert(0, process.eventCount)
    if options.isMC and not options.embedded:
        the_path.insert(0, process.dqmEventCount)
    the_path += process.tuplize
    process.schedule.append(the_path)
process.out.SelectEvents.SelectEvents = process.skimConfig.paths
output_commands.append('*_dqmEventCount_*_*')
output_commands.append('*_eventCount_*_*')
output_commands.append('*_MEtoEDMConverter_*_*')

# Setup keep/drops
for command in output_commands:
    if not command.startswith('drop') and not command.startswith('keep'):
        process.out.outputCommands.append('keep %s' % command)
    else:
        process.out.outputCommands.append(command)

# Save DQM stuff created during pat tuplization
process.MEtoEDMConverter = cms.EDProducer(
    "MEtoEDMConverter",
    Name = cms.untracked.string('MEtoEDMConverter'),
    Verbosity = cms.untracked.int32(0), # 0 provides no output
    # 1 provides basic output
    # 2 provide more detailed output
    Frequency = cms.untracked.int32(50),
    MEPathToSave = cms.untracked.string(''),
    deleteAfterCopy = cms.untracked.bool(True)
)

process.outpath = cms.EndPath(
    process.MEtoEDMConverter*
    process.out)
process.schedule.append(process.outpath)

# Tell the framework to shut up!
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

if options.keepAll:
    # Optionally keep all output
    process.out.outputCommands.append('keep *')

if options.clean:
    print "Cleaning up the cruft!"
    unrun, unused, killed = cfgcleaner.clean_cruft(
        process, process.out.outputCommands.value())
    print "Removed %i unrun and %i unused modules!" % (len(unrun), len(unused))

################################################################################
### DEBUG options ##############################################################
################################################################################

if options.verbose:
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if options.profile:
    # From https://twiki.cern.ch/twiki/bin/viewauth/CMS/MemoUnixPatrick#Timing_profiling_avec_valgrind
    # Use with maxEvents=10 or so
    # And  valgrind --tool=callgrind --combine-dumps=yes --instr-atstart=no --dump-instr=yes --separate-recs=1 cmsRun ...
    process.ProfilerService = cms.Service (
        "ProfilerService",
        firstEvent = cms.untracked.int32(15),
        lastEvent = cms.untracked.int32(100),
        paths = cms.untracked.vstring('muTauPath')
    )

if options.dumpCfg:
	dump_cfg=open(options.dumpCfg,'w')
	dump_cfg.write(process.dumpPython())

