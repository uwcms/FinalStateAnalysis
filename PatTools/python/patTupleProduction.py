'''

Main steering file for the UW PAT tuple.

The important function is configurePatTuple(process),
which adds a cms.Sequence called "tuplize" to the process.

The following options should be passed as keyword arguments:
    isMC:                   data or MC
    embedded:               is a Zmumu embedded sample
    isAOD:                  whether the base file is RECO or AOD
    calibrationTarget:      the goal for the electron energy calibrations
    puTag:                  for simulated samples, the PU scenario
    xSec:                   for simulated samples, the sample x-section

The function returns a reference to process.tuplize + the list of output
commands which needs to be added to keep the appropriate PAT tuple products.

Authors: Bucky & Friends

'''

import FWCore.ParameterSet.Config as cms

import PhysicsTools.PatAlgos.tools.trigTools as trigtools
import PhysicsTools.PatAlgos.tools.jetTools as jettools
import PhysicsTools.PatAlgos.tools.metTools as mettools
import PhysicsTools.PatAlgos.tools.tauTools as tautools
import PhysicsTools.PatAlgos.tools.coreTools as coreTools
import PhysicsTools.PatAlgos.tools.pfTools as pfTools
import PhysicsTools.PatAlgos.tools.helpers as helpers

from FinalStateAnalysis.Utilities.cfgtools import chain_sequence
from FinalStateAnalysis.Utilities.version import cmssw_major_version,\
    cmssw_minor_version
from FinalStateAnalysis.PatTools.pfIsolationTools import setup_h2tau_iso,\
    add_hZg_iso_needs
from FinalStateAnalysis.PatTools.patFinalStateProducers import \
    produce_final_states
from pdb import set_trace

def configurePatTuple(process, isMC=True, **kwargs):
    '''
    Core function for PATTuple production
    '''
    #fix argparser output
    isMC = bool(isMC)

    ########################
    ##                    ##
    ##  PATTuple content  ##
    ##                    ##
    ########################
    # Stuff we always keep
    output_commands = [
        '*_addPileupInfo_*_*',
        'edmMergeableCounter_*_*_*',
        '*_lumiProducer_*_*',
        '*_particleFlow_*_*',
        '*_offlineBeamSpot_*_*',
        '*_generalTracks_*_*',
        '*_electronGsfTracks_*_*',
        '*_gsfElectrons_*_*',
        '*_gsfElectronCores_*_*',
        '*_offlinePrimaryVertices*_*_*',
        '*_ak5GenJets_*_*',
        '*_hltTriggerSummaryAOD_*_*',
        'edmTriggerResults_TriggerResults_*_%s' % process.name_(),
        '*_MEtoEDMConverter*_*_%s' % process.name_(),
        'LHEEventProduct_*_*_*',
        'GenEventInfoProduct_generator_*_*',
        '*_kt6PFJetsForRhoComputationVoronoi_rho_*',
        '*_kt6PFJetsForIso_rho_*',
        '*_kt6PFJets_rho_*',
        '*_kt6PFJetsHZGPho_rho_*',
        '*_kt6PFJetsCentralHZGEle_rho_*',
        '*_kt6PFJetsCentralHZGMu_rho_*',
        '*_kt6PFJetsCentralNeutralHZGMu_rho_*',
        '*_kt6PFJetsCentral_rho_*',
        '*_kt6PFJetsCentralNeutral_rho_*',  # for zz muons
        '*_photonCore_*_*',
        '*_boostedFsrPhotons_*_*',
        # for Zmumu -> embedded samples
        # https://twiki.cern.ch/twiki/bin/view/CMS/MuonTauReplacementRecHit
        '*_generalTracksORG_*_EmbeddedRECO',
        '*_electronGsfTracksORG_*_EmbeddedRECO',
        'double_TauSpinnerReco_TauSpinnerWT_EmbeddedSPIN',
        'double_ZmumuEvtSelEffCorrWeightProducer_weight_EmbeddedRECO',
        'double_muonRadiationCorrWeightProducer_weight_EmbeddedRECO',
        'GenFilterInfo_generator_minVisPtFilter_EmbeddedRECO',
    ]
    # Define our patTuple production sequence
    process.tuplize = cms.Sequence()
    # Only keep interesting genParticles
    process.load("FinalStateAnalysis.RecoTools.genParticleTrimmer_cfi")
    process.genParticles = process.prunedGenParticles.clone()
    if isMC:
        #process.tuplize += process.genParticles
        #output_commands.append('*_genParticles_*_%s' % process.name_())
        output_commands.append('*_genParticles_*_*')

    output_commands.append('*_tauGenJetsSelectorAllHadrons_*_*')
    output_commands.append('*_tauGenJets_*_*')
    output_commands.append('*_ak5GenJets_*_*')

    ########################
    ##                    ##
    ##        PAT         ##
    ##                    ##
    ########################

    # Run pat default sequence
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    # Embed PF Isolation in electrons & muons
    pfTools.usePFIso(process)
    # Setup H2Tau custom iso definitions
    setup_h2tau_iso(process)
    # Setup hZg custom iso definitions
    add_hZg_iso_needs(process)

    # Now run PAT
    process.tuplize += process.patDefaultSequence

    ## Add FSR photons for ZZ analysis
    #process.load("FinalStateAnalysis.PatTools.fsrPhotons_cff")
    #process.tuplize += process.fsrPhotonSequence

    ########################
    ##        GEN         ##
    ########################

    # Disable gen match embedding - we keep it in the ntuple
    process.patMuons.embedGenMatch = False
    process.patElectrons.embedGenMatch = False
    process.patTaus.embedGenMatch = False
    process.patTaus.embedGenJetMatch = False
    process.patPhotons.embedGenMatch = False
    if not isMC:
        coreTools.runOnData(process)

    ########################
    ##       MUONS        ##
    ########################

    # Unembed junk
    process.patMuons.embedCaloMETMuonCorrs = False
    process.patMuons.embedTcMETMuonCorrs = False
    process.patMuons.embedTrack = True
    process.patMuons.pvSrc = cms.InputTag("selectedPrimaryVertex")

    process.load("FinalStateAnalysis.PatTools.patMuonProduction_cff")
    final_muon_collection = chain_sequence(
        process.customizeMuonSequence, "selectedPatMuons")
    process.customizeMuonSequence.insert(0, process.selectedPatMuons)
    process.patDefaultSequence.replace(process.selectedPatMuons,
                                       process.customizeMuonSequence)
    process.cleanPatMuons.src = final_muon_collection
    process.patMuonRochesterCorrectionEmbedder.isMC = cms.bool(bool(isMC))

    ########################
    ##        TAUS        ##
    ########################

    # Use HPS taus
    tautools.switchToPFTauHPS(process) #this NEEDS a sequence called patDefaultSequence
    # Disable tau IsoDeposits
    process.patDefaultSequence.remove(process.patPFTauIsolation)
    process.patTaus.isoDeposits = cms.PSet()
    process.patTaus.userIsolation = cms.PSet()

    process.load("FinalStateAnalysis.PatTools.patTauProduction_cff")
    # Require all taus to pass decay mode finding and have high PT
    process.patTauGarbageRemoval.cut = cms.string(
        "pt > 17 && abs(eta) < 2.5 && tauID('decayModeFindingNewDMs')")
    final_tau_collection = chain_sequence(
        process.customizeTauSequence, "selectedPatTaus")
    # Inject into the pat sequence
    process.customizeTauSequence.insert(0, process.selectedPatTaus)
    process.patDefaultSequence.replace(process.selectedPatTaus,
                                       process.customizeTauSequence)
    process.cleanPatTaus.src = final_tau_collection
    # Remove muons and electrons
    process.cleanPatTaus.checkOverlaps.muons.requireNoOverlaps = False
    process.cleanPatTaus.checkOverlaps.electrons.requireNoOverlaps = False
    # Cuts already applied by the garbage removal
    process.cleanPatTaus.preselection = ''
    process.cleanPatTaus.finalCut = ''

    ########################
    ##     ELECTRONS      ##
    ########################

    # Use POG recommendations for (these) electron Isos
    process.elPFIsoValueGamma04PFIdPFIso.deposits[0].vetos = cms.vstring(
        'EcalEndcaps:ConeVeto(0.08)')
    process.elPFIsoValueGamma04NoPFIdPFIso.deposits[0].vetos = cms.vstring(
        'EcalEndcaps:ConeVeto(0.08)')
    process.elPFIsoValueCharged04PFIdPFIso.deposits[0].vetos = cms.vstring(
        'EcalEndcaps:ConeVeto(0.015)')
    process.elPFIsoValueCharged04NoPFIdPFIso.deposits[0].vetos = cms.vstring(
        'EcalEndcaps:ConeVeto(0.015)')

    # Do extra electron ID
    process.load("FinalStateAnalysis.PatTools.electrons.electronID_cff")
    if cmssw_major_version() == 4:
        process.patDefaultSequence.replace(process.patElectrons,
                                           process.recoElectronID42X +
                                           process.patElectrons)
        process.patElectrons.electronIDSources = process.electronIDSources42X
    else:
        process.patDefaultSequence.replace(process.patElectrons,
                                           process.recoElectronID5YX +
                                           process.patElectrons)
        process.patElectrons.electronIDSources = process.electronIDSources5YX

    process.electronMatch.checkCharge = cms.bool(False)
    process.patElectrons.embedTrack = False
    process.patElectrons.embedPFCandidate = False
    process.patElectrons.embedGsfElectronCore = False
    process.patElectrons.embedSuperCluster = True

    # Produce the electron collections
    process.load("FinalStateAnalysis.PatTools.patElectronProduction_cff")

    # Electron Energy Regression and Calibrations
    process.load(
        "EgammaAnalysis.ElectronTools.electronRegressionEnergyProducer_cfi")
    process.load("EgammaAnalysis.ElectronTools.calibratedPatElectrons_cfi")

    #setup the energy regression for the specific dataset
    if kwargs['eleReg']:
        print "-- Applying Electron Regression and Calibration --"

        process.customizeElectronSequence += process.eleRegressionEnergy
        process.customizeElectronSequence += process.calibratedPatElectrons

        process.eleRegressionEnergy.energyRegressionType = cms.uint32(2)
        process.calibratedPatElectrons.correctionsType = cms.int32(2)

        if isMC:
            process.calibratedPatElectrons.inputDataset = cms.string(
                "Summer12_LegacyPaper")
        else:
            process.calibratedPatElectrons.inputDataset = cms.string(
                "22Jan2013ReReco")

        process.calibratedPatElectrons.combinationType = cms.int32(3)
        process.calibratedPatElectrons.lumiRatio = cms.double(1.0)
        process.calibratedPatElectrons.synchronization = cms.bool(True)
        process.calibratedPatElectrons.isMC = cms.bool(isMC == 1)
        process.calibratedPatElectrons.verbose = cms.bool(False)

    final_electron_collection = chain_sequence(
        process.customizeElectronSequence, "selectedPatElectrons",
        # Some of the EGamma modules have non-standard src InputTags,
        # specify them here.
        ("src", "inputPatElectronsTag", "inputElectronsTag")
    )

    #process.tuplize += process.customizeElectronSequence #why do we need this?
    process.customizeElectronSequence.insert(0, process.selectedPatElectrons)
    process.patDefaultSequence.replace(process.selectedPatElectrons,
                                       process.customizeElectronSequence)
    # We have to do the pat Jets before the pat electrons since we embed them
    process.customizeElectronSequence.insert(0, process.selectedPatJets)

    # Define cleanPatElectrons input collection
    process.cleanPatElectrons.src = final_electron_collection

    # Define the default lepton cleaning
    process.cleanPatElectrons.preselection = cms.string(
        'pt > 5')
    process.cleanPatElectrons.checkOverlaps.muons.requireNoOverlaps = False
    # Make sure we don't kill any good taus by calling them electrons
    # Note that we don't actually remove these overlaps.
    process.cleanPatElectrons.checkOverlaps.taus = cms.PSet(
        src=final_tau_collection,
        algorithm=cms.string("byDeltaR"),
        preselection=cms.string(
            "tauID('decayModeFinding') > 0.5 &&"
            "tauID('byLooseCombinedIsolationDeltaBetaCorr') > 0.5 &&"
            "tauID('againstElectronLoose') > 0.5 && "
            "pt > 10"
        ),
        deltaR=cms.double(0.1),
        checkRecoComponents=cms.bool(False),
        pairCut=cms.string(""),
        requireNoOverlaps=cms.bool(False),
    )

    ########################
    ##        JETS        ##
    ########################

    # Use PFJets and turn on JEC
    jec = ['L1FastJet', 'L2Relative', 'L3Absolute']
    # If we are running on data (not MC), or embedded sample,
    # apply the MC-DATA residual correction.
    if not isMC or kwargs['embedded']:
        jec.extend(['L2L3Residual'])

    # tmp
    # define the b-tag squences for offline reconstruction
    process.load("RecoBTag.SecondaryVertex.secondaryVertex_cff")
    process.load("RecoBTau.JetTagComputer.combinedMVA_cff")
    process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
    process.load('RecoBTag/SecondaryVertex/bToCharmDecayVertexMerger_cfi')
    #process.load("PhysicsTools.PatAlgos.patSequences_cff")

    # Define options for BTagging - these are release dependent.
    btag_options = {'doBTagging': True}
    if cmssw_major_version() == 5:
        btag_options['btagInfo'] = [
            'impactParameterTagInfos',
            'secondaryVertexTagInfos',
            'softMuonTagInfos',
            'secondaryVertexNegativeTagInfos',
            'inclusiveSecondaryVertexFinderFilteredTagInfos'
        ]
        btag_options['btagdiscriminators'] = [
            'trackCountingHighEffBJetTags',
            'trackCountingHighPurBJetTags',    
            'simpleSecondaryVertexHighEffBJetTags',
            'simpleSecondaryVertexHighPurBJetTags',
            'simpleInclusiveSecondaryVertexHighEffBJetTags',
            'simpleInclusiveSecondaryVertexHighPurBJetTags',        
            'combinedSecondaryVertexMVABJetTags',
            'combinedSecondaryVertexBJetTags',
            'jetBProbabilityBJetTags', 
            'jetProbabilityBJetTags',   
        ]

    #Avoid embedding
    process.patJets.embedPFCandidates = True
    process.patJets.embedCaloTowers = False
    process.patJets.embedGenJetMatch = True
    process.patJets.addAssociatedTracks = True
    process.patJets.embedGenPartonMatch = True
    process.patJets.addTagInfos = True
    # Add AK5chs PFJets
    jettools.addJetCollection(
        process,
        cms.InputTag('ak5PFchsJets'),
        algoLabel = "AK5",
        typeLabel = "PFchs",
        doJTA              = True,
        jetCorrLabel       = ('AK5PFchs', jec),
        doType1MET         = False,
        doL1Cleaning       = False,
        doL1Counters       = False,
        genJetCollection   = cms.InputTag('ak5GenJets'),
        doJetID            = True,
        **btag_options
    )

    # Use AK5 PFJets
    jettools.switchJetCollection(
        process,
        cms.InputTag('ak5PFJets'),
        doJTA=True,
        jetCorrLabel=('AK5PF', jec),
        #jetCorrLabel = None,
        doType1MET=False,
        doJetID=True,
        genJetCollection=cms.InputTag("ak5GenJets"),
        **btag_options
    )

    # Customize/embed all our sequences
    process.load("FinalStateAnalysis.PatTools.patJetProduction_cff")
    helpers.cloneProcessingSnippet( process, process.customizeJetSequence, 'AK5PFchs' )
    process.patJetGarbageRemoval.cut = 'pt > 12'
    final_jet_collection = chain_sequence(
        process.customizeJetSequence, "patJets")
    process.customizeJetSequence.insert(0, process.patJets)
    # Make it a "complete" sequence
    process.customizeJetSequence += process.selectedPatJets
#    process.customizeJetSequence += process.btagging
    # We can't mess up the selected pat jets because the taus use them.
    process.selectedPatJets.src = final_jet_collection
    process.patDefaultSequence.replace(process.patJets,
                                       process.customizeJetSequence)

    process.customizeJetSequenceAK5PFchs.remove( process.patJetsPUIDAK5PFchs )
    process.customizeJetSequenceAK5PFchs.remove( process.pileupJetIdProducerAK5PFchs )
    process.patJetGarbageRemovalAK5PFchs.cut = 'pt > 20'
    process.patJetCorrFactorsAK5PFchs.payload = cms.string('AK5PFchs') 
    final_jetchs_collection = chain_sequence(
        process.customizeJetSequenceAK5PFchs, "patJetsAK5PFchs")
    process.customizeJetSequenceAK5PFchs.insert(0, process.patJetsAK5PFchs)
    # Make it a "complete" sequence
    process.customizeJetSequenceAK5PFchs += process.selectedPatJetsAK5PFchs
    # We can't mess up the selected pat jets because the taus use them.
    process.selectedPatJetsAK5PFchs.src = final_jetchs_collection
    process.selectedPatJetsAK5chsPF  = process.selectedPatJetsAK5PFchs.clone() #that's what we keep
    process.customizeJetSequenceAK5PFchs += process.selectedPatJetsAK5chsPF
    process.patDefaultSequence.replace(process.patJetsAK5PFchs,
                                       process.customizeJetSequenceAK5PFchs)

    output_commands.append('*_selectedPatJets_*_*')
    output_commands.append('*_selectedPatJetsAK5chsPF_*_*')
    output_commands.append('*SecondaryVertexTagInfo*_*_*_*')
    output_commands.append('*TrackIPTagInfo*_*_*_*')
    output_commands.append('*SoftLeptonTagInfo*_*_*_*')
    output_commands.append('*_ak5PFJets_*_*')
    output_commands.append('*_ak5PFchsJets_*_*')

    ########################
    ##        MET         ##
    ########################

    # Use PFMEt
    mettools.addPfMET(process)

    # We cut out a lot of the junky taus and jets - but we need these
    # to correctly apply the MET uncertainties.  So, let's make a
    # non-cleaned version of the jet and tau sequence.
    process.jetsForMetSyst = helpers.cloneProcessingSnippet(
        process, process.customizeJetSequence, 'ForMETSyst')
    process.tausForMetSyst = helpers.cloneProcessingSnippet(
        process, process.customizeTauSequence, 'ForMETSyst')
    # Don't apply any cut for these
    process.patTauGarbageRemovalForMETSyst.cut = ''
    process.patJetGarbageRemovalForMETSyst.cut = ''
    process.tuplize += process.jetsForMetSyst
    process.tuplize += process.tausForMetSyst
    # We have to make our clone of cleanPatTaus separately, since e/mu
    # cleaning is applied - therefore it isn't in the customizeTausSequence.
    process.cleanPatTausForMETSyst = process.cleanPatTaus.clone(
        src=cms.InputTag(process.cleanPatTaus.src.value() + "ForMETSyst"))
    process.cleanPatTausForMETSyst.preselection = ''
    process.cleanPatTausForMETSyst.finalCut = ''
    process.patTausEmbedJetInfoForMETSyst.jetSrc = \
        final_jet_collection.value() + "ForMETSyst"
    process.tuplize += process.cleanPatTausForMETSyst

    # Setup MET production
    process.load("FinalStateAnalysis.PatTools.patMETProduction_cff")
    # The MET systematics depend on all other systematics
    process.systematicsMET.tauSrc = cms.InputTag("cleanPatTausForMETSyst")
    process.systematicsMET.muonSrc = cms.InputTag("cleanPatMuons")
    process.systematicsMET.electronSrc = cms.InputTag("cleanPatElectrons")

    final_met_collection = chain_sequence(
        process.customizeMETSequence, "patMETsPF")
    process.tuplize += process.customizeMETSequence
    process.patMETsPF.addGenMET = bool(isMC)
    output_commands.append('*_%s_*_*' % final_met_collection.value())

    # Make a version with the MVA MET reconstruction method
    process.load("FinalStateAnalysis.PatTools.met.mvaMetOnPatTuple_cff")
    process.tuplize += process.pfMEtMVAsequence
    mva_met_sequence = helpers.cloneProcessingSnippet(
        process, process.customizeMETSequence, "MVA")
    final_mvamet_collection = chain_sequence(
        mva_met_sequence, "patMEtMVA")
    process.tuplize += mva_met_sequence
    output_commands.append('*_%s_*_*' % final_mvamet_collection.value())

    # Keep all the data formats needed for the systematics
    output_commands.append('recoLeafCandidates_*_*_%s'
                           % process.name_())
    # We can drop to jet and tau MET specific products. They were only used for
    # computation of the MET numbers.
    output_commands.append('drop recoLeafCandidates_*ForMETSyst_*_%s'
                           % process.name_())

    #########################
    ###      PHOTONS       ##
    #########################

    ##alter the photon matching to accept various fakes
    ## and sort matches by d-pt-rel
    #if isMC:
    #    process.photonMatch = cms.EDProducer(
    #        "MCMatcherByPt",
    #        src=cms.InputTag("photons"),
    #        maxDPtRel=cms.double(100.0),
    #        mcPdgId=cms.vint32(),
    #        mcStatus=cms.vint32(1),
    #        resolveByMatchQuality=cms.bool(False),
    #        maxDeltaR=cms.double(0.3),
    #        checkCharge=cms.bool(False),
    #        resolveAmbiguities=cms.bool(True),
    #        matched=cms.InputTag("genParticles")
    #    )

    ## Setup pat::Photon Production
    #process.load("FinalStateAnalysis.PatTools.patPhotonProduction_cff")
    #final_photon_collection = chain_sequence(process.customizePhotonSequence,
    #                                         "selectedPatPhotons")
    ##setup PHOSPHOR for a specific dataset
    #if cmssw_major_version() == 4:  # for now 2011 = CMSSW42X
    #    process.patPhotonPHOSPHOREmbedder.year = cms.uint32(2011)
    #else:  # 2012 is 5YX
    #    process.patPhotonPHOSPHOREmbedder.year = cms.uint32(2012)
    #process.patPhotonPHOSPHOREmbedder.isMC = cms.bool(bool(isMC))
    ##inject photons into pat sequence
    #process.customizePhotonSequence.insert(0, process.selectedPatPhotons)
    #process.patDefaultSequence.replace(process.selectedPatPhotons,
    #                                   process.customizePhotonSequence)
    #process.cleanPatPhotons.src = final_photon_collection

    ########################
    ##      TRIGGER       ##
    ########################

    trigtools.switchOnTrigger(process)

    #configure the PAT trigger
    if kwargs['HLTprocess']:
        process.patTrigger.processName = cms.string(kwargs['HLTprocess'])
        process.patTriggerEvent.processName = cms.string(kwargs['HLTprocess'])

    ########################
    ##   --------------   ##
    ########################

    output_commands.append('*_cleanPatTaus_*_*')
    output_commands.append('*_cleanPatElectrons_*_*')
    output_commands.append('*_cleanPatMuons_*_*')
    output_commands.append('*_cleanPatPhotons_*_*')

    ########################
    ##                    ##
    ##        FSA         ##
    ##                    ##
    ########################

    # Now build the PATFinalStateLS object, which holds LumiSection info.
    process.load(
        "FinalStateAnalysis.PatTools.finalStates.patFinalStateLSProducer_cfi")
    process.tuplize += process.finalStateLS
    output_commands.append('*_finalStateLS_*_*')
    if isMC:
        process.finalStateLS.xSec = kwargs['xSec']

    # Tell the framework to shut up!
    process.load("FWCore.MessageLogger.MessageLogger_cfi")
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000

    # Which collections are used to build the final states
    fs_daughter_inputs = {
        'electrons':  'cleanPatElectrons',
        'muons':  'cleanPatMuons',
        'taus':  'cleanPatTaus',
        #'photons':  'cleanPatPhotons',
        'jets':  'selectedPatJets',
        'pfmet':  final_met_collection,
        'mvamet':  final_mvamet_collection,
    }

    # Setup all the PATFinalState objects
    produce_final_states(process, fs_daughter_inputs, output_commands,
                         process.tuplize, kwargs['puTag'],
                         zzMode=kwargs.get('zzMode', False))

    return process.tuplize, output_commands

if __name__ == "__main__":
    import doctest
    doctest.testmod()
