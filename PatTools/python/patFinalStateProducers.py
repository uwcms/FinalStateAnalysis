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
                         rochCor="", eleCor="", use25ns=False, 
                         postfix='',
                         **kwargs):

    src = dict(daughter_collections) # make a copy so we don't change the passed collection

    # Build the PATFinalStateEventObject
    if buildFSAEvent:
        if not hasattr(process,'patFinalStateEventProducer'):
            process.load("FinalStateAnalysis.PatTools.finalStates.patFinalStateEventProducer_cfi")
        fsName = 'patFinalStateEventProducer{0}'.format(postfix)
        if postfix:
            setattr(process,fsName,process.patFinalStateEventProducer.clone())
        eventProducer = getattr(process,fsName)
        eventProducer.electronSrc = cms.InputTag(src['electrons'])
        eventProducer.muonSrc = cms.InputTag(src['muons'])
        eventProducer.tauSrc = cms.InputTag(src['taus'])
        eventProducer.jetSrc = cms.InputTag(src['jets'])
        eventProducer.phoSrc = cms.InputTag(src['photons'])
        eventProducer.metSrc = cms.InputTag(src['pfmet'])
        eventProducer.puTag = cms.string(puTag)
        if 'extraWeights' in src:
            eventProducer.extraWeights = src['extraWeights']
        eventProducer.trgSrc = cms.InputTag("selectedPatTrigger")
        eventProducer.rhoSrc = cms.InputTag('fixedGridRhoAll')
        eventProducer.pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
        eventProducer.verticesSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
        eventProducer.genParticleSrc = cms.InputTag("prunedGenParticles")
        eventProducer.mets = cms.PSet(
            pfmet = cms.InputTag(src['pfmet']),
        )
        if runMVAMET:
            eventProducer.mets.mvamet = cms.InputTag(src['mvamet'])


        
        sequence += eventProducer

    # Always keep
    output_commands.append('*_{0}_*_*'.format(fsName))

    # Are we applying Rochester Corrections to the muons?
    #if rochCor != "":
    #    if rochCor not in ["RochCor2012", "RochCor2011A", "RochCor2011B"]:
    #        raise RuntimeError(rochCor + ": not a valid option")

    #    print "-- Applying Muon Rochester Corrections --"

    #    process.rochCorMuons = cms.EDProducer(
    #        "PATMuonRochesterCorrector",
    #        src=cms.InputTag(src['muons']),
    #        corr_type=cms.string("p4_" + rochCor)
    #    )

    #    src['muons'] = "rochCorMuons"

    #    sequence += process.rochCorMuons

    # Are we applying electron energy corrections?
    #if eleCor != "":
    #    if eleCor not in ["Summer12_DR53X_HCP2012",
    #                      "2012Jul13ReReco", "Fall11"]:
    #        raise RuntimeError(eleCor + ": not a valid option")

    #    print "-- Applying Electron Energy Corrections --"

    #    process.corrElectrons = cms.EDProducer(
    #        "PATElectronEnergyCorrector",
    #        src=cms.InputTag(src['electrons']),
    #        corr_type=cms.string("EGCorr_" + eleCor + "SmearedRegression")
    #    )

    #    src['electrons'] = "corrElectrons"

    #    sequence += process.corrElectrons


    ### apply final selections to the objects we'll use in the final states
    # Initialize final-state object sequence
    finalSelections = kwargs.get('finalSelection',{})
    from FinalStateAnalysis.NtupleTools.object_parameter_selector import setup_selections, getName
    objSelectName = 'selectObjectsForFinalStates{0}'.format(postfix)
    objSelect = setup_selections(
        process, 
        "FinalSelection{0}".format(postfix),
        src,
        finalSelections,
        )
    setattr(process,objSelectName,objSelect)
    for ob in finalSelections:
        src[getName(ob)+"s"] = getName(ob)+"FinalSelection{0}".format(postfix)

    if len(finalSelections):
        sequence += getattr(process,objSelectName)

    # Rank objects
    rankSeqName = 'rankObjects{0}'.format(postfix)
    rankSeq = cms.Sequence()
    for obj in ['muons','electrons','taus','jets']:
        objRankName = '{0}Rank{1}'.format(obj,postfix)
        mod = cms.EDProducer(
            "PAT{0}Ranker".format(obj[:-1].capitalize()),
            src = cms.InputTag(src[obj]),
        )
        src[obj] = objRankName
        setattr(process,objRankName,mod)
        rankSeq += getattr(process,objRankName)
    setattr(process,rankSeqName,rankSeq)
    sequence += getattr(process,rankSeqName)


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
    

    if not hasattr(process,'patFinalStateVertexFitter'):
        process.load("FinalStateAnalysis.PatTools.finalStates.patFinalStatesEmbedExtraCollections_cfi")
    vFitName = 'patFinalStateVertexFitter{0}'.format(postfix)
    mResName = 'finalStateMassResolutionEmbedder{0}'.format(postfix)
    embedObjName = 'patFinalStatesEmbedObjects{0}'.format(postfix)
    if postfix:
        setattr(process,vFitName,process.patFinalStateVertexFitter.clone())
        setattr(process,mResName,process.finalStateMassResolutionEmbedder.clone())
        setattr(process,embedObjName,cms.Sequence(getattr(process,vFitName)+getattr(process,mResName)))
    # If we don't have tracks, don't fit the FS vertices
    if noTracks:
        getattr(process,'patFinalStateVertexFitter{0}'.format(postfix)).enable = False

    crossCleaning = kwargs.get('crossCleaning','smallestDeltaR() > 0.3')


    # build single object pairs
    singleObjName = 'buildSingleObjects{0}'.format(postfix)
    singleObjSeq = cms.Sequence()
    for object in object_types:
        # Define some basic selections for building combinations
        cuts = [crossCleaning]  # basic x-cleaning

        producer = cms.EDProducer(
            "PAT%sFinalStateProducer" % object[0],
            evtSrc=cms.InputTag("patFinalStateEventProducer{0}".format(postfix)),
            leg1Src=object[1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState{0}{1}".format(object[0],postfix)
        setattr(process, producer_name + "Raw", producer)
        singleObjSeq += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, getattr(process,embedObjName), producer_name)
        singleObjSeq += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        singleObjSeq += final_module
        setattr(process, producer_name, final_module)
    setattr(process,singleObjName,singleObjSeq)
    sequence += getattr(process,singleObjName)

    # Build di-object pairs
    doubleObjName = 'buildDiObjects{0}'.format(postfix)
    doubleObjSeq = cms.Sequence()
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
            evtSrc=cms.InputTag("patFinalStateEventProducer{0}".format(postfix)),
            leg1Src=diobject[0][1],
            leg2Src=diobject[1][1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState{0}{1}{2}".format(diobject[0][0], diobject[1][0], postfix)
        setattr(process, producer_name + "Raw", producer)
        doubleObjSeq += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, getattr(process,embedObjName), producer_name)
        doubleObjSeq += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        doubleObjSeq += final_module
        setattr(process, producer_name, final_module)
    setattr(process,doubleObjName,doubleObjSeq)
    sequence += getattr(process,doubleObjName)

    # Build tri-lepton pairs
    tripleObjName = 'buildTriObjects{0}'.format(postfix)
    tripleObjSeq = cms.Sequence()
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
            evtSrc=cms.InputTag("patFinalStateEventProducer{0}".format(postfix)),
            leg1Src=triobject[0][1],
            leg2Src=triobject[1][1],
            leg3Src=triobject[2][1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState{0}{1}{2}{3}".format(
            triobject[0][0], triobject[1][0], triobject[2][0], postfix)
        setattr(process, producer_name + "Raw", producer)
        tripleObjSeq += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, getattr(process,embedObjName), producer_name)
        tripleObjSeq += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        tripleObjSeq += final_module
    setattr(process,tripleObjName,tripleObjSeq)
    sequence += getattr(process,tripleObjName)

    # Build 4 lepton final states
    quadObjName = 'buildQuadObjects{0}'.format(postfix)
    quadObjSeq = cms.Sequence()
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
            evtSrc=cms.InputTag("patFinalStateEventProducer{0}".format(postfix)),
            leg1Src=quadobject[0][1],
            leg2Src=quadobject[1][1],
            leg3Src=quadobject[2][1],
            leg4Src=quadobject[3][1],
            # X-cleaning
            cut=cms.string(' & '.join(cuts))
        )
        producer_name = "finalState{0}{1}{2}{3}{4}".format(
            quadobject[0][0], quadobject[1][0], quadobject[2][0],
            quadobject[3][0], postfix
        )
        setattr(process, producer_name + "Raw", producer)
        quadObjSeq += producer
        # Embed the other collections
        embedder_seq = helpers.cloneProcessingSnippet(
            process, getattr(process,embedObjName), producer_name)
        quadObjSeq += embedder_seq
        # Do some trickery so the final module has a nice output name
        final_module_name = chain_sequence(embedder_seq, producer_name + "Raw")
        final_module = cms.EDProducer(
            "PATFinalStateCopier", src=final_module_name)
        setattr(process, producer_name, final_module)
        quadObjSeq += final_module
    setattr(process,quadObjName,quadObjSeq)
    sequence += getattr(process,quadObjName)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
