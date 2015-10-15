# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet

parameters = {
    # minimal object kinematic cuts for the initial skim
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

    # preselections for an object to be used anywhere
    'preselection' : {
        # remove jets that are close to leptons
        'j' : {
            'e': {
                'selection' : 'pt>10 && userInt("CBIDLoose")>0.5',
                'deltaR' : 0.3,
                },
            'm': {
                'selection' : 'pt>10 && isLooseMuon && (chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()<0.2',
                'deltaR' : 0.3,
                },
            },
        },

    # selections to include object in final state (should be looser than analysis selections)
    'finalSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 && max(pt, userFloat("maxCorPt")) > 7',
        'm': 'max(pt, userFloat("maxCorPt")) > 4 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17 && tauID("decayModeFinding")',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        'j': 'pt>20 && abs(eta) < 2.5 && userFloat("idLoose")'
    },
    # cross cleaning for objects in final state
    'crossCleaning' : '',
    # additional variables for ntuple
    'eventVariables' : PSet(
        muVeto = 'vetoMuons(0.02, "isLooseMuon && pt > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.2").size()',
        muVetoNoIso = 'vetoMuons(0.02, "isLooseMuon && pt > 10 && abs(eta) < 2.4").size()',
        muVetoTight = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.12").size()',
        muVetoTightNoIso = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4").size()',
        eVeto = 'vetoElectrons(0.02, "userFloat(\'CBIDLoose\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoNoIso = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTight = 'vetoElectrons(0.02, "userFloat(\'CBIDMedium\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTightIso = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        muVetoHZZ = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        muVetoHZZIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        muVetoHZZTight = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        muVetoHZZTightIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoHZZ = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        eVetoHZZIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoHZZTight = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        eVetoHZZTightIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
    ),
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
