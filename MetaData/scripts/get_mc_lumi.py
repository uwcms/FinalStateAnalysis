#!/usr/bin/env python

'''

Get the effective integrated lumi for a MC sample, given the number of events
processed.

Usage: get_mc_lumi.py sample nevts

Return eff. int. lumi in pb-1

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
from FinalStateAnalysis.MetaData.datacommon import picobarns
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sample', help="MC sample name")
    parser.add_argument('nevts', type=int, help="Number of processed events")
    parser.add_argument('--sqrts', type=int, choices=[0, 7, 8, 13],
                        default=0,
                        help="Use 7 or 8 TeV samples. "
                        "Default 0 - automatic by CMSSW release")
    args = parser.parse_args()

    if args.sqrts == 0:
        # Default case
        import FinalStateAnalysis.MetaData.datadefs as datadefs
    elif args.sqrts == 7:
        sys.stderr.write("Using 7 TeV data definitions\n")
        import FinalStateAnalysis.MetaData.data7TeV as datadefs
    elif args.sqrts == 8:
        sys.stderr.write("Using 8 TeV data definitions\n")
        import FinalStateAnalysis.MetaData.data8TeVNew as datadefs
    elif args.sqrts == 13:
        sys.stderr.write("Using 13 TeV data definitions\n")
        import FinalStateAnalysis.MetaData.data13TeV_LFV as datadefs

    #sample_xsec = datadefs.datadefs[args.sample]['x_sec']/picobarns

    #print args.nevts/sample_xsec
