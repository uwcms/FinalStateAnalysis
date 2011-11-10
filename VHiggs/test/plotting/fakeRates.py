'''

Measure jet->mu, jet->e, and jet->tau fake rates in trilepton event topologies.

'''

import ROOT
import os
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool

# Logging options
logging.basicConfig(filename='fakeRates.log',level=logging.DEBUG, filemode='w')
#log = logging.getLogger("plotting")
#h1 = logging.StreamHandler(sys.stdout)
#h1.level = logging.DEBUG
#log.addHandler(h1)
#logging.getLogger("AnalysisPlotter").addHandler(h1)
#h2 = logging.StreamHandler(sys.stderr)
#h2.level = logging.DEBUG
#logging.getLogger("ROOTCache").addHandler(h2)

ROOT.gROOT.SetBatch(True)
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

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
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NBjetsPt20_Nbjets < 1', # Against ttbar
    'DoubleMus_HLT > 0.5 ',
    '(Muon1_hltDiMuonL3PreFiltered7 |  Muon1_hltSingleMu13L3Filtered13)',
    '(Muon2_hltDiMuonL3PreFiltered7 | Muon2_hltDiMuonL3p5PreFiltered8)',
    'Muon1Charge*Muon2Charge < 0',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'METPt < 20',
    'Muon2_NPixHits > 1',
]

# We also look at Mu-Mu (SS) + Anti-Tau.  We require the leading muon to have a
# good MT.
base_ttbar_selection = [
    'Muon1Pt > 15',
    'Muon2Pt > 9',
    'Muon1AbsEta < 2.1',
    'Muon2AbsEta < 2.1',
    'Muon1_MuRelIso < 0.15',
    'Muon1_MuID_WWID > 0.5',
    'NIsoMuonsPt5_Nmuons < 1',
    #'NBjetsPt20_Nbjets > 0', # For ttbar
    'DoubleMus_HLT > 0.5 ',
    'Muon1Charge*Muon2Charge > 0', # Same sign (to kill DY)
    'Tau_LooseHPS < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'Muon2_NPixHits > 1',
]

base_qcd_selection = [
    'Muon1Pt > 15',
    'Muon2Pt > 9',
    'Muon1AbsEta < 2.1',
    'Muon2AbsEta < 2.1',
    'Muon1_MuRelIso > 0.5',
    'Muon1_MuID_WWID > 0.5',
    'NIsoMuonsPt5_Nmuons < 1',
    #'NBjetsPt20_Nbjets > 0', # For ttbar
    'DoubleMus_HLT > 0.5 ',
    'Muon1Charge*Muon2Charge > 0', # Same sign (to kill DY)
    'Tau_LooseHPS < 0.5',
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'Muon2_NPixHits > 1',
]

# For e fake rate measurement
base_qcd_emt_selection = [

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
    'vtxNDOF > 0',
    'vtxChi2/vtxNDOF < 10',
    'METPt < 20',
    'Mu_NPixHits > 1',
]

fakerates = {
    #'tau' : {
        #'ntuple' : 'mmt',
        #'pd' : 'data_DoubleMu',
        #'exclude' : ['*DoubleE*', '*MuEG*'],
        #'mc_pd' : 'Zjets',
        #'varname' : 'TauJetPt',
        #'vartitle' : 'Tau Jet p_{T}',
        #'var' : 'TauJetPt',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 4,
        #'zMassVar' : 'Muon1_Muon2_Mass',
        #'zMassTitle' : 'Dimuon mass (GeV)',
        #'evtType' : '#mu#mu + jet',
        #'base_cuts' : base_dimuon_selection,
        #'zcuts' : [
            ##'Muon1_Muon2_Mass > 70',
            ##'Muon1_Muon2_Mass < 110',
            #'Muon1_Muon2_Mass > 86',
            #'Muon1_Muon2_Mass < 95',
            #'Leg3_MtToMET < 40'
        #],
        #'denom' : [
            #'TauPt > 15',
            #'TauAbsEta < 2.5',
            #'Tau_DecayMode > 0.5',
        #],
        #'num' : [
            #'Tau_LooseHPS > 0.5'
        #],
    #},
    'mu' : {
        'ntuple' : 'mmm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'MuJetPt',
        'var' : 'Muon3Pt + Muon3Pt*Muon3_MuRelIso',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'zMassVar' : 'Muon1_Muon2_Mass',
        'zMassTitle' : 'Dimuon mass (GeV)',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_selection,
        'zcuts' : [
            #'Muon1_Muon2_Mass > 70',
            #'Muon1_Muon2_Mass < 110',
            'Muon1_Muon2_Mass > 86',
            'Muon1_Muon2_Mass < 95',
            'Muon3_MtToMET < 10'
        ],
        'denom' : [
            'Muon3Pt > 9',
            'Muon3AbsEta < 2.1',
            'Muon3_NPixHits > 0',
        ],
        'num' : [
            'Muon3_MuID_WWID > 0.5',
            'Muon3_MuRelIso < 0.3',
        ]
    },
    'muTTbar' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'ttjets',
        'varname' : 'MuJetPt',
        'var' : 'Muon2Pt + Muon2Pt*Muon2_MuRelIso',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'zMassVar' : 'Muon1_MtToMET',
        'zMassTitle' : 'Leading Muon M_{T}',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_ttbar_selection,
        'zcuts' : [
            'Muon1_MtToMET > 30',
            'Muon2_MtToMET < 30',
            'METPt > 20',
        ],
        'denom' : [
        ],
        'num' : [
            'Muon2_MuID_WWID > 0.5',
            'Muon2_MuRelIso < 0.3',
        ]
    },
    'muQCD' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'MuJetPt',
        'var' : 'Muon2Pt + Muon2Pt*Muon2_MuRelIso',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'zMassVar' : 'Muon1_MtToMET',
        'zMassTitle' : 'Leading Muon M_{T}',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_qcd_selection,
        'zcuts' : [
            #'Leg2_MtToMET < 30',
            'METPt < 20',
        ],
        'denom' : [
        ],
        'num' : [
            'Muon2_MuID_WWID > 0.5',
            'Muon2_MuRelIso < 0.3',
        ]
    },
    'e' : {
        'ntuple' : 'emm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'EJetPt',
        'var' : 'ElecPt + ElecPt*Elec_ERelIso',
        'vartitle' : 'Electron Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'zMassVar' : 'Mu1_Mu2_Mass',
        'zMassTitle' : 'Dimuon mass (GeV)',
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_emm,
        'zcuts' : [
            #'Leg2Leg3_Mass > 70',
            #'Leg2Leg3_Mass < 110',
            'Mu1_Mu2_Mass > 86',
            'Mu1_Mu2_Mass < 95',
            'Elec_MtToMET < 40'
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
    #'eQCD' : {
        #'ntuple' : 'emt',
        #'pd' : 'data_MuEG',
        #'exclude' : ['*DoubleE*', '*DoubleMu*'],
        #'mc_pd' : 'QCDMu',
        #'varname' : 'EJetPt',
        #'var' : 'ElecPt + ElecPt*Elec_ERelIso',
        #'vartitle' : 'E Jet p_{T}',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 5,
        #'zMassVar' : 'Mu_MtToMET',
        #'zMassTitle' : 'Leading Muon M_{T}',
        #'evtType' : '#mu#mu + jet',
        #'base_cuts' : base_qcd_selection,
        #'zcuts' : [
            ##'Leg2_MtToMET < 30',
            #'METPt < 20',
        #],
        #'denom' : [
        #],
        #'num' : [
            #'Muon2_MuID_WWID > 0.5',
            #'Muon2_MuRelIso < 0.3',
        #]
    #},
    #'tauZEE' : {
        #'ntuple' : 'eet',
        #'pd' : 'data_DoubleElectron',
        #'mc_pd' : 'Zjets',
        #'exclude' : ['*DoubleMu*', '*MuEG*'],
        #'varname' : 'TauJetPt',
        #'vartitle' : 'Tau Jet p_{T}',
        #'var' : 'TauJetPt',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 4,
        #'zMassVar' : 'Muon1_Muon2_Mass',
        #'zMassTitle' : 'Dielectron mass (GeV)',
        #'evtType' : 'ee + jet',
        #'base_cuts' : base_dielectron_selection,
        #'zcuts' : [
            ##'Muon1_Muon2_Mass > 70',
            ##'Muon1_Muon2_Mass < 110',
            #'Muon1_Muon2_Mass > 86',
            #'Muon1_Muon2_Mass < 95',
            #'Leg3_MtToMET < 20'
        #],
        #'denom' : [
            #'TauPt > 15',
            #'TauAbsEta < 2.5',
            #'Tau_DecayMode > 0.5',
        #],
        #'num' : [
            #'Tau_LooseHPS > 0.5'
        #],
    #},
    'muZEE' : {
        'ntuple' : 'eem',
        'pd' : 'data_DoubleElectron',
        'mc_pd' : 'Zjets',
        'exclude' : ['*DoubleMu*', '*MuEG*'],
        'varname' : 'MuJetPt',
        'var' : 'MuPt + MuPt*Mu_MuRelIso',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'zMassVar' : 'Elec1_Elec2_Mass',
        'evtType' : 'ee + jet',
        'base_cuts' : base_dielectron_selection,
        'zMassTitle' : 'Dielectron mass (GeV)',
        'zcuts' : [
            #'Muon1_Muon2_Mass > 70',
            #'Muon1_Muon2_Mass < 110',
            'Elec1_Elec2_Mass > 86',
            'Elec1_Elec2_Mass < 95',
            'Mu_MtToMET < 20'
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

output_file = ROOT.TFile("results_fakeRates.root", "RECREATE")

for data_set, skips, int_lumi in [('2011A', ['2011B', 'EM'], 2170),
                                  ('2011B', ['2011A', 'v1_d', 'EM'], 2170),
                                  ('2011AB', ['v1_d', 'EM'], 4000)]:

    samples, plotter = data_tool.build_data(
        'VH', '2011-11-07-v1-WHAnalyze', 'scratch_results',
        int_lumi, skips, count='emt/skimCounter')

    legend = plotter.build_legend(
        '/emt/skimCounter',
        include = ['*'],
        exclude = ['*data*','*VH*'],
        drawopt='lf')

    def saveplot(filename):
        # Save the current canvas
        filetype = '.pdf'
        #legend.Draw()
        canvas.SetLogy(False)
        canvas.Update()
        canvas.Print(os.path.join(
            "plots", 'fakeRates', data_set, filename + filetype))
        canvas.SetLogy(True)
        canvas.Update()
        canvas.Print(os.path.join(
            "plots", 'fakeRates', data_set, filename + '_log' + filetype))


    for fr_type, fr_info in fakerates.iteritems():
        # Draw the Z-mumu mass
        denom_selection_list = \
                fr_info['base_cuts'] + fr_info['zcuts'] + fr_info['denom']
        denom_selection = " && ".join(denom_selection_list)

        num_selection_list = denom_selection_list + fr_info['num']
        num_selection = ' && '.join(num_selection_list)

        weight = 'puWeight_3bx_S42011AB178078'

        plotter.register_tree(
            fr_type + 'DenomZMass',
            '/%s/final/Ntuple' % fr_info['ntuple'],
            fr_info['zMassVar'],
            denom_selection,
            w = weight,
            binning = [80, 70, 110],
            include = ['*'],
            exclude = fr_info['exclude'],
        )

        plotter.register_tree(
            fr_type + 'NumZMass',
            '/%s/final/Ntuple' % fr_info['ntuple'],
            fr_info['zMassVar'],
            num_selection,
            w = weight,
            binning = [80, 70, 110],
            include = ['*'],
            exclude = fr_info['exclude'],
        )

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

        to_plot = [
            (fr_type + 'DenomZMass', 'Dilepton mass (loose)', fr_info['zMassTitle']),
            (fr_type + 'NumZMass', 'Dilepton mass (tight)', fr_info['zMassTitle']),
            (fr_type + 'Num' + fr_info['varname'], '%s mass (tight)' % fr_info['vartitle'], fr_info['vartitle']),
            (fr_type + 'Denom' + fr_info['varname'], '%s mass (loose)' % fr_info['vartitle'], fr_info['vartitle']),
        ]

        # Make plots
        for name, title, xtitle in to_plot:
            rebin = 1
            if 'ZMass' not in name:
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
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        data_denom = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        mc_num = plotter.get_histogram(
            fr_info['mc_pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        mc_denom = plotter.get_histogram(
            fr_info['mc_pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        print data_denom, data_num

        data_curve = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
        data_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
        data_fit_func.SetParameter(0, 0.02)
        data_fit_func.SetParLimits(0, 0.0, 1)
        data_fit_func.SetParameter(1, 1.87)
        data_fit_func.SetParameter(2, -9.62806e-02)
        data_fit_func.SetLineColor(ROOT.EColor.kBlack)
        data_curve.Fit(data_fit_func)

        mc_curve = ROOT.TGraphAsymmErrors(mc_num.th1, mc_denom.th1)
        mc_curve.SetMarkerColor(ROOT.EColor.kRed)
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

        multi.Draw("ape")
        multi.GetHistogram().SetMinimum(1e-3)
        multi.GetHistogram().SetMaximum(1.0)
        multi.GetHistogram().GetXaxis().SetTitle(fr_info['vartitle'])
        multi.GetHistogram().SetTitle(
            'Fake rate in ' + fr_info['evtType'] + ' events')

        data_fit_func.Draw('same')
        mc_fit_func.Draw('same')
        saveplot(fr_type + "_fakerate")

        output_file.cd()
        data_denom.Write("_".join([data_set, fr_type, 'data_denom']))
        data_num.Write("_".join([data_set, fr_type, 'data_num']))
