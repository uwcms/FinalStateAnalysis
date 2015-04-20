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
verbose=0 - print out timing information
noPhotons=0 - don't build things which depend on photons.
rerunMVAMET=0 - rerun the MVAMET algorithm
svFit=1 - run the SVfit on appropriate pairs
rerunQGJetID=0 - rerun the quark-gluon JetID
runNewElectronMVAID=0 - run the new electron MVAID
rerunJets=0   - rerun with new jet energy corrections
use25ns=1 - run on 25 ns miniAOD (default, 0 = 50ns)
runDQM=0 - run over single object final states to test all object properties (wont check diobject properties)
hzz=0 - Include FSR contribution a la HZZ4l group, include all ZZ candidates (including alternative lepton pairings).
nExtraJets=0 - Include basic info about this many jets (ordered by pt). Ignored if final state involves jets.
paramFile='' - custom parameter file for ntuple production

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

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0,  # Start at an event offset (for debugging)
    reportEvery=100,
    channels='mm,mjj,mj',
    rerunMCMatch=False,
    eventView=0,  # Switch between final state view (0) and event view (1)
    passThru=0,  # Turn off preselections
    dump=0,  # If one, dump process python to stdout
    verbose=0,  # If one print out the TimeReport
    noPhotons=0,  # If one, don't assume that photons are in the PAT tuples.
    svFit=0,  # If one, SVfit appropriate lepton pairs.
    rochCor="",
    eleCor="",
    rerunQGJetID=0,  # If one reruns the quark-gluon JetID
    runNewElectronMVAID=0,  # If one runs the new electron MVAID
    rerunMVAMET=0,  # If one, (re)build the MVA MET
    rerunJets=0,
    dblhMode=False, # For double-charged Higgs analysis
    runTauSpinner=0,
    GlobalTag="",
    use25ns=1,
    runDQM=0,
    hzz=0,
    paramFile='',
)

options.register(
    'skimCuts',
    '',
    TauVarParsing.TauVarParsing.multiplicity.list,
    TauVarParsing.TauVarParsing.varType.string,
    'additional cuts to impose on the NTuple'
)
options.register(
    'nExtraJets',
    0,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    'Number of pt-ordered jets to keep some info about. Ignored if final state involves jets.',
)


options.outputFile = "ntuplize.root"
options.parseArguments()

process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(options.inputFiles),
    skipEvents=cms.untracked.uint32(options.skipEvents),
)

from FinalStateAnalysis.NtupleTools.parameters.default import parameters
if options.paramFile:
    # add custom parameters
    if os.path.isfile(options.paramFile):
        print 'Using custom parameter file %s' % os.path.abspath(options.paramFile)
        import imp
        custParamModule = imp.load_source('custParamModule',options.paramFile)
        from custParamModule import parameters as custParams
        parameters.update(custParams)
    else:
        print 'Failed to load custom parameters, using default.'
    pass

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

#load magfield and geometry (for mass resolution)
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Need the global tag for geometry etc.
envvar = 'mcgt' if options.isMC else 'datagt'
GT = {'mcgt': 'PHYS14_50_V1::All', 'datagt': 'GR_70_V2_AN1::All'}
if options.use25ns:
    GT['mcgt'] = 'PHYS14_25_V1::All'


if options.GlobalTag:
    process.GlobalTag.globaltag = cms.string(options.GlobalTag)
else:
    try:
        process.GlobalTag.globaltag = cms.string(os.environ[envvar])
    except KeyError:
        print 'Warning: GlobalTag not defined in environment. Using default.'
        process.GlobalTag.globaltag = cms.string(GT[envvar])
    process.GlobalTag.globaltag = cms.string(GT[envvar])

print 'Using globalTag: %s' % process.GlobalTag.globaltag

# Drop the input ones, just to make sure we aren't screwing anything up
process.buildFSASeq = cms.Sequence()
from FinalStateAnalysis.PatTools.patFinalStateProducers \
    import produce_final_states
# Which collections are used to build the final states
fs_daughter_inputs = {
    'electrons': 'slimmedElectrons',
    'muons': 'slimmedMuons',
    'taus': 'slimmedTaus',
    'photons': 'slimmedPhotons',
    'jets': 'slimmedJets',
    'pfmet': 'slimmedMETs',         # only one MET in miniAOD
    'mvamet': 'fixme',              # produced later
    'fsr': 'slimmedPhotons',
}

# embed some things we need that arent in miniAOD yet (like some ids)
output_commands = []

# embed electron ids
electronMVANonTrigIDLabel = "BDTIDNonTrig"
electronMVATrigIDLabel = "BDTIDTrig"
from FinalStateAnalysis.NtupleTools.embedElectronIDs import embedElectronIDs
fs_daughter_inputs['electrons'] = embedElectronIDs(process,options.use25ns,
                                                   fs_daughter_inputs['electrons'], 
                                                   electronMVANonTrigIDLabel,
                                                   electronMVATrigIDLabel,)

# Clean out muon "ghosts" caused by track ambiguities
process.ghostCleanedMuons = cms.EDProducer("PATMuonCleanerBySegments",
                                           src = cms.InputTag(fs_daughter_inputs['muons']),
                                           preselection = cms.string("track.isNonnull"),
                                           passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                                           fractionOfSharedSegments = cms.double(0.499))
fs_daughter_inputs['muons'] = "ghostCleanedMuons"

process.miniCleanedMuons = cms.Path(process.ghostCleanedMuons)
process.schedule.append(process.miniCleanedMuons)

process.miniPatMuons = cms.EDProducer(
    "MiniAODMuonIDEmbedder",
    src=cms.InputTag(fs_daughter_inputs['muons']),
    vertices=cms.InputTag("offlineSlimmedPrimaryVertices"),
)
fs_daughter_inputs['muons'] = "miniPatMuons"

process.miniPatJets = cms.EDProducer(
    "MiniAODJetIdEmbedder",
    src=cms.InputTag(fs_daughter_inputs['jets'])
)
fs_daughter_inputs['jets'] = 'miniPatJets'

process.runMiniAODObjectEmbedding = cms.Path(
    process.miniPatMuons+
    process.miniPatJets
)
process.schedule.append(process.runMiniAODObjectEmbedding)

process.miniMuonsEmbedIp = cms.EDProducer(
    "MiniAODMuonIpEmbedder",
    src = cms.InputTag(fs_daughter_inputs['muons']),
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
fs_daughter_inputs['muons'] = 'miniMuonsEmbedIp'

process.miniElectronsEmbedIp = cms.EDProducer(
    "MiniAODElectronIpEmbedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
fs_daughter_inputs['electrons'] = 'miniElectronsEmbedIp'

process.runMiniAODLeptonIpEmbedding = cms.Path(
    process.miniMuonsEmbedIp+
    process.miniElectronsEmbedIp
)
process.schedule.append(process.runMiniAODLeptonIpEmbedding)

# Embed effective areas in muons and electrons
process.load("FinalStateAnalysis.PatTools.electrons.patElectronEAEmbedding_cfi")
process.patElectronEAEmbedder.src = cms.InputTag(fs_daughter_inputs['electrons'])
process.load("FinalStateAnalysis.PatTools.muons.patMuonEAEmbedding_cfi")
process.patMuonEAEmbedder.src = cms.InputTag(fs_daughter_inputs['muons'])
fs_daughter_inputs['electrons'] = 'patElectronEAEmbedder'
fs_daughter_inputs['muons'] = 'patMuonEAEmbedder'
# And for electrons, the new HZZ4l EAs as well
process.miniAODElectronEAEmbedding = cms.EDProducer(
    "MiniAODElectronEffectiveArea2015Embedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    label = cms.string("EffectiveArea_HZZ4l2015"), # embeds a user float with this name
    )
fs_daughter_inputs['electrons'] = 'miniAODElectronEAEmbedding'
process.EAEmbedding = cms.Path(
    process.patElectronEAEmbedder +
    process.patMuonEAEmbedder +
    process.miniAODElectronEAEmbedding
    )
process.schedule.append(process.EAEmbedding)

# Embed rhos in electrons
process.miniAODElectronRhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll"), # not sure this is right
    userLabel = cms.string("rhoCSA14")
    )
fs_daughter_inputs['electrons'] = 'miniAODElectronRhoEmbedding'

# ... and muons
process.miniAODMuonRhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag(fs_daughter_inputs['muons']),
    srcRho = cms.InputTag("fixedGridRhoFastjetCentralNeutral"), # not sure this is right
    userLabel = cms.string("rhoCSA14")
    )
fs_daughter_inputs['muons'] = 'miniAODMuonRhoEmbedding'
process.rhoEmbedding = cms.Path(
    process.miniAODElectronRhoEmbedding +
    process.miniAODMuonRhoEmbedding
    )
process.schedule.append(process.rhoEmbedding)

if options.hzz:
    # Make FSR photon collection, give them isolation
    process.load("FinalStateAnalysis.PatTools.miniAOD_fsrPhotons_cff")
    fs_daughter_inputs['fsr'] = 'boostedFsrPhotons'
    output_commands.append('*_boostedFsrPhotons_*_*')
    process.makeFSRPhotons = cms.Path(process.fsrPhotonSequence)
    process.schedule.append(process.makeFSRPhotons)

    # Embed HZZ ID and isolation decisions because we need to know them for FSR recovery
    idCheatLabel = "HZZ4lIDPass" # Gets loose ID. For tight ID, append "Tight".
    isoCheatLabel = "HZZ4lIsoPass"
    process.electronIDIsoCheatEmbedding = cms.EDProducer(
        "MiniAODElectronHZZIDDecider",
        src = cms.InputTag(fs_daughter_inputs['electrons']),
        idLabel = cms.string(idCheatLabel), # boolean stored as userFloat with this name
        isoLabel = cms.string(isoCheatLabel), # boolean stored as userFloat with this name
        rhoLabel = cms.string("rhoCSA14"), # use rho and EA userFloats with these names
        eaLabel = cms.string("EffectiveArea_HZZ4l2015"),
        vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        bdtLabel = cms.string(electronMVANonTrigIDLabel),
        )
    fs_daughter_inputs['electrons'] = 'electronIDIsoCheatEmbedding'
    output_commands.append('*_electronIDIsoCheatEmbedding_*_*')
    process.muonIDIsoCheatEmbedding = cms.EDProducer(
        "MiniAODMuonHZZIDDecider",
        src = cms.InputTag(fs_daughter_inputs['muons']),
        idLabel = cms.string(idCheatLabel), # boolean will be stored as userFloat with this name
        isoLabel = cms.string(isoCheatLabel), # boolean will be stored as userFloat with this name
        vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        # Defaults are correct as of 9 March 2015, overwrite later if needed
        )
    fs_daughter_inputs['muons'] = 'muonIDIsoCheatEmbedding'
    output_commands.append('*_muonIDIsoCheatEmbedding_*_*')
    process.embedHZZ4lIDDecisions = cms.Path(
        process.electronIDIsoCheatEmbedding +
        process.muonIDIsoCheatEmbedding
        )
    process.schedule.append(process.embedHZZ4lIDDecisions)
    

## Do preselection as requested in the analysis parameters
preselections = parameters.get('preselection',{})

from FinalStateAnalysis.NtupleTools.object_parameter_selector import setup_selections, getName
process.preselectionSequence = setup_selections(
    process, 
    "Preselection",
    fs_daughter_inputs,
    preselections,
    )
for ob in preselections:
    fs_daughter_inputs[getName(ob)+'s'] = getName(ob)+"Preselection"
    output_commands.append('*_%sPreselection_*_*'%getName(ob))
process.FSAPreselection = cms.Path(process.preselectionSequence)
process.schedule.append(process.FSAPreselection)


# embed info about nearest jet
process.miniAODElectronJetInfoEmbedding = cms.EDProducer(
    "MiniAODElectronJetInfoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['electrons']),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag(fs_daughter_inputs['jets']),
    maxDeltaR = cms.double(0.1),
)
fs_daughter_inputs['electrons'] = 'miniAODElectronJetInfoEmbedding'
process.miniAODMuonJetInfoEmbedding = cms.EDProducer(
    "MiniAODMuonJetInfoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['muons']),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag(fs_daughter_inputs['jets']),
    maxDeltaR = cms.double(0.1),
)
fs_daughter_inputs['muons'] = 'miniAODMuonJetInfoEmbedding'
process.miniAODTauJetInfoEmbedding = cms.EDProducer(
    "MiniAODTauJetInfoEmbedder",
    src = cms.InputTag(fs_daughter_inputs['taus']),
    embedBtags = cms.bool(False),
    suffix = cms.string(''),
    jetSrc = cms.InputTag(fs_daughter_inputs['jets']),
    maxDeltaR = cms.double(0.1),
)
fs_daughter_inputs['taus'] = 'miniAODTauJetInfoEmbedding'
process.jetInfoEmbedding = cms.Path(
    process.miniAODElectronJetInfoEmbedding +
    process.miniAODMuonJetInfoEmbedding +
    process.miniAODTauJetInfoEmbedding
)
process.schedule.append(process.jetInfoEmbedding)

# mvamet
process.load("RecoJets.JetProducers.ak4PFJets_cfi")
process.ak4PFJets.src = cms.InputTag("packedPFCandidates")
process.ak4PFJets.doAreaFastjet = cms.bool(True)

from JetMETCorrections.Configuration.DefaultJEC_cff import ak4PFJetsL1FastL2L3

process.load("RecoMET.METPUSubtraction.mvaPFMET_cff")
process.pfMVAMEt.srcPFCandidates = cms.InputTag("packedPFCandidates")
process.pfMVAMEt.srcVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pfMVAMEt.inputFileNames.U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmet_7_2_X_MINIAOD_BX25PU20_Mar2015.root')
process.pfMVAMEt.inputFileNames.DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrphi_7_2_X_MINIAOD_BX25PU20_Mar2015.root')
process.pfMVAMEt.inputFileNames.CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_7_2_X_MINIAOD_BX25PU20_Mar2015.root')
process.pfMVAMEt.inputFileNames.CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_7_2_X_MINIAOD_BX25PU20_Mar2015.root')
if not options.use25ns:
    process.pfMVAMEt.inputFileNames.U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmet_7_2_X_MINIAOD_BX50PU40_Jan2015.root')
    process.pfMVAMEt.inputFileNames.DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrphi_7_2_X_MINIAOD_BX50PU40_Jan2015.root')
    process.pfMVAMEt.inputFileNames.CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_7_2_X_MINIAOD_BX50PU40_Jan2015.root')
    process.pfMVAMEt.inputFileNames.CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_7_2_X_MINIAOD_BX50PU40_Jan2015.root')

process.puJetIdForPFMVAMEt.jec =  cms.string('AK4PF')
process.puJetIdForPFMVAMEt.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.puJetIdForPFMVAMEt.rho = cms.InputTag("fixedGridRhoFastjetAll")

from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs

process.miniAODMVAMEt = patMETs.clone(
    metSource=cms.InputTag("pfMVAMEt"),
    addMuonCorrections = cms.bool(False),
    addGenMET = cms.bool(False)
)
fs_daughter_inputs['mvamet'] = 'miniAODMVAMEt'

process.mvaMetSequence = cms.Path(
    process.ak4PFJets *
    process.pfMVAMEtSequence *
    process.miniAODMVAMEt
)

if options.hzz:    
    # Put FSR photons into leptons as user cands
    from FinalStateAnalysis.PatTools.miniAODEmbedFSR_cfi \
        import embedFSRInElectrons, embedFSRInMuons
    process.electronFSREmbedder = embedFSRInElectrons.clone(
        src = cms.InputTag(fs_daughter_inputs['electrons']),
        srcAlt = cms.InputTag(fs_daughter_inputs['muons']),
        srcPho = cms.InputTag(fs_daughter_inputs['fsr']),
        srcVeto = cms.InputTag(fs_daughter_inputs['electrons']),
        srcVtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
        idDecisionLabel = cms.string(idCheatLabel),
        )
    fs_daughter_inputs['electrons'] = 'electronFSREmbedder'
    output_commands.append('*_electronFSREmbedder_*_*')
    process.muonFSREmbedder = embedFSRInMuons.clone(
        src = cms.InputTag(fs_daughter_inputs['muons']),
        srcAlt = cms.InputTag(fs_daughter_inputs['electrons']),
        srcPho = cms.InputTag(fs_daughter_inputs['fsr']),
        srcVeto = cms.InputTag(fs_daughter_inputs['electrons']),
        srcVtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
        idDecisionLabel = cms.string(idCheatLabel),
        )
    fs_daughter_inputs['muons'] = 'muonFSREmbedder'
    output_commands.append('*_muonFSREmbedder_*_*')
    process.embedFSRInfo = cms.Path(
        process.electronFSREmbedder +
        process.muonFSREmbedder
        )
    process.schedule.append(process.embedFSRInfo)

# Eventually, set buildFSAEvent to False, currently working around bug
# in pat tuples.
produce_final_states(process, fs_daughter_inputs, output_commands, process.buildFSASeq,
                     'puTagDoesntMatter', buildFSAEvent=True,
                     noTracks=True, 
                     hzz=options.hzz, rochCor=options.rochCor,
                     eleCor=options.eleCor, use25ns=options.use25ns, **parameters)
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

suffix = '' # most analyses don't need to modify the final states

if options.hzz:
    process.embedHZZMESeq = cms.Sequence()
    # Embed matrix elements in relevant final states
    suffix = "HZZME"
    for quadFS in ['ElecElecElecElec', 
                   'ElecElecMuMu',
                   'MuMuMuMu']:
        oldName = "finalState%s"%quadFS
        embedProducer = cms.EDProducer(
            "MiniAODHZZMEEmbedder",
            src = cms.InputTag(oldName),
            processes = cms.vstring("p0plus_VAJHU",
                                    "bkg_VAMCFM"),
            )

        # give the FS collection the same name as before, but with an identifying suffix
        newName = oldName + suffix
        setattr(process, newName, embedProducer)
        process.embedHZZMESeq += embedProducer
        output_commands.append('*_%s_*_*'%newName)
            
    process.embedHZZME = cms.Path(process.embedHZZMESeq)
    process.schedule.append(process.embedHZZME)
        


_FINAL_STATE_GROUPS = {
    'zh': 'eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt',
    'zz': 'eeee, eemm, mmmm',
    'zgg': 'eegg, mmgg',
    'llt': 'emt, mmt, eet, mmm, emm, mm, ee, em',
    'zg': 'mmg, eeg',
    'zgxtra': 'mgg, emg, egg',
    'dqm': 'e,m,t,g,j',
    '3lep': 'eee, eem, eet, emm, emt, ett, mmm, mmt, mtt, ttt',
    '4lep': 'eeee, eeem, eeet, eemm, eemt, eett, emmm, emmt, emtt, ettt, mmmm, mmmt, mmtt, mttt, tttt',
}

# run dqm
if options.runDQM: options.channels = 'dqm'

# Generate analyzers which build the desired final states.
final_states = [x.strip() for x in options.channels.split(',')]


def order_final_state(state):
    '''
    Sorts final state objects into order expected by FSA.
    
    Sorts string of characters into ordr defined by "order." Invalid 
    characters are ignored, and a warning is pribted to stdout
    
    returns the sorted string
    '''
    order = "emtgj"
    for obj in state:
        if obj not in order:
            print "invalid Final State object "\
                "'%s' ignored" % obj
            state = state.replace(obj, "")
    return ''.join(sorted(state, key=lambda x: order.index(x)))
 
def expanded_final_states(input):
    for fs in input:
        if fs in _FINAL_STATE_GROUPS:
            for subfs in _FINAL_STATE_GROUPS[fs].split(','):
                yield subfs.strip()
        else:
            yield fs

print "Building ntuple for final states: %s" % ", ".join(final_states)
for final_state in expanded_final_states(final_states):
    extraJets = options.nExtraJets if 'j' not in final_state else 0
    final_state = order_final_state(final_state)
    analyzer = make_ntuple(*final_state, 
                            svFit=options.svFit, dblhMode=options.dblhMode,
                            runTauSpinner=options.runTauSpinner, 
                            skimCuts=options.skimCuts, suffix=suffix,
                            hzz=options.hzz, nExtraJets=extraJets, **parameters)
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
    process.options.wantSummary = cms.untracked.bool(True)
if options.passThru:
    set_passthru(process)

if options.dump:
    print process.dumpPython()
