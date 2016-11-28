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
        'e': '10',
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
        'e': 'abs(superCluster().eta) < 3.0 && pt > 7',
        'm': 'pt > 8 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>18 && abs(eta) < 4.7 && userFloat("idLoose") > 0.5'
    },



    # cross cleaning for objects in final state
    'crossCleaning' : 'smallestDeltaR() > 0.3',



    # additional variables for ntuple
    'eventVariables' : PSet(
        metSig='evt.metSig()', # Using PF Met
        metcov00='evt.metCov(0)', # 0 = (0,0) PF Met based
        metcov10='evt.metCov(1)', # 1 = (1,0)
        metcov01='evt.metCov(2)', # 2 = (0,1)
        metcov11='evt.metCov(3)', # 3 - (1,1)
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

	#### Uncomment to have LHE weights for study on theoretical uncertainties
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

        #muVetoZTTp001dxyz = 'vetoMuons(0.001, "pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        #eVetoZTTp001dxyz = 'vetoElectrons(0.001, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        #muVetoZTTp001dxyzR0 = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        #eVetoZTTp001dxyzR0 = 'vetoElectrons(0.0, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
	#dimuonVeto = 'vetoSecondMuon(0.15,"pt > 15 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isGlobalMuon > 0 & isTrackerMuon > 0 & isPFMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
	#dielectronVeto = 'vetoSecondElectron(0.15, "pt > 15 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'CBIDVeto\') > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',

        #jetVeto20ZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto20ZTT_JESUp = 'vetoJets(0.5, "userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto20ZTT_JESDown = 'vetoJets(0.5, "userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto20ZTT_JERUp = 'vetoJets(0.5, "userCand(\'jres+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto20ZTT_JERDown = 'vetoJets(0.5, "userCand(\'jres-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto30ZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto30ZTT_JESUp = 'vetoJets(0.5, "userCand(\'jes+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto30ZTT_JESDown = 'vetoJets(0.5, "userCand(\'jes-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto30ZTT_JERUp = 'vetoJets(0.5, "userCand(\'jres+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto30ZTT_JERDown = 'vetoJets(0.5, "userCand(\'jres-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #bjetCISVVeto20LooseZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.46").size()',
        #bjetCISVVeto20MediumZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8").size()',
        #bjetCISVVeto20TightZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.935").size()',
        #bjetCISVVeto30LooseZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.46").size()',
        #bjetCISVVeto30MediumZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8").size()',
        #bjetCISVVeto30TightZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.935").size()',
    #    #isHtautau='evt.findDecay(25,15)',
    #    #isHmumu='evt.findDecay(25,13)',
    #    #isHee='evt.findDecay(25,11)',

        # VBF Variables
        #vbfJetVeto30ZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30',
        #vbfJetVeto20ZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20',
        #vbfMassZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass',
        #vbfDetaZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta',
        #vbfDphiZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi',
        #vbfDijetPtZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt',

        #vbfJetVeto30ZTT_JESUp = 'vbfVariables("userCand(\'jes+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30_JESUp',
        #vbfJetVeto20ZTT_JESUp = 'vbfVariables("userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20_JESUp',
        #vbfMassZTT_JESUp = 'vbfVariables("userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass_JESUp',
        #vbfDetaZTT_JESUp = 'vbfVariables("userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta_JESUp',
        #vbfDphiZTT_JESUp = 'vbfVariables("userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi_JESUp',
        #vbfDijetPtZTT_JESUp = 'vbfVariables("userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt_JESUp',

        #vbfJetVeto30ZTT_JESDown = 'vbfVariables("userCand(\'jes-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30_JESDown',
        #vbfJetVeto20ZTT_JESDown = 'vbfVariables("userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20_JESDown',
        #vbfMassZTT_JESDown = 'vbfVariables("userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass_JESDown',
        #vbfDetaZTT_JESDown = 'vbfVariables("userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta_JESDown',
        #vbfDphiZTT_JESDown = 'vbfVariables("userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi_JESDown',
        #vbfDijetPtZTT_JESDown = 'vbfVariables("userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt_JESDown',
        
        # b tag SF promote / demote method
        #XXX NBTagPDL_idL_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & userFloat(\'btaggedL\') > 0.5 ").size()',
        #XXX NBTagPDM_idL_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & userFloat(\'btaggedM\') > 0.5 ").size()',
        #XXX NBTagPDL_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'btaggedL\') > 0.5 ").size()',
        #XXX NBTagPDM_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'btaggedM\') > 0.5 ").size()',

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
        jb1pt = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(0)',
        jb1eta = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(1)',
        jb1phi = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(2)',
        jb1csv = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(3)',
        jb1pu = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(4)',
        jb1partonflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(5)',
        jb1hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(6)',
        jb1rawf = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(7)',
        jb1ptUp = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(8)',
        jb1ptDown = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(9)',
        #jb1ptUp = 'jetVariables("pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(6)',
        #jb1ptDown = 'jetVariables("pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(7)',
        jb2pt = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(10)',
        jb2eta = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(11)',
        jb2phi = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(12)',
        jb2csv = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(13)',
        jb2pu = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(14)',
        jb2partonflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(15)',
        jb2hadronflavor = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(16)',
        jb2rawf = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(17)',
        jb2ptUp = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(18)',
        jb2ptDown = 'jetVariables("pt > 20 & userFloat(\'idLoose\') > 0.5 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(19)',
        #jb2ptUp = 'jetVariables("pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(14)',
        #jb2ptDown = 'jetVariables("pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8", 0.5).at(15)',
    ),



    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers
        objectMatchesMu23Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8Ele23Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesEle22Path      = r'matchToHLTPath({object_idx}, "HLT_Ele22_eta2p1_WP75_Gsf_v\\d+", 0.5)',
        objectMatchesEle23Path      = r'matchToHLTPath({object_idx}, "HLT_Ele23_WPLoose_Gsf_v\\d+", 0.5)',
        objectMatchesMu23Ele12Filter      = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectMatchesMu8Ele23Filter      = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectMatchesEle22Filter      = 'matchToHLTFilter({object_idx}, "hltSingleEle22WP75GsfTrackIsoFilter", 0.5)',
        objectMatchesEle23Filter      = 'matchToHLTFilter({object_idx}, "hltEle23WPLooseGsfTrackIsoFilter", 0.5)',
        objectMatchesEle25LooseFilter      = 'matchToHLTFilter({object_idx}, "hltEle25erWPLooseGsfTrackIsoFilter", 0.5)',
        objectMatchesEle25TightFilter      = 'matchToHLTFilter({object_idx}, "hltEle25erWPTightGsfTrackIsoFilter", 0.5)',
        # Proposed Triggers
        objectMatchesMu17Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8Ele17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu17Ele12Filter      = 'matchToHLTFilter({object_idx}, "hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectMatchesMu8Ele17Filter      = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecay       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().statusFlags().isDirectPromptTauDecayProduct() : -999',
        #objectZTTGenMatching = 'tauGenMatch({object_idx})', 
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
	#objectZTTThirdLeptonVeto = 'overlapElectrons({object_idx},0.001,"pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    ),



    'muonVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationR03().sumChargedHadronPt + max( {object}.pfIsolationR03().sumNeutralHadronEt \
                                        + {object}.pfIsolationR03().sumPhotonEt - 0.5 * {object}.pfIsolationR03().sumPUPt, 0.0)) / {object}.pt()',
        objectIsoDB04               = '({object}.pfIsolationR04().sumChargedHadronPt + max( {object}.pfIsolationR04().sumNeutralHadronEt \
                                        + {object}.pfIsolationR04().sumPhotonEt - 0.5 * {object}.pfIsolationR04().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers
        objectMatchesMu8Ele23Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu23Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesIsoMu17Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu17_eta2p1_v\\d+", 0.5)',
        objectMatchesIsoMu18Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu18_v\\d+", 0.5)',
        objectMu8Ele23Filter = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8", 0.5)',
        objectMu23Ele12Filter = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23", 0.5)',
        objectIsoMu17Filter = 'matchToHLTFilter({object_idx}, "hltL3crIsoL1sSingleMu16erL1f0L2f10QL3f17QL3trkIsoFiltered0p09", 0.5)',
        objectIsoMu18Filter = 'matchToHLTFilter({object_idx}, "hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09", 0.5)',
        objectIsoMu22Filter = 'matchToHLTFilter({object_idx}, "hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09", 0.5)',
        objectIsoTkMu22Filter = 'matchToHLTFilter({object_idx}, "hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09", 0.5)',
        # Proposed Triggers
        objectMatchesMu8Ele17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu17Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu8Ele17Filter = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8", 0.5)',
        objectMu17Ele12Filter = 'matchToHLTFilter({object_idx}, "hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered17", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecayFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isDirectPromptTauDecayProductFinalState() : -999',
        objectGenPromptFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isPromptFinalState() : -999',
        #objectZTTGenMatching = 'tauGenMatch({object_idx})', 
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
        ##objectZTTThirdLeptonVeto = 'overlapMuons({object_idx},0.001,"pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    ),



    'tauVariables' : PSet(
        
        #objectL1IsoTauMatch = 'l1extraIsoTauMatching({object_idx})',
        # Sync Triggers
        objectMatchesDoubleTau40Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau40TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau40Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        # Proposed Triggers
        objectMatchesDoubleTau35Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau35TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau35Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectMatchesDoubleTau32Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau32TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau32Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isPrompt() : -999',
        #objectZTTGenMatching = 'tauGenMatch({object_idx})', 
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
         object1_object2_PZetaLess0p85PZetaVis = 'pZeta({object1_idx}, {object2_idx}) - 0.85*pZetaVis({object1_idx}, {object2_idx})',
         object1_object2_pt_tt = 'PtDiTauSyst({object1_idx}, {object2_idx})',
         object1_object2_MtTotal = 'MtTotal({object1_idx}, {object2_idx})',
         object1_object2_MvaMet = 'getMVAMET({object1_idx},{object2_idx}).at(0)',
         object1_object2_MvaMetPhi = 'getMVAMET({object1_idx},{object2_idx}).at(1)',
         object1_object2_MvaMetCovMatrix00 = 'getMVAMET({object1_idx},{object2_idx}).at(2)',
         object1_object2_MvaMetCovMatrix10 = 'getMVAMET({object1_idx},{object2_idx}).at(3)',
         object1_object2_MvaMetCovMatrix01 = 'getMVAMET({object1_idx},{object2_idx}).at(4)',
         object1_object2_MvaMetCovMatrix11 = 'getMVAMET({object1_idx},{object2_idx}).at(5)',
        #object1_object2_doubleL1IsoTauMatch = 'doubleL1extraIsoTauMatching({object1_idx},{object2_idx})',
    ),
}
