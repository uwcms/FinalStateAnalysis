#!/usr/bin/env python

import ROOT
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s [inputfile.txt] [outputfile.root]"

    input = open(sys.argv[1], 'r')
    bins = []
    for line in input:
        if '#' in line:
            continue
        bins.append(float(line.strip().strip(',')))

    output_hist = ROOT.TH1F("pileup", "pileup", len(bins), 0, len(bins))

    for i, bin in enumerate(bins):
        output_hist.SetBinContent(i+1, bin)

    output_file = ROOT.TFile(sys.argv[2], 'RECREATE')
    output_file.cd()
    output_hist.Write()
    output_file.Write()
    output_file.Close()
