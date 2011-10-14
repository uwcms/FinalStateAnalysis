import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.sequencetools import chain_sequence
import itertools

def _subsort(iterables):
    for iterable in iterables:
        yield tuple(sorted(iterable))

def _combinatorics(items, n):
    ''' Build unique combination of items
    >>> items = ['Ananas', 'Abricot', 'Bouef']
    >>> list(_combinatorics(items, 2))
    [('Ananas', 'Abricot'), ('Ananas', 'Bouef'), ('Abricot', 'Bouef')]
    >>> list(_combinatorics(items, 3))
    [('Ananas', 'Abricot', 'Bouef')]
    '''
    indices = range(len(items))
    combinatorics = set(_subsort(itertools.permutations(indices, n)))
    for index_set in sorted(combinatorics):
        yield tuple(items[x] for x in index_set)


def configurePatTuple(process):
    process.tuplize = cms.Sequence()
    # Select vertices
    process.load("FinalStateAnalysis.RecoTools.vertexSelection_cff")
    process.tuplize += process.selectPrimaryVertices
    # Luminosity weighting
    process.load("FinalStateAnalysis.RecoTools.lumiWeighting_cfi")
    process.tuplize += lumiWeights
    # Rerun tau-ID
    process.load('Configuration/StandardSequences/Services_cff')
    process.load('Configuration/StandardSequences/GeometryIdeal_cff')
    process.load('Configuration/StandardSequences/MagneticField_cff')
    process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    process.sequence += process.PFTau
    # Run rho computation
    from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets
    kt6PFJets.Rho_EtaMax = cms.double(2.5)
    kt6PFJets.doRhoFastjet = True
    process.kt6PFJets = kt6PFJets
    process.tuplize += process.kt6PFJets
    # Run pat default sequence
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    process.sequence += process.patDefaultSequence
    # Define the default lepton cleaning
    # FIXME
    process.load("FinalStateAnalysis.PatTools.patTauProduction_cff")
    final_tau_collection = chain_sequence(
        process.customizeTauSequence, "cleanPatTaus")
    process.load("FinalStateAnalysis.PatTools.patMuonProduction_cff")
    final_muon_collection = chain_sequence(
        process.customizeMuonSequence, "cleanPatMuons")
    process.load("FinalStateAnalysis.PatTools.patElectronProduction_cff")
    final_electron_collection = chain_sequence(
        process.customizeElectronSequence, "cleanPatElectrons")
    # Setup MET production
    process.load("FinalStateAnalysis.PatTools.patMETProduction_cff")
    final_met_collection = chain_sequence(
        process.customizeMETSequence, "patMETsPF")
    # The MET systematics depend on all other systematics
    process.systematicsMET.tauSrc = final_tau_collection
    process.systematicsMET.muonSrc = final_muon_collection
    process.systematicsMET.electronSrc = final_electron_collection
    # Now build all of our DiLeptons and TriLepton final states
    lepton_types = [('Elec', final_electron_collection),
                    ('Mu', final_muon_collection),
                    ('Tau', final_tau_collection)]
    # Build di-lepton pairs
    for dilepton in _combinatorics(lepton_types, 2):
        producer = cms.EDProducer(
            "PAT%s%sFinalStateProducer" % (dilepton[0][0], dilepton[1][0]),
            metSrc = final_met_collection,
            pvSrc = cms.InputTag("selectedPrimaryVertex"),
            leg1Src = dilepton[0][1],
            leg2Src = dilepton[1][1],
            cut = cms.string('fixme')
        )
        producer_name = "finalState%s%s" % (dilepton[0][0], dilepton[1][0])
        setattr(process, producer_name, producer)
    # Build tri-lepton pairs
    for trilepton in _combinatorics(lepton_types, 3):
        producer = cms.EDProducer(
            "PAT%s%s%sFinalStateProducer" %
            (dilepton[0][0], dilepton[1][0], dilepton[2][0]),
            metSrc = final_met_collection,
            pvSrc = cms.InputTag("selectedPrimaryVertex"),
            leg1Src = dilepton[0][1],
            leg2Src = dilepton[1][1],
            leg3Src = dilepton[2][1],
            cut = cms.string('fixme')
        )
        producer_name = "finalState%s%s%s" % (
            dilepton[0][0], dilepton[1][0], dilepton[2][0])
        setattr(process, producer_name, producer)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
