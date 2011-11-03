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

import FinalStateAnalysis.PatTools.data as data

#skips = ['2011B', 'PromptReco_v6_1409']
#skips = ['2011B', ]
skips = ['2011A', 'v1_d']

data_sample, plotter = data.build_data(
    'Tau', '2011-11-02-v1-MuonTP', 'scratch_results', 2170, skips,
    count = '/mm/skimCounter', unweighted = False)

wjets_selection = [
    #'(IsoMu17_HLT || IsoMu20_HLT)',
    'Muon1Pt > 20',
    'Muon1AbsEta < 2.1',
    'Muon1_MtToMET > 40',
    'METPt > 30',
    'Muon1_MuRelIso < 0.1',
    'Muon1Charge*Muon2Charge > 0',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NBjetsPt20_Nbjets < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',

]

fakerates = {
    'mu' : {
        'ntuple' : 'mm',
        'pd' : 'data_SingleMu',
        'mc_pd' : 'Wjets',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'Muon2Pt + Muon2Pt*Muon2_MuRelIso',
        'varbinning' : [100, 0, 100],
        'rebin' : 4,
        'zMassVar' : 'Muon1_MtToMET',
        'zMassTitle' : 'Muon 1 MT to MET',
        'evtType' : '#mu#mu',
        'base_cuts' : wjets_selection,
        'zcuts' : [
            #'Leg1Leg2_Mass > 70',
            #'Leg1Leg2_Mass < 110',
            #'(finalStateVisP4Mass < 80 || finalStateVisP4Mass > 100)',
            #'Leg3_MtToMET < 40'
        ],
        'denom' : [
            'Muon2Pt > 9',
            'Muon2AbsEta < 2.1',
        ],
        'num' : [
            'Muon2_MuID_WWID > 0.5',
            'Muon2_MuRelIso < 0.3',
        ]
    }
}

for fr_type, fr_info in fakerates.iteritems():
    # Draw the Z-mumu mass
    denom_selection_list = \
            fr_info['base_cuts'] + fr_info['zcuts'] + fr_info['denom']
    denom_selection = " && ".join(denom_selection_list)

    num_selection_list = denom_selection_list + fr_info['num']
    num_selection = ' && '.join(num_selection_list)

    weight = 'puWeight_3bx_S42011A'

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
        fr_info['mc_pd'],
        '/%s/final/Ntuple:%s' % (
            fr_info['ntuple'], 'Num' + fr_info['varname']),
        show_overflows = True,
        rebin = fr_info['rebin'],
    )

    mc_denom = plotter.get_histogram(
        fr_info['mc_pd'],
        '/%s/final/Ntuple:%s' % (
            fr_info['ntuple'], 'Denom' + fr_info['varname']),
        show_overflows = True,
        rebin = fr_info['rebin'],
    )

    print data_denom, data_num

    data_curve = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
    data_curve.SetLineStyle(0)
    data_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
    data_fit_func.SetParameter(0, 0.02)
    data_fit_func.SetParLimits(0, 0.0, 1)
    data_fit_func.SetParameter(1, 1.87)
    data_fit_func.SetParameter(2, -9.62806e-02)
    data_fit_func.SetLineColor(ROOT.EColor.kBlack)
    data_curve.Fit(data_fit_func)

    mc_curve = ROOT.TGraphAsymmErrors(mc_num.th1, mc_denom.th1)
    mc_curve.SetMarkerColor(ROOT.EColor.kRed)
    mc_curve.SetLineStyle(0)
    mc_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
    mc_fit_func.SetParameter(0, 0.02)
    mc_fit_func.SetParLimits(0, 0.0, 1)
    mc_fit_func.SetParameter(1, 1.87)
    mc_fit_func.SetParameter(2, -9.62806e-02)
    mc_fit_func.SetLineColor(ROOT.EColor.kRed)
    mc_curve.Fit(mc_fit_func)

    canvas.Clear()
    multi = ROOT.TMultiGraph("fake_rates", "Fake Rates")
    multi.Add(mc_curve, "p")
    multi.Add(data_curve, "p")

    multi.Draw("a")
    multi.GetHistogram().SetMinimum(1e-3)
    multi.GetHistogram().GetXaxis().SetTitle(fr_info['vartitle'])
    multi.GetHistogram().SetTitle(
        'Fake rate in ' + fr_info['evtType'] + ' events')

    data_fit_func.Draw('same')
    mc_fit_func.Draw('same')
    saveplot(fr_type + "_fakerate")

    data_num = plotter.get_histogram(
        'data_SingleMu',
        '/mm/intLumi',
        show_overflows = True,
    )


    data_num.Draw()
    saveplot('intlumi')
