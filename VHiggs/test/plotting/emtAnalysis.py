'''

Implementation of e-mu-tau channel analysis

'''

import ROOT
import os
import json
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles

logging.basicConfig(filename='emtAnalysis.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("emtChannel")

ROOT.gROOT.SetBatch(True)

fake_rates_file = open('fake_rates.json')
fake_rates_info = json.load(fake_rates_file)

def get_fake_rate_weight(label, variable):
    # Load the appropriate function from the json file and use the correct
    # dependent variable
    fake_rate_fun = fake_rates_info[label]['fitted_func']
    fake_rate_fun = fake_rate_fun.replace('VAR', variable)
    weight = '((%s)/(1-%s))' % (fake_rate_fun, fake_rate_fun)
    return weight

# Wjets + ZMM FR
E_FR_WEIGHT = get_fake_rate_weight('eMIT', 'Elec_JetPt')
E_QCD_FR_WEIGHT = get_fake_rate_weight('eMITQCD', 'Elec_JetPt')

MU_FR_WEIGHT = get_fake_rate_weight('muHighPt', 'Mu_JetPt')
MU_QCD_FR_WEIGHT = get_fake_rate_weight('muHighPtQCDOnly', 'Mu_JetPt')

TAU_FR_WEIGHT = get_fake_rate_weight('tau', 'TauJetPt')

base_selection = [
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
    'Tau_ElectronMVA > 0.5',
]

passes_ht = [
    'VisFinalState_Ht > 80'
]

passes_vtx = [
    'vtxChi2/vtxNDOF < 10'
]

e_bkg_enriched = [
    '(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)',
    'Mu_MuRelIso < 0.3',
    'Mu_MuID_WWID > 0.5',
    'Tau_LooseHPS > 0.5',
]

mu_bkg_enriched = [
    '(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)',
    'Elec_EID_MITID > 0.5',
    'Elec_ERelIso < 0.3',
    'Tau_LooseHPS > 0.5',
]

tau_bkg_enriched = [
    'Mu_MuRelIso < 0.3',
    'Mu_MuID_WWID > 0.5',
    'Elec_EID_MITID > 0.5',
    'Elec_ERelIso < 0.3',
    'Tau_LooseHPS < 0.5',
]

e_mu_bkg_enriched = [
    '(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5) &&'
    '(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)',
    'Tau_LooseHPS > 0.5',
]

mu_tau_bkg_enriched = [
    '(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5) &&'
    'Tau_LooseHPS < 0.5',
    'Elec_EID_MITID > 0.5',
    'Elec_ERelIso < 0.3',
]

triple_bkg_enriched = [
    '(Mu_MuRelIso > 0.3 || Mu_MuID_WWID < 0.5)',
    '(Elec_EID_MITID < 0.5 || Elec_ERelIso > 0.3)',
    '(Tau_LooseHPS < 0.5)',
]

final_selection = [
    'Elec_EID_MITID > 0.5',
    'Elec_ERelIso < 0.3',
    'Mu_MuRelIso < 0.3',
    'Mu_MuID_WWID > 0.5',
    'Tau_LooseHPS > 0.5',
]

variables = {
#    'DiMuonMass' : ('Muon1_Muon2_Mass', 'M_{#mu#mu}', [100, 0, 300],),
    'ETauMass' : ('Elec_Tau_Mass', 'M_{e#tau}', [60, 0, 300], 5),
    #'Muon1_MtToMET' : ('Muon1_MtToMET', 'M_{T} #mu(1)-#tau', [60, 0, 300],),
#    'Muon2_MtToMET' : ('Muon2_MtToMET', 'M_{T} #mu(2)-#tau', [100, 0, 300],),
    'vtxChi2NODF' : ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NODF', [100, 0, 30], 5),
#    'electronMVA' : ('Elec_EID_MITID', 'MIT ID', [100, -2, 2],),
#    'MET' : ('METPt', 'MET', [100, 0, 200]),
    'Njets' : ('NjetsPt20_Njets', 'N_{jets}', [10, -0.5, 9.5], 1),
    'HT' : ('VisFinalState_Ht', 'L_{T}', [60, 0, 300], 5),
    'count' : ('1', 'Count', [1, 0, 1], 1),
    #'muIP3DS' : ('MuIPDS', '3D IP signficance', [50, 0, 20], 2),
    #'eIP3DS' : ('ElecIPDS', '3D IP signficance', [50, 0, 20], 2),
    #'tauIP3DS' : ('TauIPDS', '3D IP signficance', [50, 0, 20], 2),
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
            #'DiMuonMass',
            #'MuTauMass',
            #'Muon1_MtToMET',
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
            #'DiMuonMass',
            'ETauMass',
            'HT',
            #'Muon1_MtToMET',
            #'vtxChi2NODF',
            #'Njets',
            #'count',
            #'muIP3DS',
            #'eIP3DS',
            #'tauIP3DS',
        ],
    },
}

all_cuts = selections['final']['select'] + final_selection

# Determine which pair is SS
sign_categories = {
    'emu' : {
        'sign_cut' : ['ElecCharge*MuCharge > 0'],
        'fake1' : {
            'label' : 'e',
            'fr' : E_FR_WEIGHT,
            'region' : e_bkg_enriched,
            'qcdfr' : E_QCD_FR_WEIGHT,
        },
        'fake2' : {
            'label' : 'mu',
            'fr' : MU_FR_WEIGHT,
            'region' : mu_bkg_enriched,
            'qcdfr' : MU_QCD_FR_WEIGHT,
        },
        'fake3' : {
            'label' : 'tau',
            'fr' : TAU_FR_WEIGHT,
            'qcdfr' : TAU_FR_WEIGHT,
            'region' : tau_bkg_enriched,
        },
        'double' : {
            'fr' : [MU_FR_WEIGHT, E_FR_WEIGHT],
            'region' : e_mu_bkg_enriched,
        },
    },
    'mutau' : {
        'sign_cut' : ['TauCharge*MuCharge > 0'],
        'fake1' : {
            'label' : 'mu',
            'fr' : MU_FR_WEIGHT,
            'region' : mu_bkg_enriched,
            'qcdfr' : MU_QCD_FR_WEIGHT,
        },
        'fake2' : {
            'label' : 'tau',
            'fr' : TAU_FR_WEIGHT,
            'qcdfr' : TAU_FR_WEIGHT,
            'region' : tau_bkg_enriched,
        },
        'fake3' : {
            'label' : 'e',
            'fr' : E_FR_WEIGHT,
            'region' : e_bkg_enriched,
            'qcdfr' : E_QCD_FR_WEIGHT,
        },
        'double' : {
            'fr' : [MU_FR_WEIGHT, TAU_FR_WEIGHT],
            'region' : mu_tau_bkg_enriched,
        },
    }
}

if __name__ == "__main__":
    # Samples we aren't interested in
    skips = ['DoubleEl', 'EM', 'DoubleMu']
    int_lumi = 4600
    samples, plotter = data_tool.build_data(
        'VH', '2011-12-05-v1-WHAnalyze', 'scratch_results',
        int_lumi, skips, count='emt/skimCounter')

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

    for sign_label, sign_cfg in sign_categories.iteritems():
        def saveplot(filename):
            # Save the current canvas
            filetype = '.pdf'
            #legend.Draw()
            canvas.SetLogy(False)
            canvas.Update()
            canvas.Print(os.path.join(
                "plots", 'emtChannel', sign_label, filename + filetype))
            canvas.SetLogy(True)
            canvas.Update()
            canvas.Print(os.path.join(
                "plots", 'emtChannel', sign_label, filename + '_log' + filetype))

        ################################################################################
        ###  Control plot: check integrated lumi   #####################################
        ################################################################################

        # Version with weights applied
        lumi = plotter.get_histogram( 'data_MuEG', '/emt/intLumi',)
        lumi.Draw()
        saveplot('intlumi')

        ################################################################################
        ###  Get final run event numbers           #####################################
        ################################################################################

        log.info("Saving run-event numbers for final selected events")
        all_cuts_with_sign = all_cuts + sign_cfg['sign_cut']
        # Get run/evt numbers for final event selection
        run_evts = plotter.get_run_lumi_evt(
            '/emt/final/Ntuple',
            ' && '.join(all_cuts_with_sign),
            include = '*data*'
        )
        with open('emt_events.json', 'w') as run_evt_file:
            run_evt_file.write(json.dumps(run_evts, indent=4))

        # Data card output
        data_card_file = ROOT.TFile("emt_%s_shapes.root" % sign_label, 'RECREATE')

        for selection, selection_info in selections.iteritems():
            log.info("Doing " + selection)
            selection += " %s" % sign_label

            log.info("Plotting distribution of FR weights")

            sign_cut = sign_cfg['sign_cut']
            fake1_fr_selection = selection_info['select'] + sign_cut + sign_cfg['fake1']['region']
            fake2_fr_selection = selection_info['select'] + sign_cut + sign_cfg['fake2']['region']
            double_fr_selection = selection_info['select'] + sign_cut + sign_cfg['double']['region']
            triple_fr_selection = selection_info['select'] + sign_cut + triple_bkg_enriched
            the_final_selection = selection_info['select'] + sign_cut + final_selection

            ## Version with weights applied
            #plotter.register_tree(
                #selection + '_fr_weights',
                #'/emt/final/Ntuple',
                #E_FR_WEIGHT,
                #' && '.join(e_fr_selection),
                ##w = '(%s)' % E_FR_WEIGHT,
                #binning = [200, 0, 1],
                #include = ['*data*'],
            #)

            #weight_histo = plotter.get_histogram(
                #'data_MuEG',
                #'/emt/final/Ntuple:' + selection + '_fr_weights',
                #show_overflows = True,
            #)
            #weight_histo.Draw()
            #saveplot(selection + '_fr_weights')

            for var in selection_info['vars']:
                if var not in variables:
                    print "Skipping", var
                    continue
                draw_str, x_title, binning, rebin = variables[var]

                # The "Loose" selection
                plotter.register_tree(
                    selection + var + '_loose',
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(selection_info['select'] + sign_cut),
                    w = '(pu2011AB)',
                    binning = binning,
                    include = ['*'],
                )

                plotter.register_tree(
                    selection + var + '_%s_bkg' % sign_cfg['fake1']['label'],
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(fake1_fr_selection),
                    w = '(pu2011AB)',
                    binning = binning,
                    include = ['*'],
                )

                # Version with weights applied
                plotter.register_tree(
                    selection + var + '_%s_bkg_fr' % sign_cfg['fake1']['label'],
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(fake1_fr_selection),
                    w = '(pu2011AB)*(%s)' % sign_cfg['fake1']['fr'],
                    binning = binning,
                    include = ['*'],
                )

                plotter.register_tree(
                    selection + var + '_%s_bkg' % sign_cfg['fake2']['label'],
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(fake2_fr_selection),
                    w = '(pu2011AB)',
                    binning = binning,
                    include = ['*'],
                )

                # Version with weights applied
                plotter.register_tree(
                    selection + var + '_%s_bkg_fr' % sign_cfg['fake2']['label'],
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(fake2_fr_selection),
                    w = '(pu2011AB)*(%s)' % sign_cfg['fake2']['fr'],
                    binning = binning,
                    include = ['*'],
                )

                plotter.register_tree(
                    selection + var + '_double_bkg',
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(double_fr_selection),
                    w = '(pu2011AB)',
                    binning = binning,
                    include = ['*'],
                )

                # Version with weights applied
                plotter.register_tree(
                    selection + var + '_double_bkg_fr',
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(double_fr_selection),
                    w = '(pu2011AB)*(%s)*(%s)' % (
                        sign_cfg['fake1']['fr'], sign_cfg['fake2']['fr'],),
                    binning = binning,
                    include = ['*'],
                )

                # Get the triple background (QCD) extrapolated into the electron bkg region
                plotter.register_tree(
                    selection + var + '_triple_bkg_to_%s_bkg_fr' % sign_cfg['fake1']['label'],
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(triple_fr_selection),
                    w = '(pu2011AB)*(%s)*(%s)' % (sign_cfg['fake2']['qcdfr'], sign_cfg['fake3']['qcdfr']),
                    binning = binning,
                    include = ['*'],
                )

                # Get the triple background (QCD) extrapolated into the mu bkg region
                plotter.register_tree(
                    selection + var + '_triple_bkg_to_%s_bkg_fr' % sign_cfg['fake2']['label'],
                    '/emt/final/Ntuple',
                    draw_str,
                    ' && '.join(triple_fr_selection),
                    w = '(pu2011AB)*(%s)*(%s)' % (sign_cfg['fake1']['qcdfr'], sign_cfg['fake3']['qcdfr']),
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

                histo_name = selection + var + '_%s_bkg' % sign_cfg['fake1']['label']

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

                data_triple_bkg_in_fake1_bkg_fr = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_triple_bkg_to_%s_bkg_fr' % sign_cfg['fake1']['label'],
                    rebin = rebin, show_overflows = True
                )

                stack.Draw()
                data.Draw('same,pe')
                #data_triple_bkg_in_mu_bkg_fr.Draw('same,hist')
                stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum()))
                stack.GetXaxis().SetTitle(x_title)
                legend.Draw()
                canvas.Update()
                saveplot(histo_name)

                data.Draw('pe')
                data_triple_bkg_in_fake1_bkg_fr.SetLineColor(ROOT.EColor.kRed)
                data_triple_bkg_in_fake1_bkg_fr.SetLineWidth(2)
                data_triple_bkg_in_fake1_bkg_fr.Draw('same,hist')
                data.SetMaximum(2*max(data.GetMaximum(),
                                    data_triple_bkg_in_fake1_bkg_fr.GetMaximum()))
                triple_legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.90, "", "brNDC")
                triple_legend.SetBorderSize(0)
                triple_legend.SetFillStyle(0)
                triple_legend.AddEntry(data.th1, "fake1 anti-iso region", "pe")
                triple_legend.AddEntry(data_triple_bkg_in_fake1_bkg_fr.th1, "Triple fakes", "l")
                triple_legend.Draw()
                saveplot(histo_name + '_with_qcd')

                histo_name = selection + var + '_%s_bkg' % sign_cfg['fake2']['label']

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

                data_triple_bkg_in_fake2_bkg_fr = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_triple_bkg_to_%s_bkg_fr' % sign_cfg['fake2']['label'],
                    rebin = rebin, show_overflows = True
                )

                stack.Draw()
                data.Draw('same,pe')
                #data_triple_bkg_in_mu_bkg_fr.Draw('same,hist')
                stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum()))
                stack.GetXaxis().SetTitle(x_title)
                legend.Draw()
                canvas.Update()
                saveplot(histo_name)

                data.Draw('pe')
                data_triple_bkg_in_fake2_bkg_fr.SetLineColor(ROOT.EColor.kRed)
                data_triple_bkg_in_fake2_bkg_fr.SetLineWidth(2)
                data_triple_bkg_in_fake2_bkg_fr.Draw('same,hist')
                data.SetMaximum(2*max(data.GetMaximum(),
                                    data_triple_bkg_in_fake2_bkg_fr.GetMaximum()))
                triple_legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.90, "", "brNDC")
                triple_legend.SetBorderSize(0)
                triple_legend.SetFillStyle(0)
                triple_legend.AddEntry(data.th1, "fake2 anti-iso region", "pe")
                triple_legend.AddEntry(data_triple_bkg_in_fake2_bkg_fr.th1, "Triple fakes", "l")
                triple_legend.Draw()
                saveplot(histo_name + '_with_qcd')


                histo_name = selection + var + '_fin'

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
                data_fake1_bkg = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_%s_bkg' % sign_cfg['fake1']['label'],
                    rebin = rebin, show_overflows = True
                )

                # The background prediction
                data_fake1_bkg_fr = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_%s_bkg_fr' % sign_cfg['fake1']['label'],
                    rebin = rebin, show_overflows = True
                )

                # The unweighted background prediction
                data_fake2_bkg = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_%s_bkg' % sign_cfg['fake2']['label'],
                    rebin = rebin, show_overflows = True
                )

                # The background prediction
                data_fake2_bkg_fr = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_%s_bkg_fr' % sign_cfg['fake2']['label'],
                    rebin = rebin, show_overflows = True
                )

                # The background prediction from double fakes
                data_double_bkg_fr = plotter.get_histogram(
                    'data_MuEG',
                    '/emt/final/Ntuple:' + selection + var + '_double_bkg_fr',
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
                    mc_fake2_bkg_fr = plotter.get_histogram(
                        to_correct,
                        '/emt/final/Ntuple:' + selection + var + '_%s_bkg_fr' % sign_cfg['fake2']['label'],
                        rebin = rebin, show_overflows = True
                    )
                    mc_fake1_bkg_fr = plotter.get_histogram(
                        to_correct,
                        '/emt/final/Ntuple:' + selection + var + '_%s_bkg_fr' % sign_cfg['fake1']['label'],
                        rebin = rebin, show_overflows = True
                    )
                    mc_correct = mc_final - mc_fake2_bkg_fr
                    mc_correct = mc_correct - mc_fake1_bkg_fr
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

                styling.apply_style(data_fake1_bkg_fr, **samplestyles.SAMPLE_STYLES['ztt'])
                stack.Add(data_fake1_bkg_fr.th1, 'hist')
                styling.apply_style(data_fake2_bkg_fr, **samplestyles.SAMPLE_STYLES['QCD*'])
                stack.Add(data_fake2_bkg_fr.th1, 'hist')

                signal = signal*5
                stack.Add(signal.th1, 'hist')
                stack.Draw()
                data.Draw('pe,same')
                data_double_bkg_fr.SetMarkerColor(ROOT.EColor.kRed)
                data_double_bkg_fr.Draw('pe, same')
                stack.SetMaximum(max(stack.GetHistogram().GetMaximum(), data.GetMaximum())*1.5)
                stack.GetXaxis().SetTitle(x_title)

                legend.AddEntry(data_fake1_bkg_fr.th1, "e fakes", 'lf')
                legend.AddEntry(data_fake2_bkg_fr.th1, "#mu fakes", 'lf')
                legend.AddEntry(signal.th1, "VH(120) #times 5", 'lf')
                legend.Draw()

                saveplot(selection + var + '_fr')

                # Now right data card histogram
                for mass in [100, 110, 115, 120, 125, 135, 140, 145, 160]:
                    channel_dir = data_card_file.mkdir(
                        "emt_%i_%s_%s" % (mass, selection, var))
                    channel_dir.cd()
                    data.SetName('data_obs'); data.Write()
                    data_fake1_bkg_fr.SetName('e_fakes'); data_fake1_bkg_fr.Write()
                    data_fake1_bkg.SetName('e_ext_data_unweighted'); data_fake1_bkg.Write()
                    data_fake2_bkg_fr.SetName('mu_fakes'); data_fake2_bkg_fr.Write()
                    data_fake2_bkg.SetName('mu_ext_data_unweighted'); data_fake2_bkg.Write()
                    corrected_mc_histos[0].SetName('zz'); corrected_mc_histos[0].Write()
                    corrected_mc_histos[1].SetName('wz'); corrected_mc_histos[1].Write()

                    signal = plotter.get_histogram(
                        'VH%s' % mass,
                        '/emt/final/Ntuple:' + selection + var + '_fin',
                        rebin = rebin, show_overflows=True,
                    )
                    signal.SetName('signal'); signal.Write()

