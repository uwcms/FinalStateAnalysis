#!/usr/bin/env python

'''

Print all histogram yields in a file to stdout.

Author: Evan K. Friis

'''

from RecoLuminosity.LumiDB import argparse
import json
import os
import sys

def get_integral(histo):
    ''' Returns a tuple with the integral and error on the integral of a TH1 '''
    import ROOT
    err = ROOT.Double(0)
    int = histo.IntegralAndError(0, histo.GetNbinsX()+1, err)
    return (int, err)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Print the integrals of histograms in a ROOT file.  "
        "The under- and over-flow bins are included")

    parser.add_argument('file', help="ROOT file")
    parser.add_argument('--json', action='store_true',
                        help="Write output in JSON format")

    args = parser.parse_args()

    # Import after, so ROOT can't mess with sys.argv
    import rootpy.io as io

    file = io.open(args.file)

    results = {}

    for path, dirs, histonames in file.walk(class_pattern='TH1*'):
        for histoname in histonames:
            full_path = os.path.join(path, histoname)
            histo = file.Get(full_path)
            int, err = get_integral(histo)
            results[full_path] = (int, err)

    if not args.json:
        for full_path, (int, err) in results.iteritems():
            sys.stdout.write(" : ".join(
                [full_path, "%0.5g" % int, "%0.5g" % err]))
            sys.stdout.write('\n')
    else:
        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write('\n')
