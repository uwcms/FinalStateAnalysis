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
from FinalStateAnalysis.Utilities.lumitools import json_summary
import logging
import sys

log = logging.getLogger("extract_meta_info")

# Steal the args so ROOT doesn't mess them up!
parser = argparse.ArgumentParser()
args = sys.argv[:]
sys.argv = []

import ROOT

if __name__ == "__main__":
    parser.add_argument('input', type=str,
                        help='A text file with a list of input ROOT files')
    parser.add_argument('tree', type=str,
                        help='Specify the path to the meta tree.')
    parser.add_argument('output', type=str, help='Output JSON file')
    parser.add_argument('--lumimask', action='store_const',
                        const=True, default=False,
                        help = 'If true, include the run-lumi mask result')

    args = parser.parse_args(args[1:])

    files = []
    with open(args.input) as input_files:
        for input_file in input_files:
            input_file = input_file.strip()
            if input_file:
                files.append(input_file.strip())

    logging.basicConfig(stream=sys.stderr)

    log.info("Extracting meta info from %i files", len(files))

    total_events = 0
    run_lumis = {}

    for file in files:
        tfile = ROOT.TFile.Open(file, "READ")
        tree = tfile.Get(args.tree)
        for entry in xrange(tree.GetEntries()):
            tree.GetEntry(entry)
            total_events += tree.nevents
            run_lumi = (tree.run, tree.lumi)
            if run_lumi in run_lumis:
                log.error("Run-lumi %s found in file \n%s \nand %s!",
                          run_lumi, file, run_lumis[run_lumi])
            run_lumis[run_lumi] = file

    output = {
        'n_evts' : total_events,
    }
    if args.lumimask:
        output['lumi_mask'] = json_summary(run_lumis)

    with open(args.output, 'w') as output_file:
        output_file.write(json.dumps(output, indent=2, sort_keys=True) + '\n')
