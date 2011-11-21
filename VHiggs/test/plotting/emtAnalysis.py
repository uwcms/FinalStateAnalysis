'''

Implementation of e-mu-tau channel analysis

'''

import ROOT
import os
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles

logging.basicConfig(filename='emtAnalysis.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("emtChannel")

ROOT.gROOT.SetBatch(True)

#Define the fake rate versus muon pt

# Wjets FR
FAKE_RATE_0 = 1.28
FAKE_RATE_1 = 1.194e+1
FAKE_RATE_2 = 2.05
FAKE_RATE_3 = 1.47e-2

FAKE_RATE = "(%0.4f*TMath::Landau(VAR, %0.4f, %0.4f,0)+%0.4f)" % (
    FAKE_RATE_0, FAKE_RATE_1, FAKE_RATE_2, FAKE_RATE_3)

FR_X = 'Elec_JetPt'
FAKE_RATE = FAKE_RATE.replace('VAR', FR_X)
FR_WEIGHT = '((%s)/(1-%s))' % (FAKE_RATE, FAKE_RATE)

base_selection = [
    'MuPt > 18',
    'ElecPt > 9',
    'MuAbsEta < 2.1',
    'ElecAbsEta < 2.5',
    'Mu_MuRelIso < 0.3',
    'Mu_MuID_WWID > 0.5',
    'Mu17Ele8All_HLT > 0.5',
    # Object vetos
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NIsoElecPt10_Nelectrons < 0.5',
    'NBjetsPt20_Nbjets < 0.5',

    'Tau_LooseHPS > 0.5',
    'MuCharge*ElecCharge > 0',
    'Mu_MuBtag < 3.3',
    'MuDZ < 0.2',
    'ElecDZ < 0.2',
    'TauDZ < 0.2',
]

passes_ht = [
    'VisFinalState_Ht > 80'
]

passes_vtx = [
    'vtxChi2/vtxNDOF < 10'
]

bkg_enriched = [
    '(Elec_EID_WWID < 0.5 || Elec_ERelIso > 0.3)'
]

final_selection = [
    'Elec_EID_WWID > 0.5',
    'Elec_ERelIso < 0.3'
]

variables = {
#    'DiMuonMass' : ('Muon1_Muon2_Mass', 'M_{#mu#mu}', [100, 0, 300],),
    'ETauMass' : ('Elec_Tau_Mass', 'M_{e#tau}', [60, 0, 300],),
    #'Muon1_MtToMET' : ('Muon1_MtToMET', 'M_{T} #mu(1)-#tau', [60, 0, 300],),
#    'Muon2_MtToMET' : ('Muon2_MtToMET', 'M_{T} #mu(2)-#tau', [100, 0, 300],),
    'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NODF', [100, 0, 30],),
#    'MET' : ('METPt', 'MET', [100, 0, 200]),
    'HT' : ('VisFinalState_Ht', 'H_{T}', [60, 0, 300]),
}

selections = {
    'base_line' : {
        'select' : base_selection,
        'title' : "Base Selection",
        'vars' : [
            #'DiMuonMass',
            #'MuTauMass',
            #'Muon1_MtToMET',
            #'MET',
            #'HT',
            #'vtxChi2NODF',
        ],
    },
    'with_ht' : {
        'select' : base_selection + passes_ht,
        'title' : "Base Selection + H_{T}",
        'vars' : [
            'DiMuonMass',
            'MuTauMass',
            'Muon1_MtToMET',
            'vtxChi2NODF',
        ],
    },
    'with_vtx' : {
        'select' : base_selection + passes_vtx,
        'title' : "Base Selection + #chi^{2}",
        'vars' : [
            'HT',
        ],
    },
    'final' : {
        'title' : "Final Selection",
        'select' : base_selection + passes_ht + passes_vtx,
        'vars' : [
            'DiMuonMass',
            'ETauMass',
            'Muon1_MtToMET',
            'vtxChi2NODF',
        ],
    },
}

# Samples we aren't interested in
skips = ['DoubleEl', 'EM', ]
int_lumi = 4600
samples, plotter = data_tool.build_data(
    'VH', '2011-11-13-v1-WHAnalyze', 'scratch_results',
    int_lumi, skips, count='emt/skimCounter')

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
def saveplot(filename):
    # Save the current canvas
    filetype = '.pdf'
    #legend.Draw()
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'emtChannel', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'emtChannel', filename + '_log' + filetype))

################################################################################
###  Control plot: check integrated lumi   #####################################
################################################################################

# Version with weights applied
lumi = plotter.get_histogram( 'data_MuEG', '/emt/intLumi',)
lumi.Draw()
saveplot('intlumi')

# Data card output
data_card_file = ROOT.TFile("emt_shapes.root", 'RECREATE')

for selection, selection_info in selections.iteritems():
    log.info("Doing " + selection)

    log.info("Plotting distribution of FR weights")

    fr_selection = selection_info['select'] + bkg_enriched
    the_final_selection = selection_info['select'] + final_selection

    # Version with weights applied
    plotter.register_tree(
        selection + '_fr_weights',
        '/emt/final/Ntuple',
        FR_WEIGHT,
        ' && '.join(fr_selection),
        #w = '(%s)' % FR_WEIGHT,
        binning = [200, 0, 1],
        include = ['*data*'],
    )

    weight_histo = plotter.get_histogram(
        'data_MuEG',
        '/emt/final/Ntuple:' + selection + '_fr_weights',
        show_overflows = True,
    )
    weight_histo.Draw()
    saveplot(selection + '_fr_weights')

    for var in selection_info['vars']:
        if var not in variables:
            print "Skipping", var
            continue
        draw_str, x_title, binning = variables[var]

        # The "Loose" selection
        plotter.register_tree(
            selection + var + '_loose',
            '/emt/final/Ntuple',
            draw_str,
            ' && '.join(selection_info['select']),
            w = '(pu2011AB)',
            binning = binning,
            include = ['*'],
        )

        plotter.register_tree(
            selection + var + '_bkg',
            '/emt/final/Ntuple',
            draw_str,
            ' && '.join(fr_selection),
            w = '(pu2011AB)',
            binning = binning,
            include = ['*'],
        )

        # Version with weights applied
        plotter.register_tree(
            selection + var + '_bkg_fr',
            '/emt/final/Ntuple',
            draw_str,
            ' && '.join(fr_selection),
            w = '(pu2011AB)*(%s)' % FR_WEIGHT,
            binning = binning,
            include = ['*'],
        )

        plotter.register_tree(
            selection + var + '_fin',
            '/emt/final/Ntuple',
            draw_str,
            ' && '.join(the_final_selection),
            w = 'pu2011AB',
            binning = binning,
            include = ['*'],
        )

        legend = plotter.build_legend(
            '/mmt/skimCounter', exclude = ['data*', '*VH*'], drawopt='lf',
            xlow = 0.6, ylow=0.5,)

        rebin = 5

        ##########################################
        # Compute results using MC in loose region
        ##########################################
        histo_name = selection + var + '_loose'

        stack = plotter.build_stack(
            '/emt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*', '*VH*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_MuEG',
            '/emt/final/Ntuple:' + histo_name,
            rebin = rebin, show_overflows=True,
        )

        stack.Draw()
        data.Draw('same,pe')
        stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum()))
        stack.GetXaxis().SetTitle(x_title)
        legend.Draw()
        canvas.Update()
        saveplot(histo_name)

        ##########################################
        # Compute results using MC in final region
        ##########################################

        histo_name = selection + var + '_bkg'

        stack = plotter.build_stack(
            '/emt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_MuEG',
            '/emt/final/Ntuple:' + histo_name,
            rebin = rebin, show_overflows=True,
        )

        stack.Draw()
        data.Draw('same,pe')
        stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum()))
        stack.GetXaxis().SetTitle(x_title)
        legend.Draw()
        canvas.Update()
        saveplot(histo_name)

        histo_name = selection + var + '_fin'

        stack = plotter.build_stack(
            '/emt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_MuEG',
            '/emt/final/Ntuple:' + histo_name,
            rebin = rebin, show_overflows=True,
        )

        stack.Draw()
        data.Draw('same,pe')
        legend.Draw()
        stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum()))
        stack.GetXaxis().SetTitle(x_title)
        legend.Draw()
        canvas.Update()
        saveplot(histo_name)

        ##########################################
        # Compute results using FR metho
        ##########################################

        # The final selected events
        data = plotter.get_histogram(
            'data_MuEG',
            '/emt/final/Ntuple:' + selection + var + '_fin',
            rebin = rebin, show_overflows = True
        )

        # The unweighted background prediction
        data_bkg = plotter.get_histogram(
            'data_MuEG',
            '/emt/final/Ntuple:' + selection + var + '_bkg',
            rebin = rebin, show_overflows = True
        )

        # The background prediction
        data_bkg_fr = plotter.get_histogram(
            'data_MuEG',
            '/emt/final/Ntuple:' + selection + var + '_bkg_fr',
            rebin = rebin, show_overflows = True
        )

        corrected_mc = ['ZZ', 'WZ']
        corrected_mc_histos = []

        # Legend for FR plots
        legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.90, "", "brNDC")
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)

        # Now we need to correct the backgrounds which aren't correctly
        # estimated by the FR method.
        for to_correct in corrected_mc:
            mc_final = plotter.get_histogram(
                to_correct,
                '/emt/final/Ntuple:' + selection + var + '_fin',
                rebin = rebin, show_overflows = True
            )
            # Get the contribution from the FR method
            mc_bkg_fr = plotter.get_histogram(
                to_correct,
                '/emt/final/Ntuple:' + selection + var + '_bkg_fr',
                rebin = rebin, show_overflows = True
            )
            mc_correct = mc_final - mc_bkg_fr
            corrected_mc_histos.append(mc_correct)

        signal = plotter.get_histogram(
            'VH120',
            '/emt/final/Ntuple:' + selection + var + '_fin',
            rebin = rebin, show_overflows = True
        )

        stack = ROOT.THStack(selection + var + "FR_FINAL", "Final #mu#mu#tau selection")
        for histo_name, histo in zip(corrected_mc, corrected_mc_histos):
            stack.Add(histo.th1, 'hist')
            legend.AddEntry(histo.th1, histo_name, 'lf')

        styling.apply_style(data_bkg_fr, **samplestyles.SAMPLE_STYLES['ztt'])
        stack.Add(data_bkg_fr.th1, 'hist')

        signal = signal*5
        stack.Add(signal.th1, 'hist')
        stack.Draw()
        data.Draw('pe,same')
        stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum())*1.5)
        stack.GetXaxis().SetTitle(x_title)

        legend.AddEntry(data_bkg_fr.th1, "Fakes", 'lf')
        legend.AddEntry(signal.th1, "VH(120) #times 5", 'lf')
        legend.Draw()

        saveplot(selection + var + '_fr')

        # Now right data card histogram
        for mass in [100, 110, 115, 120, 125, 135, 140, 145, 160]:
            channel_dir = data_card_file.mkdir(
                "emt_%i_%s_%s" % (mass, selection, var))
            channel_dir.cd()
            data.Write('data_obs')
            data_bkg_fr.Write('fakes')
            data_bkg.Write('ext_data_unweighted')
            corrected_mc_histos[0].Write('zz')
            corrected_mc_histos[1].Write('wz')

            signal = plotter.get_histogram(
                'VH%s' % mass,
                '/emt/final/Ntuple:' + selection + var + '_fin',
                rebin = rebin, show_overflows=True,
            )
            signal.Write('signal')

