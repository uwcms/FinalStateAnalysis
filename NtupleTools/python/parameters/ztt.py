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
        'e': '7',
        't': '35',
        'j': '20'
    },
    'etaCuts' : {
        'm': '2.5',
        'e': '3.0',
        't': '2.3',
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
    #'finalSelection' : '',

    # cross cleaning for objects in final state
    'crossCleaning' : 'smallestDeltaR() > 0.3',

    # additional variables for ntuple
    'eventVariables' : PSet(
        muVetoZTT15 = 'vetoMuons(0.4, "isGlobalMuon & isTrackerMuon & pt > 15 & abs(eta) < 2.4 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & (chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt() < 0.3").size()',
        muVetoZTT10 = 'vetoMuons(0.4, "pt > 10 & abs(eta) < 2.4 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & (chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt() < 0.3 & isMediumMuon > 0").size()',
        eVetoZTT15 = 'vetoElectrons(0.4, "pt > 15 & abs(eta) < 2.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045").size()',
        eVetoZTT10 = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0").size()',
        eVetoZTT10old = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2 & abs(userFloat(\'dxy\')) < 0.045").size()',
    ),

    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),

    'electronVariables' : PSet(
        objectMatchesMu23Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu8Ele23Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu23Ele12Filter      = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
        objectMu8Ele23Filter      = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter", 0.5)',
    ),

    'muonVariables' : PSet(
        objectMatchesMu8Ele23Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMatchesMu23Ele12Path      = r'matchToHLTPath({object_idx}, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+", 0.5)',
        objectMu8Ele23Filter = 'matchToHLTFilter({object_idx}, "hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8", 0.5)',
        objectMu23Ele12Filter = 'matchToHLTFilter({object_idx}, "hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23", 0.5)',
    ),

    'tauVariables' : PSet(
        objectZTT_PVDZ = '(evt.pv.z - {object}.vertex().z())',
        objectDoubleTau40Filter = 'matchToHLTFilter({object_idx}, "hltDoublePFTau40TrackPt1MediumIsolationDz02Reg", 0.5)',
        objectMatchesDoubleTau40Path      = r'matchToHLTPath({object_idx}, "HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v\\d+", 0.5)',
    ),

    'photonVariables' : PSet(),

    'jetVariables' : PSet(),

    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(),
}
