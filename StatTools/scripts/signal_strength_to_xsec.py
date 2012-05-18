#!/usr/bin/env python
'''

Converts a JSON file with limit output as sigma/sigma_SM into a JSON file
where the limit is reported as sigma_SM.

The output is written to stdout

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
from FinalStateAnalysis.MetaData.higgs_tables import cross_section
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')
import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('processes', nargs='+',
                        help='Production processes to include')
    parser.add_argument('--sqrts', type=float, default=7.,
                        help='Collission energy')


    args = parser.parse_args()

    input_file = open(args.input, 'r')
    input = json.load(input_file)

    for datum in ['exp', "+1", "+2", "-1", "-2", "obs"]:
        if datum in input:
            xsection = 0
            for process in args.processes:
                xsection += input[datum]*cross_section(
                    process, input['mass'], args.sqrts)
            input[datum] = xsection

    sys.stdout.write(json.dumps(input, indent=2, sort_keys=True) + '\n')
