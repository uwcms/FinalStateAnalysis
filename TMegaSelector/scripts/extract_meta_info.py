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

log = logging.getLogger("extract_meta_info")

# Steal the args so ROOT doesn't mess them up!
parser = argparse.ArgumentParser()
args = sys.argv[:]
sys.argv = []

import ROOT

def group_by_run(sorted_run_lumis):
    '''
    Generate a list of lists run-lumi tuples, grouped by run
    Example:
    >>> run_lumis = [(100, 1), (100, 2), (150, 1), (150, 2), (150, 8)]
    >>> list(group_by_run(run_lumis))
    [(100, [1, 2]), (150, [1, 2, 8])]

    '''
    current_run = None
    output = []
    for run, lumi in sorted_run_lumis:
        if current_run is None or run == current_run:
            output.append(lumi)
        else:
            yield (current_run, output)
            output = [lumi]
        current_run = run
    yield (current_run, output)

def collapse_ranges_in_list(xs):
    '''
    Generate a list of contiguous ranges in a list of numbers.
    Example:
    >>> list(collapse_ranges_in_list([1, 2, 3, 5, 8, 9, 10]))
    [[1, 3], [5, 5], [8, 10]]
    '''
    output = []
    for x in xs:
        if not output:
            # Starting new range
            output = [x, x]
        elif x == output[1]+1:
            output[1] = x
        else:
            yield output
            output = [x, x]
    yield output


def json_summary(run_lumi_set):
    '''
    Compute a crab -report like json summary for a set of runs and lumis.
    Example:
    >>> run_lumis = [(100, 2), (100, 1), (150, 1), (150, 2), (150, 8)]
    >>> # Disable indentation
    >>> json_summary(run_lumis, None)
    '{"100": [[1, 2]], "150": [[1, 2], [8, 8]]}'
    '''
    run_lumis = sorted(run_lumi_set)
    output = {}
    if not run_lumis:
        return output
    for run, lumis_in_run in group_by_run(run_lumis):
        output[str(run)] = list(collapse_ranges_in_list(lumis_in_run))
    return output

if __name__ == "__main__":
    parser.add_argument('input', type=str,
                        help='A text file with a list of input ROOT files')
    parser.add_argument('tree', type=str,
                        help='Specify the path to the meta tree.')
    parser.add_argument('output', type=str, help='Output JSON file')
    parser.add_argument('--lumimask', action='store_const',
                        const=True, default=False,
                        help = 'If true, include the run-lumi mask result')
    parser.add_argument('--lumisum',  required=False, default=None,
                        help = 'Pass a file which contains the total lumi sum.')

    args = parser.parse_args(args[1:])

    files = []
    with open(args.input) as input_files:
        for input_file in input_files:
            input_file = input_file.strip()
            if input_file:
                files.append(input_file.strip())

    log.info("Extracting meta info from %i files", len(files))

    chain = ROOT.TChain(args.tree)

    for file in files:
        chain.Add(file)

    run_lumis = []
    total_events = 0

    for entry in xrange(chain.GetEntries()):
        chain.GetEntry(entry)
        total_events += chain.nevents
        run_lumis.append((chain.run, chain.lumi))

    output = {
        'n_evts' : total_events,
    }
    if args.lumimask:
        output['lumi_mask'] = json_summary(run_lumis)

    if args.lumisum:
        lumisum_file = open(args.lumisum)
        int_lumi = float(lumisum_file.read())
        output['int_lumi'] = int_lumi

    with open(args.output, 'w') as output_file:
        output_file.write(json.dumps(output, indent=2, sort_keys=True) + '\n')
