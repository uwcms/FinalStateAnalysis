import json

'''

Define top-level configuration for WH analysis.

'''

# Data source parameters
INT_LUMI = 4684
#JOBID = '2012-01-28-v1-WHAnalyze'
JOBID = '2012-02-01-v1-WHAnalyze'

# Setup function which retrieves fake rate weights
fake_rates_file = open('fake_rates.json')
fake_rates_info = json.load(fake_rates_file)
def get_fr_old(label, pt, eta):
    # Note eta is unused, only for interface
    # Load the appropriate function from the json file and use the correct
    # dependent variable
    fake_rate_fun = fake_rates_info[label]['fitted_func']
    fake_rate_fun = fake_rate_fun.replace('VAR', pt)
    weight = '((%s)/(1-%s))' % (fake_rate_fun, fake_rate_fun)
    return weight

## New method where fake rates live in a macro file - see make_fakerates.py
## and fake_rates.C
def get_fr(label, pt, eta):
    return 'weight_%s(%s, %s)' % (label, pt, eta)

# List of channels to skip
skip = [ 'emm', ('emt', 'mutau'), ('emt', 'etau') ]

cfg = {
    'emt' : {
        'ntuple' : '/emt/final/Ntuple',
        'primds' : 'data_MuEG',
        'variables' : {
            'ETauMass' : ('Elec_Tau_Mass', 'M_{e#tau}', [60, 0, 300], 5),
            'MuTauMass' : ('Mu_Tau_Mass', 'M_{#mu#tau}', [60, 0, 300], 5),
            'EJetPt' : ('Elec_JetPt', 'p_{T}', [200, 0, 200], 1),
            'MuJetPt' : ('Mu_JetPt', 'p_{T}', [200, 0, 200], 1),
            'MuPt' : ('MuPt', 'p_{T}', [100, 0, 200], 5),
            'TauJetPt' : ('TauJetPt', 'p_{T}', [100, 0, 200], 5),
            'TauLeadTrkPt' : ('TauLeadTrkPt', 'p_{T}', [100, 0, 50], 5),
            'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NDF', [100, 0, 30], 5),
            'HT' : ('VisFinalState_Ht', 'L_{T}', [60, 0, 300], 4),
            'count' : ('1', 'Count', [1, 0, 1], 1),
        },
        # The common cuts
        'baseline' : [
            'MuPt > 18',
            'ElecPt > 10',
            'TauPt > 20',
            'Mu17Ele8All_HLT > 0.5',
            'Elec_MuonOverlap < 0.5',
            # Object vetos
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'NIsoTausPt20_NIsoTaus < 0.5',
            'MuAbsEta < 2.1',
            'ElecAbsEta < 2.5',

            'Mu_InnerNPixHits > 0.5',
            'Elec_EBtag < 3.3',
            'Elec_MissingHits < 0.5',
            'Elec_hasConversion < 0.5',

            'Mu_MuBtag < 3.3',

            'MuDZ < 0.2',
            'ElecDZ < 0.2',
            'TauDZ < 0.2',
            'Tau_TauBtag < 3.3',
            'Tau_ElectronMVA > 0.5',
            'Tau_ElectronMedium > 0.5',
            #'Tau_MuonOverlap < 0.5',
            'Tau_MuonOverlapSuperLoose < 0.5',
            'Tau_ElectronOverlap < 0.5',
            #'Tau_ElectronOverlapWWID < 0.5',
        ],
        'corrections' : [
            'MuIso(MuPt, MuAbsEta, run)',
            'MuID(MuPt, MuAbsEta, run)',
            'MuHLT8(MuPt, MuAbsEta, run)',
            'EleIso(ElecPt, ElecAbsEta, run)',
            'EleID(ElecPt, ElecAbsEta, run)',
            'MuEGTrig(ElecPt, ElecAbsEta, run)',
        ],
        # Samples not applicable to this analysis
        'exclude' : ['*DoubleMu*', '*DoubleEl*'],
        # Different sub-categories w/ their charge requirements
        'charge_categories' : {
            'emu' : {
                'cat_baseline' : ['ElecCharge*MuCharge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'htonly', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        #'vars' : ['ETauMass', 'EJetPt', 'HT', 'count', 'MuPt'],
                        #'vars' : ['count', 'TauLeadTrkPt', 'ETauMass', 'MuTauMass', 'HT', ],
                        'vars' : ['count', 'ETauMass', 'EJetPt', 'MuJetPt'],
                    },
                    'htonly' : {
                        'cuts' : [ 'VisFinalState_Ht > 80',],
                        'vars' : ['vtxChi2NODF'],
                    },
                    'vtxonly' : {
                        'cuts' : ['vtxChi2/vtxNDOF < 10'],
                        'vars' : ['HT'],
                    },
                },
                'object1' : {
                    'name' : 'e',
                    'pass' : [
                        '('
                        '(ElecAbsEta < 1.479 &&  abs(Elec_EID_DeltaEta) < 0.007 && abs(Elec_EID_DeltaPhi) < 0.15 && Elec_EID_HOverE < 0.12 && Elec_EID_SigmaIEta < 0.01)'
                        ' || '
                        '(ElecAbsEta >= 1.479 &&  abs(Elec_EID_DeltaEta) < 0.009 && abs(Elec_EID_DeltaPhi) < 0.10 && Elec_EID_HOverE < 0.10 && Elec_EID_SigmaIEta < 0.03)'
                        ')',
                        'Elec_EID_MITID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : [
                        '('
                        '(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'
                        ' || '
                        '(ElecAbsEta < 1.479 &&  (abs(Elec_EID_DeltaEta) > 0.007 || abs(Elec_EID_DeltaPhi) > 0.15 || Elec_EID_HOverE > 0.12 || Elec_EID_SigmaIEta > 0.01) )'
                        ' || '
                        '(ElecAbsEta >= 1.479 &&  (abs(Elec_EID_DeltaEta) > 0.009 || abs(Elec_EID_DeltaPhi) > 0.10|| Elec_EID_HOverE > 0.10 || Elec_EID_SigmaIEta > 0.03 ))'
                        ')'
                    ],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt', 'ElecAbsEta'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt', 'ElecAbsEta'),
                },
                'object2' : {
                    'name' : '#mu',
                    'pass' : [
                        'Mu_MuRelIso < 0.3',
                        'Mu_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu_JetPt', 'MuAbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu_JetPt', 'MuAbsEta'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    #'ewk_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'),
                    #'qcd_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'), # FIXME
                    'ewk_fr' : get_fr('tauTauPt', 'TauPt', 'TauAbsEta'),
                    'qcd_fr' : get_fr('tauTauPt', 'TauPt', 'TauAbsEta'), # FIXME
                },
            },
            'mutau' : {
                'cat_baseline' : ['TauCharge*MuCharge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'htonly', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        #'vars' : ['ETauMass', 'EJetPt', 'TauJetPt', 'HT', 'count'],
                        'vars' : ['ETauMass', 'count'],
                    }
                },
                'object1' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'),
                    'qcd_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'), # FIXME
                },
                'object2' : {
                    'name' : '#mu',
                    'pass' : [
                        'Mu_MuRelIso < 0.3',
                        'Mu_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu_JetPt', 'MuAbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu_JetPt', 'MuAbsEta'),
                },
                'object3' : {
                    'name' : 'e',
                    'pass' : [
                        'Elec_EID_MITID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt', 'ElecAbsEta'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt', 'ElecAbsEta'),
                },
            },
            'etau' : {
                'cat_baseline' : ['TauCharge*ElecCharge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'htonly', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        #'vars' : ['ETauMass', 'EJetPt', 'TauJetPt', 'HT', 'count'],
                        'vars' : ['ETauMass', 'count'],
                    }
                },
                'object1' : {
                    'name' : 'e',
                    'pass' : [
                        'Elec_EID_MITID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt', 'ElecAbsEta'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt', 'ElecAbsEta'),
                },
                'object2' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'),
                    'qcd_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'), # FIXME
                },
                'object3' : {
                    'name' : '#mu',
                    'pass' : [
                        'Mu_MuRelIso < 0.3',
                        'Mu_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu_JetPt', 'MuAbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu_JetPt', 'MuAbsEta'),
                },
            },

        },
    },
    ############################################################################
    ####   MMT channel   #######################################################
    ############################################################################
    'mmt' : {
        'ntuple' : '/mmt/final/Ntuple',
        'primds' : 'data_DoubleMu',
        'variables' : {
            'MuTauMass' : ('Muon2_Tau_Mass', 'M_{#mu#tau}', [60, 0, 300], 5),
            'Mu1JetPt' : ('Muon1_JetPt', "p_{T}", [200, 0, 200], 1),
            'Mu2JetPt' : ('Muon2_JetPt', "p_{T}", [200, 0, 200], 1),
            #    'Muon2_MtToMET' : ('Muon2_MtToMET', 'M_{T} #mu(2)-#tau', [100, 0, 300],),
            'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NDF', [100, 0, 30], 5),
            #    'MET' : ('METPt', 'MET', [100, 0, 200]),
            'Njets' : ('NjetsPt20_Njets', 'N_{jets}', [10, -0.5, 9.5], 1),
            'HT' : ('VisFinalState_Ht', 'L_{T}', [60, 0, 300], 4),
            'count' : ('1', 'Count', [1, 0, 1], 1),
        },
        'baseline' : [
            'Muon1Pt > 18',
            'Muon2Pt > 9',
            'TauPt > 20',
            'Muon1AbsEta < 2.1',
            'Muon2AbsEta < 2.1',
            'DoubleMus_HLT > 0.5 ',

            # Object vetos
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'NIsoTausPt20_NIsoTaus < 0.5',

            'Muon2_InnerNPixHits > 0.5',
            'Muon1_InnerNPixHits > 0.5',
            'Muon2_MuBtag < 3.3',
            'Muon1_MuBtag < 3.3',

            'Muon1DZ < 0.2',
            'Muon2DZ < 0.2',
            'TauDZ < 0.2',

            'Tau_MuonOverlapSuperLoose < 0.5',
            'Tau_ElectronOverlapWP95 < 0.5',
            'Muon1_Muon2_Mass > 20',
        ],
        'corrections' : [
            'MuIso(Muon1Pt, Muon1AbsEta, run)',
            'MuID(Muon1Pt, Muon1AbsEta, run)',
            'MuHLT8(Muon1Pt, Muon1AbsEta, run)',
            'MuIso(Muon2Pt, Muon2AbsEta, run)',
            'MuID(Muon2Pt, Muon2AbsEta, run)',
            'MuHLT8(Muon2Pt, Muon2AbsEta, run)',
        ],
        'exclude' : ['*MuEG*', '*DoubleEl*'],
        'charge_categories' : {
            'mumu' : {
                'cat_baseline' : ['Muon1Charge*Muon2Charge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'htonly', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        'vars' : ['count', 'MuTauMass', 'Mu2JetPt', 'Mu1JetPt'],
                        #'vars' : ['count', 'MuTauMass', 'HT'],
                    },
                    'htonly' : {
                        'cuts' : [ 'VisFinalState_Ht > 80',],
                        'vars' : ['vtxChi2NODF'],
                    },
                    'vtxonly' : {
                        'cuts' : ['vtxChi2/vtxNDOF < 10'],
                        'vars' : ['HT'],
                    },
                },
                'object1' : {
                    'name' : '#mu_{2}',
                    'pass' : [
                        'Muon2_MuRelIso < 0.3',
                        'Muon2_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Muon2_MuID_WWID < 0.5 || Muon2_MuRelIso > 0.3)'],
                    'ewk_fr' : get_fr('mu', 'Muon2_JetPt', 'Muon2AbsEta'),
                    'qcd_fr' : get_fr('muQCD', 'Muon2_JetPt', 'Muon2AbsEta'),
                },
                'object2' : {
                    'name' : '#mu_{1}',
                    'pass' : [
                        'Muon1_MuRelIso < 0.3',
                        'Muon1_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Muon1_MuID_WWID < 0.5 || Muon1_MuRelIso > 0.3)'],
                    'ewk_fr' : get_fr('muHighPt', 'Muon1_JetPt', 'Muon1AbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Muon1_JetPt', 'Muon1AbsEta'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tauTauPt', 'TauPt', 'TauAbsEta'),
                    'qcd_fr' : get_fr('tauTauPt', 'TauPt', 'TauAbsEta'), # FIXME
                    #'ewk_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'),
                    #'qcd_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'), # FIXME
                },
            },
        },
    },
    ############################################################################
    ####   EMM channel   #######################################################
    ############################################################################
    'emm' : {
        'ntuple' : '/emm/final/Ntuple',
        'primds' : 'data_DoubleMu',
        'variables' : {
            'MuElecMass' : ('Elec_Mu2_Mass', 'M_{e#mu}', [60, 0, 300], 5),
            'Mu1_MtToMET' : ('Mu1_MtToMET', 'M_{T} #mu(1)-#tau', [60, 0, 300], 5),
            'HT' : ('VisFinalState_Ht', 'L_{T}', [60, 0, 300], 4),
            'count' : ('1', 'Count', [1, 0, 1], 1),
        },
        'baseline' : [
            'Elec_MuonOverlap < 0.5',
            'Mu1Pt > 18',
            'Mu2Pt > 9',
            'Mu1AbsEta < 2.1',
            'Mu2AbsEta < 2.1',
            'DoubleMus_HLT > 0.5 ',

            # Object vetos
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'NIsoTausPt20_NIsoTaus < 0.5',

            'ElecPt > 10',
            'Mu2_InnerNPixHits > 0.5',
            'Mu1DZ < 0.2',
            'Mu2DZ < 0.2',
            'ElecDZ < 0.2',
        ],
        'corrections' : [
            'MuIso(Mu1Pt, Mu1AbsEta, run)',
            'MuID(Mu1Pt, Mu1AbsEta, run)',
            'MuHLT8(Mu1Pt, Mu1AbsEta, run)',
            'MuIso(Mu2Pt, Mu2AbsEta, run)',
            'MuID(Mu2Pt, Mu2AbsEta, run)',
            'MuHLT8(Mu2Pt, Mu2AbsEta, run)',
        ],
        'exclude' : ['*MuEG*', '*DoubleEl*'],
        'charge_categories' : {
            'mumu' : {
                'cat_baseline' : ['Mu1Charge*Mu2Charge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'htonly', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        'vars' : ['count', 'MuElecMass', 'HT',],
                    }
                },
                'object1' : {
                    'name' : '#mu_{2}',
                    'pass' : [
                        'Mu2_MuRelIso < 0.1',
                        'Mu2_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu2_MuID_WWID < 0.5 || Mu2_MuRelIso > 0.1)'],
                    'ewk_fr' : get_fr('muTight', 'Mu2_JetPt', 'Mu2AbsEta'),
                    'qcd_fr' : get_fr('muQCDTight', 'Mu2_JetPt', 'Mu2AbsEta'),
                },
                'object2' : {
                    'name' : '#mu_{1}',
                    'pass' : [
                        'Mu1_MuRelIso < 0.3',
                        'Mu1_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu1_MuID_WWID < 0.5 || Mu1_MuRelIso > 0.3)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu1_JetPt', 'Mu1AbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu1_JetPt', 'Mu1AbsEta'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : [
                        'Elec_EID_WWID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt', 'ElecAbsEta'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt', 'ElecAbsEta'),
                },
            },
        },
    },
}
