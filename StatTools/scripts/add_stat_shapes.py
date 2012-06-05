#!/usr/bin/env python

'''

Add statistical shape errors (aka Barlow Beeston) to a shape .root file

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
import logging
import ROOT
import sys

log = logging.getLogger('stat_shapes')

def walk_and_copy(inputdir, outputdir, matchers, threshold):
    ''' Recursive function which copies from inputdir to outputdir '''
    for key in inputdir.GetListOfKeys():
        # Keep track of stuff we find in this directory
        directories = []
        histos = []
        name = key.GetName()
        classname = key.GetClassName()
        if classname.startswith('TDirectory'):
            directories.append(name)
        elif isinstance(inputdir.Get(name), ROOT.TH1):
            histos.append(name)
        # Copy all histograms from input -> output directory
        for histo in histos:
            th1 = inputdir.Get(histo)
            outputdir.cd()
            th1.Write()
            # Check if this histogram has shape uncertainties
            do_shapes = False
            for pattern in matchers:
                if fnmatch.fnmatch(histo, pattern):
                    do_shapes = True
                    break
            if do_shapes:
                # check all bins to see if they need to be shape-errored
                log.info("Building stat shapes for %s", histo)
                for ibin in range(1, th1.GetNbinsX()+1):
                    if th1.GetBinContent(ibin):
                        error = th1.GetBinError(ibin)
                        val = th1.GetBinContent(ibin)
                        # Check if we are above threshold
                        if error/val > threshold:
                            err_up = th1.Clone(
                                th1.GetName() + "_ss_bin_%i_up" % ibin)
                            err_down = th1.Clone(
                                th1.GetName() + "_ss_bin_%i_down" % ibin)
                            err_up.SetBinContent(ibin, val + error)
                            err_down.SetBinContent(ibin, val - error)
                            outputdir.cd()
                            err_up.Write()
                            err_down.Write()
                            log.info("==> built shape for %s bin %i", histo, ibin)

        # Now copy and recurse into subdirectories
        for subdir in directories:
            output_subdir = outputdir.mkdir(subdir)
            # Recurse
            walk_and_copy(
                inputdir.Get(subdir), output_subdir,
                matchers, threshold)

def main(inputfilename, outputfilename, matchers, threshold):
    input = ROOT.TFile(inputfilename, 'READ')
    output = ROOT.TFile(outputfilename, 'RECREATE')
    walk_and_copy(input, output, matchers, threshold)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input .root file')
    parser.add_argument('output', help='Output .root file')
    parser.add_argument('--filter', nargs='+', metavar='pattern',
                        help='Patterns of TH1F names to shape-ize')
    parser.add_argument('--threshold', type=float, default=0.05,
                        help='Minimum error for systematic creation,'
                        'default %(default)0.2f')

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    args = parser.parse_args()

    log.info("Building shape systematics. input: %s output: %s",
             args.input, args.output)
    main(args.input, args.output, args.filter, args.threshold)
