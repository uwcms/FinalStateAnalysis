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


def produce_final_states(process, daughter_collections, output_commands,
                         sequence, puTag, buildFSAEvent=True,
                         noTracks=False, runMVAMET=False, hzz=False,
                         rochCor="", eleCor="", use25ns=False, **kwargs):

    src = dict(daughter_collections) # make a copy so we don't change the passed collection

    # Build the PATFinalStateEventObject
    if buildFSAEvent:
        process.load("FinalStateAnalysis.PatTools."
                     "finalStates.patFinalStateEventProducer_cfi")
        process.patFinalStateEventProducer.electronSrc = cms.InputTag(src['electrons'])
        process.patFinalStateEventProducer.muonSrc = cms.InputTag(src['muons'])
        process.patFinalStateEventProducer.tauSrc = cms.InputTag(src['taus'])
        process.patFinalStateEventProducer.jetSrc = cms.InputTag(src['jets'])
        process.patFinalStateEventProducer.phoSrc = cms.InputTag(src['photons'])
        process.patFinalStateEventProducer.metSrc = cms.InputTag(src['pfmet'])
        process.patFinalStateEventProducer.puTag = cms.string(puTag)
        if 'extraWeights' in src:
            process.patFinalStateEventProducer.extraWeights = src['extraWeights']
        process.patFinalStateEventProducer.trgSrc = cms.InputTag("selectedPatTrigger")
        process.patFinalStateEventProducer.rhoSrc = cms.InputTag('fixedGridRhoAll')
        process.patFinalStateEventProducer.pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
        process.patFinalStateEventProducer.verticesSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
        process.patFinalStateEventProducer.genParticleSrc = cms.InputTag("prunedGenParticles")
        process.patFinalStateEventProducer.mets = cms.PSet(
            pfmet = cms.InputTag(src['pfmet']),
        )
        if runMVAMET:
            process.patFinalStateEventProducer.mets.mvamet = cms.InputTag(src['mvamet'])
        
        sequence += process.patFinalStateEventProducer

    # Always keep
  #  output_commands.append('*_patFinalStateEventProducer_*_*')
    output_commands.append('*_*_*_*')

    # Are we applying Rochester Corrections to the muons?
    if rochCor != "":
        if rochCor not in ["RochCor2012", "RochCor2011A", "RochCor2011B"]:
            raise RuntimeError(rochCor + ": not a valid option")

        print "-- Applying Muon Rochester Corrections --"

        process.rochCorMuons = cms.EDProducer(
            "PATMuonRochesterCorrector",
            src=cms.InputTag(src['muons']),
            corr_type=cms.string("p4_" + rochCor)
        )

        src['muons'] = "rochCorMuons"

        sequence += process.rochCorMuons

    # Are we applying electron energy corrections?
    if eleCor != "":
        if eleCor not in ["Summer12_DR53X_HCP2012",
                          "2012Jul13ReReco", "Fall11"]:
            raise RuntimeError(eleCor + ": not a valid option")

        print "-- Applying Electron Energy Corrections --"

        process.corrElectrons = cms.EDProducer(
            "PATElectronEnergyCorrector",
            src=cms.InputTag(src['electrons']),
            corr_type=cms.string("EGCorr_" + eleCor + "SmearedRegression")
        )

        src['electrons'] = "corrElectrons"

        sequence += process.corrElectrons


    ### apply final selections to the objects we'll use in the final states
    # Initialize final-state object sequence
    finalSelections = kwargs.get('finalSelection',{})
    from FinalStateAnalysis.NtupleTools.object_parameter_selector import setup_selections, getName
    process.selectObjectsForFinalStates = setup_selections(
        process, 
        "FinalSelection",
        src,
        finalSelections,
        )
    for ob in finalSelections:
        src[getName(ob)+"s"] = getName(ob)+"FinalSelection"

    if len(finalSelections):
        sequence += process.selectObjectsForFinalStates

    # Rank objects
    process.muonsRank = cms.EDProducer(
        "PATMuonRanker",
        src=cms.InputTag(src['muons']))
    src['muons'] = 'muonsRank'

    process.electronsRank = cms.EDProducer(
        "PATElectronRanker", src=cms.InputTag(src['electrons']))
    src['electrons'] = 'electronsRank'

    process.tausRank = cms.EDProducer(
        "PATTauRanker",
        src=cms.InputTag(src['taus']))
    src['taus'] = 'tausRank'

    process.jetsRank = cms.EDProducer(
        "PATJetRanker",
        src=cms.InputTag(src['jets']))
    src['jets'] = 'jetsRank'

    process.rankObjects = cms.Sequence(
        process.muonsRank
        + process.electronsRank
        + process.tausRank
        + process.jetsRank
        )
    sequence += process.rankObjects


    # Now build all combinatorics for E/Mu/Tau/Photon
    object_types = [
        ('Elec', cms.InputTag(src["electrons"])),
        ('Mu', cms.InputTag(src["muons"])),
        ('Tau', cms.InputTag(src["taus"])),
        ('Jet', cms.InputTag(src["jets"])),
        ('Pho', cms.InputTag(src["photons"])),
        ]

    # keep the collections we used to build the final states 
    for name, label in src.iteritems():
        if label != daughter_collections[name]:
            output_commands.append('*_%s_*_*'%label)
    

    process.load("FinalStateAnalysis.PatTools."
                 "finalStates.patFinalStatesEmbedExtraCollections_cfi")
    # If we don't have tracks, don't fit the FS vertices
    if noTracks:
        process.patFinalStateVertexFitter.enable = False

    crossCleaning = kwargs.get('crossCleaning','smallestDeltaR() > 0.3')

    process.buildSingleObjects = cms.Sequence()
    # build single object pairs
    for object in object_types:
        # Define some basic selections for building combinations
        cuts = [crossCleaning]  # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%sFinalStateProducer" % object[0],
            evtSrc=cms.InputTag("patFinalStateEventProducer"),
            leg1Src=object[1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState%s" % object[0]
        setattr(process, producer_name + "Raw", producer)
        process.buildSingleObjects += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, process.patFinalStatesEmbedObjects, producer_name)
        process.buildSingleObjects += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        process.buildSingleObjects += final_module
        setattr(process, producer_name, final_module)
    sequence += process.buildSingleObjects

    process.buildDiObjects = cms.Sequence()
    # Build di-object pairs
    for diobject in _combinatorics(object_types, 2):
        # Don't build two jet states
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Pho'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Jet'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Jet', 'Pho'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Jet', 'Jet'):
            continue

        # Define some basic selections for building combinations
        cuts = [crossCleaning]  # basic x-cleaning

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
    sequence += process.buildDiObjects

    # Build tri-lepton pairs
    process.buildTriObjects = cms.Sequence()
    for triobject in _combinatorics(object_types, 3):
        n_taus = [x[0] for x in triobject].count('Tau')
        n_phos = [x[0] for x in triobject].count('Pho')
        n_muons = [x[0] for x in triobject].count('Mu')
        n_jets = [x[0] for x in triobject].count('Jet')

        if n_phos > 2:
            continue
        if n_taus and n_phos:
            continue
        if n_jets > 0 and not (n_jets == 2 and n_muons == 1):
            continue

        # Define some basic selections for building combinations
        cuts = [crossCleaning]  # basic x-cleaning

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
    sequence += process.buildTriObjects

    # Build 4 lepton final states
    process.buildQuadObjects = cms.Sequence()
    for quadobject in _combinatorics(object_types, 4):
        # Don't build states with more than 2 hadronic taus or phos
        n_taus = [x[0] for x in quadobject].count('Tau')
        n_phos = [x[0] for x in quadobject].count('Pho')
        n_jets = [x[0] for x in quadobject].count('Jet')

        if n_phos > 2:
            continue
        if n_taus and n_phos:
            continue
        if n_jets > 0:
            continue

        cuts = [crossCleaning]  # basic x-cleaning

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
    sequence += process.buildQuadObjects


if __name__ == "__main__":
    import doctest
    doctest.testmod()
