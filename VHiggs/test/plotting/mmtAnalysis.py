'''

Implementation of mu-mu-tau channel analysis

'''

import ROOT
import os
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles

logging.basicConfig(filename='mmtAnalysis.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("mmtChannel")

ROOT.gROOT.SetBatch(True)

#Define the fake rate versus muon pt for the subleading muon
SUB_FAKE_RATE_0 = 3.174
SUB_FAKE_RATE_1 = 14.99
SUB_FAKE_RATE_2 = 2.47
SUB_FAKE_RATE_3 = 6.75e-3

SUB_FAKE_RATE = "(%0.4f*TMath::Landau(VAR, %0.4f, %0.4f,0)+%0.4f)" % (
    SUB_FAKE_RATE_0, SUB_FAKE_RATE_1, SUB_FAKE_RATE_2, SUB_FAKE_RATE_3)

SUB_FR_X = 'Muon2_JetPt'
SUB_FAKE_RATE = SUB_FAKE_RATE.replace('VAR', SUB_FR_X)
SUB_FR_WEIGHT = '((%s)/(1-%s))' % (SUB_FAKE_RATE, SUB_FAKE_RATE)

LEAD_FAKE_RATE_0 = 4.5
LEAD_FAKE_RATE_1 = 26.6
LEAD_FAKE_RATE_2 = 3.59
LEAD_FAKE_RATE_3 = 1.01e-2

LEAD_FAKE_RATE = "(%0.4f*TMath::Landau(VAR, %0.4f, %0.4f,0)+%0.4f)" % (
    LEAD_FAKE_RATE_0, LEAD_FAKE_RATE_1, LEAD_FAKE_RATE_2, LEAD_FAKE_RATE_3)

LEAD_FR_X = 'Muon1_JetPt'
LEAD_FAKE_RATE = LEAD_FAKE_RATE.replace('VAR', LEAD_FR_X)
LEAD_FR_WEIGHT = '((%s)/(1-%s))' % (LEAD_FAKE_RATE, LEAD_FAKE_RATE)

base_selection = [
    #'(run < 5 && Muon1Pt > 13.5 || Muon1Pt > 13.365)',
    #'(run < 5 && Muon2Pt > 9 || Muon2Pt > 8.91)',
    'Muon1Pt > 18',
    'Muon2Pt > 9',
    'Muon1AbsEta < 2.1',
    'Muon2AbsEta < 2.1',
    'DoubleMus_HLT > 0.5 ',

    # Object vetos
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NIsoElecPt10_Nelectrons < 0.5',
    'NBjetsPt20_Nbjets < 0.5',

    #'NIsoTausPt20_NIsoTaus < 0.5',
    #'TauPt > 20',
    'Tau_LooseHPS > 0.5',
    'Muon1Charge*Muon2Charge > 0',
    'Muon2_InnerNPixHits > 0.5',
    'Muon1_InnerNPixHits > 0.5',
    'Muon1DZ < 0.2',
    'Muon2DZ < 0.2',
    'TauDZ < 0.2',
]

passes_ht = [
    'VisFinalState_Ht > 80'
]

passes_vtx = [
    'vtxChi2/vtxNDOF < 10',
    'Muon2_MuBtag < 3.3',
    'Muon1_MuBtag < 3.3',
]

sub_bkg_enriched = [
    '(Muon2_MuID_WWID < 0.5 || Muon2_MuRelIso > 0.3)',
    'Muon1_MuRelIso < 0.3',
    'Muon1_MuID_WWID > 0.5',
]

lead_bkg_enriched = [
    '(Muon1_MuID_WWID < 0.5 || Muon1_MuRelIso > 0.3)',
    'Muon2_MuRelIso < 0.3',
    'Muon2_MuID_WWID > 0.5',
]

final_selection = [
    'Muon2_MuID_WWID > 0.5',
    'Muon2_MuRelIso < 0.3',
    'Muon1_MuRelIso < 0.3',
    'Muon1_MuID_WWID > 0.5',
]

variables = {
    'DiMuonMass' : ('Muon1_Muon2_Mass', 'M_{#mu#mu}', [100, 0, 300], 5),
    'MuTauMass' : ('Muon2_Tau_Mass', 'M_{#mu#tau}', [60, 0, 300], 5),
    'Muon1_MtToMET' : ('Muon1_MtToMET', 'M_{T} #mu(1)-#tau', [60, 0, 300], 5),
    'Muon2_Btag' : ('Muon2_MuBtag', 'Sub leading mu btag', [120, -30, 30], 5),
#    'Muon2_MtToMET' : ('Muon2_MtToMET', 'M_{T} #mu(2)-#tau', [100, 0, 300],),
    'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NODF', [100, 0, 30], 5),
#    'MET' : ('METPt', 'MET', [100, 0, 200]),
    'Njets' : ('NjetsPt20_Njets', 'N_{jets}', [10, -0.5, 9.5], 1),
    'HT' : ('VisFinalState_Ht', 'L_{T}', [60, 0, 300], 5),
    'count' : ('1', 'Count', [1, 0, 1], 1),
    'mu1IP3DS' : ('Muon1IPDS', '3D IP signficance', [50, 0, 20], 2),
    'mu2IP3DS' : ('Muon2IPDS', '3D IP signficance', [50, 0, 20], 2),
    'tauIP3DS' : ('TauIPDS', '3D IP signficance', [50, 0, 20], 2),
}

selections = {
    'base_line' : {
        'select' : base_selection,
        'title' : "Base Selection",
        'vars' : [
            #'DiMuonMass',
            #'MuTauMass',
            #'Muon1_MtToMET',
            #'Muon2_Btag',
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
            'Muon2_Btag',
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
            'MuTauMass',
            'Muon1_MtToMET',
            'vtxChi2NODF',
            'Muon2_Btag',
            'Njets',
            'count',
            'muIP3DS',
            'eIP3DS',
            'tauIP3DS',
        ],
    },
}

# Samples we aren't interested in
skips = ['MuEG', 'DoubleEl', 'EM',]
int_lumi = 4600
samples, plotter = data_tool.build_data(
    'VH', '2011-11-27-v1-WHAnalyze', 'scratch_results',
    int_lumi, skips, count='emt/skimCounter')

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
def saveplot(filename):
    # Save the current canvas
    filetype = '.pdf'
    #legend.Draw()
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'mmtChannel', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'mmtChannel', filename + '_log' + filetype))

################################################################################
###  Control plot: check integrated lumi   #####################################
################################################################################

# Version with weights applied
lumi = plotter.get_histogram( 'data_DoubleMu', '/mmt/intLumi',)
lumi.Draw()
saveplot('intlumi')

################################################################################
###  Get final run event numbers           #####################################
################################################################################

log.info("Saving run-event numbers for final selected events")
# Get run/evt numbers for final event selection
all_cuts = ' && '.join(selections['final']['select'] + final_selection)
plotter.scan_to_file(
    'mmt_channel_evts',
    '/mmt/final/Ntuple',
    'run:lumi:evt',
    all_cuts,
    include = '*data*'
)

# Data card output
data_card_file = ROOT.TFile("mmt_shapes.root", 'RECREATE')

for selection, selection_info in selections.iteritems():
    log.info("Doing " + selection)

    log.info("Plotting distribution of FR weights")

    sub_fr_selection = selection_info['select'] + sub_bkg_enriched
    lead_fr_selection = selection_info['select'] + lead_bkg_enriched
    the_final_selection = selection_info['select'] + final_selection

    # Version with weights applied
    plotter.register_tree(
        selection + '_fr_weights',
        '/mmt/final/Ntuple',
        SUB_FR_WEIGHT,
        ' && '.join(sub_fr_selection),
        #w = '(%s)' % FR_WEIGHT,
        binning = [200, 0, 1],
        include = ['*data*'],
    )

    weight_histo = plotter.get_histogram(
        'data_DoubleMu',
        '/mmt/final/Ntuple:' + selection + '_fr_weights',
        show_overflows = True,
    )
    weight_histo.Draw()
    saveplot(selection + '_fr_weights')

    for var in selection_info['vars']:
        if var not in variables:
            print "Skipping", var
            continue
        draw_str, x_title, binning, rebin = variables[var]

        # The "Loose" selection
        plotter.register_tree(
            selection + var + '_loose',
            '/mmt/final/Ntuple',
            draw_str,
            ' && '.join(selection_info['select']),
            w = '(pu2011AB)',
            binning = binning,
            include = ['*'],
        )

        plotter.register_tree(
            selection + var + '_lead_bkg',
            '/mmt/final/Ntuple',
            draw_str,
            ' && '.join(lead_fr_selection),
            w = '(pu2011AB)',
            binning = binning,
            include = ['*'],
        )

        # Version with weights applied
        plotter.register_tree(
            selection + var + '_lead_bkg_fr',
            '/mmt/final/Ntuple',
            draw_str,
            ' && '.join(lead_fr_selection),
            w = '(pu2011AB)*(%s)' % LEAD_FR_WEIGHT,
            binning = binning,
            include = ['*'],
        )

        plotter.register_tree(
            selection + var + '_sub_bkg',
            '/mmt/final/Ntuple',
            draw_str,
            ' && '.join(sub_fr_selection),
            w = '(pu2011AB)',
            binning = binning,
            include = ['*'],
        )

        # Version with weights applied
        plotter.register_tree(
            selection + var + '_sub_bkg_fr',
            '/mmt/final/Ntuple',
            draw_str,
            ' && '.join(sub_fr_selection),
            w = '(pu2011AB)*(%s)' % SUB_FR_WEIGHT,
            binning = binning,
            include = ['*'],
        )

        plotter.register_tree(
            selection + var + '_fin',
            '/mmt/final/Ntuple',
            draw_str,
            ' && '.join(the_final_selection),
            w = 'pu2011AB',
            binning = binning,
            include = ['*'],
        )

        legend = plotter.build_legend(
            '/mmt/skimCounter', exclude = ['data*', '*VH*'], drawopt='lf',
            xlow = 0.6, ylow=0.5,)

        ##########################################
        # Compute results using MC in loose region
        ##########################################
        histo_name = selection + var + '_loose'

        stack = plotter.build_stack(
            '/mmt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*', '*VH*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + histo_name,
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

        histo_name = selection + var + '_lead_bkg'

        stack = plotter.build_stack(
            '/mmt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*', '*VH*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + histo_name,
            rebin = rebin, show_overflows=True,
        )

        stack.Draw()
        data.Draw('same,pe')
        stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum()))
        stack.GetXaxis().SetTitle(x_title)
        legend.Draw()
        canvas.Update()
        saveplot(histo_name)

        histo_name = selection + var + '_sub_bkg'

        stack = plotter.build_stack(
            '/mmt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*', '*VH*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + histo_name,
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
            '/mmt/final/Ntuple:' + histo_name,
            include = ['*'],
            exclude = ['data*', '*VH*'],
            rebin = rebin, show_overflows=True,
        )

        data = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + histo_name,
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
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + selection + var + '_fin',
            rebin = rebin, show_overflows = True
        )

        # The unweighted background prediction
        data_sub_bkg = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + selection + var + '_sub_bkg',
            rebin = rebin, show_overflows = True
        )

        # The background prediction
        data_sub_bkg_fr = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + selection + var + '_sub_bkg_fr',
            rebin = rebin, show_overflows = True
        )

        # The unweighted background prediction
        data_lead_bkg = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + selection + var + '_lead_bkg',
            rebin = rebin, show_overflows = True
        )

        # The background prediction
        data_lead_bkg_fr = plotter.get_histogram(
            'data_DoubleMu',
            '/mmt/final/Ntuple:' + selection + var + '_lead_bkg_fr',
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
                '/mmt/final/Ntuple:' + selection + var + '_fin',
                rebin = rebin, show_overflows = True
            )
            # Get the contribution from the FR method
            mc_sub_bkg_fr = plotter.get_histogram(
                to_correct,
                '/mmt/final/Ntuple:' + selection + var + '_sub_bkg_fr',
                rebin = rebin, show_overflows = True
            )
            mc_lead_bkg_fr = plotter.get_histogram(
                to_correct,
                '/mmt/final/Ntuple:' + selection + var + '_lead_bkg_fr',
                rebin = rebin, show_overflows = True
            )
            mc_correct = mc_final - mc_sub_bkg_fr
            mc_correct = mc_correct - mc_lead_bkg_fr
            corrected_mc_histos.append(mc_correct)

        signal = plotter.get_histogram(
            'VH120',
            '/mmt/final/Ntuple:' + selection + var + '_fin',
            rebin = rebin, show_overflows = True
        )

        stack = ROOT.THStack(selection + var + "FR_FINAL", "Final #mu#mu#tau selection")
        for histo_name, histo in zip(corrected_mc, corrected_mc_histos):
            stack.Add(histo.th1, 'hist')
            legend.AddEntry(histo.th1, histo_name, 'lf')

        styling.apply_style(data_sub_bkg_fr, **samplestyles.SAMPLE_STYLES['ztt'])
        stack.Add(data_sub_bkg_fr.th1, 'hist')
        styling.apply_style(data_lead_bkg_fr, **samplestyles.SAMPLE_STYLES['zll'])
        stack.Add(data_lead_bkg_fr.th1, 'hist')

        signal = signal*5
        stack.Add(signal.th1, 'hist')
        stack.Draw()
        data.Draw('pe,same')
        stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum())*1.5)
        stack.GetXaxis().SetTitle(x_title)

        legend.AddEntry(data_lead_bkg_fr.th1, "#mu_{1} fakes", 'lf')
        legend.AddEntry(data_sub_bkg_fr.th1, "#mu_{2} fakes", 'lf')
        legend.AddEntry(signal.th1, "VH(120) #times 5", 'lf')
        legend.Draw()

        saveplot(selection + var + '_fr')

        # Now right data card histogram
        for mass in [100, 110, 115, 120, 125, 135, 140, 145, 160]:
            channel_dir = data_card_file.mkdir(
                "mmt_%i_%s_%s" % (mass, selection, var))
            channel_dir.cd()
            data.SetName('data_obs'); data.Write()
            data_sub_bkg_fr.SetName('sub_fakes'); data_sub_bkg_fr.Write()
            data_sub_bkg.SetName('sub_ext_data_unweighted'); data_sub_bkg.Write()
            data_lead_bkg_fr.SetName('lead_fakes'); data_lead_bkg_fr.Write()
            data_lead_bkg.SetName('lead_ext_data_unweighted'); data_lead_bkg.Write()
            corrected_mc_histos[0].SetName('zz'); corrected_mc_histos[0].Write()
            corrected_mc_histos[1].SetName('wz'); corrected_mc_histos[1].Write()

            signal = plotter.get_histogram(
                'VH%s' % mass,
                '/mmt/final/Ntuple:' + selection + var + '_fin',
                rebin = rebin, show_overflows=True,
            )
            signal.SetName('signal'); signal.Write()
