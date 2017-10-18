#!/usr/bin/env python
'''

Apply a set operation from one lumimask json from another lumimask.

Writes the result to a json on stdout.

Author: Evan K. Friis, UW Madison

'''

import json
import FinalStateAnalysis.Utilities.lumitools as lumitools
from RecoLuminosity.LumiDB import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Subtract one lumi mask from another. '
        'Can add ":first:last" to select a subset of runs')
    parser.add_argument('lumimask1', help='Lumimask 1')
    parser.add_argument('operation', help='Operation to apply',
                        choices = ['+', '-', 'and'])
    parser.add_argument('lumimask2', help='Lumimask 2')

    args = parser.parse_args()

    # Load lumis
    lumis1 = lumitools.lumi_list_from_file(args.lumimask1)
    lumis2 = lumitools.lumi_list_from_file(args.lumimask2)

    set_operations = {
        '+' : set.union,
        '-' : set.difference,
        'and' : set.intersection,
    }

    result = set_operations[args.operation](lumis1, lumis2)

    result_summary = lumitools.json_summary(result)
    json.dump(result_summary, sys.stdout, indent=2, sort_keys=True)
