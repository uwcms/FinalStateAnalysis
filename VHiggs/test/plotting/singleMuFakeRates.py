'''

Measure jet->lepton fake rates in single muon events

'''


import ROOT
import os
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool

# Logging options
logging.basicConfig(filename='singleMuFakeRates.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("fakerates")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)

ROOT.gROOT.SetBatch(True)
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

wjets_selection = [
    #'(IsoMu17_HLT || IsoMu20_HLT)',
    'Muon1Pt > 18',
    'Muon1AbsEta < 2.1',
    'Muon1_MtToMET > 30',
    'METPt > 30',
    'Muon1_MuID_WWID > 0.5',
    'Muon1_MuRelIso < 0.1',
    'Muon1Charge*Muon2Charge > 0',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NIsoElecPt10_Nelectrons < 0.5',
    #'NBjetsPt20_Nbjets < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'NIsoTausPt20_NIsoTaus < 0.5',
]

qcd_selection = [
    'Muon1Pt > 18',
    'Muon1AbsEta < 2.1',
    'Muon1_MuRelIso > 0.3',
    'Muon1Charge*Muon2Charge > 0',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NBjetsPt20_Nbjets < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'METPt < 20',
    'NIsoTausPt20_NIsoTaus < 0.5',
    'NIsoElecPt10_Nelectrons < 0.5',
]

# In the emu channels, the muon is the second leg.
wjets_selection_emu = [
    x.replace('Muon1', 'Muon2') for x in wjets_selection
]

qcd_selection_emu = [
    x.replace('Muon1', 'Muon2') for x in qcd_selection
]

fakerates = {
    'mu' : {
        'ntuple' : 'mm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'Muon2_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu',
        'base_cuts' : wjets_selection,
        'control_plots' : [
            ('Btag', 'Muon2_MuBtag',
             "Probe TCHE", [100, -5, 5]),
        ],
        'final_cuts' : [],
        'denom' : [
            'Muon2_MuBtag < 3.3',
            'Muon2_InnerNPixHits > 0.5',
            'DoubleMus_HLT > 0.5',
            'Muon2Pt > 9',
            'Muon2AbsEta < 2.1',
            'Muon1DZ < 0.2',
            'Muon2DZ < 0.2',
        ],
        'num' : [
            'Muon2_MuID_WWID > 0.5',
            'Muon2_MuRelIso < 0.3',
        ]
    },
    'muQCD' : {
        'ntuple' : 'mm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'Muon2_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 10,
        'evtType' : '#mu#mu',
        'base_cuts' : qcd_selection,
        'control_plots' : [
            ('Btag', 'Muon2_MuBtag',
             "Probe TCHE", [100, -5, 5]),
        ],
        'final_cuts' : [],
        'denom' : [
            'Muon2_MuBtag < 3.3',
            'Muon2_InnerNPixHits > 0.5',
            'DoubleMus_HLT > 0.5',
            'Muon2Pt > 9',
            'Muon2AbsEta < 2.1',
            'Muon1DZ < 0.2',
            'Muon2DZ < 0.2',
        ],
        'num' : [
            'Muon2_MuID_WWID > 0.5',
            'Muon2_MuRelIso < 0.3',
        ]
    },
    'e' : {
        'ntuple' : 'em',
        'pd' : 'data_SingleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*DoubleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'EJetPt',
        'vartitle' : 'Electron Jet Pt',
        'var' : 'Electron_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : 'e#mu',
        'base_cuts' : wjets_selection_emu,
        'control_plots' : [
            ('Njets', 'NjetsPt20_Njets',
             "Number of jets", [10, -0.5, 9.5]),
        ],
        'final_cuts' : [],
        'denom' : [
            'IsoMus_HLT > 0.5',
            'Muon2Pt > 24',
            'Mu17Ele8All_HLT > 0.5',
            'ElectronCharge*Muon2Charge > 0',
            'ElectronPt > 9',
            'ElectronAbsEta < 2.5',
            'Electron_EBtag < 3.3',
            'Muon2DZ < 0.2',
            'ElectronDZ < 0.2',
        ],
        'num' : [
            'Electron_EID_WWID > 0.5',
            'Electron_ERelIso < 0.3',
        ]
    },
    'eQCD' : {
        'ntuple' : 'em',
        'pd' : 'data_SingleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*DoubleMu*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'EJetPt',
        'vartitle' : 'Electron Jet Pt',
        'var' : 'Electron_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : 'e#mu',
        'base_cuts' : qcd_selection_emu,
        'control_plots' : [],
        'final_cuts' : [],
        'denom' : [
            'Mu17Ele8All_HLT > 0.5',
            'ElectronCharge*Muon2Charge > 0',
            'ElectronPt > 9',
            'ElectronAbsEta < 2.5',
            'Electron_EBtag < 3.3',
            'Muon2DZ < 0.2',
            'ElectronDZ < 0.2',
        ],
        'num' : [
            'Electron_EID_WWID > 0.5',
            'Electron_ERelIso < 0.3',
        ]
    }
}

output_file = ROOT.TFile("results_singleMuFakeRates.root", "RECREATE")
for data_set, skips, int_lumi in [
    ('2011A', ['2011B', 'EM', 'MuEG'], 2170),
    #('2011B', ['2011A', 'EM'], 2170),
    ('2011AB', ['EM', 'MuEG'], 4600) ]:
    log.info("Plotting dataset: %s", data_set)
    print "WARNING SKIPPING MUEG"

    samples, plotter = data_tool.build_data(
        'Mu', '2011-11-13-v2-MuonTP', 'scratch_results', int_lumi, skips,
        count = '/mm/skimCounter', unweighted = False)

    legend = plotter.build_legend(
        '/em/skimCounter',
        include = ['*'],
        exclude = ['*data*','*VH*'],
        drawopt='lf')

    def saveplot(filename):
        # Save the current canvas
        filetype = '.pdf'
        canvas.SetLogy(False)
        canvas.Update()
        canvas.Print(os.path.join(
            "plots", 'singleMuFakeRates', data_set, filename + filetype))
        canvas.SetLogy(True)
        canvas.Update()
        canvas.Print(os.path.join(
            "plots", 'singleMuFakeRates', data_set, filename + '_log' + filetype))

    for fr_type, fr_info in fakerates.iteritems():
        log.info("Doing fake rate type %s", fr_type)
        # Draw the Z-mumu mass
        denom_selection_list = \
                fr_info['base_cuts'] + fr_info['denom']
        denom_selection = " && ".join(denom_selection_list)

        num_selection_list = denom_selection_list + fr_info['num']
        num_selection = ' && '.join(num_selection_list)

        weight = 'puWeight_3bx_S42011AB178078'

        # List of final plots to make
        to_plot = [
            (fr_type + 'Num' + fr_info['varname'],
             '%s mass (tight)' % fr_info['vartitle'],
             fr_info['vartitle'], fr_info['rebin']),
            (fr_type + 'Denom' + fr_info['varname'],
             '%s mass (loose)' % fr_info['vartitle'],
             fr_info['vartitle'], fr_info['rebin']),
        ]

        for label, var, title, binning in fr_info['control_plots']:
            log.info("Plotting control plot %s", label)
            plotter.register_tree(
                fr_type + label + 'Denom',
                '/%s/final/Ntuple' % fr_info['ntuple'],
                var,
                denom_selection,
                w = weight,
                binning = binning,
                include = ['*'],
                exclude = fr_info['exclude'],
            )

            plotter.register_tree(
                fr_type + label + 'Num',
                '/%s/final/Ntuple' % fr_info['ntuple'],
                var,
                num_selection,
                w = weight,
                binning = binning,
                include = ['*'],
                exclude = fr_info['exclude'],
            )
            to_plot.append(
                (fr_type + label + 'Denom', "%s (loose)" % title, title, 1)
            )
            to_plot.append(
                (fr_type + label + 'Num', "%s (tight)" % title, title, 1)
            )

        # Add the final cuts in
        denom_selection_list += fr_info['final_cuts']
        denom_selection = " && ".join(denom_selection_list)

        num_selection_list += fr_info['final_cuts']
        num_selection = ' && '.join(num_selection_list)

        plotter.register_tree(
            fr_type + 'Denom' + fr_info['varname'],
            '/%s/final/Ntuple' % fr_info['ntuple'],
            fr_info['var'],
            denom_selection,
            w = weight,
            binning = fr_info['varbinning'],
            include = ['*'],
            exclude = fr_info['exclude'],
        )

        plotter.register_tree(
            fr_type + 'Num' + fr_info['varname'],
            '/%s/final/Ntuple' % fr_info['ntuple'],
            fr_info['var'],
            num_selection,
            w = weight,
            binning = fr_info['varbinning'],
            include = ['*'],
            exclude = fr_info['exclude'],
        )

        # Make plots
        for name, title, xtitle, rebin in to_plot:

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
            legend.Draw()
            stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)
            stack.GetHistogram().SetTitle(
                 xtitle + ' in ' + fr_info['evtType'] + ' events')

            saveplot(fr_type + '_' + name)

        # Make efficiency curve
        data_num = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )
        log.info("Data numerator has %i entries", data_num.Integral())

        data_denom = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )
        log.info("Data denom has %i entries", data_denom.Integral())

        mc_num = plotter.get_histogram(
            fr_info['mc_pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )
        log.info("MC numerator has %i entries", mc_num.Integral())

        mc_denom = plotter.get_histogram(
            fr_info['mc_pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )
        log.info("MC denominator has %i entries", mc_denom.Integral())

        frame = ROOT.TH1F("frame",
                          'Fake rate in ' + fr_info['evtType'] + ' events',
                          100, 0, 100)
        frame.GetXaxis().SetTitle(fr_info['vartitle'])
        frame.SetMinimum(1e-3)
        frame.SetMaximum(1.0)

        data_curve = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
        data_curve.SetLineStyle(0)
        data_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
        #data_fit_func = ROOT.TF1(
            #"f1", "[0] + [1]*exp([2]*(x-9))"
            #" + [3]*exp([4]*(x-9)*(x-9))",
            #0, 200)
        data_fit_func.SetParameter(0, 0.02)
        data_fit_func.SetParLimits(0, 0.0, 1)
        data_fit_func.SetParameter(1, 1.87)
        data_fit_func.SetParameter(2, -9.62806e-02)
        #data_fit_func.SetParameter(3, 1.87)
        #data_fit_func.SetParLimits(3, 0, 100)
        #data_fit_func.SetParameter(4, -9.62806e-02)
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
        multi.Add(mc_curve, "pe")
        multi.Add(data_curve, "pe")

        frame.Draw()
        multi.Draw("pe")

        data_fit_func.Draw('same')
        mc_fit_func.Draw('same')
        saveplot(fr_type + "_fakerate")

        # Save non rebinned histos
        data_num = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
        )
        log.info("Data numerator has %i entries", data_num.Integral())

        data_denom = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
        )
        log.info("Data denom has %i entries", data_denom.Integral())

        output_file.cd()
        data_denom.Write("_".join([data_set, fr_type, 'data_denom']))
        data_num.Write("_".join([data_set, fr_type, 'data_num']))
