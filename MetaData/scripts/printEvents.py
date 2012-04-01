#!/usr/bin/env python
'''

Companion to pickEvents.py

Prints out the run lumi and event numbers given a event list json file.

'''

import sys
import json

if __name__ == "__main__":
    file = open(sys.argv[1], 'r')
    runs = json.load(file)

    evtlist = []

    for dataset, runevts in runs.iteritems():
        for runlumievt in runevts:
            evtlist.append(tuple(runlumievt))

    for runlumievt in sorted(evtlist):
        print " ".join(['%s' % x for x in runlumievt])
