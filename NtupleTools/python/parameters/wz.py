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
                'selection' : 'isMediumMuon && pt > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/pt()<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.12',
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
        # muon vetos
        muVeto = 'vetoMuons(0.02, "isLooseMuon && pt > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.2").size()',
        muVetoNoIso = 'vetoMuons(0.02, "isLooseMuon && pt > 10 && abs(eta) < 2.4").size()',
        muVetoTrigIso = 'vetoMuons(0.02, "isLooseMuon && pt > 10 && abs(eta) < 2.4 && trackIso()/pt()<0.4").size()',
        muVetoMedium = 'vetoMuons(0.02, "isMediumMuon && pt > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/pt()<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.12").size()',
        muVetoMediumNoIso = 'vetoMuons(0.02, "isMediumMuon && pt > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1").size()',
        muVetoMediumTrigIso = 'vetoMuons(0.02, "isMediumMuon && pt > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/pt()<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.4").size()',
        muVetoTight = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt()<0.12").size()',
        muVetoTightNoIso = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4").size()',
        muVetoTightTrigIso = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && pt > 10 && abs(eta) < 2.4 && trackIso()/pt()<0.4").size()',

        # mes up
        muVeto_mesUp = 'vetoMuons(0.02, "isLooseMuon && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesUpMuonsPt\')<0.2").size()',
        muVetoNoIso_mesUp = 'vetoMuons(0.02, "isLooseMuon && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4").size()',
        muVetoTrigIso_mesUp = 'vetoMuons(0.02, "isLooseMuon && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && trackIso()/userFloat(\'mesUpMuonsPt\')<0.4").size()',
        muVetoMedium_mesUp = 'vetoMuons(0.02, "isMediumMuon && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/userFloat(\'mesUpMuonsPt\')<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesUpMuonsPt\')<0.12").size()',
        muVetoMediumNoIso_mesUp = 'vetoMuons(0.02, "isMediumMuon && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1").size()',
        muVetoMediumTrigIso_mesUp = 'vetoMuons(0.02, "isMediumMuon && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/userFloat(\'mesUpMuonsPt\')<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesUpMuonsPt\')<0.4").size()',
        muVetoTight_mesUp = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesUpMuonsPt\')<0.12").size()',
        muVetoTightNoIso_mesUp = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4").size()',
        muVetoTightTrigIso_mesUp = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && userFloat(\'mesUpMuonsPt\') > 10 && abs(eta) < 2.4 && trackIso()/userFloat(\'mesUpMuonsPt\')<0.4").size()',

        # mes down
        muVeto_mesDown = 'vetoMuons(0.02, "isLooseMuon && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesDownMuonsPt\')<0.2").size()',
        muVetoNoIso_mesDown = 'vetoMuons(0.02, "isLooseMuon && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4").size()',
        muVetoTrigIso_mesDown = 'vetoMuons(0.02, "isLooseMuon && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && trackIso()/userFloat(\'mesDownMuonsPt\')<0.4").size()',
        muVetoMedium_mesDown = 'vetoMuons(0.02, "isMediumMuon && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/userFloat(\'mesDownMuonsPt\')<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesDownMuonsPt\')<0.12").size()',
        muVetoMediumNoIso_mesDown = 'vetoMuons(0.02, "isMediumMuon && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1").size()',
        muVetoMediumTrigIso_mesDown = 'vetoMuons(0.02, "isMediumMuon && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && userFloat(\'ipDXY\')<0.02 && userFloat(\'dz\')<0.1 && trackIso()/userFloat(\'mesDownMuonsPt\')<0.25 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesDownMuonsPt\')<0.4").size()',
        muVetoTight_mesDown = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && (chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/userFloat(\'mesDownMuonsPt\')<0.12").size()',
        muVetoTightNoIso_mesDown = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4").size()',
        muVetoTightTrigIso_mesDown = 'vetoMuons(0.02, "userInt(\'tightID\') > 0.5  && userFloat(\'mesDownMuonsPt\') > 10 && abs(eta) < 2.4 && trackIso()/userFloat(\'mesDownMuonsPt\')<0.4").size()',

        # electron vetos
        eVeto = 'vetoElectrons(0.02, "userFloat(\'CBIDLoose\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoNoIso = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTrigIso = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5 && dr03TkSumPt()/pt()<0.2 && dr03EcalRecHitSumEt()/pt()<0.5 && dr03HcalTowerSumEt()/pt()<0.3").size()',
        eVetoMedium = 'vetoElectrons(0.02, "userFloat(\'CBIDMedium\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoMediumNoIso = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoMediumTrigIso = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5 && dr03TkSumPt()/pt()<0.2 && dr03EcalRecHitSumEt()/pt()<0.5 && dr03HcalTowerSumEt()/pt()<0.3").size()',
        eVetoTight = 'vetoElectrons(0.02, "userFloat(\'CBIDTight\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTightNoIso = 'vetoElectrons(0.02, "userFloat(\'CBIDTightNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5").size()',
        eVetoTightTrigIso = 'vetoElectrons(0.02, "userFloat(\'CBIDTightNoIso\')>0.5 && pt > 10 && abs(eta) < 2.5 && dr03TkSumPt()/pt()<0.2 && dr03EcalRecHitSumEt()/pt()<0.5 && dr03HcalTowerSumEt()/pt()<0.3").size()',

        # ees up
        eVeto_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDLoose\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoNoIso_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoTrigIso_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5 && dr03TkSumPt()/userFloat(\'eesUpElectronsPt\')<0.2 && dr03EcalRecHitSumEt()/userFloat(\'eesUpElectronsPt\')<0.5 && dr03HcalTowerSumEt()/userFloat(\'eesUpElectronsPt\')<0.3").size()',
        eVetoMedium_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDMedium\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoMediumNoIso_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoMediumTrigIso_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5 && dr03TkSumPt()/userFloat(\'eesUpElectronsPt\')<0.2 && dr03EcalRecHitSumEt()/userFloat(\'eesUpElectronsPt\')<0.5 && dr03HcalTowerSumEt()/userFloat(\'eesUpElectronsPt\')<0.3").size()',
        eVetoTight_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDTight\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoTightNoIso_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDTightNoIso\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoTightTrigIso_eesUp = 'vetoElectrons(0.02, "userFloat(\'CBIDTightNoIso\')>0.5 && userFloat(\'eesUpElectronsPt\') > 10 && abs(eta) < 2.5 && dr03TkSumPt()/userFloat(\'eesUpElectronsPt\')<0.2 && dr03EcalRecHitSumEt()/userFloat(\'eesUpElectronsPt\')<0.5 && dr03HcalTowerSumEt()/userFloat(\'eesUpElectronsPt\')<0.3").size()',

        # ees down
        eVeto_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDLoose\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoNoIso_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoTrigIso_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDLooseNoIso\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5 && dr03TkSumPt()/userFloat(\'eesDownElectronsPt\')<0.2 && dr03EcalRecHitSumEt()/userFloat(\'eesDownElectronsPt\')<0.5 && dr03HcalTowerSumEt()/userFloat(\'eesDownElectronsPt\')<0.3").size()',
        eVetoMedium_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDMedium\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoMediumNoIso_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoMediumTrigIso_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDMediumNoIso\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5 && dr03TkSumPt()/userFloat(\'eesDownElectronsPt\')<0.2 && dr03EcalRecHitSumEt()/userFloat(\'eesDownElectronsPt\')<0.5 && dr03HcalTowerSumEt()/userFloat(\'eesDownElectronsPt\')<0.3").size()',
        eVetoTight_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDTight\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoTightNoIso_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDTightNoIso\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5").size()',
        eVetoTightTrigIso_eesDown = 'vetoElectrons(0.02, "userFloat(\'CBIDTightNoIso\')>0.5 && userFloat(\'eesDownElectronsPt\') > 10 && abs(eta) < 2.5 && dr03TkSumPt()/userFloat(\'eesDownElectronsPt\')<0.2 && dr03EcalRecHitSumEt()/userFloat(\'eesDownElectronsPt\')<0.5 && dr03HcalTowerSumEt()/userFloat(\'eesDownElectronsPt\')<0.3").size()',

        # HZZ vetos
        muVetoHZZ = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        muVetoHZZIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        muVetoHZZTight = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        muVetoHZZTightIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoHZZ = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        eVetoHZZIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoHZZTight = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        eVetoHZZTightIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',

        # gen decays
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
        # default
        objectPassWZLoose = '? ({object}.userFloat("CBIDLoose")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseNoIso = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseTrigIso = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.pt<0.2 && {object}.dr03EcalRecHitSumEt/{object}.pt<0.5 && {object}.dr03HcalTowerSumEt/{object}.pt<0.3) ? 1 : 0',
        objectPassWZMedium = '? ({object}.userFloat("CBIDMedium")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZMediumNoIso = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZMediumTrigIso = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.pt<0.2 && {object}.dr03EcalRecHitSumEt/{object}.pt<0.5 && {object}.dr03HcalTowerSumEt/{object}.pt<0.3) ? 1 : 0',
        objectPassWZTight = '? ({object}.userFloat("CBIDTight")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightNoIso = '? ({object}.userFloat("CBIDTightNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightTrigIso = '? ({object}.userFloat("CBIDTightNoIso")>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.pt<0.2 && {object}.dr03EcalRecHitSumEt/{object}.pt<0.5 && {object}.dr03HcalTowerSumEt/{object}.pt<0.3) ? 1 : 0',

        # ees up
        objectPassWZLoose_eesUp = '? ({object}.userFloat("CBIDLoose")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseNoIso_eesUp = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseTrigIso_eesUp = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.userFloat(\'eesUpElectronsPt\')<0.2 && {object}.dr03EcalRecHitSumEt/{object}.userFloat(\'eesUpElectronsPt\')<0.5 && {object}.dr03HcalTowerSumEt/{object}.userFloat(\'eesUpElectronsPt\')<0.3) ? 1 : 0',
        objectPassWZMedium_eesUp = '? ({object}.userFloat("CBIDMedium")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZMediumNoIso_eesUp = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZMediumTrigIso_eesUp = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.userFloat(\'eesUpElectronsPt\')<0.2 && {object}.dr03EcalRecHitSumEt/{object}.userFloat(\'eesUpElectronsPt\')<0.5 && {object}.dr03HcalTowerSumEt/{object}.userFloat(\'eesUpElectronsPt\')<0.3) ? 1 : 0',
        objectPassWZTight_eesUp = '? ({object}.userFloat("CBIDTight")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightNoIso_eesUp = '? ({object}.userFloat("CBIDTightNoIso")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightTrigIso_eesUp = '? ({object}.userFloat("CBIDTightNoIso")>0.5 && {object}.userFloat(\'eesUpElectronsPt\') > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.userFloat(\'eesUpElectronsPt\')<0.2 && {object}.dr03EcalRecHitSumEt/{object}.userFloat(\'eesUpElectronsPt\')<0.5 && {object}.dr03HcalTowerSumEt/{object}.userFloat(\'eesUpElectronsPt\')<0.3) ? 1 : 0',

        # ees down
        objectPassWZLoose_eesDown = '? ({object}.userFloat("CBIDLoose")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseNoIso_eesDown = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZLooseTrigIso_eesDown = '? ({object}.userFloat("CBIDLooseNoIso")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.userFloat(\'eesDownElectronsPt\')<0.2 && {object}.dr03EcalRecHitSumEt/{object}.userFloat(\'eesDownElectronsPt\')<0.5 && {object}.dr03HcalTowerSumEt/{object}.userFloat(\'eesDownElectronsPt\')<0.3) ? 1 : 0',
        objectPassWZMedium_eesDown = '? ({object}.userFloat("CBIDMedium")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZMediumNoIso_eesDown = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZMediumTrigIso_eesDown = '? ({object}.userFloat("CBIDMediumNoIso")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.userFloat(\'eesDownElectronsPt\')<0.2 && {object}.dr03EcalRecHitSumEt/{object}.userFloat(\'eesDownElectronsPt\')<0.5 && {object}.dr03HcalTowerSumEt/{object}.userFloat(\'eesDownElectronsPt\')<0.3) ? 1 : 0',
        objectPassWZTight_eesDown = '? ({object}.userFloat("CBIDTight")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightNoIso_eesDown = '? ({object}.userFloat("CBIDTightNoIso")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5) ? 1 : 0',
        objectPassWZTightTrigIso_eesDown = '? ({object}.userFloat("CBIDTightNoIso")>0.5 && {object}.userFloat(\'eesDownElectronsPt\') > 10 && abs({object}.eta) < 2.5 && {object}.dr03TkSumPt/{object}.userFloat(\'eesDownElectronsPt\')<0.2 && {object}.dr03EcalRecHitSumEt/{object}.userFloat(\'eesDownElectronsPt\')<0.5 && {object}.dr03HcalTowerSumEt/{object}.userFloat(\'eesDownElectronsPt\')<0.3) ? 1 : 0',
    ),
    'muonVariables' : PSet(
        # default
        objectPassWZLoose = '? ({object}.isLooseMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.2) ? 1 : 0',
        objectPassWZLooseNoIso = '? ({object}.isLooseMuon && {object}.pt > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZLooseTrigIso = '? ({object}.isLooseMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4) ? 1 : 0',
        objectPassWZMedium = '? ({object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && {object}.trackIso/{object}.pt<0.25 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.12) ? 1 : 0',
        objectPassWZMediumNoIso = '? ({object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1) ? 1 : 0',
        objectPassWZMediumTrigIso = '? ({object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && {object}.trackIso/{object}.pt<0.25 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.4) ? 1 : 0',
        objectPassWZTight = '? ({object}.userInt("tightID") > 0.5  && {object}.pt > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.pt<0.12) ? 1 : 0',
        objectPassWZTightNoIso = '? ({object}.userInt("tightID") > 0.5  && {object}.pt > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZTightTrigIso = '? ({object}.userInt("tightID") > 0.5  && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4) ? 1 : 0',

        # mes up
        objectPassWZLoose_mesUp = '? ({object}.isLooseMuon && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesUpMuonsPt\')<0.2) ? 1 : 0',
        objectPassWZLooseNoIso_mesUp = '? ({object}.isLooseMuon && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZLooseTrigIso_mesUp = '? ({object}.isLooseMuon && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.userFloat(\'mesUpMuonsPt\')<0.4) ? 1 : 0',
        objectPassWZMedium_mesUp = '? ({object}.isMediumMuon && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesUpMuonsPt\')<0.12) ? 1 : 0',
        objectPassWZMediumNoIso_mesUp = '? ({object}.isMediumMuon && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1) ? 1 : 0',
        objectPassWZMediumTrigIso_mesUp = '? ({object}.isMediumMuon && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesUpMuonsPt\')<0.4) ? 1 : 0',
        objectPassWZTight_mesUp = '? ({object}.userInt("tightID") > 0.5  && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesUpMuonsPt\')<0.12) ? 1 : 0',
        objectPassWZTightNoIso_mesUp = '? ({object}.userInt("tightID") > 0.5  && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZTightTrigIso_mesUp = '? ({object}.userInt("tightID") > 0.5  && {object}.userFloat(\'mesUpMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.userFloat(\'mesUpMuonsPt\')<0.4) ? 1 : 0',

        # mes down
        objectPassWZLoose_mesDown = '? ({object}.isLooseMuon && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesDownMuonsPt\')<0.2) ? 1 : 0',
        objectPassWZLooseNoIso_mesDown = '? ({object}.isLooseMuon && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZLooseTrigIso_mesDown = '? ({object}.isLooseMuon && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.userFloat(\'mesDownMuonsPt\')<0.4) ? 1 : 0',
        objectPassWZMedium_mesDown = '? ({object}.isMediumMuon && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesDownMuonsPt\')<0.12) ? 1 : 0',
        objectPassWZMediumNoIso_mesDown = '? ({object}.isMediumMuon && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1) ? 1 : 0',
        objectPassWZMediumTrigIso_mesDown = '? ({object}.isMediumMuon && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesDownMuonsPt\')<0.4) ? 1 : 0',
        objectPassWZTight_mesDown = '? ({object}.userInt("tightID") > 0.5  && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && ({object}.chargedHadronIso+max({object}.photonIso+{object}.neutralHadronIso-0.5*{object}.puChargedHadronIso,0.0))/{object}.userFloat(\'mesDownMuonsPt\')<0.12) ? 1 : 0',
        objectPassWZTightNoIso_mesDown = '? ({object}.userInt("tightID") > 0.5  && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4) ? 1 : 0',
        objectPassWZTightTrigIso_mesDown = '? ({object}.userInt("tightID") > 0.5  && {object}.userFloat(\'mesDownMuonsPt\') > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.userFloat(\'mesDownMuonsPt\')<0.4) ? 1 : 0',
    ),
    'tauVariables' : PSet(),
    'photonVariables' : PSet(),
    'jetVariables' : PSet(),
    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(),
}
