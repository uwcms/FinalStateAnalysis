#!/usr/bin/env python
'''

Render the numerator and denominators and MC comparison

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import logging
import os
import re
import sys

# Steal the args so ROOT doesn't mess them up!
args = sys.argv[:]
sys.argv = [sys.argv[0]]

from rootpy.io import open
from rootpy.plotting import views

if __name__ == "__main__":
    parser.add_argument('meta', help='File with meta information')
    parser.add_argument('pd', help='Data primary dataset')
    parser.add_argument('output', help='Data primary dataset')
    parser.add_argument('files', metavar='file', nargs='+',
                        help = 'Histogram files')
    args = parser.parse_args(args[1:])

    log.info("Building views")
    views = get_views(
        args.files,
        # How to get the sample from the file name
        lambda x: os.path.basename(x).replace('.all.root', ''),
        meta_info,
        4728
    )
    data_view = views[args.pd]['view']

    mc_samples_to_stack = ['Zjets', 'QCDMu', 'Wjets', 'ttjets', 'WZ_pythia']
    # Build the MC stack
    mc_view = views.StackView(*[views[x] for x in mc_samples_to_stack])

    # We just need to figure out the directory structure from any old file
    layout_filename = data_views.values()[0]['subsamples'].values()[0]['filename']
    log.info("Getting file layout from %s", layout_filename)

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

    plot_list = open(os.path.join(args.output, 'plot_list.txt'), 'w')

    with io.open(layout_filename, 'r') as layout_file:
        for path, subdirs, histos in layout_file.walk(class_pattern='TH1F'):
            for histo in histos:
                data_histo = data_view.Get(os.path.join(path, histo))
                mc_histo = mc_view.Get(os.path.join(path, histo))
                mc_histo.Draw()
                data_histo.Draw('same')
                plot_filename = os.path.join(
                    args.output,
                    path.replace('/', '_') + '_' + histo + '.pdf
                )
                plot_list.write(plot_filename + '\n')
                canvas.SaveAs(plot_filename)
