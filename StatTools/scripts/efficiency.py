#!/usr/bin/env python
'''

A simple script that extracts the efficiency of a potential cut on a histogram
from a ROOT file

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import math
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help = 'Path to histogram')
    parser.add_argument('files', nargs='+', help = 'Input root files')
    parser.add_argument('--above', default=None,
                        type=float, help='Cut above')
    parser.add_argument('--below', default=None,
                        type=float, help='Cut below')
    args = parser.parse_args()

    from rootpy.io import open
    from FinalStateAnalysis.StatTools.efficiencies import efficiency

    # Get histogram
    for a_file in args.files:
        file = open(a_file)
        if not file:
            sys.stderr.write("Can't open file: %s\n" % args.file)
            sys.exit(2)

        histo = file.Get(args.path)
        if not histo:
            sys.stderr.write("Can't get histogram: %s\n" % args.path)
            sys.exit(3)

        total = 0
        below_below = 0
        below_above = 0
        if histo.GetEntries():
            total = histo.GetIntegral()[histo.GetNbinsX()+1]

            below_above = 0

            if args.above:
                below_above = histo.GetIntegral()[
                    histo.FindBin(args.above)]

            below_below = 1
            if args.below:
                below_below = histo.GetIntegral()[
                    histo.FindBin(args.below)]

        passed = total - (below_above)*total- (1-below_below)*total

        eff, up, down = efficiency(passed, total)

        sys.stdout.write("%s: %i/%i = %0.2g +%0.2g -%0.2g\n" % (
            a_file, int(passed), int(total), eff, up, down))
