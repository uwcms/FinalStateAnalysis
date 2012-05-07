#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    ewkSkim=1,    # Apply EWK skim conditions
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
    dataset='Fall11',
)

files = [
    "root://cmsxrootd.hep.wisc.edu//store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/FEEE3638-F297-E011-AAF8-00304867BEC0.root",
    "root://cmsxrootd.hep.wisc.edu//store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/FCFD87D7-9E98-E011-BDA2-0018F3D09642.root",
    "root://cmsxrootd.hep.wisc.edu//store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/FCFB9DE1-8598-E011-BE64-003048679076.root",
    "root://cmsxrootd.hep.wisc.edu//store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/FAD1CEE7-7A98-E011-89A0-001A92971B7E.root",
    "root://cmsxrootd.hep.wisc.edu//store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/FAA9FD72-E497-E011-A542-001A92971BC8.root",
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
        SelectEvents = cms.vstring('p',)
    ),
    outputCommands = cms.untracked.vstring(output_command)
)

# Configure the pat tuple
import FinalStateAnalysis.PatTools.patTupleProduction as tuplizer
tuplize, output_commands = tuplizer.configurePatTuple(
    process, isMC=options.isMC, xSec=options.xSec, xSecErr=options.xSecErr,
    puTag=options.puTag, dataset=options.dataset,
)

for command in output_commands:
    if not command.startswith('drop') and not command.startswith('keep'):
        process.out.outputCommands.append('keep %s' % command)
    else:
        process.out.outputCommands.append(command)

process.GlobalTag.globaltag = cms.string(options.globalTag)

if options.ewkSkim:
    process.load("FinalStateAnalysis.RecoTools.ewkSkim_cfi")
    tuplize.insert(0, process.ewkSkimSequence)

# Count events at the beginning of the pat tuplization
process.load("FinalStateAnalysis.RecoTools.eventCount_cfi")
process.load("FinalStateAnalysis.RecoTools.dqmEventCount_cfi")
tuplize.insert(0, process.eventCount)
tuplize.insert(0, process.dqmEventCount)

process.p = cms.Path(tuplize)

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

process.outpath = cms.EndPath(process.MEtoEDMConverter*process.out)

# Tell the framework to shut up!
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

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
        paths = cms.untracked.vstring('p')
    )

if options.keepAll:
    # Optionally keep all output
    process.out.outputCommands.append('keep *')

