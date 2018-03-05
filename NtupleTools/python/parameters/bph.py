# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

parameters = {
    # minimal object kinematic cuts
    'ptCuts' : {
        'm': '2',
        'e': '2',
        't': '18',
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
        'e': 'abs(eta) < 2.5 && pt > 2',
        'm': 'abs(eta) < 2.4 && pt > 2',
        't': 'abs(eta) < 2.5 && pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>18 && abs(eta) < 4.7 && userFloat("idLoose") > 0.5'
    },



    # cross cleaning for objects in final state
    #'crossCleaning' : 'smallestDeltaR() > 0.3',
    'crossCleaning' : 'smallestDeltaR() > 0.01', # CHANNEL is formatted in ./PatTools/python/patFinalStateProducers.py
  
    # additional variables for ntuple
    'eventVariables' : PSet(

        vertexFitting12 = 'userFloat("VertexFitting12")',
        vertexFitting13 = 'userFloat("VertexFitting13")',
        vertexFitting14 = 'userFloat("VertexFitting14")',
        vertexFitting23 = 'userFloat("VertexFitting23")',
        vertexFitting24 = 'userFloat("VertexFitting24")',
        vertexFitting34 = 'userFloat("VertexFitting34")',
        vertexFitting123 = 'userFloat("VertexFitting123")',
        vertexFitting124 = 'userFloat("VertexFitting124")',
        vertexFitting134 = 'userFloat("VertexFitting134")',
        vertexFitting234 = 'userFloat("VertexFitting234")',
        vertexFitting1234 = 'userFloat("VertexFitting1234")',

        # Rivet code provides the Simplifed Template Cross Section values
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
        metSig='evt.metSig()', # Using PF Met
        numGenJets = 'evt.numGenJets()',

        # Leading and sublead jets
        j1pt = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(0)',
        j1eta = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(1)',
        j1phi = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(2)',
        j1csv = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(3)',
        j1pu = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(4)',
        #j1pu_updated = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(5)',
        j1partonflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(5)',
        j1hadronflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(6)',
        j1rawf = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(7)',
        j1ptUp = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(8)',
        j1ptDown = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(9)',
        j2pt = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(10)',
        j2eta = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(11)',
        j2phi = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(12)',
        j2csv = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(13)',
        j2pu = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(14)',
        #j2pu_updated = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(16)',
        j2partonflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(15)',
        j2hadronflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(16)',
        j2rawf = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(17)',
        j2ptUp = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(18)',
        j2ptDown = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).at(19)',

        # Leading and subleading BTagged Jets
        jb1pt = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(0)',
        jb1eta = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(1)',
        jb1phi = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(2)',
        jb1csv = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(3)',
        jb1pu = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(4)',
        jb1partonflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(5)',
        jb1hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(6)',
        jb1rawf = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(7)',
        jb1ptUp = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(8)',
        jb1ptDown = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(9)',
        jb2pt = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(10)',
        jb2eta = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(11)',
        jb2phi = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(12)',
        jb2csv = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(13)',
        jb2pu = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(14)',
        jb2partonflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(15)',
        jb2hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(16)',
        jb2rawf = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(17)',
        jb2ptUp = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(18)',
        jb2ptDown = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484", 0.5).at(19)',

    ),

    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',

        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecay       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().statusFlags().isDirectPromptTauDecayProduct() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
        objectBPHGenMatching = 'tauGenMatch3({object_idx})',
    ),



    'muonVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationR03().sumChargedHadronPt + max( {object}.pfIsolationR03().sumNeutralHadronEt \
                                        + {object}.pfIsolationR03().sumPhotonEt - 0.5 * {object}.pfIsolationR03().sumPUPt, 0.0)) / {object}.pt()',
        objectIsoDB04               = '({object}.pfIsolationR04().sumChargedHadronPt + max( {object}.pfIsolationR04().sumNeutralHadronEt \
                                        + {object}.pfIsolationR04().sumPhotonEt - 0.5 * {object}.pfIsolationR04().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers

        objectMatchesUpsilonFilter_ofDimuon0UpsilonMuon = 'matchToHLTFilter({object_idx}, "hltUpsilonMuonL3Filtered", 0.1)',
        objectMatchesDimuon0UpsilonMuonPath      = r'matchToHLTPath({object_idx}, "HLT_Dimuon0_Upsilon_Muon_v\\d+", 0.1)',
        objectMatchesDimuon13UpsilonPath      = r'matchToHLTPath({object_idx}, "HLT_Dimuon13_Upsilon_v\\d+", 0.1)',
        objectMatchesDimuon8UpsilonBarrelPath      = r'matchToHLTPath({object_idx}, "HLT_Dimuon8_Upsilon_Barrel_v\\d+", 0.1)',
        objectMatchesQuadMuon0Dimuon0UpsilonPath      = r'matchToHLTPath({object_idx}, "HLT_QuadMuon0_Dimuon0_Upsilon_v\\d+", 0.1)',
        objectMatchesTripleMu533Path      = r'matchToHLTPath({object_idx}, "HLT_TripleMu_5_3_3_v\\d+", 0.1)',
        objectMatchesTripleMu12105Path      = r'matchToHLTPath({object_idx}, "HLT_TripleMu_12_10_5_v\\d+", 0.1)',

        objectMatchesIsoMu27Path = r'matchToHLTFilter({object_idx}, "HLT_IsoMu27_v\\d+", 0.5)',

        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecayFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isDirectPromptTauDecayProductFinalState() : -999',
        objectGenPromptFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isPromptFinalState() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
        objectBPHGenMatching = 'tauGenMatch3({object_idx})',
    ),


    'tauVariables' : PSet(),


    'photonVariables' : PSet(),


    'jetVariables' : PSet(),


    'dicandidateVariables' : PSet(),
}
