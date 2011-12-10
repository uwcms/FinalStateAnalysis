'''

Analyze trilepton WH(tautau) events.

Author: Evan K. Friis, UW Madison

Analysis is configured by analysis_cfg.py

'''

import ROOT
import os
import json
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool
from analysis_cfg import cfg

# Setup logging
logging.basicConfig(
    filename='analysis.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("analysis")
stderr_log = logging.StreamHandler()
log.addHandler(stderr_log)

if __name__ == "__main__":
    ############################################################################
    ### Load the data ##########################################################
    ############################################################################
    int_lumi = 4600
    skips = ['DoubleEl', 'EM']
    samples, plotter = data_tool.build_data(
        'VH', '2011-12-05-v1-WHAnalyze', 'scratch_results',
        int_lumi, skips, count='emt/skimCounter')

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

    legend = plotter.build_legend(
        '/mmt/skimCounter', exclude = ['data*', '*VH*'], drawopt='lf',
        xlow = 0.6, ylow=0.5,)

    ############################################################################
    ### Loop over all channels to analyze  #####################################
    ############################################################################
    for channel, channel_cfg in cfg.iteritems():
        log.info("Analyzing channel: %s", channel)
        # Unpack the configuration
        ntuple = channel_cfg['ntuple']
        # A dictionary describing how to plot variables
        variables = channel_cfg['variables']
        # The baseline selection
        baseline = channel_cfg['baseline']
        # Get samples to exclude
        exclude = channel_cfg['exclude']
        # Get primary dataset
        primds = channel_cfg['primds']

        ########################################################################
        ### Loop over all charge configurations ################################
        ########################################################################
        for charge_cat, charge_cat_cfg in channel_cfg['charge_categories'].iteritems():
            log.info("-- charge category: %s", charge_cat)
            # Any extra selections specific to this charge_cat.  The charge
            # selection should be included in this.  This is an extension of the
            # "baseline"
            extra_selections = charge_cat_cfg['cat_baseline']
            # The final analysis cuts
            final_selections = charge_cat_cfg['selections']['final']['cuts']

            # Get the configuration for the fake objects
            object1_cfg = charge_cat_cfg['object1']
            object2_cfg = charge_cat_cfg['object2']
            object3_cfg = charge_cat_cfg['object3']

            ####################################################################
            ### First, select the final events #################################
            ####################################################################
            log.info("---- selecting final events in data...")
            ultimate_selection = baseline + extra_selections + final_selections\
                    + object1_cfg['pass'] + object2_cfg['pass'] + \
                    object3_cfg['pass']

            run_evts = plotter.get_run_lumi_evt(
                ntuple, ' && '.join(ultimate_selection),
                include='*data*', exclude=exclude
            )
            run_event_filename = '%s_%s_events.json' % (channel, charge_cat)
            with open(run_event_filename, 'w') as run_evt_file:
                run_evt_file.write(json.dumps(run_evts, indent=4))

            ####################################################################
            ### Now, loop over each selection type  ############################
            ####################################################################
            selection_cfgs = charge_cat_cfg['selections']
            for selection_name, selection_cfg in selection_cfgs.iteritems():
                log.info("---- now running selection %s", selection_name)

                def saveplot(filename):
                    # Save the current canvas
                    filetype = '.pdf'
                    #legend.Draw()
                    canvas.SetLogy(False)
                    canvas.Update()
                    filename = os.path.join("plots", channel, charge_cat,
                                            filename + filetype)
                    canvas.Print(filename)
                    canvas.SetLogy(True)
                    canvas.Update()
                    canvas.Print(filename.replace(filetype, '_log' + filetype))

                # Cuts in this selection
                extra_cuts = selection_cfg['cuts']
                vars_to_draw = selection_cfg['vars']

                for var in vars_to_draw:
                    log.info("------ doing variable %s", var)
                    plot_base_name = '_'.join(
                        [channel, charge_cat, selection_name, var])
                    if var not in variables:
                        log.info("------- skipping variable %s!", var)
                        continue

                    # Unpack variable info
                    to_plot, xaxis_title, binning, rebin = variables[var]

                    def register_tree(label, the_selections, weight):
                        plotter.register_tree(
                            plot_base_name + '_' + label,
                            ntuple,
                            to_plot,
                            ' && '.join(the_selections),
                            w = weight,
                            binning = binning,
                            include = ['*'],
                            exclude = exclude,
                        )

                    ############################################################
                    ### Loose and ultimate selections ##########################
                    ############################################################
                    # Make the loose selection
                    log.info("------ running loose selection...")
                    loose_selection = baseline + extra_selections + extra_cuts
                    register_tree('loose', loose_selection, '(pu2011AB)')

                    log.info("------ running ultimate selection...")
                    # Make the ultimate selection
                    ult_selection = baseline + extra_selections + extra_cuts \
                            + object1_cfg['pass'] \
                            + object2_cfg['pass'] \
                            + object3_cfg['pass']
                    register_tree('ult', ult_selection, '(pu2011AB)')

                    ############################################################
                    ### Compute fake rate estimates ############################
                    ############################################################

                    log.info("------ running fake object #1 enriched selection...")
                    # Make the fake1 enriched
                    fr1en_selection = baseline + extra_selections + extra_cuts \
                            + object1_cfg['fail'] \
                            + object2_cfg['pass'] \
                            + object3_cfg['pass']
                    register_tree('fr1en', fr1en_selection, '(pu2011AB)')

                    log.info("------ apply fake object #1 EWK weights...")
                    # Extrapolate the fake1 enriched into the signal using ewk
                    # and qcd fake rates
                    register_tree('fr1s_ewk', fr1en_selection,
                                  '(pu2011AB)*(%s)' % object1_cfg['ewk_fr'])
                    log.info("------ apply fake object #1 QCD weights...")
                    register_tree('fr1s_qcd', fr1en_selection,
                                  '(pu2011AB)*(%s)' % object1_cfg['qcd_fr'])

                    # Make the fake2 enriched
                    log.info("------ running fake object #2 enriched selection...")
                    fr2en_selection = baseline + extra_selections + extra_cuts \
                            + object1_cfg['pass'] \
                            + object2_cfg['fail'] \
                            + object3_cfg['pass']
                    register_tree('fr2en', fr2en_selection, '(pu2011AB)')
                    # Extrapolate the fake2 enriched into the signal using ewk
                    # and qcd fake rates
                    log.info("------ apply fake object #2 EWK weights...")
                    register_tree('fr2s_ewk', fr2en_selection,
                                  '(pu2011AB)*(%s)' % object2_cfg['ewk_fr'])
                    log.info("------ apply fake object #2 QCD weights...")
                    register_tree('fr2s_qcd', fr2en_selection,
                                  '(pu2011AB)*(%s)' % object2_cfg['qcd_fr'])

                    # Make the double fake rate estimate
                    # Make the fake2 enriched
                    log.info("------ doing double fake object enriched selection...")
                    fr12en_selection = baseline + extra_selections + extra_cuts \
                            + object1_cfg['fail'] \
                            + object2_cfg['fail'] \
                            + object3_cfg['pass']
                    register_tree('fr12en', fr12en_selection, '(pu2011AB)')
                    # Extrapolate the fake2 enriched into the signal using ewk
                    # and qcd fake rates
                    log.info("------ applying double EWK weights...")
                    register_tree('fr12s_ewk', fr12en_selection,
                                  '(pu2011AB)*(%s)*(%s)' % (
                                      object1_cfg['ewk_fr'],
                                      object2_cfg['ewk_fr']
                                  ))
                    log.info("------ applying double QCD weights...")
                    register_tree('fr12s_qcd', fr12en_selection,
                                  '(pu2011AB)*(%s)*(%s)' % (
                                      object1_cfg['qcd_fr'],
                                      object2_cfg['qcd_fr']
                                  ))

                    # Make the triple fake rate estimate
                    # Make the fake2 enriched
                    log.info("------ selecting triple fakes...")
                    fr123en_selection = baseline + extra_selections + extra_cuts \
                            + object1_cfg['fail'] \
                            + object2_cfg['fail'] \
                            + object3_cfg['fail']
                    # Extrapolate the fake2 enriched into the signal using ewk
                    # and qcd fake rates
                    register_tree('fr123en', fr123en_selection, '(pu2011AB)')

                    # Extrapolate from triple fakes into fake1 enriched region
                    log.info("------ extrapolating (EWK) triple fakes into fake #1 region")
                    register_tree('fr123en1_ewk', fr123en_selection,
                                  '(pu2011AB)*(%s)*(%s)' % (
                                      object2_cfg['ewk_fr'],
                                      object3_cfg['ewk_fr']
                                  ))
                    log.info("------ extrapolating (QCD) triple fakes into fake #1 region")
                    register_tree('fr123en1_qcd', fr123en_selection,
                                  '(pu2011AB)*(%s)*(%s)' % (
                                      object2_cfg['qcd_fr'],
                                      object3_cfg['qcd_fr']
                                  ))
                    # Extrapolate from triple fakes into fake2 enriched region
                    register_tree('fr123en2_ewk', fr123en_selection,
                                  '(pu2011AB)*(%s)*(%s)' % (
                                      object1_cfg['ewk_fr'],
                                      object3_cfg['ewk_fr']
                                  ))
                    register_tree('fr123en2_qcd', fr123en_selection,
                                  '(pu2011AB)*(%s)*(%s)' % (
                                      object1_cfg['qcd_fr'],
                                      object3_cfg['qcd_fr']
                                  ))

                    ############################################################
                    ### Make some motherfucking plots ##########################
                    ############################################################

                    # First, just do all the plots where we only use MC
                    mc_plots = [
                        'loose', 'ult',
                        'fr1en', 'fr2en', 'fr12en',
                        'fr1s_ewk', 'fr2s_ewk', 'fr12s_ewk',
                        'fr1s_qcd', 'fr2s_qcd', 'fr12s_qcd',
                        'fr123en'
                    ]
                    for plot in mc_plots:
                        plot_name = plot_base_name + '_' + plot
                        stack = plotter.build_stack(
                            ntuple + ':' + plot_name,
                            include = ['*'],
                            exclude = ['data*', '*VH*'],
                            rebin = rebin, show_overflows=True,
                        )
                        data = plotter.get_histogram(
                            primds, ntuple + ':' + plot_name,
                            rebin = rebin, show_overflows=True,
                        )
                        stack.Draw()
                        data.Draw('same,pe')
                        legend.Draw()
                        stack.SetMaximum(max(
                            stack.GetHistogram().GetMaximum(),
                            data.GetMaximum()))
                        stack.GetXaxis().SetTitle(xaxis_title)
                        legend.Draw()
                        canvas.Update()
                        saveplot(plot_name + '_mc')

                    ############################################################
                    ### Now make control plots of the background regions #######
                    ############################################################

                    # We need to plot
                    # Each of the single fake rate CRs w/ QCD
                    # The total final prediction, with double fake correction
                    # overlayed.
                    # The total final prediction with stack FRs with double fake
                    # correction overlayed.
                    # Final prediction with combined fake rate

