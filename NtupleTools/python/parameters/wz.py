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
            'selection' : 'pt>20 && abs(eta)<4.7 && userFloat("idLoose") > 0.5',
            'e': {
                'selection' : 'pt>10 && userInt("CBIDMedium")>0.5 && abs(eta)<2.5',
                'deltaR' : 0.3,
                },
            'm': {
                'selection' : 'pt>10 && userInt("tightID") > 0.5 && abs(eta)<2.4 && (chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()<0.12',
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
        muVetoTrigIso = 'vetoMuons(0.02, "isLooseMuon && pt > 10 && abs(eta) < 2.4 && trackIso()/pt()<0.4").size()',
        muVetoMedium = 'vetoMuons(0.02, "isMediumMuon && pt > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.2").size()',
        muVetoMediumNoIso = 'vetoMuons(0.02, "isMediumMuon && pt > 10 && abs(eta) < 2.4").size()',
        muVetoMediumTrigIso = 'vetoMuons(0.02, "isMediumMuon && pt > 10 && abs(eta) < 2.4 && trackIso()/pt()<0.4").size()',
        muVetoTight = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.12").size()',
        muVetoTightNoIso = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4").size()',
        muVetoTightTrigIso = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4 && trackIso()/pt()<0.4").size()',
        eVeto = 'vetoElectrons(0.02, "userFloat(\'CBIDLoose\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoNoIso = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTrigIso = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5 && dr03TkSumPt()/pt()<0.2 && dr03EcalRecHitSumEt()/pt()<0.5 && dr03HcalTowerSumEt()/pt()<0.3").size()',
        eVetoTight = 'vetoElectrons(0.02, "userFloat(\'CBIDMedium\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTightNoIso = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTightTrigIso = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5 && dr03TkSumPt()/pt()<0.2 && dr03EcalRecHitSumEt()/pt()<0.5 && dr03HcalTowerSumEt()/pt()<0.3").size()',
        muVetoHZZ = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        muVetoHZZIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        muVetoHZZTight = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        muVetoHZZTightIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoHZZ = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        eVetoHZZIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoHZZTight = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        eVetoHZZTightIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',

        GenDecayWENu='evt.findDecay(24,11)',
        GenDecayWMuNu='evt.findDecay(24,13)',
        GenDecayWTauNu='evt.findDecay(24,15)',
        GenDecayZEE='evt.findDecay(23,11)',
        GenDecayZMuMu='evt.findDecay(23,13)',
        GenDecayZTauTau='evt.findDecay(23,15)',
    ),
    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : PSet(),
    'electronVariables' : PSet(
        objectPassWZLoose = '? ({object}.userFloat("CBIDLoose")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseNoIso = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseTrigIso = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.pt<0.2 && {object}.dr03EcalRecHitSumEt/{object}.pt<0.5 && {object}.dr03HcalTowerSumEt/{object}.pt<0.3) ? 1 : 0',
        objectPassWZTight = '? ({object}.userFloat("CBIDMedium")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightNoIso = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightTrigIso = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.pt<0.2 && {object}.dr03EcalRecHitSumEt/{object}.pt<0.5 && {object}.dr03HcalTowerSumEt/{object}.pt<0.3) ? 1 : 0',
    ),
    'muonVariables' : PSet(
        objectPassWZLoose = '? ({object}.isLooseMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.2) ? 1 : 0',
        objectPassWZLooseNoIso = '? ({object}.isLooseMuon && {object}.pt > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZLooseTrigIso = '? ({object}.isLooseMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4) ? 1 : 0',
        objectPassWZMedium = '? ({object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.2) ? 1 : 0',
        objectPassWZMediumNoIso = '? ({object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZMediumTrigIso = '? ({object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4) ? 1 : 0',
        objectPassWZTight = '? ({object}.userInt("tightID") > 0.5  && {object}.pt > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.12) ? 1 : 0',
        objectPassWZTightNoIso = '? ({object}.userInt("tightID") > 0.5  && {object}.pt > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZTightTrigIso = '? ({object}.userInt("tightID") > 0.5  && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4) ? 1 : 0',
    ),
    'tauVariables' : PSet(),
    'photonVariables' : PSet(),
    'jetVariables' : PSet(),
    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(),
}
