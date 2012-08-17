'''

Functions to build the PATFinalStateEvents and friends on top of the PAT tuple

Arguments:
    process : the CMS process
    collections : a dictionary matching
        'electrons', 'muons', 'taus', 'jets', and 'met' to the appropriate
        collections (like cleanPatElectrons)
    output_commands : will be modified in place with new products
    sequence : analysis sequence to add to
    puTag : what PU scenario we are in
    noTracks : if true, remove stuff that depends on the tracks
    buildFSAEvent : whether or not to build the FSA event object (if not,
                    it must already be in the event)

Author Evan K. Friis, UW Madison

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import chain_sequence
import PhysicsTools.PatAlgos.tools.helpers as helpers
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


def produce_final_states(process, collections, output_commands, sequence, puTag,
                         buildFSAEvent=True, noTracks=False):

    muonsrc = collections['muons']
    esrc = collections['electrons']
    tausrc = collections['taus']
    jetsrc = collections['jets']
    metsrc = collections['met']

    # Build the PATFinalStateEventObject
    if buildFSAEvent == True:
        process.load("FinalStateAnalysis.PatTools.finalStates.patFinalStateEventProducer_cfi")
        process.patFinalStateEventProducer.electronSrc = cms.InputTag(esrc)
        process.patFinalStateEventProducer.muonSrc = cms.InputTag(muonsrc)
        process.patFinalStateEventProducer.tauSrc = cms.InputTag(tausrc)
        process.patFinalStateEventProducer.jetSrc = cms.InputTag(jetsrc)
        process.patFinalStateEventProducer.metSrc = metsrc
        process.patFinalStateEventProducer.puTag = cms.string(puTag)
        sequence += process.patFinalStateEventProducer
    elif buildFSAEvent == 'eFix':
        # Temporary workaround for the 2012-05-28 PAT tuples
        # Copy the existing FS Event, but update the electron collection ref.
        process.patFinalStateEventProducer = cms.EDProducer(
            "PATFinalStateElectronFixer",
            fseSrc = cms.InputTag("patFinalStateEventProducer"),
            electronSrc = cms.InputTag(esrc)
        )
        sequence += process.patFinalStateEventProducer

    # Always keep
    output_commands.append('*_patFinalStateEventProducer_*_*')

    # Apply some loose PT cuts on the objects we use to create the final states
    # so the combinatorics don't blow up
    process.muonsForFinalStates = cms.EDFilter(
        "PATMuonRefSelector",
        src = cms.InputTag(muonsrc),
        cut = cms.string('pt > 4 & (isGlobalMuon | isTrackerMuon)'),
        filter = cms.bool(False),
    )

    process.electronsForFinalStates = cms.EDFilter(
        "PATElectronRefSelector",
        src = cms.InputTag(esrc),
        cut = cms.string('abs(eta) < 2.5 & pt > 7'),
        filter = cms.bool(False),
    )

    # Require that the PT of the jet (either corrected jet or tau)
    # to be greater than 17
    process.tausForFinalStates = cms.EDFilter(
        "PATTauRefSelector",
        src = cms.InputTag(tausrc),
        cut = cms.string('abs(eta) < 2.5 & pt > 17 & tauID("decayModeFinding")'),
        filter = cms.bool(False),
    )

    process.selectObjectsForFinalStates = cms.Sequence(
        process.muonsForFinalStates
        + process.electronsForFinalStates
        + process.tausForFinalStates
    )

    sequence += process.selectObjectsForFinalStates

    # Now build all of our DiLeptons and TriLepton final states
    lepton_types = [('Elec', cms.InputTag("electronsForFinalStates")),
                    ('Mu', cms.InputTag("muonsForFinalStates")),
                    ('Tau', cms.InputTag("tausForFinalStates"))]

    process.buildDiLeptons = cms.Sequence()

    process.load(
        "FinalStateAnalysis.PatTools.finalStates.patFinalStatesEmbedExtraCollections_cfi")
    # If we don't have tracks, don't fit the FS vertices
    if noTracks:
        process.patFinalStateVertexFitter.enable = False

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
        final_module = cms.EDProducer(
            "PATFinalStateCopier",
            src = final_module_name
        )
        setattr(process, producer_name, final_module)
        process.buildDiLeptons += final_module
        setattr(process, producer_name, final_module)
        output_commands.append("*_%s_*_*" % producer_name)

    sequence += process.buildDiLeptons
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
        final_module = cms.EDProducer(
            "PATFinalStateCopier",
            src = final_module_name
        )
        setattr(process, producer_name, final_module)
        process.buildTriLeptons += final_module
        output_commands.append("*_%s_*_*" % producer_name)
    sequence += process.buildTriLeptons

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
        final_module = cms.EDProducer(
            "PATFinalStateCopier",
            src = final_module_name
        )
        setattr(process, producer_name, final_module)
        process.buildQuadLeptons += final_module
        output_commands.append("*_%s_*_*" % producer_name)
    sequence += process.buildQuadLeptons

if __name__ == "__main__":
    import doctest
    doctest.testmod()
