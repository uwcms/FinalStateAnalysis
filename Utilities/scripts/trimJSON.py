#!/usr/bin/env python

'''

Select a subset of runs in a JSON mask file

'''

import json
import os
import sys
from RecoLuminosity.LumiDB import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description = "Select a subset of runs in a JSON mask file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', dest='inputfile',action='store',
                        required=True,
                        help='run/lumi json file')

    parser.add_argument('-o', dest='outputfile',action='store',
                        required=True,
                        help='output file')

    parser.add_argument('-firstRun', dest='first',action='store',
                        required=False, type=int,
                        default = 1, help='First run to use')

    parser.add_argument('-lastRun', dest='last',action='store',
                        required=False, type=int,
                        default = -1, help='Last run to use')

    options=parser.parse_args()
    input = file(options.inputfile, 'r')
    input_json = json.loads(input.read())

    output_json = {}
    for run, lumilist in input_json.iteritems():
        run_int = int(run)
        if run_int < options.first:
            continue
        if options.last > 0 and run_int > options.last:
            continue
        output_json[run] = lumilist

    output_file = file(options.outputfile, 'w')
    output_file.write(json.dumps(output_json))
