
import FinalStateAnalysis.PatTools.data as data_tool
from tabulartext import PrettyTable
import copy
import math

skips = ['data', 'EM']
int_lumi = 4600
samples, plotter = data_tool.build_data(
    'VH', '2011-12-05-v1-WHAnalyze', 'scratch_results',
    int_lumi, skips, count='emt/skimCounter')

to_check = [
    'VH120', 'WZ', 'ZZ', 'Wjets', 'Zjets', 'ttjets', 'WW', 'VGamma',
]

signal = [
    'VH120'
]

fakes = [
    'Wjets', 'Zjets', 'ttjets', 'WW', 'VGamma',
]

irred = [
    'WZ', 'ZZ',
]

def get_yields(cuts=None, ntuple=None):
    histo_name = str(hash(tuple(cuts)))
    plotter.register_tree(
        histo_name,
        ntuple,
        '1',
        ' && '.join(cuts),
        w = '(pu2011AB)',
        binning = [1, -0.5, 2.5],
        include = ['*'],
    )
    output = {}
    for sample in to_check:
        histo = plotter.get_histogram(sample, ntuple + ':' + histo_name)
        output[sample] = histo.Integral()
    return output

channels = {
    'mtt' : {
        'ntuple' : '/mtt/final/Ntuple',
        'cuts' : [
            'MuPt > 30',
            'Tau1Pt > 20',
            'Tau2Pt > 20',
            'MuAbsEta < 2.1',
            'Tau1AbsEta < 2.5',
            'Tau2AbsEta < 2.5',
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'Mu_InnerNPixHits > 0.5',
            'Tau1Charge*Tau2Charge < 0',
            'Mu_MuBtag < 3.3',
            'MuDZ < 0.2',
            'Tau1DZ < 0.2',
            'Tau2DZ < 0.2',
            'Tau1_MediumHPS > 0.5',
            'Tau2_MediumHPS > 0.5',
            'Mu_MuID_WWID > 0.5',
            'Mu_MuRelIso < 0.3',
            'VisFinalState_Ht > 80',
            'vtxChi2/vtxNDOF < 10'
            #'METPt > 20',
        ],
    },
    'eet' : {
        'ntuple' : '/eet/final/Ntuple',
        'cuts' : [
            'Elec1Pt > 20',
            'Elec2Pt > 10',
            'TauPt > 20',
            'TauAbsEta < 2.5',
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'Elec1Charge*Elec2Charge > 0',
            'TauDZ < 0.2',
            'Elec1_EBtag < 3.3',
            'Elec1_MissingHits < 0.5',
            'Elec1_hasConversion < 0.5',
            'Elec2_EBtag < 3.3',
            'Elec2_MissingHits < 0.5',
            'Elec2_hasConversion < 0.5',
            'Elec1_EID_MITID > 0.5',
            'Elec1_ERelIso < 0.1',
            'Elec2_EID_MITID > 0.5',
            'Elec2_ERelIso < 0.1',
            'Tau_MediumHPS > 0.5',
            'VisFinalState_Ht > 80',
            'vtxChi2/vtxNDOF < 10',
            #'METPt > 40',
            'Tau_ElectronMVA > 0.5',
        ],
    },
    'eem' : {
        'ntuple' : '/eem/final/Ntuple',
        'cuts' : [
            'MuPt > 20',
            'Elec1Pt > 10',
            'Elec2Pt > 10',
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'Elec1Charge*Elec2Charge > 0',
            'Elec1_EBtag < 3.3',
            'Elec1_MissingHits < 0.5',
            'Elec1_hasConversion < 0.5',
            'Elec2_EBtag < 3.3',
            'Elec2_MissingHits < 0.5',
            'Elec2_hasConversion < 0.5',
            'Elec1_EID_MITID > 0.5',
            'Elec1_ERelIso < 0.15',
            'Elec2_EID_MITID > 0.5',
            'Elec2_ERelIso < 0.15',
            'VisFinalState_Ht > 80',
            'vtxChi2/vtxNDOF < 10',
            'Mu_MuBtag < 3.3',
            'MuDZ < 0.2',
            'Mu_MuID_WWID > 0.5',
            'Mu_MuRelIso < 0.3',
        ],
    },
    'emm' : {
        'ntuple' : '/emm/final/Ntuple',
        'cuts' : [
            'Mu1Pt > 18',
            'Mu2Pt > 9',
            'Mu1AbsEta < 2.1',
            'Mu2AbsEta < 2.1',
            'Mu1_MuRelIso < 0.1',
            'Mu1_MuID_WWID > 0.5',
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'Elec_EID_WWID > 0.5',
            'Elec_ERelIso < 0.3',
            'ElecPt > 10',
            'Mu1Charge*Mu2Charge > 0',
            'Mu2_InnerNPixHits > 0.5',
            'Mu1DZ < 0.2',
            'Mu2DZ < 0.2',
            'ElecDZ < 0.2',
            'VisFinalState_Ht > 80',
            'vtxChi2/vtxNDOF < 10',
            'Mu2_MuBtag < 3.3',
            'Mu1_MuBtag < 3.3',
            'Mu2_MuRelIso < 0.1',
            'Mu2_MuID_WWID > 0.5',
        ]
    },
    'mmt' : {
        'ntuple' : '/mmt/final/Ntuple',
        'cuts' : [
            'Muon1Pt > 18',
            'Muon2Pt > 9',
            'Muon1AbsEta < 2.1',
            'Muon2AbsEta < 2.1',
            'NIsoMuonsPt5_Nmuons < 0.5',
            'NIsoElecPt10_Nelectrons < 0.5',
            'NBjetsPt20_Nbjets < 0.5',
            'Muon1Charge*Muon2Charge > 0',
            'Muon2_InnerNPixHits > 0.5',
            'Muon1_InnerNPixHits > 0.5',
            'Muon1DZ < 0.2',
            'Muon2DZ < 0.2',
            'TauDZ < 0.2',
            'Tau_LooseHPS > 0.5',
            'VisFinalState_Ht > 80',
            'vtxChi2/vtxNDOF < 10',
            'Muon2_MuBtag < 3.3',
            'Muon1_MuBtag < 3.3',
            'Muon2_MuID_WWID > 0.5',
            'Muon2_MuRelIso < 0.3',
            'Muon1_MuRelIso < 0.3',
            'Muon1_MuID_WWID > 0.5',
        ],
    },
    'emt' : {
        'ntuple' : '/emt/final/Ntuple',
        'cuts' : [
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

            #'MuCharge*ElecCharge > 0',
            'Mu_MuBtag < 3.3',

            'MuDZ < 0.2',
            'ElecDZ < 0.2',
            'TauDZ < 0.2',
            'Tau_TauBtag < 3.3',
            'VisFinalState_Ht > 80',
            'vtxChi2/vtxNDOF < 10',
            'Elec_EID_MITID > 0.5',
            'Elec_ERelIso < 0.3',
            'Mu_MuRelIso < 0.3',
            'Mu_MuID_WWID > 0.5',
            'Tau_LooseHPS > 0.5',
            'ElecCharge*MuCharge > 0',
        ],
    }
}

channels['mtt_met30'] = copy.deepcopy(channels['mtt'])
channels['mtt_met30']['cuts'].append('METPt > 30')

channels['eet_met30'] = copy.deepcopy(channels['eet'])
channels['eet_met30']['cuts'].append('METPt > 30')

channels['mmt_met30'] = copy.deepcopy(channels['mmt'])
channels['mmt_met30']['cuts'].append('METPt > 30')

channels['emt_met30'] = copy.deepcopy(channels['emt'])
channels['emt_met30']['cuts'].append('METPt > 30')

results = {}

table = PrettyTable()
table.field_names = ['channel'] + signal + ['s/sqrt(s+b)'] + ['fakes'] + ['irred'] + fakes + irred

columns = signal + ['s/sqrt(s+b)', 'fakes', 'irred'] + fakes + irred

for channel in sorted(channels.keys()):
    channel_config = channels[channel]
    print "running", channel
    result = get_yields(**channel_config)
    result['fakes'] = sum(result[x] for x in fakes)
    result['irred'] = sum(result[x] for x in irred)
    result['s/sqrt(s+b)'] = result['VH120']/math.sqrt(result['VH120'] + result['fakes'] + result['irred'])

    table.add_row([channel] + ['%0.2f' % result[x] for x in columns])
print  table.get_string(hrules=True)

