# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet

parameters = {
    # minimal object kinematic cuts
    'ptCuts' : {
        'm': '5',
        'e': '7',
        't': '18',
        'g': '10',
        'j': '20'
    },
    'etaCuts' : {
        'm': '2.5',
        'e': '3.0',
        't': '2.3',
        'g': '3.0',
        'j': '2.5'
    },
    # selections to include object in final state (should be looser than analysis selections)
    'objectSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 & max(pt, userFloat("maxCorPt")) > 7',
        'm': 'max(pt, userFloat("maxCorPt")) > 4 & (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 & pt > 17 & tauID("decayModeFinding")',
        'g': 'abs(superCluster().eta()) < 3.0 & pt > 10',
        'j': 'pt>20 & abs(eta) < 2.5 & userFloat("idLoose")'
    },
    # selections to clean jets
    'jetCleaningSelections' : {
        'e': 'pt>10&&userInt("CBIDVeto")>0&&(userIso(0)+max(userIso(1)+neutralHadronIso()-0.5*userIso(2),0.0))/pt()<0.3',
        'm': 'pt>10&&isGlobalMuon&&isTrackerMuon&&(userIso(0)+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso(),0))/pt()<0.3',
    },
    'jetDeltaRCleaning' : 0.3,
    # cross cleaning for objects in final state
    'crossCleaning' : 'smallestDeltaR() > 0.3',
    # additional variables for ntuple
    'eventVariables' : PSet(),
    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),
    'electronVariables' : PSet(),
    'muonVariables' : PSet(),
    'tauVariables' : PSet(),
    'photonVariables' : PSet(),
    'jetVariables' : PSet(),
    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(),
}
