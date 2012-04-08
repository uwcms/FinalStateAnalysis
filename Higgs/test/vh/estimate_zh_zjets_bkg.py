#!/usr/bin/env python

'''

Estimate the yield in the OS both-pass region
by:

    1) in the SS region
    2) measure leg1 iso/anti-iso, leg2 iso/anti-iso
    3) anti-iso both OS legs
    4) multiply by both FRs

Stores output in a JSON written to stdout

'''

from RecoLuminosity.LumiDB import argparse
import json
import logging
import math
import os
import sys
from uncertainties import ufloat

# Steal the args so ROOT doesn't mess them up!
args = sys.argv[:]
sys.argv = [sys.argv[0]]

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
    parser.add_argument('--histo', default='z1Mass',
                        help='Histogram to extract yield from.')
    args = parser.parse_args(args[1:])

    log.info("Building views")
    data_views = data_views(args.files,args.pd)

    log.info("Getting view of data. PD = %s", args.pd)
    data_view = data_views[args.pd]['view']

    def get_yield(sample, os, passed1, passed2):
        ''' Get the yield of a given sample for this configuration '''
        output = "_".join([
            os,
            args.l1name,
            passed1,
            args.l2name,
            passed2
        ])
        output += "/" + args.histo

        return data_views[sample]['view'].Get(output).Integral()

    yields = {}

    log.info("Building info about region yields for all samples")
    for sample in [args.pd, 'Zjets', 'WZ_pythia', 'ZZ']:
        log.info("Getting yields for %s", sample)
        sample_info = {}
        yields[sample] = sample_info
        for is_os in ['os', 'ss']:
            for l1_pass in ['pass', 'fail']:
                for l2_pass in ['pass', 'fail']:
                    key = (is_os, l1_pass, l2_pass)
                    sample_info["_".join(key)] = get_yield(sample, *key)

    def uint(n):
        ''' Build a ufloat with sqrt(n) errors '''
        return ufloat( (n, math.sqrt(n)) )

    def ufloat_rel(x, err):
        ''' Build a ufloat with relative errors '''
        return ufloat( (x, err*x) )

    log.info("Computing %s fake rate for data", args.l1name)
    data_yields = yields[args.pd]
    data_yields["ss_fr1"] = ((
        uint(data_yields["ss_pass_fail"]) -
        ufloat_rel(yields['WZ_pythia']["ss_pass_fail"], 0.3)) /
        (
            uint(data_yields["ss_fail_fail"]) -
            ufloat_rel(yields['WZ_pythia']["_".join(('ss', 'fail', 'fail'))], 0.3)
        )
    )
    data_yields["ss_fr2"] = ((
        uint(data_yields["ss_fail_pass"]) -
        ufloat_rel(yields['WZ_pythia']["ss_fail_pass"], 0.3)) /
        (
            uint(data_yields["ss_fail_fail"]) -
            ufloat_rel(yields['WZ_pythia']["ss_fail_fail"], 0.3)
        )
    )
    data_yields['total_fr'] = data_yields["ss_fr2"]*data_yields["ss_fr1"]
    data_yields['os_zj_estimate'] = (
        uint(data_yields['os_fail_fail'])*
        data_yields['total_fr']
    )
    data_yields['ss_zj_estimate'] = (
        uint(data_yields['os_fail_fail'])*
        data_yields['total_fr']
    )

    json.dump(yields, sys.stdout, indent=2, sort_keys=True, default=repr)
