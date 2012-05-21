#!/usr/bin/env python
'''

Give the yields in the (data) control regions

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
import tabulartext

from FinalStateAnalysis.MetaData.data_views import data_views

if __name__ == "__main__":
    log = logging.getLogger("render_zh_plots")
    view_builder = logging.getLogger("data_views")
    view_builder.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    parser = argparse.ArgumentParser()
    parser.add_argument('pd', help='Primary dataset')
    parser.add_argument('l1name', help='Name of first lepton')
    parser.add_argument('l2name', help='Name of first lepton')
    parser.add_argument('files', metavar='file',
                        nargs='+', help = 'Histogram files')
    args = parser.parse_args(args[1:])

    log.info("Building views")
    data_views = data_views(args.files,args.pd)

    data_view = data_views[args.pd]['view']

    def write(to_stdout):
        sys.stdout.write(to_stdout)
        sys.stdout.write('\n')

    # Print out regions in the OS
    table = tabulartext.PrettyTable(
        ["Sign", "Final", "%s anti-iso" % args.l1name,
         "%s anti-iso" % args.l2name, "both anti-iso",
         "%s FR %%" % args.l1name, "%s FR %%" % args.l2name,
         'both x SS FR1 x SS FR2',
        ]
    )

    def get_yield(is_os, passed1, passed2, histo='z1Mass'):
        ''' Get the histo given the configuration '''
        output = "_".join([
            "os" if is_os else "ss",
            args.l1name,
            "pass" if passed1 else "fail",
            args.l2name,
            "pass" if passed2 else "fail",
        ])
        output += "/" + histo

        return data_view.Get(output).Integral()

    table.add_row(
        ["OS",
         get_yield(True, True, True),
         get_yield(True, False, True),
         get_yield(True, True, False),
         get_yield(True, False, False),
         '%0.2f' % (100*get_yield(True, False, True)/get_yield(True, False, False)),
         '%0.2f' % (100*get_yield(True, True, False)/get_yield(True, False, False)),
          '%0.2f' % (get_yield(True, False, False)* get_yield(False, False, True) * get_yield(False, True, False)/(get_yield(False, False, False)*get_yield(False, False, False))),
        ]
    )
    table.add_row(
        ["SS",
         get_yield(False, True, True),
         get_yield(False, False, True),
         get_yield(False, True, False),
         get_yield(False, False, False),
         '%0.2f' % (100*get_yield(False, False, True)/get_yield(False, False, False)),
         '%0.2f' % (100*get_yield(False, True, False)/get_yield(False, False, False)),
          '%0.2f' % (get_yield(False, False, False)* get_yield(False, False, True) * get_yield(False, True, False)/(get_yield(False, False, False)*get_yield(False, False, False))),
        ]
    )
    print table
