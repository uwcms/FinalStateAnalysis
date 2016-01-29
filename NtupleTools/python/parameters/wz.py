# Default parameters to be used in production of ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

from FinalStateAnalysis.Utilities.cfgtools import PSet


wzLooseE = '{object}.userFloat(\'WWLoose\')>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5'
wzMediumE = '{object}.userFloat(\'WWLoose\')>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.userFloat(\'CBIDMedium\')>0.5'
wzTightE = '{object}.userFloat(\'WWLoose\')>0.5 && {object}.pt > 10 && abs({object}.eta) < 2.5 && {object}.userFloat(\'CBIDTight\')>0.5'

wzLooseM = '{object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4 && ({object}.pfIsolationR04().sumChargedHadronPt+max(0.,{object}.pfIsolationR04().sumNeutralHadronEt+{object}.pfIsolationR04().sumPhotonEt-0.5*{object}.pfIsolationR04().sumPUPt))/{object}.pt<0.4'
wzMediumM = '{object}.isMediumMuon && {object}.pt > 10 && abs({object}.eta) < 2.4 && {object}.trackIso/{object}.pt<0.4 && {object}.userFloat(\'ipDXY\')<0.02 && {object}.userFloat(\'dz\')<0.1 && ({object}.pfIsolationR04().sumChargedHadronPt+max(0.,{object}.pfIsolationR04().sumNeutralHadronEt+{object}.pfIsolationR04().sumPhotonEt-0.5*{object}.pfIsolationR04().sumPUPt))/{object}.pt<0.15'

wzLooseE_eesUp    = wzLooseE.replace('pt','userFloat(\'eesUpElectronsPt\')')
wzLooseE_eesDown  = wzLooseE.replace('pt','userFloat(\'eesDownElectronsPt\')')
wzMediumE_eesUp   = wzMediumE.replace('pt','userFloat(\'eesUpElectronsPt\')')
wzMediumE_eesDown = wzMediumE.replace('pt','userFloat(\'eesDownElectronsPt\')')
wzTightE_eesUp    = wzTightE.replace('pt','userFloat(\'eesUpElectronsPt\')')
wzTightE_eesDown  = wzTightE.replace('pt','userFloat(\'eesDownElectronsPt\')')

wzLooseM_mesUp    = wzLooseM.replace('pt','userFloat(\'mesUpMuonsPt\')')
wzLooseM_mesDown  = wzLooseM.replace('pt','userFloat(\'mesDownMuonsPt\')')
wzMediumM_mesUp   = wzMediumM.replace('pt','userFloat(\'mesUpMuonsPt\')')
wzMediumM_mesDown = wzMediumM.replace('pt','userFloat(\'mesDownMuonsPt\')')

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
                'selection' : wzMediumE.replace('{object}.',''),
                'deltaR' : 0.3,
                },
            'm': {
                'selection' : wzMediumM.replace('{object}.',''),
                'deltaR' : 0.3,
                },
            },
        },

    # selections to include object in final state (should be looser than analysis selections)
    'finalSelection' : {
        'e': 'abs(superCluster().eta) < 3.0 && pt > 7',
        'm': 'pt > 4 && (isGlobalMuon | isTrackerMuon)',
        't': 'abs(eta) < 2.5 && pt > 17 && tauID("decayModeFinding")',
        'g': 'abs(superCluster().eta()) < 3.0 && pt > 10',
        #'j': 'pt>20 && abs(eta) < 2.5 && userFloat("idLoose")'
        'j' : {
            'selection' : 'pt>20 && abs(eta)<4.7 && userFloat("idLoose") > 0.5',
            'e': {
                'selection' : 'pt>10 && userFloat("CBIDMedium")>0.5 && abs(eta)<2.5',
                'deltaR' : 0.3,
                },
            'm': {
                'selection' : 'pt>10 && userInt("tightID") > 0.5 && abs(eta)<2.4 && (chargedHadronIso()+max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()<0.12',
                'deltaR' : 0.3,
                },
            },

    },
    # cross cleaning for objects in final state
    'crossCleaning' : '',
    # additional variables for ntuple
    'eventVariables' : PSet(
        # muon vetos
        muVetoLoose = 'vetoMuons(0.02, "{0}").size()'.format(wzLooseM.replace('{object}.','')),
        muVetoMedium = 'vetoMuons(0.02, "{0}").size()'.format(wzMediumM.replace('{object}.','')),

        # mes up
        muVetoLoose_mesUp = 'vetoMuons(0.02, "{0}").size()'.format(wzLooseM_mesUp.replace('{object}.','')),
        muVetoMedium_mesUp = 'vetoMuons(0.02, "{0}").size()'.format(wzMediumM_mesUp.replace('{object}.','')),

        # mes down
        muVetoLoose_mesDown = 'vetoMuons(0.02, "{0}").size()'.format(wzLooseM_mesDown.replace('{object}.','')),
        muVetoMedium_mesDown = 'vetoMuons(0.02, "{0}").size()'.format(wzMediumM_mesDown.replace('{object}.','')),

        # electron vetos
        eVetoLoose = 'vetoElectrons(0.02, "{0}").size()'.format(wzLooseE.replace('{object}.','')),
        eVetoMedium = 'vetoElectrons(0.02, "{0}").size()'.format(wzMediumE.replace('{object}.','')),
        eVetoTight = 'vetoElectrons(0.02, "{0}").size()'.format(wzTightE.replace('{object}.','')),

        # ees up
        eVetoLoose_eesUp = 'vetoElectrons(0.02, "{0}").size()'.format(wzLooseE_eesUp.replace('{object}.','')),
        eVetoMedium_eesUp = 'vetoElectrons(0.02, "{0}").size()'.format(wzMediumE_eesUp.replace('{object}.','')),
        eVetoTight_eesUp = 'vetoElectrons(0.02, "{0}").size()'.format(wzTightE_eesUp.replace('{object}.','')),

        # ees down
        eVetoLoose_eesDown = 'vetoElectrons(0.02, "{0}").size()'.format(wzLooseE_eesDown.replace('{object}.','')),
        eVetoMedium_eesDown = 'vetoElectrons(0.02, "{0}").size()'.format(wzMediumE_eesDown.replace('{object}.','')),
        eVetoTight_eesDown = 'vetoElectrons(0.02, "{0}").size()'.format(wzTightE_eesDown.replace('{object}.','')),

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
        objectPassWZLoose = '? ({0}) ? 1 : 0'.format(wzLooseE),
        objectPassWZMedium = '? ({0}) ? 1 : 0'.format(wzMediumE),
        objectPassWZTight = '? ({0}) ? 1 : 0'.format(wzTightE),

        # ees up
        objectPassWZLoose_eesUp = '? ({0}) ? 1 : 0'.format(wzLooseE_eesUp),
        objectPassWZMedium_eesUp = '? ({0}) ? 1 : 0'.format(wzMediumE_eesUp),
        objectPassWZTight_eesUp = '? ({0}) ? 1 : 0'.format(wzTightE_eesUp),

        # ees down
        objectPassWZLoose_eesDown = '? ({0}) ? 1 : 0'.format(wzLooseE_eesDown),
        objectPassWZMedium_eesDown = '? ({0}) ? 1 : 0'.format(wzMediumE_eesDown),
        objectPassWZTight_eesDown = '? ({0}) ? 1 : 0'.format(wzTightE_eesDown),
    ),
    'muonVariables' : PSet(
        # default
        objectPassWZLoose = '? ({0}) ? 1 : 0'.format(wzLooseM),
        objectPassWZMedium = '? ({0}) ? 1 : 0'.format(wzMediumM),

        # mes up
        objectPassWZLoose_mesUp = '? ({0}) ? 1 : 0'.format(wzLooseM_mesUp),
        objectPassWZMedium_mesUp = '? ({0}) ? 1 : 0'.format(wzMediumM_mesUp),

        # mes down
        objectPassWZLoose_mesDown = '? ({0}) ? 1 : 0'.format(wzLooseM_mesDown),
        objectPassWZMedium_mesDown = '? ({0}) ? 1 : 0'.format(wzMediumM_mesDown),
    ),
    'tauVariables' : PSet(),
    'photonVariables' : PSet(),
    'jetVariables' : PSet(),
    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : PSet(),
}
