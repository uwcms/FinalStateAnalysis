#!/usr/bin/env python

'''

Get the effective integrated lumi for a MC sample, given the number of events
processed.

Usage: get_mc_lumi.py sample nevts

Return eff. int. lumi in pb-1

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import FinalStateAnalysis.MetaData.datadefs as datadefs
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sample', help="MC sample name")
    parser.add_argument('nevts', type=int, help="Number of processed events")
    args = parser.parse_args()

    sample_xsec = datadefs.datadefs[args.sample]['x_sec']/datadefs.picobarns

    print args.nevts/sample_xsec
