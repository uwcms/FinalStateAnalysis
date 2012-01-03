import json

# Setup function which retrieves fake rate weights
fake_rates_file = open('fake_rates.json')
fake_rates_info = json.load(fake_rates_file)
def get_fr(label, variable):
    # Load the appropriate function from the json file and use the correct
    # dependent variable
    fake_rate_fun = fake_rates_info[label]['fitted_func']
    fake_rate_fun = fake_rate_fun.replace('VAR', variable)
    weight = '((%s)/(1-%s))' % (fake_rate_fun, fake_rate_fun)
    return weight

cfg = {
    'emt' : {
        'ntuple' : '/emt/final/Ntuple',
        'primds' : 'data_MuEG',
        'variables' : {
            'ETauMass' : ('Elec_Tau_Mass', 'M_{e#tau}', [60, 0, 300], 5),
            'EJetPt' : ('Elec_JetPt', 'p_{T}', [100, 0, 200], 5),
            'TauJetPt' : ('TauJetPt', 'p_{T}', [100, 0, 200], 5),
            'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NDF', [100, 0, 30], 5),
            'HT' : ('VisFinalState_Ht', 'L_{T}', [60, 0, 300], 4),
            'count' : ('1', 'Count', [1, 0, 1], 1),
        },
        'baseline' : [
            'MuPt > 18',
            'ElecPt > 10',
            'MuAbsEta < 2.1',
            'ElecAbsEta < 2.5',
            'Mu17Ele8All_HLT > 0.5',
            # Object vetos
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',

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
        ],
        'exclude' : ['*DoubleMu*', '*DoubleEl*'],
        'charge_categories' : {
            'emu' : {
                'cat_baseline' : ['ElecCharge*MuCharge > 0'],
                'cuts' : [],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        'vars' : ['ETauMass', 'EJetPt', 'HT', 'count'],
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
                        'Elec_EID_MITID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt'),
                },
                'object2' : {
                    'name' : '#mu',
                    'pass' : [
                        'Mu_MuRelIso < 0.3',
                        'Mu_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu_JetPt'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu_JetPt'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tau', 'TauJetPt'),
                    'qcd_fr' : get_fr('tau', 'TauJetPt'), # FIXME
                },
            },
            'mutau' : {
                'cat_baseline' : ['TauCharge*MuCharge > 0'],
                'cuts' : [],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        'vars' : ['ETauMass', 'EJetPt', 'TauJetPt', 'HT', 'count'],
                    }
                },
                'object1' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tau', 'TauJetPt'),
                    'qcd_fr' : get_fr('tau', 'TauJetPt'), # FIXME
                },
                'object2' : {
                    'name' : '#mu',
                    'pass' : [
                        'Mu_MuRelIso < 0.3',
                        'Mu_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu_JetPt'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu_JetPt'),
                },
                'object3' : {
                    'name' : 'e',
                    'pass' : [
                        'Elec_EID_MITID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt'),
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
            'Muon1AbsEta < 2.1',
            'Muon2AbsEta < 2.1',
            'DoubleMus_HLT > 0.5 ',

            # Object vetos
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',

            'Muon2_InnerNPixHits > 0.5',
            'Muon1_InnerNPixHits > 0.5',
            'Muon2_MuBtag < 3.3',
            'Muon1_MuBtag < 3.3',

            'Muon1DZ < 0.2',
            'Muon2DZ < 0.2',
            'TauDZ < 0.2',
        ],
        'exclude' : ['*MuEG*', '*DoubleEl*'],
        'charge_categories' : {
            'mumu' : {
                'cat_baseline' : ['Muon1Charge*Muon2Charge > 0'],
                'cuts' : [],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        'vars' : ['MuTauMass', 'HT', 'count'],
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
                    'ewk_fr' : get_fr('mu', 'Muon2_JetPt'),
                    'qcd_fr' : get_fr('muQCD', 'Muon2_JetPt'),
                },
                'object2' : {
                    'name' : '#mu_{1}',
                    'pass' : [
                        'Muon1_MuRelIso < 0.3',
                        'Muon1_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Muon1_MuID_WWID < 0.5 || Muon1_MuRelIso > 0.3)'],
                    'ewk_fr' : get_fr('muHighPt', 'Muon1_JetPt'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Muon1_JetPt'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tau', 'TauJetPt'),
                    'qcd_fr' : get_fr('tau', 'TauJetPt'), # FIXME
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
            'Mu1Pt > 18',
            'Mu2Pt > 9',
            'Mu1AbsEta < 2.1',
            'Mu2AbsEta < 2.1',
            'DoubleMus_HLT > 0.5 ',

            # Object vetos
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',

            'ElecPt > 10',
            'Mu2_InnerNPixHits > 0.5',
            'Mu1DZ < 0.2',
            'Mu2DZ < 0.2',
            'ElecDZ < 0.2',
        ],
        'exclude' : ['*MuEG*', '*DoubleEl*'],
        'charge_categories' : {
            'mumu' : {
                'cat_baseline' : ['Mu1Charge*Mu2Charge > 0'],
                'cuts' : [],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'VisFinalState_Ht > 80',
                            'vtxChi2/vtxNDOF < 10',
                        ],
                        'vars' : ['MuElecMass', 'HT', 'count'],
                    }
                },
                'object1' : {
                    'name' : '#mu_{2}',
                    'pass' : [
                        'Mu2_MuRelIso < 0.1',
                        'Mu2_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu2_MuID_WWID < 0.5 || Mu2_MuRelIso > 0.1)'],
                    'ewk_fr' : get_fr('muTight', 'Mu2_JetPt'),
                    'qcd_fr' : get_fr('muQCDTight', 'Mu2_JetPt'),
                },
                'object2' : {
                    'name' : '#mu_{1}',
                    'pass' : [
                        'Mu1_MuRelIso < 0.3',
                        'Mu1_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu1_MuID_WWID < 0.5 || Mu1_MuRelIso > 0.3)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu1_JetPt'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu1_JetPt'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : [
                        'Elec_EID_WWID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt'),
                },
            },
        },
    },
}













