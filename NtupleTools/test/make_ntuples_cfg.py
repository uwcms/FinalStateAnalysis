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
useMiniAOD=1 - run on miniAOD rather than UW PATTuples (default)
use25ns=1 - run on 25 ns miniAOD (default, 0 = 50ns)
runDQM=0 - run over single object final states to test all object properties (wont check diobject properties)
hzz=0 - Include FSR contribution a la HZZ4l group, include all ZZ candidates (including alternative lepton pairings).
nExtraJets=0 - Include basic info about this many jets (ordered by pt). Ignored if final state involves jets.


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
    rochCor="",
    eleCor="",
    rerunQGJetID=0,  # If one reruns the quark-gluon JetID
    runNewElectronMVAID=0,  # If one runs the new electron MVAID
    rerunMVAMET=0,  # If one, (re)build the MVA MET
    rerunJets=0,
    dblhMode=False, # For double-charged Higgs analysis
    runTauSpinner=0,
    GlobalTag="",
    useMiniAOD=1,
    use25ns=1,
    runDQM=0,
    hzz=0,
)

# options.register(
#     'hzz',
#     0,
#     TauVarParsing.TauVarParsing.multiplicity.singleton,
#     TauVarParsing.TauVarParsing.varType.int,
#     'MiniAOD version of FSR with the HZZ4l algorithm'
# )

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
            GT['mcgt'] = 'PHYS14_25_V1::All'
        else:
            GT['mcgt'] = 'PHYS14_50_V1::All'
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
            'fsr': 'slimmedPhotons',
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

        # Turn on versioned cut-based ID
        from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
        process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
        process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(fs_daughter_inputs['electrons'])
        output_commands.append('*_egmGsfElectronIDs_*_*')
        from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
        process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)
        if options.use25ns:
            cb_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V1_miniAOD_cff']
        else:
            print "50 ns cut based electron IDs don't exist yet for PHYS14. Using CSA14 cuts."
            cb_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_CSA14_50ns_V1_cff']
        for idmod in cb_id_modules:
            setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

        CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight"] # keys of cut based id user floats
        if options.use25ns:
            CBIDTags = [
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto'),
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose'),
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium'),
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight'),
                ]
        else:
            CBIDTags = [ # almost certainly wrong. Just don't use 50ns miniAOD any more
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-veto'),
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-loose'),
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-medium'),
                cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-tight'),
                ]

        # Embed cut-based VIDs
        process.miniAODElectronCutBasedID = cms.EDProducer(
            "MiniAODElectronCutBasedIDEmbedder",
            src=cms.InputTag(fs_daughter_inputs['electrons']),
            idLabels = cms.vstring(*CBIDLabels),
            ids = cms.VInputTag(*CBIDTags)
        )
        output_commands.append('*_miniAODElectronCutBasedID_*_*')
        fs_daughter_inputs['electrons'] = "miniAODElectronCutBasedID"

        # Embed MVA VIDs (weights will change soon for PHYS14!)
        trigMVAWeights = [
            'EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_25ns_EB_BDT.weights.xml',
            'EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_25ns_EE_BDT.weights.xml',
            ]
        nonTrigMVAWeights = [
            'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB1_5_oldscenario2phys14_BDT.weights.xml',
            'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB2_5_oldscenario2phys14_BDT.weights.xml',
            'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EE_5_oldscenario2phys14_BDT.weights.xml',
            'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB1_10_oldscenario2phys14_BDT.weights.xml',
            'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB2_10_oldscenario2phys14_BDT.weights.xml',
            'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EE_10_oldscenario2phys14_BDT.weights.xml',
            ]
        if not options.use25ns:
            for wt in trigMVAWeights+nonTrigMVAWeights:
                wt.replace('25ns','50ns')
        process.miniAODElectronMVAID = cms.EDProducer(
            "MiniAODElectronMVAIDEmbedder",
            src=cms.InputTag(fs_daughter_inputs['electrons']),
            trigWeights = cms.vstring(*trigMVAWeights),
            trigLabel = cms.string('BDTIDTrig'), # triggering MVA ID userfloat key
            nonTrigWeights = cms.vstring(*nonTrigMVAWeights),
            nonTrigLabel = cms.string('BDTIDNonTrig') # nontriggering MVA ID userfloat key
            )
        output_commands.append('*_miniAODElectronMVAID_*_*')
        fs_daughter_inputs['electrons'] = 'miniAODElectronMVAID'
        
        process.miniAODElectrons = cms.Path(
            process.egmGsfElectronIDSequence+
            process.miniAODElectronCutBasedID+
            process.miniAODElectronMVAID
            )
        process.schedule.append(process.miniAODElectrons)

        # Clean out muon "ghosts" caused by track ambiguities
        process.ghostCleanedMuons = cms.EDProducer("PATMuonCleanerBySegments",
                                                   src = cms.InputTag(fs_daughter_inputs['muons']),
                                                   preselection = cms.string("track.isNonnull"),
                                                   passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                                                   fractionOfSharedSegments = cms.double(0.499))
        output_commands.append('*_ghostCleanedMuons_*_*')
        fs_daughter_inputs['muons'] = "ghostCleanedMuons"

        process.miniCleanedMuons = cms.Path(process.ghostCleanedMuons)
        process.schedule.append(process.miniCleanedMuons)

        process.miniPatMuons = cms.EDProducer(
            "MiniAODMuonIDEmbedder",
            src=cms.InputTag(fs_daughter_inputs['muons']),
            vertices=cms.InputTag("offlineSlimmedPrimaryVertices"),
        )
        output_commands.append('*_miniPatMuons_*_*')
        fs_daughter_inputs['muons'] = "miniPatMuons"

        process.miniPatJets = cms.EDProducer(
            "MiniAODJetIdEmbedder",
            src=cms.InputTag(fs_daughter_inputs['jets'])
        )
        output_commands.append('*_miniPatJets_*_*')
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
        output_commands.append('*_miniAODElectronEAEmbedding_*_*')
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
        output_commands.append('*_miniAODElectronRhoEmbedding_*_*')

        # ... and muons
        process.miniAODMuonRhoEmbedding = cms.EDProducer(
            "MuonRhoOverloader",
            src = cms.InputTag(fs_daughter_inputs['muons']),
            srcRho = cms.InputTag("fixedGridRhoFastjetCentralNeutral"), # not sure this is right
            userLabel = cms.string("rhoCSA14")
            )
        fs_daughter_inputs['muons'] = 'miniAODMuonRhoEmbedding'
        output_commands.append('*_miniAODMuonRhoEmbedding_*_*')
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
    
            # Embed ID and isolation decisions to "cheat" in FSR algorithm
            idCheatLabel = "HZZ4lTightIDPass"
            isoCheatLabel = "HZZ4lIsoPass"
            process.electronIDIsoCheatEmbedding = cms.EDProducer(
                "MiniAODElectronHZZIDDecider",
                src = cms.InputTag(fs_daughter_inputs['electrons']),
                idLabel = cms.string(idCheatLabel), # boolean stored as userFloat with this name
                isoLabel = cms.string(isoCheatLabel), # boolean stored as userFloat with this name
                rhoLabel = cms.string("rhoCSA14"), # use rho and EA userFloats with these names
                eaLabel = cms.string("EffectiveArea_HZZ4l2015"),
                vtxSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
                # Defaults are correct as of 9 March 2015, overwrite later if needed
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

            # Clean jets overlapping with tight-ID'd leptons
#             process.hzzJetCleaning = cms.EDProducer(
#                 "PATJetCleaner",
#                 src = cms.InputTag(fs_daughter_inputs['jets']),
#                 preselection = cms.string(

    # Eventually, set buildFSAEvent to False, currently working around bug
    # in pat tuples.
    produce_final_states(process, fs_daughter_inputs, output_commands, process.buildFSASeq,
                         'puTagDoesntMatter', buildFSAEvent=True,
                         noTracks=True, noPhotons=options.noPhotons,
                         hzz=options.hzz, rochCor=options.rochCor,
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
    '3lep': 'eee, eem, eet, emm, emt, ett, mmm, mmt, mtt, ttt',
    '4lep': 'eeee, eeem, eeet, eemm, eemt, eett, emmm, emmt, emtt, ettt, mmmm, mmmt, mmtt, mttt, tttt',
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
    extraJets = options.nExtraJets if 'j' not in final_state else 0
    analyzer = make_ntuple(*final_state, 
                            svFit=options.svFit, dblhMode=options.dblhMode,
                            runTauSpinner=options.runTauSpinner, 
                            skimCuts=options.skimCuts,useMiniAOD=options.useMiniAOD,
                            hzz=options.hzz, nExtraJets=extraJets)
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
