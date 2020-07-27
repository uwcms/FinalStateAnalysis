# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

parameters = {
    # minimal object kinematic cuts
    'ptCuts' : {
        'm': '8',
        'e': '9',
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
        't': 'abs(eta) < 2.3 && pt > 17 && userFloat("byVVVLooseDeepTau2017v2p1VSjet")>0',
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
        Rivet_stage1_1_cat_pTjet25GeV='evt.getRivetInfo().stage1_1_cat_pTjet25GeV',
        Rivet_stage1_1_cat_pTjet30GeV='evt.getRivetInfo().stage1_1_cat_pTjet30GeV',
        Rivet_stage1_1_fine_cat_pTjet25GeV='evt.getRivetInfo().stage1_1_fine_cat_pTjet25GeV',
        Rivet_stage1_1_fine_cat_pTjet30GeV='evt.getRivetInfo().stage1_1_fine_cat_pTjet30GeV',
        Rivet_errorCode='evt.getRivetInfo().errorCode',
        Rivet_prodMode='evt.getRivetInfo().prodMode',
        Rivet_higgsPt='evt.getRivetInfo().higgs.pt()',
        Rivet_higgsEta='evt.getRivetInfo().higgs.eta()',
        Rivet_higgsRapidity='evt.getRivetInfo().higgs.Rapidity()',
        Rivet_VPt='evt.getRivetInfo().V.pt()',
        Rivet_VEta='evt.getRivetInfo().V.eta()',
        Rivet_p4decay_VPt='evt.getRivetInfo().p4decay_V.pt()',
        Rivet_p4decay_VEta='evt.getRivetInfo().p4decay_V.eta()',
        Rivet_nJets30='evt.getRivetInfo().jets30.size()',
        Rivet_nJets25='evt.getRivetInfo().jets25.size()',

	Rivet_j1pt='? (evt.getRivetInfo().jets30.size()>0) ? evt.getRivetInfo().jets30[0].pt() : -99',
        Rivet_j2pt='? (evt.getRivetInfo().jets30.size()>1) ? evt.getRivetInfo().jets30[1].pt() : -99',
	Rivet_j1eta='? (evt.getRivetInfo().jets30.size()>0) ? evt.getRivetInfo().jets30[0].eta() : -99',
        Rivet_j2eta='? (evt.getRivetInfo().jets30.size()>1) ? evt.getRivetInfo().jets30[1].eta() : -99',
        Rivet_j1phi='? (evt.getRivetInfo().jets30.size()>0) ? evt.getRivetInfo().jets30[0].phi() : -99',
        Rivet_j2phi='? (evt.getRivetInfo().jets30.size()>1) ? evt.getRivetInfo().jets30[1].phi() : -99',
        Rivet_j1m='? (evt.getRivetInfo().jets30.size()>0) ? evt.getRivetInfo().jets30[0].M() : -99',
        Rivet_j2m='? (evt.getRivetInfo().jets30.size()>1) ? evt.getRivetInfo().jets30[1].M() : -99',

        gentau1_pt='evt.findGenTau(25,15).at(0)',
        gentau1_eta='evt.findGenTau(25,15).at(1)',
        gentau2_pt='evt.findGenTau(25,15).at(2)',
        gentau2_eta='evt.findGenTau(25,15).at(3)',

        dressedElectron_pt='evt.findDressedLepton(11).at(0)',
        dressedMuon_pt='evt.findDressedLepton(13).at(0)',

	HTTgenfinalstate='evt.findHTTfinalstate()',

  	genMetPt='evt.findRivetMet().at(0)',
        genMetPhi='evt.findRivetMet().at(1)',

        #Flag_badGlobalMuonFilter='evt.getFilterFlags("badGlobalMuonFilter")',
        #Flag_badCloneMuonFilter='evt.getFilterFlags("cloneGlobalMuonFilter")',
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
	Flag_ecalBadCalibReducedMINIAODFilter='evt.getFilterFlags("Flag_ecalBadCalibReducedMINIAODFilter")',
        #Flag_noBadMuons='evt.getFilterFlags("Flag_noBadMuons")',
        #metSig='evt.metSig()', # Using PF Met
        metcov00='evt.met("pfmet").getSignificanceMatrix[0][0]',
        metcov10='evt.met("pfmet").getSignificanceMatrix[1][0]',
        metcov01='evt.met("pfmet").getSignificanceMatrix[0][1]',
        metcov11='evt.met("pfmet").getSignificanceMatrix[1][1]',
        puppimetcov00='evt.met("puppimet").getSignificanceMatrix[0][0]',
        puppimetcov10='evt.met("puppimet").getSignificanceMatrix[1][0]',
        puppimetcov01='evt.met("puppimet").getSignificanceMatrix[0][1]',
        puppimetcov11='evt.met("puppimet").getSignificanceMatrix[1][1]',
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

        ##sm_weight_nlo='evt.lheweights().at(1080)',
        ##ps_weight_nlo='evt.lheweights().at(1081)',
        ##mm_weight_nlo='evt.lheweights().at(1082)',


        ##PythiaWeight_isr_muR0p5='evt.geninfoweights().at(6)',
        ##PythiaWeight_fsr_muR0p5='evt.geninfoweights().at(7)',
        ##PythiaWeight_isr_muR2='evt.geninfoweights().at(8)',
        ##PythiaWeight_fsr_muR2='evt.geninfoweights().at(9)',
        ##PythiaWeight_isr_muR0p25='evt.geninfoweights().at(10)',
        ##PythiaWeight_fsr_muR0p25='evt.geninfoweights().at(11)',
	##PythiaWeight_isr_muR4='evt.geninfoweights().at(12)',
        ##PythiaWeight_fsr_muR4='evt.geninfoweights().at(13)',
        #
	##lheweight_nominal='evt.lheweights().at(0)',
	##lheweight_muR1_muF2='evt.lheweights().at(1)',
        ##lheweight_muR1_muF0p5='evt.lheweights().at(2)',
        ##lheweight_muR2_muF1='evt.lheweights().at(3)',
        ##lheweight_muR2_muF2='evt.lheweights().at(4)',
        ##lheweight_muR2_muF0p5='evt.lheweights().at(5)',
        ##lheweight_muR0p5_muF1='evt.lheweights().at(6)',
        ##lheweight_muR0p5_muF2='evt.lheweights().at(7)',
        ##lheweight_muR0p5_muF0p5='evt.lheweights().at(8)',
#
        ##lheweight9='evt.lheweights[9]',
        ##lheweight10='evt.lheweights[10]',
        ##lheweight11='evt.lheweights[11]',
        ##lheweight12='evt.lheweights[12]',
        ##lheweight13='evt.lheweights[13]',
        ##lheweight14='evt.lheweights[14]',
        ##lheweight15='evt.lheweights[15]',
        ##lheweight16='evt.lheweights[16]',
        ##lheweight17='evt.lheweights[17]',
        ##lheweight18='evt.lheweights[18]',
        ##lheweight19='evt.lheweights[19]',
        ##lheweight20='evt.lheweights[20]',
        ##lheweight21='evt.lheweights[21]',
        ##lheweight22='evt.lheweights[22]',
        ##lheweight23='evt.lheweights[23]',
        ##lheweight24='evt.lheweights[24]',
        ##lheweight25='evt.lheweights[25]',
        ##lheweight26='evt.lheweights[26]',
        ##lheweight27='evt.lheweights[27]',
        ##lheweight28='evt.lheweights[28]',
        ##lheweight29='evt.lheweights[29]',
        ##lheweight30='evt.lheweights[30]',
        ##lheweight31='evt.lheweights[31]',
        ##lheweight32='evt.lheweights[32]',
        ##lheweight33='evt.lheweights[33]',
        ##lheweight34='evt.lheweights[34]',
        ##lheweight35='evt.lheweights[35]',
        ##lheweight36='evt.lheweights[36]',
        ##lheweight37='evt.lheweights[37]',
        ##lheweight38='evt.lheweights[38]',
        ##lheweight39='evt.lheweights[39]',
        ##lheweight40='evt.lheweights[40]',
        ##lheweight41='evt.lheweights[41]',
        ##lheweight42='evt.lheweights[42]',
        ##lheweight43='evt.lheweights[43]',
        ##lheweight44='evt.lheweights[44]',
        ##lheweight45='evt.lheweights[45]',
        ##lheweight46='evt.lheweights[46]',
        ##lheweight47='evt.lheweights[47]',
        ##lheweight48='evt.lheweights[48]',
        ##lheweight49='evt.lheweights[49]',
        ##lheweight50='evt.lheweights[50]',
        ##lheweight51='evt.lheweights[51]',
        ##lheweight52='evt.lheweights[52]',
        ##lheweight53='evt.lheweights[53]',
        ##lheweight54='evt.lheweights[54]',
        ##lheweight55='evt.lheweights[55]',
        ##lheweight56='evt.lheweights[56]',
        ##lheweight57='evt.lheweights[57]',
        ##lheweight58='evt.lheweights[58]',
        ##lheweight59='evt.lheweights[59]',
        ##lheweight60='evt.lheweights[60]',
        ##lheweight61='evt.lheweights[61]',
        ##lheweight62='evt.lheweights[62]',
        ##lheweight63='evt.lheweights[63]',
        ##lheweight64='evt.lheweights[64]',
        ##lheweight65='evt.lheweights[65]',
        ##lheweight66='evt.lheweights[66]',
        ##lheweight67='evt.lheweights[67]',
        ##lheweight68='evt.lheweights[68]',
        ##lheweight69='evt.lheweights[69]',
        ##lheweight70='evt.lheweights[70]',
        ##lheweight71='evt.lheweights[71]',
        ##lheweight72='evt.lheweights[72]',
        ##lheweight73='evt.lheweights[73]',
        ##lheweight74='evt.lheweights[74]',
        ##lheweight75='evt.lheweights[75]',
        ##lheweight76='evt.lheweights[76]',
        ##lheweight77='evt.lheweights[77]',
        ##lheweight78='evt.lheweights[78]',
        ##lheweight79='evt.lheweights[79]',
        ##lheweight80='evt.lheweights[80]',
        ##lheweight81='evt.lheweights[81]',
        ##lheweight82='evt.lheweights[82]',
        ##lheweight83='evt.lheweights[83]',
        ##lheweight84='evt.lheweights[84]',
        ##lheweight85='evt.lheweights[85]',
        ##lheweight86='evt.lheweights[86]',
        ##lheweight87='evt.lheweights[87]',
        ##lheweight88='evt.lheweights[88]',
        ##lheweight89='evt.lheweights[89]',
        ##lheweight90='evt.lheweights[90]',
        ##lheweight91='evt.lheweights[91]',
        ##lheweight92='evt.lheweights[92]',
        ##lheweight93='evt.lheweights[93]',
        ##lheweight94='evt.lheweights[94]',
        ##lheweight95='evt.lheweights[95]',
        ##lheweight96='evt.lheweights[96]',
        ##lheweight97='evt.lheweights[97]',
        ##lheweight98='evt.lheweights[98]',
        ##lheweight99='evt.lheweights[99]',
        ##lheweight100='evt.lheweights[100]',
        ##lheweight101='evt.lheweights[101]',
        ##lheweight102='evt.lheweights[102]',
        ##lheweight103='evt.lheweights[103]',
        ##lheweight104='evt.lheweights[104]',
        ##lheweight105='evt.lheweights[105]',
        ##lheweight106='evt.lheweights[106]',
        ##lheweight107='evt.lheweights[107]',
        ##lheweight108='evt.lheweights[108]',
        ##lheweight109='evt.lheweights[109]',
	##lheweight110='evt.lheweights[110]',

	prefiring_weight='evt.prefiringweights[0]',
        prefiring_weight_up='evt.prefiringweights[1]',
        prefiring_weight_down='evt.prefiringweights[2]',

	#bweight_2016='bVariables("pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5", 0.5).at(0)',
        #bweight_2017='bVariables("pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5", 0.5).at(1)',
        #bweight_2018='bVariables("pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5", 0.5).at(2)',


    ),

    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',

        objectMatchesEle24Tau30Path= r'matchToHLTPath({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24HPSTau30Path= r'matchToHLTPath({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle25Path= r'matchToHLTPath({object_idx}, "HLT_Ele25_eta2p1_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle32Path= r'matchToHLTPath({object_idx}, "HLT_Ele32_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle27Path= r'matchToHLTPath({object_idx}, "HLT_Ele27_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle35Path= r'matchToHLTPath({object_idx}, "HLT_Ele35_WPTight_Gsf_v\\d+", 0.5)',

        objectMatchesEle24Tau30Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24HPSTau30Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v\\d+", 0.5)',
        #objectMatchesEle24Tau30EmbeddedFilter= r'matchToGivenHLTFilter({object_idx}, "hltEle24erWPTightGsfTrackIsoFilterForTau", 0.5)',
        objectMatchesEle25Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele25_eta2p1_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle32Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele32_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle27Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele27_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle35Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele35_WPTight_Gsf_v\\d+", 0.5)',
	objectMatchesMu23e12DZFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
 	objectMatchesMu23e12Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
	objectMatchesMu8e23DZFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
	objectMatchesMu8e23Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu23e12DZPath= r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesMu23e12Path= r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8e23DZPath= r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesMu8e23Path= r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',

        objectMatchesEle23Ele12DZFilter= r'matchToHLTFilter({object_idx}, "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesEle23Ele12Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesEle23Ele12DZPath= r'matchToHLTPath({object_idx}, "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesEle23Ele12Path= r'matchToHLTPath({object_idx}, "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',

        objectMatchEmbeddedFilterEle27 = '? {object}.hasUserInt("matchEmbeddedFilterEle27") ? {object}.userInt("matchEmbeddedFilterEle27") : -10',
        objectMatchEmbeddedFilterEle32 = '? {object}.hasUserInt("matchEmbeddedFilterEle32") ? {object}.userInt("matchEmbeddedFilterEle32") : -10',
        objectMatchEmbeddedFilterEle32DoubleL1_v1 = '? {object}.hasUserInt("matchEmbeddedFilterEle32DoubleL1_v1") ? {object}.userInt("matchEmbeddedFilterEle32DoubleL1_v1") : -10',
        objectMatchEmbeddedFilterEle32DoubleL1_v2 = '? {object}.hasUserInt("matchEmbeddedFilterEle32DoubleL1_v2") ? {object}.userInt("matchEmbeddedFilterEle32DoubleL1_v2") : -10',
        objectMatchEmbeddedFilterEle35 = '? {object}.hasUserInt("matchEmbeddedFilterEle35") ? {object}.userInt("matchEmbeddedFilterEle35") : -10',
        objectMatchEmbeddedFilterEle24Tau30 = '? {object}.hasUserInt("matchEmbeddedFilterEle24Tau30") ? {object}.userInt("matchEmbeddedFilterEle24Tau30") : -10',

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
        objectMatchesIsoMu22Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu22_v\\d+", 0.5)',
        objectMatchesIsoMu22eta2p1Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu22_eta2p1_v\\d+", 0.5)',
        objectMatchesIsoTkMu22Path      = r'matchToHLTPath({object_idx}, "HLT_IsoTkMu22_v\\d+", 0.5)',
        objectMatchesIsoTkMu22eta2p1Path      = r'matchToHLTPath({object_idx}, "HLT_IsoTkMu22_eta2p1_v\\d+", 0.5)',
        objectMatchesIsoMu27Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu27_v\\d+", 0.5)',
        objectMatchesIsoMu24Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu24_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20SingleL1Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v\\d+", 0.5)',
        objectMatchesIsoMu20Tau27Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesIsoMu20HPSTau27Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v\\d+", 0.5)',

        objectMatchesIsoMu22Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoMu22_v\\d+", 0.5)',
        objectMatchesIsoMu22eta2p1Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoMu22_eta2p1_v\\d+", 0.5)',
        objectMatchesIsoTkMu22Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoTkMu22_v\\d+", 0.5)',
        objectMatchesIsoTkMu22eta2p1Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoTkMu22_eta2p1_v\\d+", 0.5)',
        objectMatchesIsoMu27Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoMu27_v\\d+", 0.5)',
        objectMatchesIsoMu24Filter      = r'matchToHLTFilter({object_idx}, "HLT_IsoMu24_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20SingleL1Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v\\d+", 0.5)',
        objectMatchesIsoMu20Tau27Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesIsoMu20HPSTau27Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesMu23e12DZFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesMu23e12Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8e23DZFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesMu8e23Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu23e12DZPath= r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesMu23e12Path= r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8e23DZPath= r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesMu8e23Path= r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',

        objectMatchesdoubleMuDZminMass3p8Path= r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v\\d+", 0.5)',
        objectMatchesdoubleMuDZminMass3p8Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v\\d+", 0.5)',
        objectMatchesdoubleMuDZminMass8Path= r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v\\d+", 0.5)',
        objectMatchesdoubleMuDZminMass8Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v\\d+", 0.5)',
        objectMatchesdoubleMuDZPath= r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesdoubleMuDZFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesdoubleMuPath= r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesdoubleMuFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu8DZPath= r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu8DZFilter= r'matchToHLTFilter({object_idx}, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu8Path= r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu8Filter= r'matchToHLTFilter({object_idx}, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu17TkMu8DZPath= r'matchToHLTPath({object_idx}, "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu17TkMu8DZFilter= r'matchToHLTFilter({object_idx}, "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu17TkMu8Path= r'matchToHLTPath({object_idx}, "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesdoubleMuTkMu17TkMu8Filter= r'matchToHLTFilter({object_idx}, "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v\\d+", 0.5)',

        objectMatchEmbeddedFilterMu24 = '? {object}.hasUserInt("matchEmbeddedFilterMu24") ? {object}.userInt("matchEmbeddedFilterMu24") : -10',
        objectMatchEmbeddedFilterMu27 = '? {object}.hasUserInt("matchEmbeddedFilterMu27") ? {object}.userInt("matchEmbeddedFilterMu27") : -10',
        objectMatchEmbeddedFilterMu19Tau20_2016 = '? {object}.hasUserInt("matchEmbeddedFilterMu19Tau20_2016") ? {object}.userInt("matchEmbeddedFilterMu19Tau20_2016") : -10',
        objectMatchEmbeddedFilterMu20Tau27_2017 = '? {object}.hasUserInt("matchEmbeddedFilterMu20Tau27_2017") ? {object}.userInt("matchEmbeddedFilterMu20Tau27_2017") : -10',
        objectMatchEmbeddedFilterMu20Tau27_2018 = '? {object}.hasUserInt("matchEmbeddedFilterMu20Tau27_2018") ? {object}.userInt("matchEmbeddedFilterMu20Tau27_2018") : -10',


        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecayFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isDirectPromptTauDecayProductFinalState() : -999',
        objectGenPromptFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isPromptFinalState() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
    ),



    'tauVariables' : PSet(
        objectL1IsoTauMatch = 'l1extraIsoTauMatching({object_idx})',
        objectL1IsoTauPt = 'l1extraIsoTauPt({object_idx})',
        objectMatchesIsoMu20Tau27Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesIsoMu20HPSTau27Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24Tau30Path= r'matchToHLTPath({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24HPSTau30Path= r'matchToHLTPath({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesDoubleMediumIsoTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIso_PFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumCombinedIsoTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMedium_CombinedIso_PFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',

        objectMatchesDoubleMediumTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau40Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau40Path = r'matchToHLTPath({object_idx}, "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumHPSTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightHPSTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumHPSTau40Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightHPSTau40Path = r'matchToHLTPath({object_idx}, "HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20SingleL1Path= r'matchToHLTPath({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v\\d+", 0.5)',

        objectMatchesIsoMu20Tau27Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24Tau30Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumTau40Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightTau40Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesIsoMu20HPSTau27Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesEle24HPSTau30Filter= r'matchToHLTFilter({object_idx}, "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v\\d+", 0.5)',
        objectMatchesDoubleMediumHPSTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightHPSTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleMediumHPSTau40Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTightHPSTau40Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v\\d+", 0.5)',
        objectMatchesIsoMu19Tau20SingleL1Filter= r'matchToHLTFilter({object_idx}, "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v\\d+", 0.5)',

        #originally were missing 2016 th_th path and filters
        objectMatchesDoubleTauCmbIso35RegFilter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTauCmbIso35RegPath = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTau35Filter = r'matchToHLTFilter({object_idx}, "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\d", 0.5)',
        objectMatchesDoubleTau35Path = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',

        objectMatchEmbeddedFilterMu20Tau27 = '? {object}.hasUserInt("matchEmbeddedFilterMu20Tau27") ? {object}.userInt("matchEmbeddedFilterMu20Tau27") : -10',
        objectMatchEmbeddedFilterMu19Tau20 = '? {object}.hasUserInt("matchEmbeddedFilterMu19Tau20") ? {object}.userInt("matchEmbeddedFilterMu19Tau20") : -10',
        objectMatchEmbeddedFilterMu20HPSTau27 = '? {object}.hasUserInt("matchEmbeddedFilterMu20HPSTau27") ? {object}.userInt("matchEmbeddedFilterMu20HPSTau27") : -10',
        objectMatchEmbeddedFilterEle24Tau30 = '? {object}.hasUserInt("matchEmbeddedFilterEle24Tau30") ? {object}.userInt("matchEmbeddedFilterEle24Tau30") : -10',
        objectMatchEmbeddedFilterTauTau = '? {object}.hasUserInt("matchEmbeddedFilterTauTau") ? {object}.userInt("matchEmbeddedFilterTauTau") : -10',
        objectMatchEmbeddedFilterTauTau2016 = '? {object}.hasUserInt("matchEmbeddedFilterTauTau2016") ? {object}.userInt("matchEmbeddedFilterTauTau2016") : -10',

        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
        objectZTTGenPt = 'tauGenKin({object_idx}).at(0)', 
        objectZTTGenEta = 'tauGenKin({object_idx}).at(1)', 
        objectZTTGenPhi = 'tauGenKin({object_idx}).at(2)', 
    ),



    'photonVariables' : PSet(),



    'jetVariables' : PSet(),



    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(
     #    object1_object2_doubleL1IsoTauMatch = 'doubleL1extraIsoTauMatching({object1_idx},{object2_idx})',
    ),
}
