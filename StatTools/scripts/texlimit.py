#!/usr/bin/env python

'''

Make a limit tex table given a set of json limit data files.

'''

import glob
from RecoLuminosity.LumiDB import argparse
import FinalStateAnalysis.StatTools.limitplot as limitplot
import ROOT
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='+', help='JSON files with limit data')
    parser.add_argument('--method', type=str, default='cls',
                        help='Limit method to use.  Default: cls')
    parser.add_argument('--label', type=str, default='',
                        help='Limit label to use.  Default: None')


    args = parser.parse_args()

    all_files = []
    for file in args.data:
        all_files.extend(glob.glob(file))

    limit_data = limitplot.get_limit_info(all_files)

    key = (args.method, args.label)

    sys.stdout.write(
        ' & '.join(['Mass', '-2$\\sigma$', '-1$\\sigma$', 'Expected',
                    '+1$\\sigma$', '+2$\\sigma$', 'Observed']) + '\\\\\n'
    )
    sys.stdout.write('\hline\n')

    template = ' & '.join([
        '{mass:0.0f} \\GeV',
        '{-2:5.1f}', '{-1:5.1f}', '{exp:5.1f}', '{+1:5.1f}',
        '{+2:5.1f}', '{obs:5.1f}']) + '\\\\\n'


    for mass in sorted(limit_data[key].keys()):
        if mass == 'mass':
            continue
        sys.stdout.write(template.format(mass=mass,
            **limit_data[key][mass]))



