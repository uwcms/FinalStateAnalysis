import FWCore.ParameterSet.Config as cms

import PhysicsTools.PatAlgos.tools.trigTools as trigtools
import PhysicsTools.PatAlgos.tools.jetTools as jettools
import PhysicsTools.PatAlgos.tools.metTools as mettools
import PhysicsTools.PatAlgos.tools.tauTools as tautools
import PhysicsTools.PatAlgos.tools.coreTools as coreTools
import PhysicsTools.PatAlgos.tools.helpers as helpers
import PhysicsTools.PatAlgos.patEventContent_cff as patContent

from FinalStateAnalysis.Utilities.cfgtools import chain_sequence
from FinalStateAnalysis.PatTools.pfNoPileup import configurePFNoPileup
from FinalStateAnalysis.PatTools.muons.pfIsolation import addMuPFIsolation
from FinalStateAnalysis.PatTools.electrons.pfIsolation import addElecPFIsolation

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
    ]
    # Define our patTuple production sequence
    process.tuplize = cms.Sequence()
    # Only keep interesting genParticles
    process.load("FinalStateAnalysis.RecoTools.genParticleTrimmer_cfi")
    process.genParticles = process.prunedGenParticles.clone()
    if isMC:
        process.tuplize += process.genParticles
        output_commands.append('*_genParticles_*_%s' % process.name_())

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
    process.tuplize += process.recoTauClassicHPSSequence
    # Run rho computation
    from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets
    kt6PFJets.Rho_EtaMax = cms.double(2.5)
    kt6PFJets.doRhoFastjet = True
    process.kt6PFJets = kt6PFJets
    process.tuplize += process.kt6PFJets
    # Run pat default sequence
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    # Load PFNoPileup.  Make sure we do this after pat messes around w/ it
    process.tuplize += configurePFNoPileup(process)
    # Embed muon tracks
    process.patMuons.embedTrack = True
    process.patMuons.pvSrc = cms.InputTag("selectedPrimaryVertex")
    # Do extra electron ID
    process.load("FinalStateAnalysis.PatTools.electrons.electronID_cff")
    process.tuplize += process.recoElectronID
    #output_commands.append('*_particleFlow_*_*')
    #print repr(process.pfPostSequence)
    process.tuplize += process.patDefaultSequence
    # Embed PF Isolation in electrons & muons
    addMuPFIsolation(process, process.patDefaultSequence)
    addElecPFIsolation(process, process.patDefaultSequence)
    process.patElectrons.electronIDSources = process.electronIDSources
    # Use HPS taus
    tautools.switchToPFTauHPS(process)
    # Disable tau IsoDeposits
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
    # Use PFMEt
    mettools.addPfMET(process)
    if not isMC:
        coreTools.runOnData(process)
        process.patMETsPF.addGenMET = False
    output_commands.append('patJets_selectedPatJets_*_*')

    # Customize/embed all our sequences
    process.load("FinalStateAnalysis.PatTools.patJetProduction_cff")
    # Cut all jets with pt < 5
    process.patJetGarbageRemoval.cut = 'pt > 17 | correctedP4("Uncorrected").pt > 17'

    final_jet_collection = chain_sequence(
        process.customizeJetSequence, "patJets")
    process.customizeJetSequence.insert(0, process.patJets)
    # Make it a "complete" sequence
    process.customizeJetSequence += process.selectedPatJets
    # We can't mess up the selected pat jets because the taus use them.
    process.selectedPatJets.src = final_jet_collection
    # Apply a pt cut on the uncorrected jet to get rid of really low pt junk
    #process.selectedPatJets.cut = 'userCand("uncorr").pt > 5'
    process.patDefaultSequence.replace(process.patJets,
                                       process.customizeJetSequence)

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
    # Don't apply any prselections
    process.cleanPatTaus.preselection = ''

    # Make clones of the Tau and Jet sequences w/o and pt requirement
    process.jetsForMetSyst = helpers.cloneProcessingSnippet(
        process, process.customizeJetSequence, 'ForMETSyst')
    process.tausForMetSyst = helpers.cloneProcessingSnippet(
        process, process.customizeTauSequence, 'ForMETSyst')
    # Don't apply any cut for these
    process.patJetGarbageRemovalForMETSyst.cut = ''
    process.tuplize += process.jetsForMetSyst
    process.tuplize += process.tausForMetSyst
    # We have to make our clone of cleanPatTaus separately, since e/mu
    # cleaning is applied - therefore it isn't in the customizeTausSequence.
    process.cleanPatTausForMETSyst = process.cleanPatTaus.clone(
        src = cms.InputTag(process.cleanPatTaus.src.value() + "ForMETSyst"))
    process.tuplize += process.cleanPatTausForMETSyst

    # Setup MET production
    process.load("FinalStateAnalysis.PatTools.patMETProduction_cff")
    final_met_collection = chain_sequence(
        process.customizeMETSequence, "patMETsPF")
    process.tuplize += process.customizeMETSequence
    # The MET systematics depend on all other systematics
    process.systematicsMET.tauSrc = cms.InputTag("cleanPatTausForMETSyst")
    process.systematicsMET.muonSrc = cms.InputTag("cleanPatMuons")
    process.systematicsMET.electronSrc = cms.InputTag("cleanPatElectrons")

    # Keep all the data formats needed for the systematics
    output_commands.append('recoLeafCandidates_*_*_%s'
                           % process.name_())
    # We can drop to jet and tau MET specific products. They were only used for
    # computation of the MET numbers.
    output_commands.append('drop recoLeafCandidates_*ForMETSyst_*_%s'
                           % process.name_())

    # Define the default lepton cleaning
    process.cleanPatElectrons.preselection = cms.string('pt > 8')
    process.cleanPatElectrons.checkOverlaps.muons.requireNoOverlaps = False
    # Make sure we don't kill any good taus by calling them electrons
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
