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
        Rivet_stage1_1_cat_pTjet25GeV='evt.getRivetInfo().stage1_1_cat_pTjet25GeV',
        Rivet_stage1_1_cat_pTjet30GeV='evt.getRivetInfo().stage1_1_cat_pTjet30GeV',
        Rivet_stage1_1_fine_cat_pTjet25GeV='evt.getRivetInfo().stage1_1_fine_cat_pTjet25GeV',
        Rivet_stage1_1_fine_cat_pTjet30GeV='evt.getRivetInfo().stage1_1_fine_cat_pTjet30GeV',
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
        metSig='evt.metSig()', # Using PF Met
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

        sm_weight_nlo='evt.lheweights().at(1080)',
        ps_weight_nlo='evt.lheweights().at(1081)',
        mm_weight_nlo='evt.lheweights().at(1082)',
        
        #lheweight0='evt.lheweights().at(0)',
        #lheweight1='evt.lheweights().at(1)',
        #lheweight2='evt.lheweights().at(2)',
        #lheweight3='evt.lheweights().at(3)',
        #lheweight4='evt.lheweights().at(4)',
        #lheweight5='evt.lheweights().at(5)',
        #lheweight6='evt.lheweights().at(6)',
        #lheweight7='evt.lheweights().at(7)',
        #lheweight8='evt.lheweights().at(8)',
        #lheweight9='evt.lheweights[9]',
        #lheweight10='evt.lheweights[10]',
        #lheweight11='evt.lheweights[11]',
        #lheweight12='evt.lheweights[12]',
        #lheweight13='evt.lheweights[13]',
        #lheweight14='evt.lheweights[14]',
        #lheweight15='evt.lheweights[15]',
        #lheweight16='evt.lheweights[16]',
        #lheweight17='evt.lheweights[17]',
        #lheweight18='evt.lheweights[18]',
        #lheweight19='evt.lheweights[19]',
        #lheweight20='evt.lheweights[20]',
        #lheweight21='evt.lheweights[21]',
        #lheweight22='evt.lheweights[22]',
        #lheweight23='evt.lheweights[23]',
        #lheweight24='evt.lheweights[24]',
        #lheweight25='evt.lheweights[25]',
        #lheweight26='evt.lheweights[26]',
        #lheweight27='evt.lheweights[27]',
        #lheweight28='evt.lheweights[28]',
        #lheweight29='evt.lheweights[29]',
        #lheweight30='evt.lheweights[30]',
        #lheweight31='evt.lheweights[31]',
        #lheweight32='evt.lheweights[32]',
        #lheweight33='evt.lheweights[33]',
        #lheweight34='evt.lheweights[34]',
        #lheweight35='evt.lheweights[35]',
        #lheweight36='evt.lheweights[36]',
        #lheweight37='evt.lheweights[37]',
        #lheweight38='evt.lheweights[38]',
        #lheweight39='evt.lheweights[39]',
        #lheweight40='evt.lheweights[40]',
        #lheweight41='evt.lheweights[41]',
        #lheweight42='evt.lheweights[42]',
        #lheweight43='evt.lheweights[43]',
        #lheweight44='evt.lheweights[44]',
        #lheweight45='evt.lheweights[45]',
        #lheweight46='evt.lheweights[46]',
        #lheweight47='evt.lheweights[47]',
        #lheweight48='evt.lheweights[48]',
        #lheweight49='evt.lheweights[49]',
        #lheweight50='evt.lheweights[50]',
        #lheweight51='evt.lheweights[51]',
        #lheweight52='evt.lheweights[52]',
        #lheweight53='evt.lheweights[53]',
        #lheweight54='evt.lheweights[54]',
        #lheweight55='evt.lheweights[55]',
        #lheweight56='evt.lheweights[56]',
        #lheweight57='evt.lheweights[57]',
        #lheweight58='evt.lheweights[58]',
        #lheweight59='evt.lheweights[59]',
        #lheweight60='evt.lheweights[60]',
        #lheweight61='evt.lheweights[61]',
        #lheweight62='evt.lheweights[62]',
        #lheweight63='evt.lheweights[63]',
        #lheweight64='evt.lheweights[64]',
        #lheweight65='evt.lheweights[65]',
        #lheweight66='evt.lheweights[66]',
        #lheweight67='evt.lheweights[67]',
        #lheweight68='evt.lheweights[68]',
        #lheweight69='evt.lheweights[69]',
        #lheweight70='evt.lheweights[70]',
        #lheweight71='evt.lheweights[71]',
        #lheweight72='evt.lheweights[72]',
        #lheweight73='evt.lheweights[73]',
        #lheweight74='evt.lheweights[74]',
        #lheweight75='evt.lheweights[75]',
        #lheweight76='evt.lheweights[76]',
        #lheweight77='evt.lheweights[77]',
        #lheweight78='evt.lheweights[78]',
        #lheweight79='evt.lheweights[79]',
        #lheweight80='evt.lheweights[80]',
        #lheweight81='evt.lheweights[81]',
        #lheweight82='evt.lheweights[82]',
        #lheweight83='evt.lheweights[83]',
        #lheweight84='evt.lheweights[84]',
        #lheweight85='evt.lheweights[85]',
        #lheweight86='evt.lheweights[86]',
        #lheweight87='evt.lheweights[87]',
        #lheweight88='evt.lheweights[88]',
        #lheweight89='evt.lheweights[89]',
        #lheweight90='evt.lheweights[90]',
        #lheweight91='evt.lheweights[91]',
        #lheweight92='evt.lheweights[92]',
        #lheweight93='evt.lheweights[93]',
        #lheweight94='evt.lheweights[94]',
        #lheweight95='evt.lheweights[95]',
        #lheweight96='evt.lheweights[96]',
        #lheweight97='evt.lheweights[97]',
        #lheweight98='evt.lheweights[98]',
        #lheweight99='evt.lheweights[99]',
        #lheweight100='evt.lheweights[100]',
        #lheweight101='evt.lheweights[101]',
        #lheweight102='evt.lheweights[102]',
        #lheweight103='evt.lheweights[103]',
        #lheweight104='evt.lheweights[104]',
        #lheweight105='evt.lheweights[105]',
        #lheweight106='evt.lheweights[106]',
        #lheweight107='evt.lheweights[107]',
        #lheweight108='evt.lheweights[108]',
        #lheweight109='evt.lheweights[109]',
	#lheweight110='evt.lheweights[110]',

	prefiring_weight='evt.prefiringweights[0]',
        prefiring_weight_up='evt.prefiringweights[1]',
        prefiring_weight_down='evt.prefiringweights[2]',

	bweight_2016='bVariables("pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5", 0.5).at(0)',
        bweight_2017='bVariables("pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5", 0.5).at(1)',
        bweight_2018='bVariables("pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5", 0.5).at(2)',

        # Leading and sublead jets
        j1pt = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(0)',
        j1eta = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(1)',
        j1phi = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(2)',
        j1csv = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(3)',
        j1hadronflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(6)',
        j2pt = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(10)',
        j2eta = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(11)',
        j2phi = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(12)',
        j2csv = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(13)',
        j2hadronflavor = 'jetVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(16)',

        j1ptWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(0)',
        j1etaWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(1)',
        j1phiWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(2)',
        j1csvWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(3)',
        j1hadronflavorWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(6)',
        j2ptWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(10)',
        j2etaWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(11)',
        j2phiWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(12)',
        j2csvWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(13)',
        j2hadronflavorWoNoisyJets = 'jetVariables("(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)", 0.5).at(16)',


        # Leading and subleading BTagged Jets
        jb1pt_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(0)',
        jb1eta_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(1)',
        jb1phi_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(2)',
        jb1hadronflavor_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(6)',
        jb2pt_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(10)',
        jb2eta_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(11)',
        jb2phi_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(12)',
        jb2hadronflavor_2016 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321", 0.5).at(16)',

        jb1pt_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(0)',
        jb1eta_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(1)',
        jb1phi_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(2)',
        jb1hadronflavor_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(6)',
        jb2pt_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(10)',
        jb2eta_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(11)',
        jb2phi_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941", 0.5).at(12)',
        jb2hadronflavor_2017 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\'))  > 0.4941", 0.5).at(16)',

        jb1pt_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(0)',
        jb1eta_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(1)',
        jb1phi_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(2)',
        jb1hadronflavor_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(6)',
        jb2pt_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(10)',
        jb2eta_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(11)',
        jb2phi_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(12)',
        jb2hadronflavor_2018 = 'jetVariables("pt > 25 & userFloat(\'idTight\') > 0.5 & abs(eta) < 2.4 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184", 0.5).at(16)',

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
        objectZTTGenDR = 'tauGenKin({object_idx}).at(3)', 


        objectRerunMVArun2v2DBoldDMwLTraw = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTrawRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTrawRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVVLooseRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVLooseRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTLooseRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTMedium = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTMediumRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTMediumRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTTightRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVTightRerun") : -10',
        objectRerunMVArun2v2DBoldDMwLTVVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBoldDMwLTVVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBoldDMwLTVVTightRerun") : -10',

#NewDM
      objectRerunMVArun2v2DBnewDMwLTraw = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTrawRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTrawRerun") : -10',
              objectRerunMVArun2v2DBnewDMwLTVVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVVLooseRerun") : -10',
              objectRerunMVArun2v2DBnewDMwLTVLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVLooseRerun") : -10',
              objectRerunMVArun2v2DBnewDMwLTLoose = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTLooseRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTLooseRerun") : -10',
              objectRerunMVArun2v2DBnewDMwLTMedium = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTMediumRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTMediumRerun") : -10',
              objectRerunMVArun2v2DBnewDMwLTTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTTightRerun") : -10',
              objectRerunMVArun2v2DBnewDMwLTVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVTightRerun") : -10',
      objectRerunMVArun2v2DBnewDMwLTVVTight = '? {object}.hasUserFloat("byIsolationMVArun2v2DBnewDMwLTVVTightRerun") ? {object}.userFloat("byIsolationMVArun2v2DBnewDMwLTVVTightRerun") : -10',





        #objectDpfTau2016v1VSallraw = '? {object}.hasUserFloat("byDpfTau2016v1VSallraw") ? {object}.userFloat("byDpfTau2016v1VSallraw") : -10',
        #objectTightDpfTau2016v1VSall = '? {object}.hasUserFloat("byTightDpfTau2016v1VSall") ? {object}.userFloat("byTightDpfTau2016v1VSall") : -10',
        #objectDpfTau2016v0VSallraw = '? {object}.hasUserFloat("byDpfTau2016v0VSallraw") ? {object}.userFloat("byDpfTau2016v0VSallraw") : -10',
        #objectTightDpfTau2016v0VSall = '? {object}.hasUserFloat("byTightDpfTau2016v0VSall") ? {object}.userFloat("byTightDpfTau2016v0VSall") : -10',

        objectDeepTau2017v2p1VSmuraw = '? {object}.hasUserFloat("byDeepTau2017v2p1VSmuraw") ? {object}.userFloat("byDeepTau2017v2p1VSmuraw") : -10',
        objectVVVLooseDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVVVLooseDeepTau2017v2p1VSmu") ? {object}.userFloat("byVVVLooseDeepTau2017v2p1VSmu") : -10',
        objectVVLooseDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVVLooseDeepTau2017v2p1VSmu") ? {object}.userFloat("byVVLooseDeepTau2017v2p1VSmu") : -10',
        objectVLooseDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVLooseDeepTau2017v2p1VSmu") ? {object}.userFloat("byVLooseDeepTau2017v2p1VSmu") : -10',
        objectLooseDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byLooseDeepTau2017v2p1VSmu") ? {object}.userFloat("byLooseDeepTau2017v2p1VSmu") : -10',
        objectMediumDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byMediumDeepTau2017v2p1VSmu") ? {object}.userFloat("byMediumDeepTau2017v2p1VSmu") : -10',
        objectTightDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byTightDeepTau2017v2p1VSmu") ? {object}.userFloat("byTightDeepTau2017v2p1VSmu") : -10',
        objectVTightDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVTightDeepTau2017v2p1VSmu") ? {object}.userFloat("byVTightDeepTau2017v2p1VSmu") : -10',
        objectVVTightDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVVTightDeepTau2017v2p1VSmu") ? {object}.userFloat("byVVTightDeepTau2017v2p1VSmu") : -10',

        objectDeepTau2017v2p1VSeraw = '? {object}.hasUserFloat("byDeepTau2017v2p1VSeraw") ? {object}.userFloat("byDeepTau2017v2p1VSeraw") : -10',
        objectVVVLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVVVLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byVVVLooseDeepTau2017v2p1VSe") : -10',
        objectVVLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVVLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byVVLooseDeepTau2017v2p1VSe") : -10',
        objectVLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byVLooseDeepTau2017v2p1VSe") : -10',
        objectLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byLooseDeepTau2017v2p1VSe") : -10',
        objectMediumDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byMediumDeepTau2017v2p1VSe") ? {object}.userFloat("byMediumDeepTau2017v2p1VSe") : -10',
        objectTightDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byTightDeepTau2017v2p1VSe") ? {object}.userFloat("byTightDeepTau2017v2p1VSe") : -10',
        objectVTightDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVTightDeepTau2017v2p1VSe") ? {object}.userFloat("byVTightDeepTau2017v2p1VSe") : -10',
        objectVVTightDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVVTightDeepTau2017v2p1VSe") ? {object}.userFloat("byVVTightDeepTau2017v2p1VSe") : -10',

        objectDeepTau2017v2p1VSjetraw = '? {object}.hasUserFloat("byDeepTau2017v2p1VSjetraw") ? {object}.userFloat("byDeepTau2017v2p1VSjetraw") : -10',
        objectVVVLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVVVLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byVVVLooseDeepTau2017v2p1VSjet") : -10',
        objectVVLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVVLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byVVLooseDeepTau2017v2p1VSjet") : -10',
        objectVLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byVLooseDeepTau2017v2p1VSjet") : -10',
        objectLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byLooseDeepTau2017v2p1VSjet") : -10',
        objectMediumDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byMediumDeepTau2017v2p1VSjet") ? {object}.userFloat("byMediumDeepTau2017v2p1VSjet") : -10',
        objectTightDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byTightDeepTau2017v2p1VSjet") ? {object}.userFloat("byTightDeepTau2017v2p1VSjet") : -10',
        objectVTightDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVTightDeepTau2017v2p1VSjet") ? {object}.userFloat("byVTightDeepTau2017v2p1VSjet") : -10',
        objectVVTightDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVVTightDeepTau2017v2p1VSjet") ? {object}.userFloat("byVVTightDeepTau2017v2p1VSjet") : -10',

        objectAgainstElectronMVA6Raw2018 = '? {object}.hasUserFloat("againstElectronMVA6Raw2018") ? {object}.userFloat("againstElectronMVA6Raw2018") : -10',
        objectAgainstElectronMVA6category2018 = '? {object}.hasUserFloat("againstElectronMVA6category2018") ? {object}.userFloat("againstElectronMVA6category2018") : -10',
        objectAgainstElectronVLooseMVA62018 = '? {object}.hasUserFloat("againstElectronVLooseMVA62018") ? {object}.userFloat("againstElectronVLooseMVA62018") : -10',
        objectAgainstElectronLooseMVA62018 = '? {object}.hasUserFloat("againstElectronLooseMVA62018") ? {object}.userFloat("againstElectronLooseMVA62018") : -10',
        objectAgainstElectronMediumMVA62018 = '? {object}.hasUserFloat("againstElectronMediumMVA62018") ? {object}.userFloat("againstElectronMediumMVA62018") : -10',
        objectAgainstElectronTightMVA62018 = '? {object}.hasUserFloat("againstElectronTightMVA62018") ? {object}.userFloat("againstElectronTightMVA62018") : -10',
        objectAgainstElectronVTightMVA62018 = '? {object}.hasUserFloat("againstElectronVTightMVA62018") ? {object}.userFloat("againstElectronVTightMVA62018") : -10',

    ),



    'photonVariables' : PSet(),



    'jetVariables' : PSet(),



    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(
         object1_object2_doubleL1IsoTauMatch = 'doubleL1extraIsoTauMatching({object1_idx},{object2_idx})',
    ),
}
