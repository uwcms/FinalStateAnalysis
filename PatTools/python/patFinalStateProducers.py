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
                         noTracks=False, noPhotons=False, hzz=False,
                         rochCor="", eleCor="", useMiniAOD=False, use25ns=False):

    muonsrc = collections['muons']
    esrc = collections['electrons']
    tausrc = collections['taus']
    jetsrc = collections['jets']
    pfmetsrc = collections['pfmet']
    mvametsrc = collections['mvamet']
    phosrc = collections['photons']
    try:
        fsrsrc = collections['fsr']
    except KeyError:
        fsrsrc = 'boostedFsrPhotons'

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
        if 'extraWeights' in collections:
            process.patFinalStateEventProducer.extraWeights = collections['extraWeights']
        if useMiniAOD:
            # first, recalculate pfMet without type1 corrections
            #from RecoMET.METProducers.PFMET_cfi import pfMet
            #process.pfMet = pfMet.clone(src = "packedPFCandidates")
            #process.pfMet.calculateSignificance = False # this can't be easily implemented on packed PF candidates at the moment
            #sequence += process.pfMet
            # now produce the final states
            #process.patFinalStateEventProducerMiniAOD.mets.pfmet = cms.InputTag("pfMet")
            process.patFinalStateEventProducer.miniAOD = cms.bool(True)
            process.patFinalStateEventProducer.trgSrc = cms.InputTag("selectedPatTrigger")
            process.patFinalStateEventProducer.rhoSrc = cms.InputTag('fixedGridRhoAll')
            process.patFinalStateEventProducer.pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
            process.patFinalStateEventProducer.verticesSrc = cms.InputTag("offlineSlimmedPrimaryVertices")
            process.patFinalStateEventProducer.genParticleSrc = cms.InputTag("prunedGenParticles")
            process.patFinalStateEventProducer.mets = cms.PSet(
                pfmet = cms.InputTag(pfmetsrc),
            )
        else:
            process.patFinalStateEventProducer.mets.pfmet = pfmetsrc
            process.patFinalStateEventProducer.mets.mvamet = mvametsrc
        sequence += process.patFinalStateEventProducer

    # Always keep
    output_commands.append('*_patFinalStateEventProducer_*_*')

    # Apply some loose PT cuts on the objects we use to create the final states
    # so the combinatorics don't blow up
    muon_string = (
        'max(pt, userFloat("maxCorPt")) > 4 &'
        '& (isGlobalMuon | isTrackerMuon)' )
    
    elec_string = (
        'abs(superCluster().eta) < 3.0 '
        '& max(pt, userFloat("maxCorPt")) > 7' )


    # Initialize final-state object sequence
    process.selectObjectsForFinalStates = cms.Sequence()

    # Are we applying Rochester Corrections to the muons?
    if rochCor != "":
        if rochCor not in ["RochCor2012", "RochCor2011A", "RochCor2011B"]:
            raise RuntimeError(rochCor + ": not a valid option")

        print "-- Applying Muon Rochester Corrections --"

        process.rochCorMuons = cms.EDProducer(
            "PATMuonRochesterCorrector",
            src=cms.InputTag(muonsrc),
            corr_type=cms.string("p4_" + rochCor)
        )

        muonsrc = "rochCorMuons"

        process.selectObjectsForFinalStates += process.rochCorMuons

    # Are we applying electron energy corrections?
    if eleCor != "":
        if eleCor not in ["Summer12_DR53X_HCP2012",
                          "2012Jul13ReReco", "Fall11"]:
            raise RuntimeError(eleCor + ": not a valid option")

        print "-- Applying Electron Energy Corrections --"

        process.corrElectrons = cms.EDProducer(
            "PATElectronEnergyCorrector",
            src=cms.InputTag(esrc),
            corr_type=cms.string("EGCorr_" + eleCor + "SmearedRegression")
        )

        esrc = "corrElectrons"

        process.selectObjectsForFinalStates += process.corrElectrons

    process.muonsRank = cms.EDProducer(
        "PATMuonRanker",
        src=cms.InputTag(muonsrc))

    process.muonsForFinalStates = cms.EDFilter(
        "PATMuonRefSelector",
        src=cms.InputTag("muonsRank"),
        cut=cms.string(muon_string),
        filter=cms.bool(False),
    )

    process.electronsRank = cms.EDProducer(
        "PATElectronRanker", src=cms.InputTag(esrc))

    process.electronsForFinalStates = cms.EDFilter(
        "PATElectronRefSelector",
        src=cms.InputTag("electronsRank"),
        cut=cms.string(elec_string),
        filter=cms.bool(False),
    )

    process.photonsForFinalStates = cms.EDFilter(
        "PATPhotonRefSelector",
        src=cms.InputTag(phosrc),
        cut=cms.string('abs(superCluster().eta()) < 3.0 & pt > 10'),
        filter=cms.bool(False),
    )

    process.tausRank = cms.EDProducer(
        "PATTauRanker",
        src=cms.InputTag(tausrc))

    # Require that the PT of the jet (either corrected jet or tau)
    # to be greater than 17
    process.tausForFinalStates = cms.EDFilter(
        "PATTauRefSelector",
        src=cms.InputTag("tausRank"),
        cut=cms.string('abs(eta) < 2.5 & pt > 17 & tauID("decayModeFinding")'),
        filter=cms.bool(False),
    )

    if use25ns:
        electronCleaning = ("pt>10&&userInt('cutBasedElectronID-CSA14-PU20bx25-V0-standalone-veto')>0"
                            "&&(userIso(0)+max(userIso(1)+neutralHadronIso()"
                            "-0.5*userIso(2),0.0))/pt()<0.3")
    else:
        electronCleaning = ("pt>10&&userInt('cutBasedElectronID-CSA14-50ns-V1-standalone-veto')>0"
                            "&&(userIso(0)+max(userIso(1)+neutralHadronIso()"
                            "-0.5*userIso(2),0.0))/pt()<0.3")

    process.jetsFiltered = cms.EDProducer(
        "PATJetCleaner",
        src=cms.InputTag(jetsrc),
        # I leave it loose here, can be tightened at the last step
        preselection=cms.string(
            "pt>20 & abs(eta) < 2.5"
            "& userFloat('idLoose')"),
        # overlap checking configurables
        checkOverlaps=cms.PSet(
            muons=cms.PSet(
                src=cms.InputTag("muonsForFinalStates"),
                algorithm=cms.string("byDeltaR"),
                preselection=cms.string(
                    "pt>10&&isGlobalMuon&&isTrackerMuon&&"
                    "(userIso(0)+max(photonIso()+neutralHadronIso()"
                    "-0.5*puChargedHadronIso(),0))/pt()<0.3"),
                deltaR=cms.double(0.3),
                checkRecoComponents=cms.bool(False),
                pairCut=cms.string(""),
                requireNoOverlaps=cms.bool(True),
            ),
            electrons=cms.PSet(
                src=cms.InputTag("electronsForFinalStates"),
                algorithm=cms.string("byDeltaR"),
                preselection=cms.string(electronCleaning),
                deltaR=cms.double(0.3),
                checkRecoComponents=cms.bool(False),
                pairCut=cms.string(""),
                requireNoOverlaps=cms.bool(True),
            ),
        ),
        # finalCut (any string-based cut on pat::Jet)
        finalCut=cms.string('')
    )
    process.jetsForFinalStates = cms.EDProducer(
        "PATJetRanker",
        src=cms.InputTag("jetsFiltered"))

    process.selectObjectsForFinalStates = cms.Sequence(
        process.muonsRank
        + process.muonsForFinalStates
        + process.electronsRank
        + process.electronsForFinalStates
        + process.tausRank
        + process.tausForFinalStates
        + process.jetsFiltered
        + process.jetsForFinalStates
    )
    if not noPhotons:
        process.selectObjectsForFinalStates += process.photonsForFinalStates

    sequence += process.selectObjectsForFinalStates

    # Now build all combinatorics for E/Mu/Tau/Photon
    object_types = [('Elec', cms.InputTag("electronsForFinalStates")),
                    ('Mu', cms.InputTag("muonsForFinalStates")),
                    ('Tau', cms.InputTag("tausForFinalStates")),
                    ('Jet', cms.InputTag("jetsForFinalStates"))]

    if not noPhotons:
        object_types.append(('Pho', cms.InputTag("photonsForFinalStates")))



    process.load("FinalStateAnalysis.PatTools."
                 "finalStates.patFinalStatesEmbedExtraCollections_cfi")
    # If we don't have tracks, don't fit the FS vertices
    if noTracks:
        process.patFinalStateVertexFitter.enable = False

    process.buildSingleObjects = cms.Sequence()
    # build single object pairs
    for object in object_types:
        # Define some basic selections for building combinations
        cuts = ['smallestDeltaR() > 0.3']  # basic x-cleaning

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
        output_commands.append("*_%s_*_*" % producer_name)
    sequence += process.buildSingleObjects

    process.buildDiObjects = cms.Sequence()
    # Build di-object pairs
    for diobject in _combinatorics(object_types, 2):
        # Don't build two jet states
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Tau'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Pho'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Tau', 'Jet'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Jet', 'Pho'):
            continue
        if (diobject[0][0], diobject[1][0]) == ('Jet', 'Jet'):
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
        n_taus = [x[0] for x in quadobject].count('Tau')
        n_phos = [x[0] for x in quadobject].count('Pho')
        n_jets = [x[0] for x in quadobject].count('Jet')

        if n_phos > 2:
            continue
        if n_taus and n_phos:
            continue
        if n_jets > 0:
            continue

        # Define some basic selections for building combinations (but not for HZZ)
        if hzz:
            cuts = []
        else:
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
