'''

Functions to build the PATFinalStateEvents and friends on top of the PAT tuple

Arguments:
    process : the CMS process
    collections : a dictionary matching
        'electrons', 'muons', 'taus', 'jets', 'photons', and 'met'
        to the appropriate collections (like cleanPatElectrons)
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
    >>> list(_combinatorics(items, 2))[0:3]
    [('Ananas', 'Ananas'), ('Ananas', 'Abricot'), ('Ananas', 'Bouef')]
    '''
    indices = range(len(items))
    combinatorics = set(_subsort(itertools.product(indices, repeat=n)))
    for index_set in sorted(combinatorics):
        yield tuple(items[x] for x in index_set)


def produce_final_states(process, collections, output_commands,
                         sequence, puTag, buildFSAEvent=True,
                         noTracks=False, noPhotons=False):

    muonsrc = collections['muons']
    esrc = collections['electrons']
    tausrc = collections['taus']
    jetsrc = collections['jets']
    pfmetsrc = collections['pfmet']
    mvametsrc = collections['mvamet']
    phosrc = collections['photons']

    # Build the PATFinalStateEventObject
    if buildFSAEvent:
        process.load("FinalStateAnalysis.PatTools."
                     "finalStates.patFinalStateEventProducer_cfi")
        process.patFinalStateEventProducer.electronSrc = cms.InputTag(esrc)
        process.patFinalStateEventProducer.muonSrc = cms.InputTag(muonsrc)
        process.patFinalStateEventProducer.tauSrc = cms.InputTag(tausrc)
        process.patFinalStateEventProducer.jetSrc = cms.InputTag(jetsrc)
        process.patFinalStateEventProducer.phoSrc = cms.InputTag(phosrc)
        process.patFinalStateEventProducer.metSrc = pfmetsrc
        process.patFinalStateEventProducer.puTag = cms.string(puTag)
        process.patFinalStateEventProducer.mets.pfmet = pfmetsrc
        process.patFinalStateEventProducer.mets.mvamet = mvametsrc
        sequence += process.patFinalStateEventProducer

    # Always keep
    output_commands.append('*_patFinalStateEventProducer_*_*')

    # Apply some loose PT cuts on the objects we use to create the final states
    # so the combinatorics don't blow up
    process.muonsForFinalStates = cms.EDFilter(
        "PATMuonRefSelector",
        src=cms.InputTag(muonsrc),
        cut=cms.string('pt > 4 & (isGlobalMuon | isTrackerMuon)'),
        filter=cms.bool(False),
    )

    process.electronsForFinalStates = cms.EDFilter(
        "PATElectronRefSelector",
        src=cms.InputTag(esrc),
        cut=cms.string('abs(eta) < 2.5 & pt > 7'),
        filter=cms.bool(False),
    )

    process.photonsForFinalStates = cms.EDFilter(
        "PATPhotonRefSelector",
        src=cms.InputTag(phosrc),
        cut=cms.string('abs(superCluster().eta()) < 3.0 & pt > 10'),
        filter=cms.bool(False),
    )

    # Require that the PT of the jet (either corrected jet or tau)
    # to be greater than 17
    process.tausForFinalStates = cms.EDFilter(
        "PATTauRefSelector",
        src=cms.InputTag(tausrc),
        cut=cms.string('abs(eta) < 2.5 & pt > 17 & tauID("decayModeFinding")'),
        filter=cms.bool(False),
    )

    process.selectObjectsForFinalStates = cms.Sequence(
        process.muonsForFinalStates
        + process.electronsForFinalStates
        + process.tausForFinalStates
    )
    if not noPhotons:
        process.selectObjectsForFinalStates += process.photonsForFinalStates

    sequence += process.selectObjectsForFinalStates

    # Now build all combinatorics for E/Mu/Tau/Photon
    object_types = [('Elec', cms.InputTag("electronsForFinalStates")),
                    ('Mu', cms.InputTag("muonsForFinalStates")),
                    ('Tau', cms.InputTag("tausForFinalStates"))]

    if not noPhotons:
        object_types.append(('Pho', cms.InputTag("photonsForFinalStates")))

    process.buildDiObjects = cms.Sequence()

    process.load("FinalStateAnalysis.PatTools."
                 "finalStates.patFinalStatesEmbedExtraCollections_cfi")
    # If we don't have tracks, don't fit the FS vertices
    if noTracks:
        process.patFinalStateVertexFitter.enable = False

    # Build di-object pairs
    for diobject in _combinatorics(object_types, 2):
        # Don't build two jet states
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Tau'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Pho'):
            continue

        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3']  # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%s%sFinalStateProducer" % (diobject[0][0], diobject[1][0]),
            evtSrc=cms.InputTag("patFinalStateEventProducer"),
            leg1Src=diobject[0][1],
            leg2Src=diobject[1][1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s%s" % (diobject[0][0], diobject[1][0])
        setattr(process, producer_name + "Raw", producer)
        process.buildDiObjects += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, process.patFinalStatesEmbedObjects, producer_name)
        process.buildDiObjects += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        process.buildDiObjects += final_module
        setattr(process, producer_name, final_module)
        output_commands.append("*_%s_*_*" % producer_name)
    sequence += process.buildDiObjects

    # Build tri-lepton pairs
    process.buildTriObjects = cms.Sequence()
    for triobject in _combinatorics(object_types, 3):
        # Don't build three jet states
        if (triobject[0][0], triobject[1][0], triobject[2][0]) == \
           ('Tau', 'Tau', 'Tau'):
            continue
        n_taus = [x[0] for x in triobject].count('Tau')
        n_phos = [x[0] for x in triobject].count('Pho')
        if n_taus > 2:
            continue
        if n_phos > 2:
            continue
        if n_taus and n_phos:
            continue

        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3']  # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%s%s%sFinalStateProducer" %
            (triobject[0][0], triobject[1][0], triobject[2][0]),
            evtSrc=cms.InputTag("patFinalStateEventProducer"),
            leg1Src=triobject[0][1],
            leg2Src=triobject[1][1],
            leg3Src=triobject[2][1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s%s%s" % (
            triobject[0][0], triobject[1][0], triobject[2][0])
        #setattr(process, producer_name, producer)
        #process.buildTriLeptons += producer
        setattr(process, producer_name + "Raw", producer)
        process.buildTriObjects += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, process.patFinalStatesEmbedObjects, producer_name)
        process.buildTriObjects += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        process.buildTriObjects += final_module
        output_commands.append("*_%s_*_*" % producer_name)
    sequence += process.buildTriObjects

    # Build 4 lepton final states
    process.buildQuadObjects = cms.Sequence()
    for quadobject in _combinatorics(object_types, 4):
        # Don't build states with more than 2 hadronic taus or phos
        n_taus = [x[0] for x in triobject].count('Tau')
        n_phos = [x[0] for x in triobject].count('Pho')
        if n_taus > 2:
            continue
        if n_phos > 2:
            continue
        if n_taus and n_phos:
            continue

        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3']  # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%s%s%s%sFinalStateProducer" %
            (quadobject[0][0], quadobject[1][0], quadobject[2][0],
             quadobject[3][0]),
            evtSrc=cms.InputTag("patFinalStateEventProducer"),
            leg1Src=quadobject[0][1],
            leg2Src=quadobject[1][1],
            leg3Src=quadobject[2][1],
            leg4Src=quadobject[3][1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s%s%s%s" % (
            quadobject[0][0], quadobject[1][0], quadobject[2][0],
            quadobject[3][0]
        )
        #setattr(process, producer_name, producer)
        #process.buildTriLeptons += producer
        setattr(process, producer_name + "Raw", producer)
        process.buildQuadObjects += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, process.patFinalStatesEmbedObjects, producer_name)
        process.buildQuadObjects += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        process.buildQuadObjects += final_module
        output_commands.append("*_%s_*_*" % producer_name)
    sequence += process.buildQuadObjects

if __name__ == "__main__":
    import doctest
    doctest.testmod()
