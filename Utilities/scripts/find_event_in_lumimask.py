#! /bin/env python

from RecoLuminosity.LumiDB import argparse
import FinalStateAnalysis.Utilities.prettyjson as prettyjson
import sys
import os

def txt2tuple(line):
    return tuple([ int(i.strip()) for i in line.split(':') ])

def is_in_json(evt, jsonmask):
    run  = evt[0]
    lumi = evt[1]
    if str(run) in jsonmask:
        for lumis in jsonmask[str(run)]:
            if lumis[0] <= lumi <= lumis[1]:
                return True
    return False


parser = argparse.ArgumentParser()
parser.add_argument('event')
parser.add_argument('masks', nargs='+')

args = parser.parse_args()
event = txt2tuple(args.event)

#print args.masks
jsons = [ (i, prettyjson.loads( open(i).read() )) for i in args.masks ]

for name, mask in jsons:
    if is_in_json(event, mask):
        print "Event %s should be in %s" % (args.event, name)
        sys.exit(0)

print "Event %s not found in any json!" % args.event

