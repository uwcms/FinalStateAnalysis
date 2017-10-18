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
        't': '2.5',
        'g': '3.0',
        'j': '4.7'
    },

    # preselections for an object to be used anywhere
    'preselection' : {
        'e': 'abs(superCluster().eta) < 3.0 & pt > 7',
        'm': 'pt > 4 & (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 & pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 & pt > 10',
        # remove jets that are close to leptons
        'j': {
            'selection' : 'pt>20 & abs(eta) < 4.7 & userFloat("idLoose")',
            'e': {
                'selection' : 'pt>10&&userFloat("CBIDLoose")>0&&(chargedHadronIso()+max(0.0,neutralHadronIso()+photonIso()-userFloat("rho_fastjet")*userFloat("EffectiveArea")))/pt()<0.2',
                'deltaR' : 0.3,
                },
            'm': {
                'selection' : 'pt>10&&isLooseMuon&&(chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()<0.2',
                'deltaR' : 0.3,
                },
            },

        },

    # selections to include object in final state (should be looser than analysis selections)
    'finalSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 & pt > 7',
        'm': 'pt > 4 & (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 & pt > 17',
        'g': 'abs(superCluster().eta()) < 3.0 & pt > 10',
        'j': 'pt>20 & abs(eta) < 4.7 & userFloat("idLoose")',
    },

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
