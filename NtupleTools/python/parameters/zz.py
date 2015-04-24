# Parameters to be used in production of ZZ ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

parameters = {
    # selections on all objects whether they're included in final states or not, done immediately after necessary variables are embedded
    'preselection' : OrderedDict(
        [
            # Veto electrons that are very close to muons
            ('e', {
                    'm' : {
                        'deltaR' : 0.05,
                        'selection' : 'userFloat("HZZ4lIDPassTight") > 0.5',
                        },
                    },
             ),
            # Remove jets that are near tight ID'd, no-FSR isolated leptons
            ('j', {
                    'selection' : 'pt > 30 && eta < 4.7 && eta > -4.7 && userFloat("puID") > 0.5',
                    'e' : {
                        'deltaR' : 0.4,
                        'selection' : 'userFloat("HZZ4lIDPassTight") > 0.5 && userFloat("HZZ4lIsoPass") > 0.5',
                        },
                    'm' : {
                        'deltaR' : 0.4,
                        'selection' : 'userFloat("HZZ4lIDPassTight") > 0.5 && userFloat("HZZ4lIsoPass") > 0.5',
                        },
                    }
             )
            ]),
            
    # selections to include object in final state (should be looser than analysis selections)
    'finalSelection' : OrderedDict(
        [
            ('e', 'abs(superCluster().eta) < 3.0 && max(pt, userFloat("maxCorPt")) > 7'),
            ('m', 'max(pt, userFloat("maxCorPt")) > 4 && (isGlobalMuon || isTrackerMuon)'),
            ]
        ),
    
    # Don't automaticaly cross clean among FS objects
    'crossCleaning' : '',

    # additional variables for ntuple
    'eventVariables' : PSet(
        muVeto = 'vetoMuons(0.4, "isLooseMuon & pt > 10 & abs(eta) < 2.4").size()',
        muVetoIso = 'vetoMuons(0.4, "isLooseMuon & pt > 10 & abs(eta) < 2.4 & (chargedHadronIso()+max(0.0,neutralHadronIso()+photonIso()-userFloat(\'rhoCSA14\')*userFloat(\'EffectiveArea_HZZ4l2015\')))/pt()<0.2").size()',
        eVeto = 'vetoElectrons(0.4, "userFloat(\'CBIDLoose\')>0.5 & pt > 10 & abs(eta) < 2.5").size()',
        eVetoIso = 'vetoElectrons(0.4, "userFloat(\'CBIDLoose\')>0.5 & pt > 10 & abs(eta) < 2.5 & (chargedHadronIso()+max(0.0,neutralHadronIso()+photonIso()-userFloat(\'rhoCSA14\')*userFloat(\'EffectiveArea_HZZ4l2015\')))/pt() < 0.2").size()',
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
