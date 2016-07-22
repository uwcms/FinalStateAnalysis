#!/usr/bin/env python
'''

The FinalStateAnalyzer classes in FinalStateAnalysis/Selector
produce "meta" info trees, which contain an entry for every *processed*
run/lumi which contains the number of originally processed events.

You can use this to normalize an MC sample to a given int. lumi.

This script extract that info and puts in it a json file.

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import json
import logging
import sys

from FinalStateAnalysis.PlotTools.MegaPath import resolve_file
from FinalStateAnalysis.Utilities.lumitools import json_summary

log = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, metavar='input(.txt|.root)',
                        help='A text file with a list of input ROOT files.'
                        ' If paths are relative, the $MEGAPATH will be'
                        ' searched to locate the files.'
                        'If the name does not end in .txt, it will be '
                        'considered a comma separated list of input files.')
    parser.add_argument('tree', type=str,
                        help='Specify the path to the meta tree.')
    parser.add_argument('output', type=str, help='Output JSON file')
    parser.add_argument('--lumimask', action='store_const',
                        const=True, default=False,
                        help='If true, include the run-lumi mask result')
    parser.add_argument('--debug', action='store_const',
                        const=True, default=False,
                        help='Print debug output')
    parser.add_argument('--histo', type=str,
                        help='Specify the path to the meta histo.')
    args = parser.parse_args()
    import ROOT

    files = []
    if '.txt' in args.input:
        with open(args.input) as input_files:
            for input_file in input_files:
                input_file = input_file.strip()
                if input_file and '#' not in input_file:
                    files.append(resolve_file(input_file))
    else:
        files = [resolve_file(x.strip()) for x in args.input.split(',')]

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(stream=sys.stderr, level=level)

    log.info("Extracting meta info from %i files", len(files))

    total_events = 0
    total_weights = 0
    run_lumis = {}

    for file in files:
        log.debug("OPEN file %s", file)
        tfile = ROOT.TFile.Open(file, "READ")
        #histo = tfile.Get(args.histo)
        #if not histo :
        #    log.error("Cannot get weights histo %s from file %s", args.histo, file)
        #    raise SystemExit(1)
        #total_weights+=histo.Integral()
 
        tree = tfile.Get(args.tree)
        if not tree:
            log.error("Cannot get tree %s from file %s", args.tree, file)
            raise SystemExit(1)
        for entry in xrange(tree.GetEntries()):
            tree.GetEntry(entry)
            total_events += tree.nevents
            total_weights+= tree.summedWeights
            # We only care about this if we are building the lumimask
            if args.lumimask:
                run_lumi = (tree.run, tree.lumi)
                log.debug("R-L %s %s", repr(run_lumi), file)
                if run_lumi in run_lumis:
                    log.error("Run-lumi %s found in file \n%s \nand %s!",
                              run_lumi, file, run_lumis[run_lumi])
                run_lumis[run_lumi] = file
        #log.info("Summed Weights: %s", str(total_weights))
        tfile.Close()

    output = {
        'n_evts': total_events,
        'sumweights': total_weights,
    }
    if args.lumimask:
        output['lumi_mask'] = json_summary(run_lumis)

    with open(args.output, 'w') as output_file:
        output_file.write(json.dumps(output, indent=2, sort_keys=True) + '\n')
