#!/usr/bin/env python
'''

Convert an event list on stdin to a lumimask on stdout

Usage:

    cat mylist.txt | eventlist2lumimask.py > mylist.json

Author: Evan K. Friis, UW Madison

'''

import sys
import json
import FinalStateAnalysis.Utilities.lumitools as lumitools

if __name__ == "__main__":
    run_lumis = set([])
    for line in sys.stdin.readlines():
        # Convert to space separated
        line = line.replace('*', ' ').strip()
        if not line or 'Row' in line:
            continue
        fields = line.split()

        # always take last 3 fields
        assert(len(fields) >= 3)

        run, lumi, event = int(fields[-3]), int(fields[-2]), int(fields[-1])

        run_lumis.add( (run, lumi) )

    json.dump(lumitools.json_summary(run_lumis), sys.stdout, indent=2,
              sort_keys=True)
