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

skipEvents=0 - events to skip (for debugging)
maxEvents=-1 - events to run on
rerunMCMatch=0 - rerun MC matching
eventView=0 - make a row in the ntuple correspond to an event
instead of a final state in an event.
passThru=0 - turn off any preselection/skim
dump=0     - if one, dump process python to stdout
rerunFSA=0 - regenerate PATFinalState dataformats
verbose=0 - print out timing information
noPhotons=0 - don't build things which depend on photons.
rerunMVAMET=0 - rerun the MVAMET algorithm
svFit=1 - run the SVfit on appropriate pairs
rerunQGJetID=0 - rerun the quark-gluon JetID
runNewElectronMVAID=0 - run the new electron MVAID
rerunJets=0   - rerun with new jet energy corrections
useMiniAOD=0 - run on miniAOD rather than UW PATTuples
use25ns=0 - run on 25 ns miniAOD (50 ns default)
runDQM=0 - run over single object final states to test all object properties (wont check diobject properties)


'''

import FWCore.ParameterSet.Config as cms
import os
from FinalStateAnalysis.NtupleTools.hzg_sync_mod import set_passthru
from FinalStateAnalysis.NtupleTools.ntuple_builder import \
    make_ntuple, add_ntuple
from FinalStateAnalysis.Utilities.version import cmssw_major_version, \
    cmssw_minor_version
from FinalStateAnalysis.NtupleTools.rerun_matchers import rerun_matchers
from FinalStateAnalysis.NtupleTools.rerun_QGJetID import rerun_QGJetID
from FinalStateAnalysis.NtupleTools.rerun_Jets import rerun_jets
import PhysicsTools.PatAlgos.tools.helpers as helpers

process = cms.Process("Ntuples")

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0,  # Start at an event offset (for debugging)
    reportEvery=100,
    channels='mm,mjj,mj',
    rerunMCMatch=False,
    eventView=0,  # Switch between final state view (0) and event view (1)
    passThru=0,  # Turn off preselections
    dump=0,  # If one, dump process python to stdout
    rerunFSA=1,  # If one, rebuild the PAT FSA events
    verbose=0,  # If one print out the TimeReport
    noPhotons=0,  # If one, don't assume that photons are in the PAT tuples.
    svFit=0,  # If one, SVfit appropriate lepton pairs.
    zzMode=False,
    rochCor="",
    eleCor="",
    rerunQGJetID=0,  # If one reruns the quark-gluon JetID
    runNewElectronMVAID=0,  # If one runs the new electron MVAID
    rerunMVAMET=0,  # If one, (re)build the MVA MET
    rerunJets=0,
    dblhMode=False, # For double-charged Higgs analysis
    runTauSpinner=0,
    GlobalTag="",
    useMiniAOD=0,
    use25ns=0,
    runDQM=0,
)

options.register(
    'skimCuts',
    '',
    TauVarParsing.TauVarParsing.multiplicity.list,
    TauVarParsing.TauVarParsing.varType.string,
    'additional cuts to impose on the NTuple'
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
    elif cmssw_major_version() == 7:
        process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    else:
        process.load('Configuration.StandardSequences.GeometryIdeal_cff')

    if cmssw_major_version() == 7:
        process.load('Configuration.StandardSequences.MagneticField_38T_cff')
    else:
        process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load(
        'Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

    # Need the global tag for geometry etc.
    envvar = 'mcgt' if options.isMC else 'datagt'
    GT = {'mcgt': 'START53_V27::All', 'datagt': 'FT53_V21A_AN6::All'}
    if options.useMiniAOD:
        if options.use25ns:
            GT['mcgt'] = 'PLS170_V7AN1::All'
        else:
            GT['mcgt'] = 'PLS170_V6AN1::All'
        GT['datagt'] = 'GR_70_V2_AN1::All'


    if options.GlobalTag:
        process.GlobalTag.globaltag = cms.string(options.GlobalTag)
    else:
        try:
            process.GlobalTag.globaltag = cms.string(os.environ[envvar])
        except KeyError:
            print 'Warning: GlobalTag not defined in environment. Using default.'
            process.GlobalTag.globaltag = cms.string(GT[envvar])
        if options.useMiniAOD:
            process.GlobalTag.globaltag = cms.string(GT[envvar])

    print 'Using globalTag: %s' % process.GlobalTag.globaltag

    if options.useMiniAOD:
        mvamet_collection = 'slimmedMETs'
    else:
        mvamet_collection = 'systematicsMETMVA'

    # Make a version with the MVA MET reconstruction method
    # Works only if we rerun the FSA!
    if options.rerunMVAMET:
        process.load("FinalStateAnalysis.PatTools.met.mvaMetOnPatTuple_cff")
        if options.useMiniAOD:
            process.isotaus.src = "slimmedTaus"
            mvamet_collection = "slimmedMETs"
        else:
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
    if options.useMiniAOD:
        fs_daughter_inputs = {
            'electrons': 'slimmedElectrons',
            'muons': 'slimmedMuons',
            'taus': 'slimmedTaus',
            'photons': 'slimmedPhotons',
            'jets': 'slimmedJets',
            'pfmet': 'slimmedMETs',         # only one MET in miniAOD
            'mvamet': mvamet_collection,
            'fsr': 'slimmedPhotons',        # not available?
        }
    else:
        fs_daughter_inputs = {
            'electrons': 'cleanPatElectrons',
            'muons': 'cleanPatMuons',
            'taus': 'cleanPatTaus',
            'photons': 'cleanPatPhotons',
            'jets': 'selectedPatJets',
#            'jets':  'selectedPatJetsAK5chsPF',
            'pfmet': 'systematicsMET',
            'mvamet': mvamet_collection,
            'fsr': 'boostedFsrPhotons',
        }
    #re run the MC matching, if requested
    if options.rerunMCMatch:
        print 'doing rematching!'
        rerun_matchers(process)
        process.schedule.append(process.rerunMCMatchPath)
        fs_daughter_inputs['electrons'] = 'cleanPatElectronsRematched'
        fs_daughter_inputs['muons'] = 'cleanPatMuonsRematched'
        fs_daughter_inputs['taus'] = 'cleanPatTausRematched'
        fs_daughter_inputs['photons'] = 'photonParentage'
#        fs_daughter_inputs['jets'] = 'selectedPatJetsRematched'
        fs_daughter_inputs['jets'] = 'selectedPatJetsAK5chsPFRematched'

    if options.runTauSpinner:
        process.load('FinalStateAnalysis.RecoTools.TauSpinner_cfi')
        process.TauSpinnerPath = cms.Path( process.TauSpinnerReco )
        process.schedule.append(process.TauSpinnerPath)
        fs_daughter_inputs['extraWeights'] = cms.PSet(
            tauSpinnerWeight = cms.InputTag("TauSpinnerReco", "TauSpinnerWT") 
        )

    if options.runTauSpinner:
        process.load('FinalStateAnalysis.RecoTools.TauSpinner_cfi')
        process.TauSpinnerPath = cms.Path( process.TauSpinnerReco )
        process.schedule.append(process.TauSpinnerPath)
        fs_daughter_inputs['extraWeights'] = cms.PSet(
            tauSpinnerWeight = cms.InputTag("TauSpinnerReco", "TauSpinnerWT") 
        )

    if options.rerunQGJetID:
        process.schedule.append(
            rerun_QGJetID(process, fs_daughter_inputs)
        )

    if options.rerunJets:
        process.schedule.append(rerun_jets(process))

    if options.runNewElectronMVAID:
        process.load("FinalStateAnalysis.PatTools."
                     "electrons.patElectronSummer13MVAID_cfi")
        helpers.massSearchReplaceAnyInputTag(
            process.runAndEmbedSummer13Id,
            'fixme',
            fs_daughter_inputs['electrons'])
        fs_daughter_inputs['electrons'] = 'patElectrons2013MVAID'
        process.runNewElectronMVAID = cms.Path(process.runAndEmbedSummer13Id)
        process.schedule.append(process.runNewElectronMVAID)

    # embed some things we need that arent in miniAOD yet (like some ids)
    output_commands = []
    if options.useMiniAOD:
        bx = '25ns' if options.use25ns else '50ns'
        process.miniPatElectrons = cms.EDProducer(
            "MiniAODElectronIDEmbedder",
            src=cms.InputTag(fs_daughter_inputs['electrons']),
            MVAId=cms.InputTag("mvaTrigV0CSA14","","addMVAid"),
            vertices=cms.InputTag("offlineSlimmedPrimaryVertices"),
            convcollection=cms.InputTag("reducedEgamma:reducedConversions"),
            beamspot=cms.InputTag("offlineBeamSpot"),
            bunchspacing=cms.untracked.string(bx)
        )
        output_commands.append('*_miniPatElectrons_*_*')
        fs_daughter_inputs['electrons'] = "miniPatElectrons"

        process.miniPatJets = cms.EDProducer(
            "MiniJetIdEmbedder",
            src=cms.InputTag(fs_daughter_inputs['jets'])
        )
        output_commands.append('*_miniPatJets_*_*')
        fs_daughter_inputs['jets'] = 'miniPatJets'

        process.runMiniAODObjectEmbedding = cms.Path(
            process.miniPatElectrons+
            process.miniPatJets
        )
        process.schedule.append(process.runMiniAODObjectEmbedding)

        process.miniMuonsEmbedIp = cms.EDProducer(
            "MiniAODMuonIpEmbedder",
            src = cms.InputTag(fs_daughter_inputs['muons']),
            vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        )
        output_commands.append('*_miniMuonsEmbedIp_*_*')
        fs_daughter_inputs['muons'] = 'miniMuonsEmbedIp'

        process.miniElectronsEmbedIp = cms.EDProducer(
            "MiniAODElectronIpEmbedder",
            src = cms.InputTag(fs_daughter_inputs['electrons']),
            vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        )
        output_commands.append('*_miniElectronsEmbedIp_*_*')
        fs_daughter_inputs['electrons'] = 'miniElectronsEmbedIp'

        process.runMiniAODLeptonIpEmbedding = cms.Path(
            process.miniMuonsEmbedIp+
            process.miniElectronsEmbedIp
        )
        process.schedule.append(process.runMiniAODLeptonIpEmbedding)
        

    # Eventually, set buildFSAEvent to False, currently working around bug
    # in pat tuples.
    produce_final_states(process, fs_daughter_inputs, output_commands, process.buildFSASeq,
                         'puTagDoesntMatter', buildFSAEvent=True,
                         noTracks=True, noPhotons=options.noPhotons,
                         zzMode=options.zzMode, rochCor=options.rochCor,
                         eleCor=options.eleCor, useMiniAOD=options.useMiniAOD, 
                         use25ns=options.use25ns)
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
    'llt': 'emt, mmt, eet, mmm, emm, mm, ee, em',
    'zg': 'mmg, eeg',
    'zgxtra': 'mgg, emg, egg',
    'dqm': 'e,m,t,g,j',
}

# run dqm
if options.runDQM: options.channels = 'dqm'

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
    zz_mode = (final_state in ['mmmm', 'eeee', 'eemm'])
    analyzer = make_ntuple(*final_state, zz_mode=options.zzMode,
                            svFit=options.svFit, dblhMode=options.dblhMode,
                            runTauSpinner=options.runTauSpinner, 
                            skimCuts=options.skimCuts,useMiniAOD=options.useMiniAOD)
    add_ntuple(final_state, analyzer, process,
               process.schedule, options.eventView)


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.categories.append('FSAEventMissingProduct')
process.MessageLogger.categories.append('UndefinedPreselectionInfo')
process.MessageLogger.categories.append('GsfElectronAlgo')

# Don't go nuts if there are a lot of missing products.
process.MessageLogger.cerr.FSAEventMissingProduct = cms.untracked.PSet(
    limit=cms.untracked.int32(10)
)
# process.MessageLogger.suppresssWarning = cms.untracked.vstring("GsfElectronAlgo","UndefinedPreselectionInfo")
process.MessageLogger.cerr.GsfElectronAlgo = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)
process.MessageLogger.cerr.UndefinedPreselectionInfo = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)

if options.verbose:
    process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))
if options.passThru:
    set_passthru(process)

if options.dump:
    print process.dumpPython()
