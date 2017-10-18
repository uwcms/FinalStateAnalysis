'''

Common definitions and helpers used by the dataset definitions.

Author: Evan K. Friis, UW Madison

'''

import fnmatch
import math
from RecoLuminosity.LumiDB import argparse
from FinalStateAnalysis.Utilities.prettytable import PrettyTable
import sys

# Conversions to pico barns
millibarns = 1.0e+9
microbarns = 1.0e+6
nanobarns  = 1.0e+3
picobarns =  1.0
femtobarns = 1.0e-3

# Branching ratios
#LAG 26 DEC 2012 -- set Z->leptons branching to PDG values
br_w_leptons = 0.1075+0.1057+0.1125
br_z_leptons = 0.03363+0.03366+0.03370 #e,mu,tau

def square(x):
    return x*x

def cube(x):
    return x*x*x

def quad(*xs):
    # Add stuff in quadrature
    return math.sqrt(sum(x*x for x in xs))

def query_cli(datadefs, argv=None):
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(description='Query datasets')
    query_group = parser.add_argument_group(
        title='query', description="Query parameters (ORed)")
    query_group.add_argument(
        '--name', required=False, type=str,
        help='"Nice" dataset name (ex: Zjets_M50)')
    query_group.add_argument(
        '--dataset', required=False, type=str,
        help='DBS dataset name (ex: '
        '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/*')
    output_group = parser.add_argument_group(
        title='output', description="Output parameters")
    output_group.add_argument(
        '--columns', nargs='+',  help='Output columns',
        default=['name', 'datasetpath'],
        choices=['name', 'datasetpath', 'pu', 'x_sec', 'lumi_mask',
                 'firstRun', 'lastRun'])
    output_group.add_argument(
        '--sort', default='name', help='Column to sort by')
    output_group.add_argument(
        '--noborder', action='store_false', default=True, help='Show border')

    args = parser.parse_args(argv[1:])

    if not args.name and not args.dataset:
        print "Must specify either --name or --dataset.  Did you forget to quote a '*'?"
        sys.exit(1)

    table = PrettyTable(args.columns)

    for col in args.columns:
        table.set_field_align(col, 'l')

    for key in sorted(datadefs.keys()):
        value = datadefs[key]
        matched = False
        if args.name and fnmatch.fnmatch(key, args.name):
            matched = True
        if args.dataset and fnmatch.fnmatch(value['datasetpath'], args.dataset):
            matched = True
        if matched:
            row = []
            for column in args.columns:
                if column == 'name':
                    row.append(key)
                else:
                    row.append(value.get(column, '-'))
            table.add_row(row)

    table.printt(sortby=args.sort, border=(args.noborder))
