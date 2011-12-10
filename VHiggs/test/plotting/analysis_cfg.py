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
                        'vars' : ['ETauMass'],
                    }
                },
                'object1' : {
                    'pass' : [
                        'Elec_EID_MITID > 0.5',
                        'Elec_ERelIso < 0.3',
                    ],
                    'fail' : ['(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)'],
                    'ewk_fr' : get_fr('eMIT', 'Elec_JetPt'),
                    'qcd_fr' : get_fr('eMITQCD', 'Elec_JetPt'),
                },
                'object2' : {
                    'pass' : [
                        'Mu_MuRelIso < 0.3',
                        'Mu_MuID_WWID > 0.5',
                    ],
                    'fail' : ['(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'Mu_JetPt'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'Mu_JetPt'),
                },
                'object3' : {
                    'pass' : ['Tau_LooseHPS > 0.5'],
                    'fail' : ['Tau_LooseHPS < 0.5'],
                    'ewk_fr' : get_fr('tau', 'TauJetPt'),
                    'qcd_fr' : get_fr('tau', 'TauJetPt'), # FIXME
                },
            },
        },
    }
}













