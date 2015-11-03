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
        't': '37',
        'j': '18'
    },
    'etaCuts' : {
        'm': '2.4',
        'e': '2.5',
        't': '2.1',
        'j': '4.7'
    },

    # selections on all objects whether they're included in final states or not, done immediately after necessary variables are embedded
    'preselection' : OrderedDict(
        [
            # Remove jets that overlap our leptons
            ('j', {
                    'selection' : 'pt > 20 && abs(eta) < 4.7 && userFloat("idLoose") > 0.5',
                    'e' : {
                        'deltaR' : 0.5,
                        'selection' : 'userFloat("MVANonTrigWP90") > 0.5 && pt > 10 && abs(eta) < 2.5',
                        },
                    'm' : {
                        'deltaR' : 0.5,
                        'selection' : 'isMediumMuon() > 0.5 && pt > 10 && abs(eta) < 2.4',
                        },
                    }
             )
            ]),

    # selections to include object in final state (should be looser than analysis selections)
    # Based on default finalSelection, this is a little tighter for muons so we keep the min Pt Mu for our triggers
    # But we don't svFit them.
    'finalSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 && max(pt, userFloat("maxCorPt")) > 7',
        'm': 'max(pt, userFloat("maxCorPt")) > 10 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>20 && abs(eta) < 2.5 && userFloat("idLoose")'
    },



    # cross cleaning for objects in final state
    'crossCleaning' : 'smallestDeltaR() > 0.3',



    # additional variables for ntuple
    'eventVariables' : PSet(
        muVetoZTT10 = 'vetoMuons(0.4, "pt > 10 & abs(eta) < 2.4 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & (chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt() < 0.3 & isMediumMuon > 0").size()',
        muVetoZTT10new = 'vetoMuons(0.01, "pt > 10 & abs(eta) < 2.4 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & ( ( pfIsolationR03().sumChargedHadronPt + max( pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - 0.5 * pfIsolationR03().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0").size()',
        muVetoZTT10new2 = 'vetoMuons(0.001, "pt > 10 & abs(eta) < 2.4 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & ( ( pfIsolationR03().sumChargedHadronPt + max( pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - 0.5 * pfIsolationR03().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0").size()',
        eVetoZTT10 = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0").size()',
        eVetoZTT10new = 'vetoElectrons(0.01, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0").size()',
        eVetoZTT10new2 = 'vetoElectrons(0.001, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0").size()',
        eVetoZTT10old = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045").size()',
        jetVeto20ZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 4.7").size()',
        bjetCISVVeto20MediumZTT = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.814").size()',
    ),



    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),



    'electronVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationVariables().sumChargedHadronPt + max( {object}.pfIsolationVariables().sumNeutralHadronEt \
                                    + {object}.pfIsolationVariables().sumPhotonEt - 0.5 * {object}.pfIsolationVariables().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers
        objectMatchesMu23Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8Ele23Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu23Ele12Filter      = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectMu8Ele23Filter      = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        # Proposed Triggers
        objectMatchesMu17Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8Ele17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu17Ele12Filter      = 'matchToHLTFilter({object_idx}, "hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectMu8Ele17Filter      = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPrompt() : -999',
        objectGenIsDecayedLeptonHadron       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isDecayedLeptonHadron() : -999',
        objectGenIsTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isTauDecayProduct() : -999',
        objectGenIsPromptTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPromptTauDecayProduct() : -999',
        objectGenIsDirectTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isDirectTauDecayProduct() : -999',
        objectGenIsDirectPromptTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isDirectPromptTauDecayProduct() : -999',
        objectGenIsDirectHadronDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isDirectHadronDecayProduct() : -999',
        objectGenIsHardProcess       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isHardProcess() : -999',
        objectGenIsHardProcessTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isHardProcessTauDecayProduct() : -999',
        objectGenIsDirectHardProcessTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isDirectHardProcessTauDecayProduct() : -999',
        objectGenFromHardProcess       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().fromHardProcess() : -999',
    ),



    'muonVariables' : PSet(
        objectIsoDB03               = '({object}.pfIsolationR03().sumChargedHadronPt + max( {object}.pfIsolationR03().sumNeutralHadronEt \
                                        + {object}.pfIsolationR03().sumPhotonEt - 0.5 * {object}.pfIsolationR03().sumPUPt, 0.0)) / {object}.pt()',
        objectIsoDB04               = '({object}.pfIsolationR04().sumChargedHadronPt + max( {object}.pfIsolationR04().sumNeutralHadronEt \
                                        + {object}.pfIsolationR04().sumPhotonEt - 0.5 * {object}.pfIsolationR04().sumPUPt, 0.0)) / {object}.pt()',
        # Sync Triggers
        objectMatchesMu8Ele23Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu23Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu8Ele23Filter = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8", 0.5)',
        objectMu23Ele12Filter = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23", 0.5)',
        # Proposed Triggers
        objectMatchesMu8Ele17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu17Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu8Ele17Filter = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8", 0.5)',
        objectMu17Ele12Filter = 'matchToHLTFilter({object_idx}, "hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered17", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',
        objectGenIsDecayedLeptonHadron       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isDecayedLeptonHadron() : -999',
        objectGenIsTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isTauDecayProduct() : -999',
        objectGenIsPromptTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPromptTauDecayProduct() : -999',
        objectGenIsDirectTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isDirectTauDecayProduct() : -999',
        objectGenIsDirectPromptTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isDirectPromptTauDecayProduct() : -999',
        objectGenIsDirectHadronDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isDirectHadronDecayProduct() : -999',
        objectGenIsHardProcess       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isHardProcess() : -999',
        objectGenIsHardProcessTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isHardProcessTauDecayProduct() : -999',
        objectGenIsDirectHardProcessTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isDirectHardProcessTauDecayProduct() : -999',
        objectGenFromHardProcess       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().fromHardProcess() : -999',
    ),



    'tauVariables' : PSet(
        # Sync Triggers
        objectDoubleTau40Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau40TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau40Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        # Proposed Triggers
        objectDoubleTau35Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau35TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau35Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\d+", 0.5)',
        objectGenIsPrompt       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isPrompt() : -999',
        objectGenIsDecayedLeptonHadron       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isDecayedLeptonHadron() : -999',
        objectGenIsTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isTauDecayProduct() : -999',
        objectGenIsPromptTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isPromptTauDecayProduct() : -999',
        objectGenIsDirectTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isDirectTauDecayProduct() : -999',
        objectGenIsDirectPromptTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isDirectPromptTauDecayProduct() : -999',
        objectGenIsDirectHadronDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isDirectHadronDecayProduct() : -999',
        objectGenIsHardProcess       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isHardProcess() : -999',
        objectGenIsHardProcessTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isHardProcessTauDecayProduct() : -999',
        objectGenIsDirectHardProcessTauDecayProduct       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().isDirectHardProcessTauDecayProduct() : -999',
        objectGenFromHardProcess       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).statusFlags().fromHardProcess() : -999',
    ),



    'photonVariables' : PSet(),



    'jetVariables' : PSet(),



    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(),
}
