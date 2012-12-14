'''

CFG file to make all Higgs ntuples

You can turn on different ntuples by passing option=1 using one of:

    makeH2Tau (em, et, and mt)
    makeDiObject (mm, ee, gg)
    makeTNP (ee & mm)
    makeTrilepton (emt, mmt, eet, emm, mmm)
    makeQuad (a bunch for 2l2tau)
    make4L (eeee, eemm, mmmm)
    makeHZG (eeg, mmg)
    makeTGC (eeg, mmg, eg, mg)
    makeQuartic ( permutations of e mu tau pho... )

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.NtupleTools.hzg_sync_mod import set_passthru
from FinalStateAnalysis.Utilities.version import cmssw_major_version, \
    cmssw_minor_version

process = cms.Process("TrileptonNtuple")

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0,  # Start at an event offset (for debugging)
    puScenario='S4',
    saveSkim=0,
    reportEvery=100,
    makeDiObject=0,
    makeH2Tau=0,
    makeTNP=0,
    makeTrilepton=0,
    makeQuad=0,
    make4L=0,
    makeQuartic=0,
    makeTGC=0,
    makeHZG=0,
    eventView=0, #switch between final state view (0) and event view (1)
    passThru=0, #turn off preselections
    dump=0, # If one, dump process python to stdout
    rerunFSA=0, # If one, rebuild the PAT FSA events
    verbose=0, # If one print out the TimeReport
    noPhotons=0,  # If one, don't assume that photons are in the PAT tuples.
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

    #need the global tag because of the above
    if options.globalTag == "":
        raise RuntimeError("Global tag not specified!"\
                           "Try sourcing environment.sh\n")
    else:
        print 'Using globalTag: %s'%options.globalTag

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
        'mvamet': 'systematicsMETMVA',
    }
    # Eventually, set buildFSAEvent to False, currently working around bug
    # in pat tuples.
    produce_final_states(process, fs_daughter_inputs, [], process.buildFSASeq,
                         'puTagDoesntMatter', buildFSAEvent=True,
                         noTracks=True, noPhotons=options.noPhotons)
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

from FinalStateAnalysis.NtupleTools.tnp_ntuples_cfi import add_tnp_ntuples
from FinalStateAnalysis.NtupleTools.h2tau_ntuples_cfi import add_h2tau_ntuples
from FinalStateAnalysis.NtupleTools.di_object_ntuples_cfi \
     import add_di_object_ntuples
from FinalStateAnalysis.NtupleTools.trilepton_ntuples_cfi \
    import add_trilepton_ntuples
from FinalStateAnalysis.NtupleTools.lepton_photon_ntuples_cfi \
    import add_leptonphoton_ntuples

from FinalStateAnalysis.NtupleTools.quad_ntuples_cfi import add_quad_ntuples

if options.makeDiObject:
    add_di_object_ntuples(process, process.schedule,
                          event_view = options.eventView)

if options.makeH2Tau:
    add_h2tau_ntuples(process, process.schedule, event_view=options.eventView)

if options.makeTNP:
    add_tnp_ntuples(process, process.schedule, event_view=options.eventView)

if options.makeTrilepton:
    add_trilepton_ntuples(
        process, process.schedule, event_view=options.eventView)

if options.makeQuad:
    add_quad_ntuples(process, process.schedule,
                     do_zz=False, do_zh=True,
                     event_view=options.eventView)

if options.make4L:
    add_quad_ntuples(process, process.schedule,
                     do_zh=False, do_zz=True,
                     event_view=options.eventView)

if options.makeHZG:
    add_trilepton_ntuples(process, process.schedule,
                          do_trileptons=False, do_photons=True,
                          event_view=options.eventView)

if options.makeTGC:
    add_leptonphoton_ntuples(process, process.schedule,
                             options.eventView)
    add_trilepton_ntuples(process, process.schedule,
                          do_trileptons=False, do_photons=True,
                          event_view=options.eventView)
if options.makeQuartic:
    add_trilepton_ntuples(process, process.schedule,
                          do_trileptons=True, do_photons=True,
                          event_view=options.eventView)
    add_quad_ntuples(process, process.schedule,
                     do_zh=False, do_zz=False, do_zgg=True,
                     event_view=options.eventView)


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
