import FWCore.ParameterSet.Config as cms

import PhysicsTools.PatAlgos.tools.trigTools as trigtools
import PhysicsTools.PatAlgos.tools.jetTools as jettools
import PhysicsTools.PatAlgos.tools.metTools as mettools
import PhysicsTools.PatAlgos.tools.tauTools as tautools
import PhysicsTools.PatAlgos.tools.coreTools as coreTools
import PhysicsTools.PatAlgos.tools.pfTools as pfTools

from FinalStateAnalysis.Utilities.cfgtools import chain_sequence
from FinalStateAnalysis.Utilities.version import cmssw_major_version
from FinalStateAnalysis.PatTools.pfIsolationTools import setup_h2tau_iso
from FinalStateAnalysis.PatTools.patFinalStateProducers import produce_final_states

def configurePatTuple(process, isMC=True, **kwargs):

    # Stuff we always keep
    output_commands = [
#        '*',
        '*_addPileupInfo_*_*',
        'edmMergeableCounter_*_*_*',
        '*_lumiProducer_*_*',
        '*_particleFlow_*_*',
        '*_offlineBeamSpot_*_*',
        '*_generalTracks_*_*',
        '*_electronGsfTracks_*_*',
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
        '*_kt6PFJetsCentralNeutral_rho_*', #for zz muons
        # for Zmumu -> embedded samples
        '*_generator_weight_*', # 2k11
        "GenFilterInfo_generator_minVisPtFilter_*", #2k12
        '*_genDaughters_*_*',
        '*_boosted*_*_*',
        '*_tmfTracks_*_*',
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
    # Select vertices
    process.load("FinalStateAnalysis.RecoTools.vertexSelection_cff")
    output_commands.append('*_selectedPrimaryVertex_*_*')
    output_commands.append('*_selectPrimaryVerticesQuality_*_*')
    process.tuplize += process.selectPrimaryVertices

    # Run the ZZ recipe for rho
    from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets \
            as zzCantDoAnythingRight

    process.kt6PFJetsForIso = zzCantDoAnythingRight.clone(
        rParam = cms.double(0.6),
        doAreaFastjet = cms.bool(True),
        doRhoFastjet = cms.bool(True),
        Rho_EtaMax = cms.double(2.5),
        Ghost_EtaMax = cms.double(2.5),
    )
    process.tuplize += process.kt6PFJetsForIso

    # Standard services
    process.load('Configuration.StandardSequences.Services_cff')
    process.load('Configuration.StandardSequences.GeometryIdeal_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

    # Rerun tau ID
    if cmssw_major_version() == 4:
        process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
        # Optimization - remove PFTauTagInfo compatibility layer
        process.recoTauClassicHPSSequence.remove(process.pfRecoTauTagInfoProducer)
        process.recoTauClassicHPSSequence.remove(process.ak5PFJetTracksAssociatorAtVertex)
        assert(process.combinatoricRecoTaus.modifiers[3].name.value() == 'TTIworkaround')
        del process.combinatoricRecoTaus.modifiers[3]
        # Don't build junky taus below 19 GeV
        process.combinatoricRecoTaus.builders[0].minPtToBuild = cms.double(17)
        process.tuplize += process.recoTauClassicHPSSequence
    else:
        # We can run less tau stuff in 52, since HPS taus already built.
        process.load("RecoTauTag.Configuration.updateHPSPFTaus_cff")
        process.tuplize += process.updateHPSPFTaus

    ## Run rho computation.  Only necessary in 42X
    if cmssw_major_version() == 4:
        from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets
        kt6PFJets.Rho_EtaMax = cms.double(4.4)
        kt6PFJets.doRhoFastjet = True
        process.kt6PFJets = kt6PFJets
        process.tuplize += process.kt6PFJets

    # In 4_X we have to rerun ak5PFJets with area computation enabled.
    if cmssw_major_version() == 4:
        process.load("RecoJets.Configuration.RecoPFJets_cff")
        process.ak5PFJets.doAreaFastjet = True
        process.tuplize += process.ak5PFJets
        # Only keep the new ak5PFJets
        output_commands.append('*_ak5PFJets_*_%s' % process.name_())
    else:
        # Just keep the normal ones
        output_commands.append('*_ak5PFJets_*_*')

    # In the embedded samples, we need to re-run the b-tagging
    if kwargs['embedded']:
       process.load('RecoBTag/Configuration/RecoBTag_cff')
       process.load('RecoJets/JetAssociationProducers/ak5JTA_cff')
       process.ak5JetTracksAssociatorAtVertex.jets   = cms.InputTag("ak5PFJets")
       process.ak5JetTracksAssociatorAtVertex.tracks = cms.InputTag("tmfTracks")
       process.tuplize += process.ak5JetTracksAssociatorAtVertex
       process.tuplize += process.btagging

    # Run pat default sequence
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    # Embed PF Isolation in electrons & muons
    pfTools.usePFIso(process)
    # Setup H2Tau custom iso definitions
    setup_h2tau_iso(process)
    # Use POG recommendations for (these) electron Isos
    process.elPFIsoValueGamma04PFIdPFIso.deposits[0].vetos = cms.vstring('EcalEndcaps:ConeVeto(0.08)')
    process.elPFIsoValueGamma04NoPFIdPFIso.deposits[0].vetos = cms.vstring('EcalEndcaps:ConeVeto(0.08)')
    process.elPFIsoValueCharged04PFIdPFIso.deposits[0].vetos = cms.vstring('EcalEndcaps:ConeVeto(0.015)')
    process.elPFIsoValueCharged04NoPFIdPFIso.deposits[0].vetos = cms.vstring('EcalEndcaps:ConeVeto(0.015)')

    # Unembed junk
    process.patMuons.embedCaloMETMuonCorrs = False
    process.patMuons.embedTcMETMuonCorrs = False
    process.patMuons.embedTrack = True
    process.patMuons.pvSrc = cms.InputTag("selectedPrimaryVertex")

    # Do extra electron ID
    process.load("FinalStateAnalysis.PatTools.electrons.electronID_cff")
    process.tuplize += process.recoElectronID
    process.patElectrons.electronIDSources = process.electronIDSources
    process.patElectrons.embedTrack = True

    # Now run PAT
    process.tuplize += process.patDefaultSequence

    # Add FSR photons for ZZ analysis
    process.load("FinalStateAnalysis.PatTools.fsrPhotons_cff")
    process.tuplize += process.fsrPhotonSequence

    # Use HPS taus
    tautools.switchToPFTauHPS(process)
    # Disable tau IsoDeposits
    process.patDefaultSequence.remove(process.patPFTauIsolation)
    process.patTaus.isoDeposits = cms.PSet()
    process.patTaus.userIsolation = cms.PSet()

    # Disable gen match embedding - we keep it in the ntuple
    process.patMuons.embedGenMatch = False
    process.patElectrons.embedGenMatch = False
    process.patTaus.embedGenMatch = False
    process.patTaus.embedGenJetMatch = False

    # Use PFJets and turn on JEC
    jec = [ 'L1FastJet', 'L2Relative', 'L3Absolute' ]
    # If we are running on data (not MC), or embedded sample,
    # apply the MC-DATA residual correction.
    if not isMC or kwargs['embedded']:
        jec.extend([ 'L2L3Residual' ])

    # Define options for BTagging - these are release dependent.
    btag_options = {'doBTagging' : True}
    if cmssw_major_version() == 5:
        btag_options['btagInfo'] = [
            'impactParameterTagInfos',
            'secondaryVertexTagInfos',
            'softMuonTagInfos',
            'secondaryVertexNegativeTagInfos'
        ]
        btag_options['btagdiscriminators'] = [
            'trackCountingHighEffBJetTags',
            'simpleSecondaryVertexHighEffBJetTags',
            'combinedSecondaryVertexMVABJetTags',
            'combinedSecondaryVertexBJetTags',
        ]

    # Use AK5 PFJets
    jettools.switchJetCollection(
        process,
        cms.InputTag('ak5PFJets'),
        doJTA = False,
        jetCorrLabel = ('AK5PF', jec),
        #jetCorrLabel = None,
        doType1MET = False,
        doJetID = True,
        genJetCollection = cms.InputTag("ak5GenJets"),
        **btag_options
    )
    process.patJets.embedPFCandidates = False
    process.patJets.embedCaloTowers = False
    process.patJets.embedGenJetMatch = False
    process.patJets.addAssociatedTracks = False
    process.patJets.embedGenPartonMatch = False
    #process.patJetCorrFactors.useRho = True
    ## Let's use the same rho as in the TauID, so we don't need to do it twice.
    #process.patJetCorrFactors.rho = cms.InputTag(
        #"kt6PFJetsForRhoComputationVoronoi", "rho")

    # Use PFMEt
    mettools.addPfMET(process)
    if not isMC:
        coreTools.runOnData(process)
        process.patMETsPF.addGenMET = False
    output_commands.append('*_selectedPatJets_*_*')

    # Customize/embed all our sequences
    process.load("FinalStateAnalysis.PatTools.patJetProduction_cff")
    # We have to keep all jets (for the MVA MET...)
    process.patJetGarbageRemoval.cut = 'pt > 0'

    final_jet_collection = chain_sequence(
        process.customizeJetSequence, "patJets")
    process.customizeJetSequence.insert(0, process.patJets)
    # Make it a "complete" sequence
    process.customizeJetSequence += process.selectedPatJets
    # We can't mess up the selected pat jets because the taus use them.
    process.selectedPatJets.src = final_jet_collection
    process.patDefaultSequence.replace(process.patJets,
                                       process.customizeJetSequence)

    # Produce the electron collections
    process.load("FinalStateAnalysis.PatTools.patElectronProduction_cff")
    final_electron_collection = chain_sequence(
        process.customizeElectronSequence, "selectedPatElectrons")
    process.tuplize += process.customizeElectronSequence
    process.customizeElectronSequence.insert(0, process.selectedPatElectrons)
    process.patDefaultSequence.replace(process.selectedPatElectrons,
                                       process.customizeElectronSequence)
    # We have to do the pat Jets before the pat electrons since we embed them
    process.customizeElectronSequence.insert(0, process.selectedPatJets)
    process.cleanPatElectrons.src = final_electron_collection

    process.load("FinalStateAnalysis.PatTools.patMuonProduction_cff")
    final_muon_collection = chain_sequence(
        process.customizeMuonSequence, "selectedPatMuons")
    process.customizeMuonSequence.insert(0, process.selectedPatMuons)
    process.patDefaultSequence.replace(process.selectedPatMuons,
                                       process.customizeMuonSequence)
    process.cleanPatMuons.src = final_muon_collection

    process.load("FinalStateAnalysis.PatTools.patTauProduction_cff")
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
    # Apply a loose preselection
    process.cleanPatTaus.preselection = 'abs(eta) < 2.5 & pt > 17'
    # Don't apply any "final" cut
    process.cleanPatTaus.finalCut = ''

    # Setup MET production
    process.load("FinalStateAnalysis.PatTools.patMETProduction_cff")
    final_met_collection = chain_sequence(
        process.customizeMETSequence, "patMETsPF")
    process.tuplize += process.customizeMETSequence
    # The MET systematics depend on all other systematics
    process.systematicsMET.tauSrc = cms.InputTag("cleanPatTaus")
    process.systematicsMET.muonSrc = cms.InputTag("cleanPatMuons")
    process.systematicsMET.electronSrc = cms.InputTag("cleanPatElectrons")

    # Keep all the data formats needed for the systematics
    output_commands.append('recoLeafCandidates_*_*_%s'
                           % process.name_())

    # Define the default lepton cleaning
    process.cleanPatElectrons.preselection = cms.string('pt > 5')
    process.cleanPatElectrons.checkOverlaps.muons.requireNoOverlaps = False
    # Make sure we don't kill any good taus by calling them electrons
    # Note that we don't actually remove these overlaps.
    process.cleanPatElectrons.checkOverlaps.taus = cms.PSet(
        src = final_tau_collection,
        algorithm = cms.string("byDeltaR"),
        preselection = cms.string(
            "tauID('decayModeFinding') > 0.5 &&"
            "tauID('byLooseCombinedIsolationDeltaBetaCorr') > 0.5 &&"
            "tauID('againstElectronLoose') > 0.5 && "
            "pt > 10"
        ),
        deltaR = cms.double(0.1),
        checkRecoComponents = cms.bool(False),
        pairCut = cms.string(""),
        requireNoOverlaps = cms.bool(False),
    )

    output_commands.append('*_cleanPatTaus_*_*')
    output_commands.append('*_cleanPatElectrons_*_*')
    output_commands.append('*_cleanPatMuons_*_*')
    output_commands.append('*_%s_*_*' % final_met_collection.value())

    trigtools.switchOnTrigger(process)

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
        'electrons' : 'cleanPatElectrons',
        'muons' : 'cleanPatMuons',
        'taus' : 'cleanPatTaus',
        'jets' : 'selectedPatJets',
        'met' : final_met_collection,
    }

    # Setup all the PATFinalState objects
    produce_final_states(process, fs_daughter_inputs, output_commands,
                         process.tuplize, kwargs['puTag'])

    return process.tuplize, output_commands

if __name__ == "__main__":
    import doctest
    doctest.testmod()
