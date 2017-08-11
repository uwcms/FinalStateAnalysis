# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

parameters = {
    # minimal object kinematic cuts
    'ptCuts' : {
        'm': '5',
        'e': '5',
        't': '18',
        'j': '18'
    },
    'etaCuts' : {
        'm': '4.',
        'e': '4.',
        't': '2.3',
        'j': '4.7'
    },

    # selections on all objects whether they're included in final states or not, done immediately after necessary variables are embedded
    'preselection' : OrderedDict(),
        # Commented out because of 80X jet cleaning memory leak
        #[
        #    # Remove jets that overlap our leptons
        #    ('j', { # Made pt requirement for E/Mu to clean an overlapping jet so
        #            # that this never happens
        #            'selection' : 'pt > 20 && abs(eta) < 4.7 && userFloat("idLoose") > 0.5',
        #            'e' : {
        #                'deltaR' : 0.5,
        #                'selection' : 'userFloat("MVANonTrigWP90") > 0.5 && pt > 9999 && abs(eta) < 2.5',
        #                },
        #            'm' : {
        #                'deltaR' : 0.5,
        #                'selection' : 'isMediumMuon() > 0.5 && pt > 9999 && abs(eta) < 2.4',
        #                },
        #            }
        #     )
        #    ]),

    # selections to include object in final state (should be looser than analysis selections)
    # Based on default finalSelection, this is a little tighter for muons so we keep the min Pt Mu for our triggers
    # But we don't svFit them.
    'finalSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 && pt > 5',
        'm': 'pt > 5 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>20 && abs(eta) < 4.7 && userFloat("idLoose")'
    },



    # cross cleaning for objects in final state
    'crossCleaning' : 'smallestDeltaR() > 0.3',



    # additional variables for ntuple
    'eventVariables' : PSet(
        muVetoAZHdR0 = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.25 & (isGlobalMuon | isTrackerMuon) & isPFMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        #NOT WORKING with the enum eVetoAZHdR0 = 'vetoElectrons(0.0, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2 && gsfTrack().hitPattern().numberOfHits(1) < 2").size()', # For numberOfHits see: http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_9_2_3/doc/html/db/d39/HitPattern_8h_source.html line 163 where 1 = reco::hitPattern::MISSING_INNER_HITS
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
        topQuarkPt1 = 'getTopQuarkInitialPts().at(0)',
        topQuarkPt2 = 'getTopQuarkInitialPts().at(1)',
        #buildGenTaus = 'buildGenTaus.size()',
        numGenJets = 'evt.numGenJets()',
        genMass = 'evt.getGenMass()',
        muVetoLLTTp001dxyz = 'vetoMuons(0.001, "pt > 5 & abs(eta) < 2.4 & ( ( pfIsolationR03().sumChargedHadronPt + max( pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - 0.5 * pfIsolationR03().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        eVetoLLTTp001dxyz = 'vetoElectrons(0.001, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        muVetoLLTTp001dxyzR0 = 'vetoMuons(0.0, "pt > 5 & abs(eta) < 2.4 & ( ( pfIsolationR03().sumChargedHadronPt + max( pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - 0.5 * pfIsolationR03().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
        eVetoLLTTp001dxyzR0 = 'vetoElectrons(0.0, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',

        jetVeto20ZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto20UpZTT = 'vetoJets(0.5, "userCand(\'jes+\').pt > 20 & abs(eta) < 4.7").size()',
        #jetVeto20DownZTT = 'vetoJets(0.5, "userCand(\'jes-\').pt > 20 & abs(eta) < 4.7").size()',
        jetVeto30ZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
        #jetVeto30UpZTT = 'vetoJets(0.5, "userCand(\'jes+\').pt > 30 & abs(eta) < 4.7").size()',
        #jetVeto30DownZTT = 'vetoJets(0.5, "userCand(\'jes-\').pt > 30 & abs(eta) < 4.7").size()',
        bjetCISVVeto20LooseZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.46").size()',
        bjetCISVVeto20MediumZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8").size()',
        bjetCISVVeto20TightZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.935").size()',
        bjetCISVVeto30LooseZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.46").size()',
        bjetCISVVeto30MediumZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8").size()',
        bjetCISVVeto30TightZTT = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.935").size()',
        isHtautau='evt.findDecay(25,15)',
        isHmumu='evt.findDecay(25,13)',
        isHee='evt.findDecay(25,11)',

        # VBF Variables
        vbfJetVeto30ZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7", 0.5).jets30',
        vbfJetVeto20ZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7", 0.5).jets20',
        vbfMassZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7", 0.5).mass',
        vbfDetaZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7", 0.5).deta',
        vbfDphiZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7", 0.5).dphi',
        vbfDijetPtZTT = 'vbfVariables("pt > 20 & abs(eta) < 4.7", 0.5).dijetpt',
        
        # b tag SF promote / demote method
        NBTagPDL_idL_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & userFloat(\'btaggedL\') > 0.5 ").size()',
        NBTagPDM_idL_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & userFloat(\'btaggedM\') > 0.5 ").size()',
        NBTagPDL_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'btaggedL\') > 0.5 ").size()',
        NBTagPDM_jVeto = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'btaggedM\') > 0.5 ").size()',

        # Leading and sublead jets
        j1pt = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(0)',
        j1eta = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(1)',
        j1phi = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(2)',
        j1csv = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(3)',
        #j1pu = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(4)',
        j1flavor = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(5)',
        #j1ptUp = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(6)',
        #j1ptDown = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(7)',
        j2pt = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(8)',
        j2eta = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(9)',
        j2phi = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(10)',
        j2csv = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(11)',
        #j2pu = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(12)',
        j2flavor = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(13)',
        #j2ptUp = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(14)',
        #j2ptDown = 'jetVariables("pt > 20 & abs(eta) < 4.7", 0.5).at(15)',

    ),



    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers
        objectMatchesEle22eta2p1LoosePath      = r'matchToHLTPath({object_idx}, "HLT_Ele22_eta2p1_WPLoose_Gsf_v\\d+", 0.5)',
        objectMatchesEle25eta2p1LoosePath      = r'matchToHLTPath({object_idx}, "HLT_Ele25_eta2p1_WPLoose_Gsf_v\\d+", 0.5)',
        objectMatchesEle25eta2p1TightPath      = r'matchToHLTPath({object_idx}, "HLT_Ele25_eta2p1_WPTight_Gsf_v\\d+", 0.5)',
        objectMatchesEle27eta2p1LoosePath      = r'matchToHLTPath({object_idx}, "HLT_Ele27_eta2p1_WPLoose_Gsf_v\\d+", 0.5)',
        objectMatchesEle27TightPath      = r'matchToHLTPath({object_idx}, "HLT_Ele27_WPTight_Gsf_v\\d+\\d+", 0.5)',
        objectMatchesEle23LoosePath      = r'matchToHLTPath({object_idx}, "HLT_Ele23_WPLoose_Gsf_v\\d+", 0.5)',
        objectMatchesEle17LoosePath      = r'matchToHLTPath({object_idx}, "HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesEle12LoosePath      = r'matchToHLTPath({object_idx}, "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesDoubleEPath      = r'matchToHLTPath({object_idx}, "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesDoubleE23_12Path      = r'matchToHLTPath({object_idx}, "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+", 0.5)',
        objectMatchesDoubleEFilter      = 'matchToHLTFilter({object_idx}, "HLT2PhotonPhotonDZ", 0.5)',
        objectMatchesDoubleE23_12Filter      = 'matchToHLTFilter({object_idx}, "hltEle23Ele12CaloIdLTrackIdLIsoVLDZFilter", 0.5)',
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
        objectMatchesMu50Path      = r'matchToHLTPath({object_idx}, "HLT_Mu50_v\\d+", 0.5)',
        objectMatchesIsoMu17eta2p1Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu17_eta2p1_v\\d+", 0.5)',
        objectMatchesMu17VVLPath      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesMu17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_v\\d+", 0.5)',
        objectMatchesMu8VVLPath      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_v\\d+", 0.5)',
        objectMatchesMu8Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_v\\d+", 0.5)',
        objectMatchesIsoMu18Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu18_v\\d+", 0.5)',
        objectMatchesIsoMu20Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu20_v\\d+", 0.5)',
        objectMatchesIsoMu22Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu22_v\\d+", 0.5)',
        objectMatchesIsoMu27Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu27_v\\d+", 0.5)',
        objectMatchesIsoMu22eta2p1Path      = r'matchToHLTPath({object_idx}, "HLT_IsoMu22_eta2p1_v\\d+", 0.5)',
        objectMatchesIsoTkMu20Path      = r'matchToHLTPath({object_idx}, "HLT_IsoTkMu20_v\\d+", 0.5)',
        objectMatchesIsoTkMu22Path      = r'matchToHLTPath({object_idx}, "HLT_IsoTkMu22_v\\d+", 0.5)',
        objectMatchesDoubleMuPath1      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesDoubleMuPath2      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+", 0.5)',
        objectMatchesDoubleMuFilter1 = 'matchToHLTFilter({object_idx}, "hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2", 0.5)',
        objectMatchesDoubleMuFilter2 = 'matchToHLTFilter({object_idx}, "hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenDirectPromptTauDecayFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isDirectPromptTauDecayProductFinalState() : -999',
        objectGenPromptFinalState       = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef().isPromptFinalState() : -999',
        objectZTTGenMatching = 'tauGenMatch2({object_idx})', 
    ),



    'tauVariables' : PSet(
        
        #objectL1IsoTauMatch = 'l1extraIsoTauMatching({object_idx})',
        # Sync Triggers
        objectDoubleTau40Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau40TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau40Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        # Proposed Triggers
        objectDoubleTau35Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau35TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau35Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectDoubleTau32Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau32TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau32Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v\\d+", 0.5)',
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
