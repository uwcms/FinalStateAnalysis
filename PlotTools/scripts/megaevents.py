#!/usr/bin/env python

'''

Command Line tool to get the events which pass a set of cuts.

Maybe should be parallelized in the future?

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import logging
import json
import os
from progressbar import ETA, ProgressBar, FormatLabel, Bar
import sys

log = logging.getLogger("megadebug")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
log.setLevel(logging.WARNING)

parser = argparse.ArgumentParser()
args = sys.argv[:]
sys.argv = []

import ROOT

if __name__ == "__main__":

    parser.add_argument('selector', metavar='selector', type=str,
                        help='Path to TPySelector module')

    parser.add_argument('inputs', metavar='inputs', type=str,
                        help='.txt file with input files.  '
                        'One job will be created for each input file.'
                        ' If the file name ends in .root, it will be used.')

    parser.add_argument('tree', metavar='tree', type=str,
                        help='Path to TTree in data files (Ex: /my/dir/myTree)')

    parser.add_argument('output', type=str,
                        help='Output JSON file')

    parser.add_argument('selections', metavar="selection", nargs="+",
                        help="Which selections to apply in the cut flow."
                        " The selections must be importable from the Selector.")

    parser.add_argument('--branches', default=[], metavar="branch", nargs='*',
                        help="Store the values of the branches in the output")

    args = parser.parse_args(args[1:])

    log.info("Checking inputs file %s exists..." % args.inputs)
    # Get the inputs to make sure it exists
    if not os.path.exists(args.inputs):
        log.error(
            "Error: inputs %s input file does not exist", args.inputs)
        sys.exit(5)

    file_list = []
    if args.inputs.endswith('.root'):
        file_list.append(args.inputs)
    else:
        with open(args.inputs) as inputs_file:
            for line in inputs_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    file_list.append(line)

    if not file_list:
        log.error("Dataset %s has no files!  Skipping..." % args.inputs)
        sys.exit(1)

    log.info("Building TChain")
    chain = ROOT.TChain(args.tree)
    for file in file_list:
        chain.AddFile(file)

    log.info("Building selectors")
    path_to_selector = os.path.dirname(os.path.abspath(args.selector))
    module_name = os.path.basename(args.selector)
    class_name = module_name.replace('.py', '')
    log.info("Importing class %s from %s", class_name, path_to_selector)

    module = __import__(class_name, fromlist=[args.selections])
    log.info("Loading %i selections", len(args.selections))
    selections = []
    for selection in args.selections:
        selection = selection.replace('+', '')
        selection = selection.replace('-', '')
        selections.append( (selection, getattr(module, selection)) )

    log.info("Beginning loop over %i TChain entries", chain.GetEntries())
    current_event = (None, None, None)

    log.info("Trying to import meta tree")
    try:
        #metamodule = __import__(class_name, fromlist=['meta'])
        meta = getattr(module, 'meta')
        log.info("Got meta tree! - Disabling unused branches")
        chain.SetBranchStatus('*', 0)
        for b in meta.active_branches():
            chain.SetBranchStatus(b, 1)
        chain.SetBranchStatus('run', 1)
        chain.SetBranchStatus('lumi', 1)
        chain.SetBranchStatus('evt', 1)
        for b in args.branches:
            chain.SetBranchStatus(b, 1)
    except:
        raise
        log.warning("Couldn't get meta tree - will not disable branches")


    passed_events = []

    nrows = chain.GetEntries()
    pbar = ProgressBar(widgets=[
        FormatLabel('Processed %(value)i/' + str(nrows) + ' rows. '),
        ETA(), Bar('>')], maxval=nrows).start()
    pbar.update(0)

    for row in xrange(nrows):
        pbar.update(row)
        chain.GetEntry(row)
        all_passed = True
        for name, selection in selections:
            passed = selection(chain)
            if not passed:
                all_passed = False
                break
        if all_passed:
            this_event = {
                'evt': (chain.run, chain.lumi, chain.evt),
            }
            for branch in args.branches:
                this_event[branch] = getattr(chain, branch)
            passed_events.append(this_event)

    log.info("Dumping output")
    with open(args.output, 'w') as json_file:
        json.dump(passed_events, json_file, indent=2)


