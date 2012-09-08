'''

Measure jet->lepton fake rates in single muon events

'''

import copy
import logging
import os
import re
import sys

import ROOT
import FinalStateAnalysis.PatTools.data as data_tool
import FinalStateAnalysis.Utilities.styling as styling

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
    'm1Pt > 20',
    'm1AbsEta < 2.1',
    'm1MtToMET > 40',
    #'metEt > 30',
    'm1PFIDTight > 0.5',
    'm1RelPFIsoDB < 0.1',
    'm1Charge*m2Charge > 0',
    'muVetoPt5 < 0.5',
    # Fixme
    #'NIsoElecPt10_Nelectrons < 0.5',
    'tauVetoPt20 < 0.5',
    'abs(m1DZ) < 0.2'
]

qcd_selection = [
    'm1Pt > 20',
    'm1AbsEta < 2.1',
    'm1RelPFIsoDB > 0.3',
    'm1Charge*m2Charge > 0',
    'muVetoPt5 < 0.5',
    'bjetCSVVeto < 0.5',
    'metEt < 20',
    'tauVetoPt20 < 0.5',
    # Fixme
    #'NIsoElecPt10_Nelectrons < 0.5',
    'abs(m1DZ) < 0.2'
]

# In the emu channels, the muon is the second leg.
wjets_selection_emu = [
    x.replace('m1', 'm2') for x in wjets_selection
]
wjets_selection_tau = [
    x.replace('m2', 'Tau') for x in wjets_selection
]

qcd_selection_emu = [
    x.replace('m1', 'm2') for x in qcd_selection
]

fakerates = {
    'mu' : {
        'ntuple' : 'mm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'm2_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu',
        'base_cuts' : wjets_selection,
        'control_plots' : [
            #('Btag', 'm2JetBtag',
             #"Probe TCHE", [100, -5, 5]),
            #('metEt', 'metEt',
             #"metEt", [100, 0, 100]),
        ],
        'final_cuts' : [],
        'denom' : [
            'm2JetBtag < 3.3',
            'm2PixHits > 0.5',
            'doubleMuPass > 0.5',
            'm2Pt > 10',
            'm2AbsEta < 2.1',
            'abs(m1DZ) < 0.2',
            'abs(m2DZ) < 0.2',
        ],
        'num' : [
            'm2PFIDTight > 0.5',
            'm2RelPFIsoDB < 0.3',
        ]
    },
    'muHighPt' : {
        'ntuple' : 'mm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'm2_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu',
        'base_cuts' : wjets_selection,
        'control_plots' : [
            #('Btag', 'm2JetBtag',
             #"Probe TCHE", [100, -5, 5]),
            #('metEt', 'metEt',
             #"metEt", [100, 0, 100]),
        ],
        'final_cuts' : [],
        'denom' : [
            'm2JetBtag < 3.3',
            'm2PixHits > 0.5',
            'doubleMuPass > 0.5',
            'm2Pt > 20',
            'm2AbsEta < 2.1',
            'abs(m1DZ) < 0.2',
            'abs(m2DZ) < 0.2',
        ],
        'num' : [
            'm2PFIDTight > 0.5',
            'm2RelPFIsoDB < 0.3',
        ]
    },
    #'muHighPtTight' : {
        #'ntuple' : 'mm',
        #'pd' : 'data_DoubleMu',
        #'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        #'mc_pd' : 'Wjets',
        #'varname' : 'MuJetPt',
        #'vartitle' : 'Mu Jet Pt',
        #'var' : 'm2_JetPt',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 5,
        #'evtType' : '#mu#mu',
        #'base_cuts' : wjets_selection,
        #'control_plots' : [
            ##('Btag', 'm2JetBtag',
             ##"Probe TCHE", [100, -5, 5]),
            ##('metEt', 'metEt',
             ##"metEt", [100, 0, 100]),
        #],
        #'final_cuts' : [],
        #'denom' : [
            #'m2JetBtag < 3.3',
            #'m2PixHits > 0.5',
            #'doubleMuPass > 0.5',
            #'m2Pt > 20',
            #'m2AbsEta < 2.1',
            #'abs(m1DZ) < 0.2',
            #'abs(m2DZ) < 0.2',
        #],
        #'num' : [
            #'m2PFIDTight > 0.5',
            #'m2RelPFIsoDB < 0.15',
        #]
    #},
    'muQCD' : {
        'ntuple' : 'mm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'm2_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 10,
        'evtType' : '#mu#mu',
        'base_cuts' : qcd_selection,
        'control_plots' : [
            #('Btag', 'm2JetBtag',
             #"Probe TCHE", [100, -5, 5]),
        ],
        'final_cuts' : [],
        'denom' : [
            'm2JetBtag < 3.3',
            'm2PixHits > 0.5',
            'doubleMuPass > 0.5',
            'm2Pt > 9',
            'm2AbsEta < 2.1',
            'abs(m1DZ) < 0.2',
            'abs(m2DZ) < 0.2',
        ],
        'num' : [
            'm2PFIDTight > 0.5',
            'm2RelPFIsoDB < 0.3',
        ]
    },
    #'muTight' : {
        #'ntuple' : 'mm',
        #'pd' : 'data_DoubleMu',
        #'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        #'mc_pd' : 'Wjets',
        #'varname' : 'MuJetPt',
        #'vartitle' : 'Mu Jet Pt',
        #'var' : 'm2_JetPt',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 5,
        #'evtType' : '#mu#mu',
        #'base_cuts' : wjets_selection,
        #'control_plots' : [ ],
        #'final_cuts' : [],
        #'denom' : [
            #'m2JetBtag < 3.3',
            #'m2PixHits > 0.5',
            #'doubleMuPass > 0.5',
            #'m2Pt > 9',
            #'m2AbsEta < 2.1',
            #'abs(m1DZ) < 0.2',
            #'abs(m2DZ) < 0.2',
        #],
        #'num' : [
            #'m2PFIDTight > 0.5',
            #'m2RelPFIsoDB < 0.15',
        #]
    #},
    'muQCDHighPt' : {
        'ntuple' : 'mm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'MuJetPt',
        'vartitle' : 'Mu Jet Pt',
        'var' : 'm2_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 10,
        'evtType' : '#mu#mu',
        'base_cuts' : qcd_selection,
        'control_plots' : [
            #('Btag', 'm2JetBtag',
             #"Probe TCHE", [100, -5, 5]),
        ],
        'final_cuts' : [],
        'denom' : [
            'm2JetBtag < 3.3',
            'm2PixHits > 0.5',
            'doubleMuPass > 0.5',
            'm2Pt > 20',
            'm2AbsEta < 2.1',
            'abs(m1DZ) < 0.2',
            'abs(m2DZ) < 0.2',
        ],
        'num' : [
            'm2PFIDTight > 0.5',
            'm2RelPFIsoDB < 0.3',
        ]
    },
    #'muQCDHighPtTight' : {
        #'ntuple' : 'mm',
        #'pd' : 'data_DoubleMu',
        #'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        #'mc_pd' : 'QCDMu',
        #'varname' : 'MuJetPt',
        #'vartitle' : 'Mu Jet Pt',
        #'var' : 'm2_JetPt',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 10,
        #'evtType' : '#mu#mu',
        #'base_cuts' : qcd_selection,
        #'control_plots' : [
            ##('Btag', 'm2JetBtag',
             ##"Probe TCHE", [100, -5, 5]),
        #],
        #'final_cuts' : [],
        #'denom' : [
            #'m2JetBtag < 3.3',
            #'m2PixHits > 0.5',
            #'doubleMuPass > 0.5',
            #'m2Pt > 20',
            #'m2AbsEta < 2.1',
            #'abs(m1DZ) < 0.2',
            #'abs(m2DZ) < 0.2',
        #],
        #'num' : [
            #'m2PFIDTight > 0.5',
            #'m2RelPFIsoDB < 0.3',
            #'m2RelPFIsoDB < 0.15',
        #]
    #},
    #'muQCDTight' : {
        #'ntuple' : 'mm',
        #'pd' : 'data_DoubleMu',
        #'exclude' : ['*DoubleE*', '*MuEG*', '*SingleMu*'],
        #'mc_pd' : 'QCDMu',
        #'varname' : 'MuJetPt',
        #'vartitle' : 'Mu Jet Pt',
        #'var' : 'm2_JetPt',
        #'varbinning' : [100, 0, 100],
        #'rebin' : 10,
        #'evtType' : '#mu#mu',
        #'base_cuts' : qcd_selection,
        #'control_plots' : [ ],
        #'final_cuts' : [],
        #'denom' : [
            #'m2JetBtag < 3.3',
            #'m2PixHits > 0.5',
            #'doubleMuPass > 0.5',
            #'m2Pt > 10',
            #'m2AbsEta < 2.1',
            #'abs(m1DZ) < 0.2',
            #'abs(m2DZ) < 0.2',
        #],
        #'num' : [
            #'m2PFIDTight > 0.5',
            #'m2RelPFIsoDB < 0.15',
        #]
    #},
    'eMIT' : {
        'ntuple' : 'em',
        'pd' : 'data_MuEG',
        'exclude' : ['*DoubleE*', '*SingleMu*', '*DoubleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'EJetPt',
        'vartitle' : 'electron Jet Pt',
        'var' : 'electron_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : 'e#mu',
        'base_cuts' : wjets_selection_emu,
        'control_plots' : [
            #('Njets', 'NjetsPt20_Njets',
             #"Number of jets", [10, -0.5, 9.5]),
            #('Nbjets', 'bjetCSVVeto',
             #"Number of b-jets", [10, -0.5, 9.5]),
            #('AbsIso', 'electronRelPFIsoDB*electronPt',
             #"Absolute Iso", [100, 0, 20]),
        ],
        'final_cuts' : [
        ],
        'denom' : [
            'mu17ele8Pass > 0.5',
            'electronChargeIdTight > 0.5',
            'm2JetBtag < 0.5',
            'electronCharge*m2Charge > 0',
            'electronPt > 10',
            'electronAbsEta < 2.5',
            'electronJetBtag < 3.3',
            'abs(m2DZ) < 0.2',
            'abs(electronDZ) < 0.2',
            'electronMissingHits < 0.5',
            'electronHasConversion < 0.5',
            'electronMuOverlap < 0.5',
        ],
        'num' : [
            'electronMVAIDH2TauWP > 0.5',
            'electronRelPFIsoDB < 0.3',
        ]
    },
    'eQCDMIT' : {
        'ntuple' : 'em',
        'pd' : 'data_MuEG',
        'exclude' : ['*DoubleE*', '*SingleMu*', '*DoubleMu*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'EJetPt',
        'vartitle' : 'electron Jet Pt',
        'var' : 'electron_JetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : 'e#mu',
        'base_cuts' : qcd_selection_emu,
        'control_plots' : [
            #('Nhits', 'electronMissingHits',
             #"Number of hits", [10, -0.5, 9.5]),
            #('AbsIso', 'electronRelPFIsoDB*electronPt',
             #"Absolute Iso", [100, 0, 20]),
        ],
        'final_cuts' : [],
        'denom' : [
            'Mu17Ele8All_HLT > 0.5',
            'electronChargeIdTight > 0.5',
            'm2JetBtag < 0.5',
            'electronCharge*m2Charge > 0',
            'electronPt > 10',
            'electronAbsEta < 2.5',
            'electronJetBtag < 3.3',
            'abs(m2DZ) < 0.2',
            'abs(electronDZ) < 0.2',
            'electronMissingHits < 0.5',
            'electronHasConversion < 0.5',
            'electronMuOverlap < 0.5',
        ],
        'num' : [
            'electronMVAIDH2TauWP > 0.5',
            'electronRelPFIsoDB < 0.3',
        ]
    },
    'tau' : {
        'ntuple' : 'mt',
        'pd' : 'data_SingleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*DoubleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'tauJetPt',
        'vartitle' : 'Tau Jet Pt',
        'var' : 'tauJetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#tau',
        'base_cuts' : wjets_selection_tau,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'isoMuPass > 0.5',
            'tauCharge*m1Charge > 0',
            'tauPt > 20',
            'tauAbsEta < 2.3',
            'tauJetBtag < 3.3',
            'abs(tauDZ) < 0.2',
            'tauAntielectronMVA > 0.5',
            'tauAntiMuonTight > 0.5',
            # fixme
            #'tauMuOverlapGlb < 0.5',
            #'tau_electronOverlapWP95 < 0.5',
        ],
        'num' : [
            'tauLooseMVAIso > 0.5',
        ]
    },
    'tautauPt' : {
        'ntuple' : 'mt',
        'pd' : 'data_SingleMu',
        'exclude' : ['*DoubleE*', '*MuEG*', '*DoubleMu*'],
        'mc_pd' : 'Wjets',
        'varname' : 'tauPt',
        'vartitle' : 'tau p_{T}',
        'var' : 'tauPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#tau',
        'base_cuts' : wjets_selection_tau,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'isoMuPass > 0.5',
            'tauCharge*m1Charge > 0',
            'tauPt > 20',
            'tauAbsEta < 2.3',
            'tauJetBtag < 3.3',
            'abs(tauDZ) < 0.2',
            'tauAntielectronMVA > 0.5',
            # FIXME
            #'tauMuOverlapGlb < 0.5',
            #'tau_electronOverlapWP95 < 0.5',
            'tauAntiMuonTight > 0.5',
        ],
        'num' : [
            'tauLooseMVAIso > 0.5',
        ]
    },
}

# Hack to split by eta
varname_extractor = re.compile('(?P<var>\w+)AbsEta\s*<\s*[0-9\.]+')
for fr in list(fakerates.keys()):
    # For now, skip the eat split
    continue
    info = fakerates[fr]
    barrel_info_clone = copy.deepcopy(info)
    endcap_info_clone = copy.deepcopy(info)
    # Figure out variable name
    varname = None
    for cut in info['denom']:
        match = varname_extractor.match(cut)
        if match:
            varname = match.group('var')
    assert(varname)
    barrel_info_clone['denom'].append('%sAbsEta <= 1.48' % varname)
    endcap_info_clone['denom'].append('%sAbsEta > 1.48' % varname)
    fakerates[fr + '_endcap'] = endcap_info_clone
    fakerates[fr + '_barrel'] = barrel_info_clone

output_file = ROOT.TFile("results_singleMuFakeRates.root", "RECREATE")
for data_set, skips, int_lumi, puTag in [
    ('2011A', ['2011B', 'EM',], 2170, 'pu2011A'),
    #('2011B', ['2011A', 'EM'], 2170),
    ('2011AB', ['EM',], 4684, 'pu2011AB') ]:
    log.info("Plotting dataset: %s", data_set)

    samples, plotter = data_tool.build_data(
        'Mu', '2012-04-14-v1-MuonTP', 'scratch_results', int_lumi, skips,
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

        weight = '(%s)' % puTag

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

            cms_label = styling.cms_preliminary(int_lumi)
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
        cms_label = styling.cms_preliminary(int_lumi)
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
