import json

'''

Define top-level configuration for WH analysis.

'''

# Data source parameters
INT_LUMI = 4960
#JOBID = '2012-01-28-v1-WHAnalyze'
JOBID = '2012-04-14-v1-WHAnalyze'

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

#mass_binning = [0, 25, 50, 75, 100, 140, 180]
mass_binning = [0, 25, 50, 75, 100, 125, 150, 175]
pt_binning = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#mass_binning = 5

cfg = {
    'emt' : {
        'ntuple' : '/emt/final/Ntuple',
        'primds' : 'data_mEG',
        'variables' : {
            'ETauMass' : ('e_t_Mass', 'M_{e#tau} (GeV)', [60, 0, 300],
                          mass_binning),
            'MuTauMass' : ('m_t_Mass', 'M_{#mu#tau} (GeV)', [60, 0, 300],
                           mass_binning),
            'SubleadingMass' : (
                '((ePt < mPt)*e_t_Mass + (ePt > mPt)*m_t_Mass)',
                'M_{l2 #tau} (GeV)', [60, 0, 300], mass_binning),

            'EJetPt' : ('eJetPt', 'p_{T}', [200, 0, 200], 1),
            'mJetPt' : ('mJetPt', 'p_{T}', [200, 0, 200], 1),
            'mPt' : ('mPt', 'p_{T}', [100, 0, 200], pt_binning),
            'ePt' : ('ePt', 'p_{T}', [100, 0, 200], pt_binning),
            'tPt' : ('tPt', 'p_{T}', [100, 0, 200], pt_binning),
            'tJetPt' : ('tJetPt', 'p_{T}', [100, 0, 200], 5),
            'tLeadTrkPt' : ('tLeadTrkPt', 'p_{T}', [100, 0, 50], 5),
            'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NDF', [100, 0, 30], 5),
            'HT' : ('LT', 'L_{T} (GeV)', [60, 0, 300], 4),
            'count' : ('1', 'Count', [1, 0, 1], 1),
        },
        # The common cuts
        'baseline' : [
            'mPt > 20',
            'ePt > 10',
            'tPt > 20',
            'mu17ele8Pass > 0.5',
            'tAbsEta < 2.3',
            'eMuOverlap < 0.5',
            # Object vetos
            'muVetoPt5 < 0.5',
            # fixme
            #'NIsoePt10_Nelectrons < 0.5',
            'bjetCSVVeto < 0.5',
            'tauVetoPt20 < 0.5',
            'mAbsEta < 2.1',
            'eAbsEta < 2.5',

            'mPixHits > 0.5',
            'eJetBtag < 3.3',
            'eMissingHits < 0.5',
            'eHasConversion < 0.5',

            'mJetBtag < 3.3',

            'abs(mDZ) < 0.2',
            'abs(eDZ) < 0.2',
            'abs(tDZ) < 0.2',
            'tJetBtag < 3.3',
            'tAntiElectronMVA > 0.5',
            'tMuOverlap < 0.5',
            # FIXME
            #'t_etronOverlap < 0.5',
        ],
        'corrections' : [
            'mIso(mPt, mAbsEta, run)',
            'mID(mPt, mAbsEta, run)',
            'mHLT8(mPt, mAbsEta, run)',
            'EleIso(ePt, eAbsEta, run)',
            'EleID(ePt, eAbsEta, run)',
            'mEGTrig(ePt, eAbsEta, run)',
        ],
        # Samples not applicable to this analysis
        'exclude' : ['*Doublem*', '*DoubleEl*'],
        # Different sub-categories w/ their charge requirements
        'charge_categories' : {
            'emu' : {
                'cat_baseline' : ['eCharge*mCharge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'LT > 80',
                        ],
                        #'vars' : ['ETauMass', 'EJetPt', 'HT', 'count', 'mPt'],
                        #'vars' : ['count', 'TauLeadTrkPt', 'ETauMass', 'mTauMass', 'HT', ],
                        #'vars' : ['count', 'ETauMass', 'EJetPt', 'mJetPt'],
                        'vars' : ['count', 'SubleadingMass'],
                    },
                    'vtxonly' : {
                        'cuts' : [],
                        #'vars' : ['HT', 'mPt', 'ePt', 'TauPt', 'ETauMass'],
                        'vars' : ['HT', ],
                    },
                },
                'object1' : {
                    'name' : 'e',
                    'pass' : [
                        '('
                        '(eAbsEta < 1.479 &&  abs(e_EID_DeltaEta) < 0.007 && abs(e_EID_DeltaPhi) < 0.15 && e_EID_HOverE < 0.12 && e_EID_SigmaIEta < 0.01)'
                        ' || '
                        '(eAbsEta >= 1.479 &&  abs(e_EID_DeltaEta) < 0.009 && abs(e_EID_DeltaPhi) < 0.10 && e_EID_HOverE < 0.10 && e_EID_SigmaIEta < 0.03)'
                        ')',
                        'e_EID_MITID > 0.5',
                        'e_ERelIso < 0.3',
                    ],
                    'fail' : [
                        '('
                        '(e_EID_MITID < 0.5 || e_ERelIso > 0.3)'
                        ' || '
                        '(eAbsEta < 1.479 &&  (abs(e_EID_DeltaEta) > 0.007 || abs(e_EID_DeltaPhi) > 0.15 || e_EID_HOverE > 0.12 || e_EID_SigmaIEta > 0.01) )'
                        ' || '
                        '(eAbsEta >= 1.479 &&  (abs(e_EID_DeltaEta) > 0.009 || abs(e_EID_DeltaPhi) > 0.10|| e_EID_HOverE > 0.10 || e_EID_SigmaIEta > 0.03 ))'
                        ')'
                    ],
                    'ewk_fr' : get_fr('eMIT', 'eJetPt', 'eAbsEta'),
                    'qcd_fr' : get_fr('eMITQCD', 'eJetPt', 'eAbsEta'),
                },
                'object2' : {
                    'name' : '#mu',
                    'pass' : [
                        'mPFRelIsoDB < 0.3',
                        'mPFIDTight > 0.5',
                    ],
                    'fail' : ['(mPFRelIsoDB > 0.3 || mPFIDTight < 0.5)'],
                    'ewk_fr' : get_fr('muHighPt', 'mJetPt', 'mAbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'mJetPt', 'mAbsEta'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : ['tLooseMVAIso > 0.5'],
                    'fail' : ['tLooseMVAIso < 0.5'],
                    #'ewk_fr' : get_fr('tau', 'TauJetPt', 'tAbsEta'),
                    #'qcd_fr' : get_fr('tau', 'tJetPt', 'tAbsEta'), # FIXME
                    'ewk_fr' : get_fr('tauTauPt', 'tPt', 'tAbsEta'),
                    'qcd_fr' : get_fr('tauTauPt', 'tPt', 'tAbsEta'), # FIXME
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
            'MuTauMass' : ('m2_t_Mass', 'M_{#mu_{2}#tau}', [60, 0, 300], mass_binning),
            'Mu1JetPt' : ('m1JetPt', "p_{T}", [200, 0, 200], 1),
            'Mu2JetPt' : ('m2JetPt', "p_{T}", [200, 0, 200], 1),
            #    'm2_MtToMET' : ('m2_MtToMET', 'M_{T} #mu(2)-#tau', [100, 0, 300],),
            'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NDF', [100, 0, 30], 5),
            #    'MET' : ('METPt', 'MET', [100, 0, 200]),
            'Njets' : ('NjetsPt20_Njets', 'N_{jets}', [10, -0.5, 9.5], 1),
            'HT' : ('LT', 'L_{T} (GeV)', [60, 0, 300], 4),
            'count' : ('1', 'Count', [1, 0, 1], 1),
            'm1Pt' : ('m1Pt', 'p_{T}', [100, 0, 200], pt_binning),
            'm2Pt' : ('m2Pt', 'p_{T}', [100, 0, 200], pt_binning),
            'TauPt' : ('tPt', 'p_{T}', [100, 0, 200], pt_binning),
        },
        'baseline' : [
            'm1Pt > 20',
            'm2Pt > 10',
            'tPt > 20',
            'm1AbsEta < 2.1',
            'm2AbsEta < 2.1',
            'tAbsEta < 2.3',
            'DoubleMus_HLT > 0.5 ',

            # Object vetos
            'muVetoPt5 < 0.5',
            # fixme
            #'NIsoElecPt10_Nelectrons < 0.5',
            'bjetCSVVeto < 0.5',
            'tauVetoPt20 < 0.5',

            'm2PixHits > 0.5',
            'm1PixHits > 0.5',
            'm2JetBtag < 3.3',
            'm1JetBtag < 3.3',

            'abs(m1DZ) < 0.2',
            'abs(m2DZ) < 0.2',
            'abs(tDZ) < 0.2',

            't_MuonOverlapSuperLoose < 0.5',
            't_ElectronOverlapWP95 < 0.5',
            'm1_m2_Mass > 20',
        ],
        'corrections' : [
            'MuIso(m1Pt, m1AbsEta, run)',
            'MuID(m1Pt, m1AbsEta, run)',
            'MuHLT8(m1Pt, m1AbsEta, run)',
            'MuIso(m2Pt, m2AbsEta, run)',
            'MuID(m2Pt, m2AbsEta, run)',
            'MuHLT8(m2Pt, m2AbsEta, run)',
        ],
        'exclude' : ['*MuEG*', '*DoubleEl*'],
        'charge_categories' : {
            'mumu' : {
                'cat_baseline' : ['m1Charge*m2Charge > 0'],
                'cuts' : [],
                'selection_order' : ['final', 'vtxonly'],
                'selections' : {
                    'final' : {
                        'cuts' : [
                            'LT > 80',
                        ],
                        #'vars' : ['count', 'MuTauMass', 'Mu2JetPt', 'Mu1JetPt'],
                        'vars' : ['count', 'MuTauMass', ],
                        #'vars' : ['count', 'MuTauMass', 'HT'],
                    },
                    'vtxonly' : {
                        'cuts' : [],
                        #'vars' : ['HT', 'TauPt', 'm1Pt', 'm2Pt', 'MuTauMass'],
                        'vars' : ['HT'],
                    },
                },
                'object1' : {
                    'name' : '#mu_{2}',
                    'pass' : [
                        'm2PFRelIsoDB < 0.3',
                        'm2PFIDTight > 0.5',
                    ],
                    'fail' : ['(m2PFIDTight < 0.5 || m2PFRelIsoDB > 0.3)'],
                    'ewk_fr' : get_fr('mu', 'm2JetPt', 'm2AbsEta'),
                    'qcd_fr' : get_fr('muQCD', 'm2JetPt', 'm2AbsEta'),
                },
                'object2' : {
                    'name' : '#mu_{1}',
                    'pass' : [
                        'm1PFRelIsoDB < 0.3',
                        'm1PFIDTight > 0.5',
                    ],
                    'fail' : ['(m1PFIDTight < 0.5 || m1PFRelIsoDB > 0.3)'],
                    'ewk_fr' : get_fr('muHighPt', 'm1JetPt', 'm1AbsEta'),
                    'qcd_fr' : get_fr('muHighPtQCDOnly', 'm1JetPt', 'm1AbsEta'),
                },
                'object3' : {
                    'name' : '#tau',
                    'pass' : ['tLooseMVAIso > 0.5'],
                    'fail' : ['tLooseMVAIso < 0.5'],
                    'ewk_fr' : get_fr('tauTauPt', 'tPt', 'tAbsEta'),
                    'qcd_fr' : get_fr('tauTauPt', 'tPt', 'tAbsEta'), # FIXME
                    #'ewk_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'),
                    #'qcd_fr' : get_fr('tau', 'TauJetPt', 'TauAbsEta'), # FIXME
                },
            },
        },
    },
}
