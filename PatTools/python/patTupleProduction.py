import FWCore.ParameterSet.Config as cms

import PhysicsTools.PatAlgos.tools.trigTools as trigtools
import PhysicsTools.PatAlgos.tools.jetTools as jettools
import PhysicsTools.PatAlgos.tools.metTools as mettools
import PhysicsTools.PatAlgos.tools.tauTools as tautools
import PhysicsTools.PatAlgos.tools.coreTools as coreTools
import PhysicsTools.PatAlgos.tools.helpers as helpers
import PhysicsTools.PatAlgos.tools.pfTools as pfTools
import PhysicsTools.PatAlgos.patEventContent_cff as patContent

from FinalStateAnalysis.Utilities.cfgtools import chain_sequence

import itertools

def _subsort(iterables):
    for iterable in iterables:
        yield tuple(sorted(iterable))

def _combinatorics(items, n):
    ''' Build unique combination of items
    >>> items = ['Ananas', 'Abricot', 'Bouef']
    >>> list(_combinatorics(items, 2))
    [('Ananas', 'Ananas'), ('Ananas', 'Abricot'), ('Ananas', 'Bouef'), ('Abricot', 'Abricot'), ('Abricot', 'Bouef'), ('Bouef', 'Bouef')]
    '''
    indices = range(len(items))
    combinatorics = set(_subsort(itertools.product(indices, repeat=n)))
    for index_set in sorted(combinatorics):
        yield tuple(items[x] for x in index_set)

def configurePatTuple(process, isMC=True, **kwargs):
    # Stuff we always keep
    output_commands = [
        '*_addPileupInfo_*_*',
        'edmMergeableCounter_*_*_*',
        '*_lumiProducer_*_*',
        '*_particleFlow_*_*',
        '*_offlineBeamSpot_*_*',
        '*_trackCandidates_*_*',
        '*_gsfTrackCandidates_*_*',
        '*_generalTracks_*_*',
        '*_electronGsfTracks_*_*',
        '*_offlinePrimaryVertices*_*_*',
        '*_ak5PFJets_*_*',
        '*_ak5GenJets_*_*',
        '*_hltTriggerSummaryAOD_*_*',
        '*_MEtoEDMConverter*_*_%s' % process.name_(),
        'LHEEventProduct_*_*_*',
        'GenEventInfoProduct_generator_*_*',
        '*_kt6PFJetsForRhoComputationVoronoi_rho_*',
    ]
    # Define our patTuple production sequence
    process.tuplize = cms.Sequence()
    # Only keep interesting genParticles
    process.load("FinalStateAnalysis.RecoTools.genParticleTrimmer_cfi")
    process.genParticles = process.prunedGenParticles.clone()
    if isMC:
        #process.tuplize += process.genParticles
        output_commands.append('*_genParticles_*_%s' % process.name_())
        output_commands.append('*_genParticles_*_*')

    output_commands.append('*_tauGenJetsSelectorAllHadrons_*_*')
    output_commands.append('*_tauGenJets_*_*')
    output_commands.append('*_ak5GenJets_*_*')
    # Select vertices
    process.load("FinalStateAnalysis.RecoTools.vertexSelection_cff")
    output_commands.append('*_selectedPrimaryVertex_*_*')
    output_commands.append('*_selectPrimaryVerticesQuality_*_*')
    process.tuplize += process.selectPrimaryVertices

    # Rerun tau-ID
    process.load('Configuration/StandardSequences/Services_cff')
    process.load('Configuration/StandardSequences/GeometryIdeal_cff')
    process.load('Configuration/StandardSequences/MagneticField_cff')
    process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

    # Optimization - remove PFTauTagInfo compatibility layer
    process.recoTauClassicHPSSequence.remove(process.pfRecoTauTagInfoProducer)
    assert(process.combinatoricRecoTaus.modifiers[3].name.value() == 'TTIworkaround')
    del process.combinatoricRecoTaus.modifiers[3]

    process.tuplize += process.recoTauClassicHPSSequence
    ## Run rho computation
    #from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets
    #kt6PFJets.Rho_EtaMax = cms.double(2.5)
    #kt6PFJets.doRhoFastjet = True
    #process.kt6PFJets = kt6PFJets
    #process.tuplize += process.kt6PFJets

    # Run pat default sequence
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    # Embed PF Isolation in electrons & muons
    pfTools.usePFIso(process)

    # Unembed junks
    process.patMuons.embedCaloMETMuonCorrs = False
    process.patMuons.embedTcMETMuonCorrs = False
    process.patMuons.embedTrack = False
    process.patMuons.pvSrc = cms.InputTag("selectedPrimaryVertex")

    # Do extra electron ID
    process.load("FinalStateAnalysis.PatTools.electrons.electronID_cff")
    process.tuplize += process.recoElectronID
    process.patElectrons.electronIDSources = process.electronIDSources

    # Run EGamma electron energy calibration
    process.load("EgammaCalibratedGsfElectrons.CalibratedElectronProducers.calibratedGsfElectrons_cfi")
    process.RandomNumberGeneratorService.calibratedGsfElectrons = cms.PSet(
        initialSeed = cms.untracked.uint32(1), # A frickin billion
        engineName = cms.untracked.string('TRandom3')
    )
    process.calibratedGsfElectrons.inputDataset = kwargs['dataset']
    process.calibratedGsfElectrons.isMC = bool(isMC)
    process.calibratedGsfElectrons.isAOD = True
    process.calibratedGsfElectrons.updateEnergyError = cms.bool(True)
    # Run a sanity check on the calibration configuration.
    from FinalStateAnalysis.PatTools.electrons.patElectronEmbedCalibratedGsf_cfi \
            import validate_egamma_calib_config
    validate_egamma_calib_config(process)

    process.tuplize += process.calibratedGsfElectrons
    # Keep the calibratedGsfElectrons - we embed refs to this into the
    # pat::Electrons
    output_commands.append('*_calibratedGsfElectrons_*_*')

    # Now run PAT
    process.tuplize += process.patDefaultSequence

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
    if not isMC:
        jec.extend([ 'L2L3Residual' ])
    # Use AK5 PFJets
    jettools.switchJetCollection(process,
                                 cms.InputTag('ak5PFJets'),
                                 doJTA = False,
                                 doBTagging = True,
                                 jetCorrLabel = ('AK5PF', jec),
                                 #jetCorrLabel = None,
                                 doType1MET = False,
                                 doJetID = True,
                                 genJetCollection = cms.InputTag("ak5GenJets"))
    process.patJets.embedPFCandidates = False
    process.patJets.embedCaloTowers = False
    process.patJetCorrFactors.useRho = True
    # Let's use the same rho as in the TauID, so we don't need to do it twice.
    process.patJetCorrFactors.rho = cms.InputTag(
        "kt6PFJetsForRhoComputationVoronoi", "rho")

    # Use PFMEt
    mettools.addPfMET(process)
    if not isMC:
        coreTools.runOnData(process)
        process.patMETsPF.addGenMET = False
    output_commands.append('patJets_selectedPatJets_*_*')

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
    # The "effective area" calculation needs to know if it is data/mc, etc.
    process.patElectronEffectiveAreaEmbedder.target = kwargs['target']

    process.load("FinalStateAnalysis.PatTools.patMuonProduction_cff")
    final_muon_collection = chain_sequence(
        process.customizeMuonSequence, "selectedPatMuons")
    process.customizeMuonSequence.insert(0, process.selectedPatMuons)
    process.patDefaultSequence.replace(process.selectedPatMuons,
                                       process.customizeMuonSequence)
    process.cleanPatMuons.src = final_muon_collection
    # The "effective area" calculation needs to know if it is data/mc, etc.
    process.patMuonEffectiveAreaEmbedder.target = kwargs['target']

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
    # Don't apply any prselections
    process.cleanPatTaus.preselection = ''

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

    #process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerMatcher_cfi")
    #trigtools.switchOnTriggerMatchEmbedding(process)
    trigtools.switchOnTrigger(process)

    # Build the PATFinalStateEventObject
    process.load("FinalStateAnalysis.PatTools.finalStates.patFinalStateEventProducer_cfi")
    process.patFinalStateEventProducer.electronSrc = final_electron_collection
    process.patFinalStateEventProducer.muonSrc = cms.InputTag("cleanPatMuons")
    process.patFinalStateEventProducer.tauSrc = cms.InputTag("cleanPatTaus")
    process.patFinalStateEventProducer.jetSrc = cms.InputTag("selectedPatJets")
    process.patFinalStateEventProducer.metSrc = final_met_collection
    process.tuplize += process.patFinalStateEventProducer
    output_commands.append('*_patFinalStateEventProducer_*_*')
    process.patFinalStateEventProducer.puTag = cms.string(kwargs['puTag'])

    # Now build the PATFinalStateLS object, which holds LumiSection info.
    process.load(
        "FinalStateAnalysis.PatTools.finalStates.patFinalStateLSProducer_cfi")
    process.tuplize += process.finalStateLS
    output_commands.append('*_finalStateLS_*_*')
    if isMC:
        process.finalStateLS.xSec = kwargs['xSec']

    # Apply some loose PT cuts on the objects we use to create the final states
    # so the combinatorics don't blow up
    process.muonsForFinalStates = cms.EDFilter(
        "PATMuonRefSelector",
        src = cms.InputTag("cleanPatMuons"),
        cut = cms.string('pt > 4'),
        filter = cms.bool(False),
    )

    process.electronsForFinalStates = cms.EDFilter(
        "PATElectronRefSelector",
        src = cms.InputTag("cleanPatElectrons"),
        cut = cms.string('abs(eta) < 2.5 & pt > 4'),
        filter = cms.bool(False),
    )

    # Require that the PT of the jet (either corrected jet or tau)
    # to be greater than 17
    process.tausForFinalStates = cms.EDFilter(
        "PATTauRefSelector",
        src = cms.InputTag("cleanPatTaus"),
        cut = cms.string('abs(eta) < 2.5 & pt > 17 & tauID("decayModeFinding")'),
        filter = cms.bool(False),
    )

    process.selectObjectsForFinalStates = cms.Sequence(
        process.muonsForFinalStates
        + process.electronsForFinalStates
        + process.tausForFinalStates
    )

    process.tuplize += process.selectObjectsForFinalStates

    # Now build all of our DiLeptons and TriLepton final states
    lepton_types = [('Elec', cms.InputTag("electronsForFinalStates")),
                    ('Mu', cms.InputTag("muonsForFinalStates")),
                    ('Tau', cms.InputTag("tausForFinalStates"))]
    #lepton_types = [('Elec', cms.InputTag("cleanPatElectrons")),
                    #('Mu', cms.InputTag("cleanPatMuons")),
                    #('Tau', cms.InputTag("cleanPatTaus"))]

    process.buildDiLeptons = cms.Sequence()

    process.load(
        "FinalStateAnalysis.PatTools.finalStates.patFinalStatesEmbedExtraCollections_cfi")

    # Build di-lepton pairs
    for dilepton in _combinatorics(lepton_types, 2):
        # Don't build two jet states
        if (dilepton[0][0], dilepton[1][0]) == ('Tau', 'Tau'):
            continue

        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3'] # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%s%sFinalStateProducer" % (dilepton[0][0], dilepton[1][0]),
            evtSrc = cms.InputTag("patFinalStateEventProducer"),
            leg1Src = dilepton[0][1],
            leg2Src = dilepton[1][1],
            # X-cleaning
            cut = cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s%s" % (dilepton[0][0], dilepton[1][0])
        setattr(process, producer_name + "Raw", producer)
        process.buildDiLeptons += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(process,
            process.patFinalStatesEmbedObjects, producer_name)
        process.buildDiLeptons += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = getattr(process, final_module_name.value())
        final_module.setLabel(producer_name)
        setattr(process, producer_name, final_module)
        output_commands.append("*_%s_*_*" % producer_name)

    process.tuplize += process.buildDiLeptons
    # Build tri-lepton pairs
    process.buildTriLeptons = cms.Sequence()
    for trilepton in _combinatorics(lepton_types, 3):
        # Don't build three jet states
        if (trilepton[0][0], trilepton[1][0], trilepton[2][0]) == \
           ('Tau', 'Tau', 'Tau'):
            continue

        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3'] # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%s%s%sFinalStateProducer" %
            (trilepton[0][0], trilepton[1][0], trilepton[2][0]),
            evtSrc = cms.InputTag("patFinalStateEventProducer"),
            leg1Src = trilepton[0][1],
            leg2Src = trilepton[1][1],
            leg3Src = trilepton[2][1],
            # X-cleaning
            cut = cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s%s%s" % (
            trilepton[0][0], trilepton[1][0], trilepton[2][0])
        #setattr(process, producer_name, producer)
        #process.buildTriLeptons += producer
        setattr(process, producer_name + "Raw", producer)
        process.buildTriLeptons += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(process,
            process.patFinalStatesEmbedObjects, producer_name)
        process.buildTriLeptons += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = getattr(process, final_module_name.value())
        final_module.setLabel(producer_name)
        setattr(process, producer_name, final_module)
        output_commands.append("*_%s_*_*" % producer_name)
    process.tuplize += process.buildTriLeptons

    # Build 4 lepton final states
    process.buildQuadLeptons = cms.Sequence()
    for quadlepton in _combinatorics(lepton_types, 4):
        # Don't build states with more than 2 hadronic taus
        if [x[0] for x in quadlepton].count('Tau') > 2:
            continue

        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3'] # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%s%s%s%sFinalStateProducer" %
            (quadlepton[0][0], quadlepton[1][0], quadlepton[2][0],
             quadlepton[3][0]),
            evtSrc = cms.InputTag("patFinalStateEventProducer"),
            leg1Src = quadlepton[0][1],
            leg2Src = quadlepton[1][1],
            leg3Src = quadlepton[2][1],
            leg4Src = quadlepton[3][1],
            # X-cleaning
            cut = cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s%s%s%s" % (
            quadlepton[0][0], quadlepton[1][0], quadlepton[2][0],
            quadlepton[3][0]
        )
        #setattr(process, producer_name, producer)
        #process.buildTriLeptons += producer
        setattr(process, producer_name + "Raw", producer)
        process.buildQuadLeptons += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(process,
            process.patFinalStatesEmbedObjects, producer_name)
        process.buildQuadLeptons += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = getattr(process, final_module_name.value())
        final_module.setLabel(producer_name)
        setattr(process, producer_name, final_module)
        output_commands.append("*_%s_*_*" % producer_name)
    process.tuplize += process.buildQuadLeptons

    # Tell the framework to shut up!
    process.load("FWCore.MessageLogger.MessageLogger_cfi")
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000

    return process.tuplize, output_commands

if __name__ == "__main__":
    import doctest
    doctest.testmod()
