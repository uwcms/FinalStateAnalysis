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
                'selection' : 'pt>10&&userInt("CBIDLoose")>0&&(chargedHadronIso()+max(0.0,neutralHadronIso()+photonIso()-userFloat("rhoCSA14")*userFloat("EffectiveArea_HZZ4l2015")))/pt()<0.2',
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
        'e': 'abs(superCluster().eta) < 3.0 & max(pt, userFloat("maxCorPt")) > 7',
        'm': 'max(pt, userFloat("maxCorPt")) > 4 & (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 & pt > 17 & tauID("decayModeFinding")',
        'g': 'abs(superCluster().eta()) < 3.0 & pt > 10',
        'j': 'pt>20 & abs(eta) < 2.5 & userFloat("idLoose")'
    },
    # cross cleaning for objects in final state
    'crossCleaning' : '',
    # additional variables for ntuple
    'eventVariables' : PSet(
        muVeto = 'vetoMuons(0.4, "isLooseMuon & pt > 10 & abs(eta) < 2.4").size()',
        muVetoTight = 'vetoMuons(0.4, "userInt(\'tightID\') > 0.5  & pt > 10 & abs(eta) < 2.4 & (chargedHadronIso()+max(0.0,neutralHadronIso()+photonIso()-userFloat(\'rhoCSA14\')*userFloat(\'EffectiveArea_HZZ4l2015\')))/pt()<0.2").size()',
        eVeto = 'vetoElectrons(0.4, "userFloat(\'CBIDLoose\')>0.5 & pt > 10 & abs(eta) < 2.5").size()',
        eVetoTight = 'vetoElectrons(0.4, "userFloat(\'CBIDMedium\')>0.5 & pt > 10 & abs(eta) < 2.5").size()',
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
