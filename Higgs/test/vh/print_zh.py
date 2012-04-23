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
                try:
                    yield_dict = json.load(yield_file)
                except ValueError:
                    sys.stderr.write("Couldn't decode JSON from file: %s\n" %
                                     yield_filename)
                    sys.exit(2)
                channels[yield_dict['channel']] = yield_dict

    def write(to_stdout):
        sys.stdout.write(to_stdout)
        sys.stdout.write('\n')

    columns = ["Channel",
         "Data",
         "All bkg.",
         #"Z+jets est.",
         #"WZ",
         "ZZ",
         "Region 1",
         "Region 2",
         "Region 0",
         "1+2-0",
        ]

    for region in ['os', 'ss']:
        for use_corr in [False]:
            print "%s region" % region
            if use_corr:
                print "With SS FR correction"
            else:
                print "NO SS FR correction"
            # Print out regions in the OS
            table = tabulartext.PrettyTable(columns)

            total_obs = 0
            total_zj = 0
            total_wz = 0
            total_zz = 0
            total_1 = 0
            total_2 = 0
            total_0 = 0
            total_120 = 0

            def rel_float(x, err):
                return ufloat( (x, x*err) )

            for channel, channel_info in channels.iteritems():
                wz = rel_float(channel_info['WZ_pythia']['%s_pass_pass' % region], 0.25)
                zz = rel_float(channel_info['ZZ']['%s_pass_pass' % region], 0.1)
                zjets = ufloat(channel_info['data']['%s_zj_estimate' % region])
                est120 = ufloat(channel_info['data']['%s_type120_est' % region])
                est1 = ufloat(channel_info['data']['%s_type_1_est' % region])
                est2 = ufloat(channel_info['data']['%s_type_2_est' % region])
                est0 = ufloat(channel_info['data']['%s_type_0_est' % region])

                if region == 'os' and use_corr:
                    zjets = ufloat(channel_info['data']['%s_zj_estimate_corr' % region])

                def make_positive(x):
                    if x.nominal_value < 0:
                        return ufloat( (0, x.std_dev()) )
                    return x

                zjets = make_positive(zjets)
                est1 = make_positive(est1)
                est2 = make_positive(est2)
                est0 = make_positive(est0)
                est120 = make_positive(est120)

                data = channel_info['data']['%s_pass_pass' % region]
                total_wz += wz
                total_zz += zz
                total_zj += zjets
                total_obs += data
                #total_bkg = zjets + wz + zz
                total_bkg = est120 + zz
                total_120 += est120
                total_1 += est1
                total_2 += est2
                total_0 += est0
                table.add_row([
                    channel,
                    '%0.f' % data,
                    '%0.2f +/- %0.2f' % (total_bkg.nominal_value, total_bkg.std_dev()),
                #    '%0.2f +/- %0.2f' % (zjets.nominal_value, zjets.std_dev()),
                #    '%0.2f +/- %0.2f' % (wz.nominal_value, wz.std_dev()),
                    '%0.2f +/- %0.2f' % (zz.nominal_value, zz.std_dev()),
                    '%0.2f +/- %0.2f' % (est1.nominal_value, est1.std_dev()),
                    '%0.2f +/- %0.2f' % (est2.nominal_value, est2.std_dev()),
                    '%0.2f +/- %0.2f' % (est0.nominal_value, est0.std_dev()),
                    '%0.2f +/- %0.2f' % (est120.nominal_value, est120.std_dev()),
                ])
            total_bkg = total_120 + total_zz
            table.add_row([
                'all',
                '%0.f' % total_obs,
                '%0.2f +/- %0.2f' % (total_bkg.nominal_value, total_bkg.std_dev()),
                #'%0.2f +/- %0.2f' % (total_zj.nominal_value, total_zj.std_dev()),
                #'%0.2f +/- %0.2f' % (total_wz.nominal_value, total_wz.std_dev()),
                '%0.2f +/- %0.2f' % (total_zz.nominal_value, total_zz.std_dev()),
                '%0.2f +/- %0.2f' % (total_1.nominal_value, total_1.std_dev()),
                '%0.2f +/- %0.2f' % (total_2.nominal_value, total_2.std_dev()),
                '%0.2f +/- %0.2f' % (total_0.nominal_value, total_0.std_dev()),
                '%0.2f +/- %0.2f' % (total_120.nominal_value, total_120.std_dev()),
            ])

            print table

            #print "Channel & Data & Type 1 & Type 2 & Type 0 & 1 + 2 - 0 \\\\"
            #for row in table._rows:
                #def texify(x):
                    #return '$' + x.replace('+/-', '\pm') + '$'
                #print " & ".join( [
                    #row[0],
                    #row[1],
                    #texify(row[6]),
                    #texify(row[7]),
                    #texify(row[8]),
                    #texify(row[9]),
                #]) + "\\\\"

