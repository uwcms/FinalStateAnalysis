#!/usr/bin/env cmsRun
'''

Ntuple Generation
=================

Generates the ntuples for a given list of final state generation.

Usage:

    ./make_ntuples_cfg.py channels="mt,em,mm,eemm" [options]

There are some additional pre-defined groups of channels which are expanded
for your convenience::

    zh = eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt,
    zz = eeee, eemm, mmmm,
    zgg = eegg, mmgg
    llt = emt, mmt, eet, mmm, emm
    zg = mmg,eeg
    zgxtra = mgg, emg, egg,

The available options (which are set to zero or one) are::

    skipEvents=0            - events to skip (for debugging)
    maxEvents=-1            - events to run on
    rerunMCMatch=0          - rerun MC matching
    eventView=0             - make a row in the ntuple correspond to an event
                              instead of a final state in an event.
    passThru=0              - turn off any preselection/skim
    rerunFSA=0              - regenerate PATFinalState dataformats
    verbose=0               - print out timing information
    noPhotons=0             - don't build things which depend on photons.

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.NtupleTools.hzg_sync_mod import set_passthru
from FinalStateAnalysis.NtupleTools.ntuple_builder import \
    make_ntuple, add_ntuple
from FinalStateAnalysis.Utilities.version import cmssw_major_version, \
    cmssw_minor_version
from FinalStateAnalysis.NtupleTools.rerun_matchers import rerun_matchers

process = cms.Process("Ntuples")

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0,  # Start at an event offset (for debugging)
    reportEvery=100,
    channels='mm',
    rerunMCMatch=False,
    eventView=0,  # Switch between final state view (0) and event view (1)
    passThru=0,  # Turn off preselections
    dump=0,  # If one, dump process python to stdout
    rerunFSA=0,  # If one, rebuild the PAT FSA events
    verbose=0,  # If one print out the TimeReport
    noPhotons=0,  # If one, don't assume that photons are in the PAT tuples.
    zzMode=False,
    rerunMVAMET=0,  # If one, (re)build the MVA MET
)

options.outputFile = "ntuplize.root"
options.parseArguments()

process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(options.inputFiles),
    skipEvents=cms.untracked.uint32(options.skipEvents),
)


if options.eventsToProcess:
    process.source.eventsToProcess = cms.untracked.VEventRange(
        options.eventsToProcess)

# If desired, apply a luminosity mask
if options.lumiMask:
    print "Applying LumiMask from", options.lumiMask
    process.source.lumisToProcess = options.buildPoolSourceLumiMask()

process.TFileService = cms.Service(
    "TFileService", fileName=cms.string(options.outputFile)
)

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(options.maxEvents))

process.schedule = cms.Schedule()

# Check if we want to rerun creation of the FSA objects
if options.rerunFSA:
    print "Rebuilding FS composite objects"

    #load magfield and geometry (for mass resolution)
    if cmssw_major_version() == 5 and cmssw_minor_version() >= 3:
        process.load('Configuration.Geometry.GeometryIdeal_cff')
    else:
        process.load('Configuration.StandardSequences.GeometryIdeal_cff')

    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load(
        'Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

    # Need the global tag for geometry etc.
    if options.globalTag == "":
        raise RuntimeError("Global tag not specified! "
                           "Try sourcing environment.sh\n")
    else:
        print 'Using globalTag: %s' % options.globalTag
    process.GlobalTag.globaltag = cms.string(options.globalTag)

    mvamet_collection = 'systematicsMETMVA'

    # Make a version with the MVA MET reconstruction method
    # Works only if we rerun the FSA!
    if options.rerunMVAMET:
        process.load("FinalStateAnalysis.PatTools.met.mvaMetOnPatTuple_cff")
        process.isotaus.src = "cleanPatTaus"
        mvamet_collection = "patMEtMVA"
        if not options.isMC:
            process.patMEtMVA.addGenMET = False
        process.mvaMetPath = cms.Path(process.pfMEtMVAsequence)
        process.schedule.append(process.mvaMetPath)
        print "rerunning MVA MET sequence, output collection will be {n}"\
            .format(n=mvamet_collection)

    # Drop the input ones, just to make sure we aren't screwing anything up
    process.buildFSASeq = cms.Sequence()
    from FinalStateAnalysis.PatTools.patFinalStateProducers \
        import produce_final_states
    # Which collections are used to build the final states
    fs_daughter_inputs = {
        'electrons': 'cleanPatElectrons',
        'muons': 'cleanPatMuons',
        'taus': 'cleanPatTaus',
        'photons': 'cleanPatPhotons',
        'jets': 'selectedPatJets',
        'pfmet': 'systematicsMET',
        'mvamet': mvamet_collection,
        'fsr': 'boostedFsrPhotons',
    }
    #re run the MC matching, if requested
    if options.rerunMCMatch:
        rerun_matchers(process)
        process.schedule.append(process.rerunMCMatchPath)
        fs_daughter_inputs['electrons'] = 'cleanPatElectronsRematched'
        fs_daughter_inputs['muons'] = 'cleanPatMuonsRematched'
        fs_daughter_inputs['taus'] = 'cleanPatTausRematched'
        fs_daughter_inputs['photons'] = 'cleanPatPhotonsRematched'
        fs_daughter_inputs['jets'] = 'selectedPatJetsRematched'

    # Eventually, set buildFSAEvent to False, currently working around bug
    # in pat tuples.
    produce_final_states(process, fs_daughter_inputs, [], process.buildFSASeq,
                         'puTagDoesntMatter', buildFSAEvent=True,
                         noTracks=True, noPhotons=options.noPhotons, zzMode=options.zzMode)
    process.buildFSAPath = cms.Path(process.buildFSASeq)
    # Don't crash if some products are missing (like tracks)
    process.patFinalStateEventProducer.forbidMissing = cms.bool(False)
    process.schedule.append(process.buildFSAPath)
    # Drop the old stuff.
    process.source.inputCommands = cms.untracked.vstring(
        'keep *',
        'drop PATFinalStatesOwned_finalState*_*_*',
        'drop *_patFinalStateEvent*_*_*'
    )


_FINAL_STATE_GROUPS = {
    'zh': 'eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt',
    'zz': 'eeee, eemm, mmmm',
    'zgg': 'eegg, mmgg',
    'llt': 'emt, mmt, eet, mmm, emm',
    'zg': 'mmg, eeg',
    'zgxtra': 'mgg, emg, egg',
}

# Generate analyzers which build the desired final states.
final_states = [x.strip() for x in options.channels.split(',')]


def expanded_final_states(input):
    for fs in input:
        if fs in _FINAL_STATE_GROUPS:
            for subfs in _FINAL_STATE_GROUPS[fs].split(','):
                yield subfs.strip()
        else:
            yield fs

print "Building ntuple for final states: %s" % ", ".join(final_states)
for final_state in expanded_final_states(final_states):

    zz_mode = ( final_state in ['mmmm','eeee','eemm'] )

    analyzer = make_ntuple(*final_state, zz_mode=zz_mode)
    add_ntuple(final_state, analyzer, process,
               process.schedule, options.eventView)

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.categories.append('FSAEventMissingProduct')

# Don't go nuts if there are a lot of missing products.
process.MessageLogger.cerr.FSAEventMissingProduct = cms.untracked.PSet(
    limit=cms.untracked.int32(10)
)

if options.verbose:
    process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))
if options.passThru:
    set_passthru(process)

if options.dump:
    print process.dumpPython()
