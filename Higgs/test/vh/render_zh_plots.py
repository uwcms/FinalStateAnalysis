#!/usr/bin/env python
'''

Render the Zmumu control plots

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import json
import logging
import os
import re
import sys

# Steal the args so ROOT doesn't mess them up!
args = sys.argv[:]
sys.argv = [sys.argv[0]]

import rootpy.io as io
from rootpy.plotting import views
from rootpy.plotting import Canvas, Legend

from FinalStateAnalysis.MetaData.data_views import data_views

if __name__ == "__main__":
    log = logging.getLogger("render_zh_plots")
    view_builder = logging.getLogger("data_views")
    view_builder.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='Output directory')
    parser.add_argument('pd', help='Primary dataset')
    parser.add_argument('files', metavar='file',
                        nargs='+', help = 'Histogram files')
    args = parser.parse_args(args[1:])

    log.info("Building views")
    data_views = data_views(args.files,args.pd)

    data_view = data_views[args.pd]['view']

    mc_samples_to_stack = ['Zjets', 'QCDMu', 'Wjets',
                           'ttjets', 'WZ_pythia', 'ZZ']

    # Build the MC stack
    mc_view = views.StackView(
        *[data_views[x]['view'] for x in mc_samples_to_stack], sort=True)

    # We just need to figure out the directory structure from any old file
    layout_filename = data_views.values()[0]['subsamples'].values()[0]['filename']
    log.info("Getting file layout from %s", layout_filename)

    canvas = Canvas()

    if not os.path.exists(args.output):
        log.info("Creating output directory: %s", args.output)
        os.makedirs(args.output)

    plot_list = open(os.path.join(args.output, 'plot_list.txt'), 'w')

    with io.open(layout_filename, 'r') as layout_file:
        log.info("Plotting all histograms")
        for path, subdirs, histos in layout_file.walk(class_pattern='TH1F'):
            for histo in histos:
                log.info("Plotting %s in %s", histo, path)
                data_histo = data_view.Get(os.path.join(path, histo))
                mc_histo = mc_view.Get(os.path.join(path, histo))
                log.info("Data histo has %f entries", data_histo.Integral())
                mc_histo.Draw()
                data_histo.Draw('same')
                legend = Legend(7, leftmargin=0.5)
                legend.AddEntry(mc_histo)
                legend.AddEntry(data_histo)
                legend.SetBorderSize(0)
                legend.Draw()
                mc_histo.SetMaximum(1.2*max(
                    mc_histo.GetMaximum(), data_histo.GetMaximum()))

                plot_filename = os.path.join(
                    args.output,
                    path.replace('/', '_') + '_' + histo + '.pdf'
                )
                plot_list.write(plot_filename + '\n')
                canvas.SaveAs(plot_filename)
