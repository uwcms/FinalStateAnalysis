# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

parameters = {
    # minimal object kinematic cuts
    'ptCuts' : {
        'm': '4.5',
        'e': '4.5',
        't': '19',
        'j': '18'
    },
    'etaCuts' : {
        'm': '2.4',
        'e': '2.5',
        't': '2.3',
        'j': '4.7'
    },

    # selections on all objects whether they're included in final states or not, done immediately after necessary variables are embedded
    'preselection' : OrderedDict(),
     #    # Commented out because of 80X jet cleaning memory leak
     #    [
     #       # Remove jets that overlap our leptons
     #       ('j', { # Made pt requirement for E/Mu to clean an overlapping jet so
     #               # that this never happens
     #               'selection' : 'pt > 20 && abs(eta) < 4.7 && userFloat("idLoose") > 0.5',
     #               'e' : {
     #                   'deltaR' : 0.5,
     #                   'selection' : 'userFloat("MVANonTrigWP90") > 0.5 && pt > 9999 && abs(eta) < 2.5',
     #                   },
     #               'm' : {
     #                   'deltaR' : 0.5,
     #                   'selection' : 'isMediumMuon() > 0.5 && pt > 9999 && abs(eta) < 2.4',
     #                   },
     #               }
     #        )
     #    ]),

    # selections to include object in final state (should be looser than analysis selections)
    # Based on default finalSelection, this is a little tighter for muons so we keep the min Pt Mu for our triggers
    # But we don't svFit them.
    'finalSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 && pt > 4.5',
        'm': 'pt > 4.5 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>18 && abs(eta) < 4.7 && userFloat("idLoose") > 0.5'
    },

    # cross cleaning for objects in final state
    'crossCleaning' : 'smallestDeltaR() > 0.05',
    #'crossCleaning' : 'smallestDeltaR() > 0.05 && channelSpecificObjCuts("CHANNEL")', # CHANNEL is formatted in ./PatTools/python/patFinalStateProducers.py
  
    # additional variables for ntuple
    'eventVariables' : PSet(

        #nbZDee='evt.countFindDecay(1023,11)',
        #nbZDmumu='evt.countFindDecay(1023,13)',
        #nbZDtautau='evt.countFindDecay(1023,15)',

        Flag_badGlobalMuonFilter='evt.getFilterFlags("badGlobalMuonFilter")',
        Flag_badCloneMuonFilter='evt.getFilterFlags("cloneGlobalMuonFilter")',
        Flag_BadChargedCandidateFilter='evt.getFilterFlags("BadChargedCandidateFilter")',
        Flag_BadPFMuonFilter='evt.getFilterFlags("BadPFMuonFilter")',
        Flag_HBHENoiseFilter='evt.getFilterFlags("Flag_HBHENoiseFilter")',
        Flag_HBHENoiseIsoFilter='evt.getFilterFlags("Flag_HBHENoiseIsoFilter")',
        Flag_globalTightHalo2016Filter='evt.getFilterFlags("Flag_globalTightHalo2016Filter")',
        Flag_goodVertices='evt.getFilterFlags("Flag_goodVertices")',
        Flag_eeBadScFilter='evt.getFilterFlags("Flag_eeBadScFilter")',
        Flag_EcalDeadCellTriggerPrimitiveFilter='evt.getFilterFlags("Flag_EcalDeadCellTriggerPrimitiveFilter")',
	Flag_badMuons='evt.getFilterFlags("Flag_badMuons")',
        Flag_duplicateMuons='evt.getFilterFlags("Flag_duplicateMuons")',
        Flag_noBadMuons='evt.getFilterFlags("Flag_noBadMuons")',
        vispX='tauGenMotherKin().at(0)',
        vispY='tauGenMotherKin().at(1)',
        genpX='tauGenMotherKin().at(2)',
        genpY='tauGenMotherKin().at(3)',
        genpT='tauGenMotherKin().at(4)',
        genM='tauGenMotherKin().at(5)',
        genEta='tauGenMotherKin().at(6)',
        genPhi='tauGenMotherKin().at(7)',
        topQuarkPt1 = 'getTopQuarkInitialPts().at(0)',
        topQuarkPt2 = 'getTopQuarkInitialPts().at(1)',
        #buildGenTaus = 'buildGenTaus.size()',
        numGenJets = 'evt.numGenJets()',
        genMass = 'evt.getGenMass()',

        # Leading and subleading BTagged Jets
        jb1pt = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.0).at(0)',
        jb1eta = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.0).at(1)',
        jb1phi = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.0).at(2)',
        jb1csv = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.0).at(3)',
        jb1hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.0).at(6)',

    ),

    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',

        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecay       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().statusFlags().isDirectPromptTauDecayProduct() : -999',
        #objectZTTGenMatching = 'tauGenMatch({object_idx})', 
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 

    ),



    'muonVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationR03().sumChargedHadronPt + max( {object}.pfIsolationR03().sumNeutralHadronEt \
                                        + {object}.pfIsolationR03().sumPhotonEt - 0.5 * {object}.pfIsolationR03().sumPUPt, 0.0)) / {object}.pt()',
        objectIsoDB04               = '({object}.pfIsolationR04().sumChargedHadronPt + max( {object}.pfIsolationR04().sumNeutralHadronEt \
                                        + {object}.pfIsolationR04().sumPhotonEt - 0.5 * {object}.pfIsolationR04().sumPUPt, 0.0)) / {object}.pt()',

        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecayFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isDirectPromptTauDecayProductFinalState() : -999',
        objectGenPromptFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isPromptFinalState() : -999',
        #objectZTTGenMatching = 'tauGenMatch({object_idx})', 
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
    ),



    'tauVariables' : PSet(
        
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isPrompt() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
        objectZTTGenPt = 'tauGenKin({object_idx}).at(0)', 
        objectZTTGenEta = 'tauGenKin({object_idx}).at(1)', 
        objectZTTGenPhi = 'tauGenKin({object_idx}).at(2)', 
        objectZTTGenDR = 'tauGenKin({object_idx}).at(3)', 

    ),

    'photonVariables' : PSet(),

    'jetVariables' : PSet(),

    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(
    ),
}
