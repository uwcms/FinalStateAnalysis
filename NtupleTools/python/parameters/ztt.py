# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

parameters = {
    # minimal object kinematic cuts
    'ptCuts' : {
        'm': '10',
        'e': '10',
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
     #               'selection' : 'pt > 20 && abs(eta) < 4.7 && userFloat("idTight") > 0.5',
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
        'e': 'abs(superCluster().eta) < 3.0 && pt > 7',
        'm': 'pt > 8 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>18 && abs(eta) < 4.7 && userFloat("idTight") > 0.5'
    },



    # cross cleaning for objects in final state
    #'crossCleaning' : 'smallestDeltaR() > 0.3',
    'crossCleaning' : 'smallestDeltaR() > 0.3 && channelSpecificObjCuts("CHANNEL")', # CHANNEL is formatted in ./PatTools/python/patFinalStateProducers.py
  



    # additional variables for ntuple
    'eventVariables' : PSet(

        # Rivet code provides the Simplifed Template Cross Section values
        Rivet_stage0_cat='evt.getRivetInfo().stage0_cat',
        Rivet_stage1_cat_pTjet25GeV='evt.getRivetInfo().stage1_cat_pTjet25GeV',
        Rivet_stage1_cat_pTjet30GeV='evt.getRivetInfo().stage1_cat_pTjet30GeV',
        Rivet_errorCode='evt.getRivetInfo().errorCode',
        Rivet_prodMode='evt.getRivetInfo().prodMode',
        Rivet_higgsPt='evt.getRivetInfo().higgs.pt()',
        Rivet_higgsEta='evt.getRivetInfo().higgs.eta()',
        Rivet_VPt='evt.getRivetInfo().V.pt()',
        Rivet_VEta='evt.getRivetInfo().V.eta()',
        Rivet_p4decay_VPt='evt.getRivetInfo().p4decay_V.pt()',
        Rivet_p4decay_VEta='evt.getRivetInfo().p4decay_V.eta()',
        Rivet_nJets30='evt.getRivetInfo().jets30.size()',
        Rivet_nJets25='evt.getRivetInfo().jets25.size()',

        #Flag_badGlobalMuonFilter='evt.getFilterFlags("badGlobalMuonFilter")',
        #Flag_badCloneMuonFilter='evt.getFilterFlags("cloneGlobalMuonFilter")',
        Flag_ecalBadCalibReducedMINIAODFilter='evt.getFilterFlags("ecalBadCalibReducedMINIAODFilter")',
        Flag_BadChargedCandidateFilter='evt.getFilterFlags("Flag_BadChargedCandidateFilter")',
        Flag_BadPFMuonFilter='evt.getFilterFlags("Flag_BadPFMuonFilter")',
        Flag_HBHENoiseFilter='evt.getFilterFlags("Flag_HBHENoiseFilter")',
        Flag_HBHENoiseIsoFilter='evt.getFilterFlags("Flag_HBHENoiseIsoFilter")',
        Flag_globalTightHalo2016Filter='evt.getFilterFlags("Flag_globalTightHalo2016Filter")',
        Flag_globalSuperTightHalo2016Filter='evt.getFilterFlags("Flag_globalSuperTightHalo2016Filter")',
        Flag_goodVertices='evt.getFilterFlags("Flag_goodVertices")',
        Flag_eeBadScFilter='evt.getFilterFlags("Flag_eeBadScFilter")',
        Flag_ecalBadCalibFilter='evt.getFilterFlags("Flag_ecalBadCalibFilter")',
        Flag_EcalDeadCellTriggerPrimitiveFilter='evt.getFilterFlags("Flag_EcalDeadCellTriggerPrimitiveFilter")',
        Flag_badMuons='evt.getFilterFlags("Flag_badMuons")',
        Flag_duplicateMuons='evt.getFilterFlags("Flag_duplicateMuons")',
        #Flag_noBadMuons='evt.getFilterFlags("Flag_noBadMuons")',
        metSig='evt.metSig()', # Using PF Met
        metcov00='evt.metCov(0)', # 0 = (0,0) PF Met based
        metcov10='evt.metCov(1)', # 1 = (1,0)
        metcov01='evt.metCov(2)', # 2 = (0,1)
        metcov11='evt.metCov(3)', # 3 - (1,1)
        metcov00_DESYlike='evt.met("pfmet").getSignificanceMatrix[0][0]',
        metcov10_DESYlike='evt.met("pfmet").getSignificanceMatrix[1][0]',
        metcov01_DESYlike='evt.met("pfmet").getSignificanceMatrix[0][1]',
        metcov11_DESYlike='evt.met("pfmet").getSignificanceMatrix[1][1]',
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
        npNLO = 'evt.npNLO()',

        # Leading and sublead jets
        j1pt = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(0)',
        j1eta = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(1)',
        j1phi = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(2)',
        j1csv = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(3)',
        j1hadronflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(6)',
        j2pt = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(10)',
        j2eta = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(11)',
        j2phi = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(12)',
        j2csv = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(13)',
        j2hadronflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(16)',

        j1ptWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(0)',
        j1etaWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(1)',
        j1phiWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(2)',
        j1csvWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(3)',
        j1hadronflavorWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(6)',
        j2ptWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(10)',
        j2etaWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(11)',
        j2phiWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(12)',
        j2csvWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(13)',
        j2hadronflavorWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5", 0.5).at(16)',


        # Leading and subleading BTagged Jets
        jb1pt = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(0)',
        jb1eta = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(1)',
        jb1phi = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(2)',
        jb1csv = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(3)',
        #jb1pu = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(4)',
        jb1hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(6)',
        jb2pt = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(10)',
        jb2eta = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(11)',
        jb2phi = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(12)',
        jb2csv = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(13)',
        #jb2pu = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(14)',
        jb2hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(16)',

        jb1ptWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(0)',
        jb1etaWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(1)',
        jb1phiWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(2)',
        jb1csvWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(3)',
        #jb1puWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(4)',
        jb1hadronflavorWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(6)',
        jb2ptWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(10)',
        jb2etaWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(11)',
        jb2phiWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(12)',
        jb2csvWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(13)',
        #jb2puWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(14)',
        jb2hadronflavorWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfDeepCSVDiscriminatorsJetTags:BvsAll\') > 0.4941", 0.5).at(16)',

    ),

    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',

        objectMatchesEle24Tau30Path= r'matchToHLTPath({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle32Path= r'matchToHLTPath({object_idx}, "HLT_Ele32_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle27Path= r'matchToHLTPath({object_idx}, "HLT_Ele27_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle35Path= r'matchToHLTPath({object_idx}, "HLT_Ele35_WPTight_Gsf_v\\d+", 0.5)',

        objectMatchesEle24Tau30Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle32Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele32_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle27Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele27_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle35Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele35_WPTight_Gsf_v\\d+", 0.5)',

        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecay       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().statusFlags().isDirectPromptTauDecayProduct() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
    ),



    'muonVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationR03().sumChargedHadronPt + max( {object}.pfIsolationR03().sumNeutralHadronEt \
                                        + {object}.pfIsolationR03().sumPhotonEt - 0.5 * {object}.pfIsolationR03().sumPUPt, 0.0)) / {object}.pt()',
        objectIsoDB04               = '({object}.pfIsolationR04().sumChargedHadronPt + max( {object}.pfIsolationR04().sumNeutralHadronEt \
                                        + {object}.pfIsolationR04().sumPhotonEt - 0.5 * {object}.pfIsolationR04().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers
        objectMatchesIsoMu27Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu27_v\\d+", 0.5)',
        objectMatchesIsoMu24Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu24_v\\d+", 0.5)',
        objectMatchesIsoMu20Tau27Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',

        objectMatchesIsoMu27Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoMu27_v\\d+", 0.5)',
        objectMatchesIsoMu24Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoMu24_v\\d+", 0.5)',
        objectMatchesIsoMu20Tau27Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',

        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecayFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isDirectPromptTauDecayProductFinalState() : -999',
        objectGenPromptFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isPromptFinalState() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
    ),



    'tauVariables' : PSet(
        objectL1IsoTauMatch = 'l1extraIsoTauMatching({object_idx})',
        objectL1IsoTauPt = 'l1extraIsoTauPt({object_idx})',
        objectMatchesIsoMu20Tau27Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24Tau30Path= r'matchToHLTPath({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau40Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau40Path = r'matchToHLTPath({object_idx}, "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',

        objectMatchesIsoMu20Tau27Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24Tau30Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau40Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau40Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',

        #objectDoubleL2IsoTau26Filter = 'matchToHLTFilter2({object_idx}, "hltDoubleL2IsoTau26eta2p2", 0.5)',
        
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
        objectZTTGenPt = 'tauGenKin({object_idx}).at(0)', 
        objectZTTGenEta = 'tauGenKin({object_idx}).at(1)', 
        objectZTTGenPhi = 'tauGenKin({object_idx}).at(2)', 
        objectZTTGenDR = 'tauGenKin({object_idx}).at(3)', 

        objectRerunMVArun2v1DBoldDMwLTraw = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTrawRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTrawRerun") : -10',
        objectRerunMVArun2v1DBoldDMwLTVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTVLooseRerun") : -10',
        objectRerunMVArun2v1DBoldDMwLTLoose = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTLooseRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTLooseRerun") : -10',
        objectRerunMVArun2v1DBoldDMwLTMedium = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTMediumRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTMediumRerun") : -10',
        objectRerunMVArun2v1DBoldDMwLTTight = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTTightRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTTightRerun") : -10',
        objectRerunMVArun2v1DBoldDMwLTVTight = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTVTightRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTVTightRerun") : -10',
        objectRerunMVArun2v1DBoldDMwLTVVTight = '? {object}.hasUserFloat("byIsolationMVArun2v1DBoldDMwLTVVTightRerun") ? {object}.userFloat("byIsolationMVArun2v1DBoldDMwLTVVTightRerun") : -10',

        objectRerunMVArun2v2DBoldDMwLTraw = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTrawRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTrawRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVVLooseRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVLooseRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTLooseRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTMedium = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTMediumRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTMediumRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTTightRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVTightRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVVTightRerun") : -10',
   


objectRerunMVArun2v2DBnewDMwLTraw = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTrawRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTrawRerun") : -10',
        objectRerunMVArun2v2DBnewDMwLTVVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVVLooseRerun") : -10',
        objectRerunMVArun2v2DBnewDMwLTVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVLooseRerun") : -10',
        objectRerunMVArun2v2DBnewDMwLTLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTLooseRerun") : -10',
        objectRerunMVArun2v2DBnewDMwLTMedium = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTMediumRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTMediumRerun") : -10',
        objectRerunMVArun2v2DBnewDMwLTTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTTightRerun") : -10',
        objectRerunMVArun2v2DBnewDMwLTVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVTightRerun") : -10',
objectRerunMVArun2v2DBnewDMwLTVVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVVTightRerun") : -10',



 ),



    'photonVariables' : PSet(),



    'jetVariables' : PSet(),



    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(
         object1_object2_doubleL1IsoTauMatch = 'doubleL1extraIsoTauMatching({object1_idx},{object2_idx})',
    ),
}
