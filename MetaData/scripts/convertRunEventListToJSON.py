#!/usr/bin/env python

'''

Convert a run-lumi-event list file to a json file usable by pickEvents.py

Usage:
    convertRunEventListToJSON.py events.txt primds out.json

'''


import sys
import FinalStateAnalysis.MetaData.datatools as datatools
import re
import json

# Replace any nonnumeric w/ spaces
replacer = re.compile(r'[^\d]+')

def get_fields(stream):
    for line in stream:
        line = line.strip()
        if not line:
            continue
        whitespace_only = replacer.sub(' ', line)
        yield tuple( int(x) for x in whitespace_only.split() )

if __name__  == "__main__":
    file1name = sys.argv[1]
    primds = sys.argv[2]
    outfilename = sys.argv[3]
    file1 = open(file1name)
    file1evts = set(get_fields(file1))

    output = {}

    for run, lumi, evt in file1evts:
        dataname = datatools.find_data_for_run(run,primds)
        run_list = output.setdefault(dataname, [])
        if (run, lumi, evt) not in run_list:
            run_list.append( (run, lumi, evt) )

    outfile = open(outfilename, 'w')
    json.dump(output, outfile, indent=4)
