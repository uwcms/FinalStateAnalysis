#!/usr/bin/env python

'''

Command Line tool to run a python selector on a datasets

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import logging
import multiprocessing
import os
import sys

from FinalStateAnalysis.PlotTools.ChainProcessor import ChainProcessor
from FinalStateAnalysis.PlotTools.Dispatcher import MegaDispatcher

log = multiprocessing.log_to_stderr()
log.setLevel(logging.WARNING)

parser = argparse.ArgumentParser()
args = sys.argv[:]
sys.argv = []

if __name__ == "__main__":

    parser.add_argument('selector', metavar='selector', type=str,
                        help='Path to TPySelector module')

    parser.add_argument('inputs', metavar='inputs', type=str,
                        help='Text file with input files.  '
                        'If this option does not end with ".txt", '
                        'it will be assumed to be a comma separated list of '
                        'files (no spaces please).')

    parser.add_argument('output', metavar='output',
                        type=str, help='Output root file')

    parser.add_argument('--tree', metavar='tree', type=str, default='',
                        help='Override path to TTree in data files'
                        ' (Ex: /my/dir/myTree)')

    parser.add_argument('--workers', type=int, required=False, default=4,
                        help='Number of worker processes (def: 4)')

    parser.add_argument('--chain', type=int, required=False,
                        default=1, help='Number of files to chain together')

    parser.add_argument('--single-mode', action='store_true', dest='single',
                        help="Run as a single job.")

    parser.add_argument('--verbose', action='store_const', const=True,
                        default=False, help='Print debug output')

    args = parser.parse_args(args[1:])

    if args.verbose:
        logging.info("Increasing verbosity...")
        log.setLevel(logging.DEBUG)
        multiprocessing.get_logger().setLevel(logging.DEBUG)

    if not args.single:
        log.info("Creating mega session with %i workers" % args.workers)
    else:
        log.info("Creating mega session with 1 workers - single mode")

    file_list = []
    if '.txt' in args.inputs:
        log.info("Checking inputs file %s exists..." % args.inputs)
        # Get the inputs to make sure it exists
        if not os.path.exists(args.inputs):
            log.error(
                "Error: inputs %s input file does not exist", args.inputs)
            sys.exit(5)
        with open(args.inputs) as inputs_file:
            for line in inputs_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    file_list.append(line)
    else:
        for x in args.inputs.split(','):
            file_list.append(x.strip())

    # If the files are on HDFS, access them using xrootd
    for idx, input_file in enumerate(file_list):
        if input_file.startswith('/store'):
            file_list[idx] = 'root://cmsxrootd.hep.wisc.edu/' + input_file

    if not file_list:
        log.error("Dataset %s has no files!  Skipping..." % args.inputs)
        sys.exit(1)

    log.info("Dataset has %i files", len(file_list))

    path_to_selector = os.path.dirname(os.path.abspath(args.selector))
    module_name = os.path.basename(args.selector)
    class_name = module_name.replace('.py', '')
    log.info("Importing class %s from %s", class_name, path_to_selector)

    module = __import__(class_name, fromlist=[class_name])
    selector = getattr(module, class_name)
    log.info("Selector class: %s", selector)

    tree_name = None
    if args.tree:
        tree_name = args.tree
    else:
        log.info("Getting tree name from selector module")
        tree_name = selector.tree

    if not args.single:
        log.info("Dispatching jobs")
        dispatch = MegaDispatcher(file_list, tree_name, args.output, selector,
                                  args.workers, nchain=args.chain)
        dispatch.run()
    else:
        log.info("Running job as single process")
        print args.output
        processor = ChainProcessor(file_list, tree_name, selector,
                                   args.output, log)
        result = processor.process()
    log.info("Mega2 job is complete")
