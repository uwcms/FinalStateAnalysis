'''

Measure jet->mu, jet->e, and jet->tau fake rates in trilepton event topologies.

'''

import ROOT
import os
import sys
import glob
import logging
import math
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles

# Logging options
logging.basicConfig(filename='fakeRates.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("plotting")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)
logging.getLogger("AnalysisPlotter").addHandler(h1)
h2 = logging.StreamHandler(sys.stderr)
h2.level = logging.DEBUG
logging.getLogger("ROOTCache").addHandler(h2)

ROOT.gROOT.SetBatch(True)
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

def saveplot(filename):
    # Save the current canvas
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'fakeRates', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'fakeRates', filename + '_log' + filetype))

from data import build_data
skips =['EM', '2011B_PromptReco_v1_b', '2011B']
samples, plotter = build_data('2011-10-25-WHReSkim', 'scratch_results',
                              2170, skips, count='emtFilter/skimCounter')


# Dimuon selection
base_dimuon_selection = [
    #'(run < 5 && Muon1Pt > 13.5 || Muon1Pt > 13.365)',
    #'(run < 5 && Muon2Pt > 9 || Muon2Pt > 8.91)',
    'Muon1Pt > 15',
    'Muon2Pt > 9',
    'Muon1AbsEta < 2.1',
    'Muon2AbsEta < 2.1',
    'Muon1_MuRelIso < 0.15',
    'Muon2_MuRelIso < 0.15',
    'Muon1_MuID_WWID > 0.5',
    'Muon2_MuID_WWID > 0.5',
    'NIsoMuonsPt5_Nmuons < 1',
    'NBjetsPt20_Nbjets < 1', # Against ttbar
    'DoubleMuTriggers_HLT > 0.5 ',
    'Muon1Charge*Muon2Charge < 0',
]

# Stupid names are different, fix this
base_dimuon_emm = [
    x.replace('Muon1', 'Mu1').replace('Muon2', 'Mu2')
    for x in base_dimuon_selection
]

# Selecting Z->ee events
base_dielectron_selection = [
    'Elec1Pt > 15',
    'Elec2Pt > 10',
    'Elec1AbsEta < 2.5',
    'Elec2AbsEta < 2.5',
    'Elec1_ERelIso < 0.15',
    'Elec2_ERelIso < 0.15',
    'Elec1_EID_WWID > 0.5',
    'Elec2_EID_WWID > 0.5',
    'NIsoMuonsPt5_Nmuons < 1',
    'NBjetsPt20_Nbjets < 1', # Against ttbar
    #'DoubleMuTriggers_HLT > 0.5 ',
    'Elec1Charge*Elec2Charge < 0',
]

fakerates = {
    'tau' : {
        'ntuple' : 'mmtFilter',
        'pd' : 'data_DoubleMu',
        'varname' : 'TauJetPt',
        'vartitle' : 'Tau Jet p_{T}',
        'var' : 'TauJetPt',
        'varbinning' : [300, 0, 300],
        'rebin' : 4,
        'zMassVar' : 'Leg1Leg2_Mass',
        'zMassTitle' : 'Dimuon mass (GeV)',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_selection,
        'zcuts' : [
            'Leg1Leg2_Mass > 70',
            'Leg1Leg2_Mass < 110',
            'Leg3_MtToMET < 40'
        ],
        'denom' : [
            'TauPt > 15',
            'TauAbsEta < 2.5',
            'Tau_DecayMode > 0.5',
        ],
        'num' : [
            'Tau_LooseHPS > 0.5'
        ],
    },
    'mu' : {
        'ntuple' : 'mmmFilter',
        'pd' : 'data_DoubleMu',
        'varname' : 'MuJetPt',
        'var' : 'Muon3Pt + Muon3Pt*Muon3_MuRelIso',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [300, 0, 300],
        'rebin' : 5,
        'zMassVar' : 'Leg1Leg2_Mass',
        'zMassTitle' : 'Dimuon mass (GeV)',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_selection,
        'zcuts' : [
            'Leg1Leg2_Mass > 70',
            'Leg1Leg2_Mass < 110',
            'Leg3_MtToMET < 40'
        ],
        'denom' : [
            'Muon3Pt > 9',
            'Muon3AbsEta < 2.1',
        ],
        'num' : [
            'Muon3_MuID_WWID > 0.5',
            'Muon3_MuRelIso < 0.3',
        ]
    },
    'e' : {
        'ntuple' : 'emmFilter',
        'pd' : 'data_DoubleMu',
        'varname' : 'EJetPt',
        'var' : 'ElecPt + ElecPt*Elec_ERelIso',
        'vartitle' : 'Electron Jet p_{T}',
        'varbinning' : [300, 0, 300],
        'rebin' : 5,
        'zMassVar' : 'Leg2Leg3_Mass',
        'zMassTitle' : 'Dimuon mass (GeV)',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_emm,
        'zcuts' : [
            'Leg2Leg3_Mass > 70',
            'Leg2Leg3_Mass < 110',
            'Leg1_MtToMET < 40'
        ],
        'denom' : [
            'ElecPt > 10',
            'ElecAbsEta < 2.5',
        ],
        'num' : [
            'Elec_EID_WWID > 0.5',
            'Elec_ERelIso < 0.3',
        ]
    },
    'tauZEE' : {
        'ntuple' : 'eetFilter',
        'pd' : 'data_DoubleElectron',
        'varname' : 'TauJetPt',
        'vartitle' : 'Tau Jet p_{T}',
        'var' : 'TauJetPt',
        'varbinning' : [300, 0, 300],
        'rebin' : 4,
        'zMassVar' : 'Leg1Leg2_Mass',
        'zMassTitle' : 'Dielectron mass (GeV)',
        'evtType' : 'ee + jet',
        'base_cuts' : base_dielectron_selection,
        'zcuts' : [
            'Leg1Leg2_Mass > 70',
            'Leg1Leg2_Mass < 110',
            'Leg3_MtToMET < 40'
        ],
        'denom' : [
            'TauPt > 15',
            'TauAbsEta < 2.5',
            'Tau_DecayMode > 0.5',
        ],
        'num' : [
            'Tau_LooseHPS > 0.5'
        ],
    },
    'muZEE' : {
        'ntuple' : 'eemFilter',
        'pd' : 'data_DoubleElectron',
        'varname' : 'MuJetPt',
        'var' : 'MuPt + MuPt*Mu_MuRelIso',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [300, 0, 300],
        'rebin' : 5,
        'zMassVar' : 'Leg1Leg2_Mass',
        'evtType' : 'ee + jet',
        'base_cuts' : base_dielectron_selection,
        'zMassTitle' : 'Dielectron mass (GeV)',
        'zcuts' : [
            'Leg1Leg2_Mass > 70',
            'Leg1Leg2_Mass < 110',
            'Leg3_MtToMET < 40'
        ],
        'denom' : [
            'MuPt > 9',
            'MuAbsEta < 2.1',
        ],
        'num' : [
            'Mu_MuID_WWID > 0.5',
            'Mu_MuRelIso < 0.3',
        ]
    },
}

for fr_type, fr_info in fakerates.iteritems():
    # Draw the Z-mumu mass
    denom_selection_list = \
            fr_info['base_cuts'] + fr_info['zcuts'] + fr_info['denom']
    denom_selection = " && ".join(denom_selection_list)

    num_selection_list = denom_selection_list + fr_info['num']
    num_selection = ' && '.join(num_selection_list)

    weight = 'puWeight2011A'

    plotter.register_tree(
        'DenomZMass',
        '/%s/final/Ntuple' % fr_info['ntuple'],
        fr_info['zMassVar'],
        denom_selection,
        w = weight,
        binning = [80, 70, 110],
        include = ['*'],
    )

    plotter.register_tree(
        'NumZMass',
        '/%s/final/Ntuple' % fr_info['ntuple'],
        fr_info['zMassVar'],
        num_selection,
        w = weight,
        binning = [80, 70, 110],
        include = ['*'],
    )

    plotter.register_tree(
        'Denom' + fr_info['varname'],
        '/%s/final/Ntuple' % fr_info['ntuple'],
        fr_info['var'],
        denom_selection,
        w = weight,
        binning = fr_info['varbinning'],
        include = ['*'],
    )

    plotter.register_tree(
        'Num' + fr_info['varname'],
        '/%s/final/Ntuple' % fr_info['ntuple'],
        fr_info['var'],
        num_selection,
        w = weight,
        binning = fr_info['varbinning'],
        include = ['*'],
    )

    to_plot = [
        ('DenomZMass', 'Dilepton mass (loose)', fr_info['zMassTitle']),
        ('NumZMass', 'Dilepton mass (tight)', fr_info['zMassTitle']),
        ('Num' + fr_info['varname'], '%s mass (tight)' % fr_info['vartitle'], fr_info['vartitle']),
        ('Denom' + fr_info['varname'], '%s mass (loose)' % fr_info['vartitle'], fr_info['vartitle']),
    ]

    # Make plots
    for name, title, xtitle in to_plot:
        rebin = 1
        if 'Z' not in name:
            rebin = fr_info['rebin']

        stack = plotter.build_stack(
            '/%s/final/Ntuple:%s' % (fr_info['ntuple'], name),
            include = ['*'],
            exclude = ['*data*'],
            title = title,
            show_overflows = True,
            rebin = rebin,
        )
        data = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (fr_info['ntuple'], name),
            show_overflows = True,
            rebin = rebin,
        )
        stack.Draw()
        stack.GetXaxis().SetTitle(xtitle)
        data.Draw("pe, same")
        stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)
        stack.GetHistogram().SetTitle(
             xtitle + ' in ' + fr_info['evtType'] + ' events')

        saveplot(fr_type + '_' + name)

    # Make efficiency curve
    data_num = plotter.get_histogram(
        fr_info['pd'],
        '/%s/final/Ntuple:%s' % (
            fr_info['ntuple'], 'Num' + fr_info['varname']),
        show_overflows = True,
        rebin = fr_info['rebin'],
    )

    data_denom = plotter.get_histogram(
        fr_info['pd'],
        '/%s/final/Ntuple:%s' % (
            fr_info['ntuple'], 'Denom' + fr_info['varname']),
        show_overflows = True,
        rebin = fr_info['rebin'],
    )

    mc_num = plotter.get_histogram(
        'Zjets',
        '/%s/final/Ntuple:%s' % (
            fr_info['ntuple'], 'Num' + fr_info['varname']),
        show_overflows = True,
        rebin = fr_info['rebin'],
    )

    mc_denom = plotter.get_histogram(
        'Zjets',
        '/%s/final/Ntuple:%s' % (
            fr_info['ntuple'], 'Denom' + fr_info['varname']),
        show_overflows = True,
        rebin = fr_info['rebin'],
    )

    print data_denom, data_num

    data_curve = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
    data_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
    data_fit_func.SetParameter(0, 0.02)
    data_fit_func.SetParameter(1, 1.87)
    data_fit_func.SetParameter(2, -9.62806e-02)
    data_fit_func.SetLineColor(ROOT.EColor.kBlack)
    data_curve.Fit(data_fit_func)

    mc_curve = ROOT.TGraphAsymmErrors(mc_num.th1, mc_denom.th1)
    mc_curve.SetMarkerColor(ROOT.EColor.kRed)
    mc_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
    mc_fit_func.SetParameter(0, 0.02)
    mc_fit_func.SetParameter(1, 1.87)
    mc_fit_func.SetParameter(2, -9.62806e-02)
    mc_fit_func.SetLineColor(ROOT.EColor.kRed)
    mc_curve.Fit(mc_fit_func)

    canvas.Clear()
    multi = ROOT.TMultiGraph("fake_rates", "Fake Rates")
    multi.Add(data_curve, "pe")
    multi.Add(mc_curve, "pe")

    multi.Draw("ape")
    multi.GetHistogram().SetMinimum(1e-3)
    multi.GetHistogram().GetXaxis().SetTitle(fr_info['vartitle'])
    multi.GetHistogram().SetTitle(
        'Fake rate in ' + fr_info['evtType'] + ' events')

    data_curve.Draw('same')
    mc_curve.Draw('same')
    saveplot(fr_type + "_fakerate")
