#!/usr/bin/env python
'''

Give the yields in the (data) control regions

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import glob
import json
import logging
import os
import sys
from uncertainties import ufloat

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
    parser.add_argument('yields', nargs='+', help='JSON files with yields')
    args = parser.parse_args(args[1:])

    channels = {}

    for yield_filenames in args.yields:
        for yield_filename in glob.glob(yield_filenames):
            with open(yield_filename) as yield_file:
                yield_dict = json.load(yield_file)
                channels[yield_dict['channel']] = yield_dict

    def write(to_stdout):
        sys.stdout.write(to_stdout)
        sys.stdout.write('\n')

    columns = ["Channel",
         "Data",
         "All bkg.",
         "Z+jets est.",
         "WZ",
         "ZZ",
        ]

    for region in ['os', 'ss']:
        print "%s region" % region
        # Print out regions in the OS
        table = tabulartext.PrettyTable(columns)

        total_obs = 0
        total_zj = 0
        total_wz = 0
        total_zz = 0

        for channel, channel_info in channels.iteritems():
            wz = channel_info['WZ_pythia']['%s_pass_pass' % region]
            zz = channel_info['ZZ']['%s_pass_pass' % region]
            zjets = ufloat(channel_info['data']['%s_zj_estimate' % region])
            data = channel_info['data']['%s_pass_pass' % region]
            total_wz += wz
            total_zz += zz
            total_zj += zjets
            total_obs += data
            table.add_row([
                channel,
                data,
                wz + zz + zjets,
                zjets,
                wz,
                zz
            ])
        table.add_row([
            'all',
            total_obs,
            total_zj + total_wz + total_zz,
            total_zj,
            total_wz,
            total_zz
        ])

        print table
