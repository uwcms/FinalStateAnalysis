#!/usr/bin/env python

'''

Compare two event lists.

Usage:
    compareEventLists.py file_1 file_2

Format:

    All non-numeric characters are replaced with spaces.

'''

import sys
import re

# Replace any nonnumeric w/ spaces
replacer = re.compile(r'[^\d]+')

def get_fields(stream):
    for line in stream:
        line = line.strip()
        if not line:
            continue
        whitespace_only = replacer.sub(' ', line)
        yield tuple( int(x) for x in whitespace_only.split() )

def run_evt_only(fields):
    for event_info in fields:
        if len(event_info) == 2:
            run, event = event_info
            yield run, event
        elif len(event_info) == 3:
            run, lumi, event = event_info
            yield run, event

if __name__  == "__main__":
    file1name = sys.argv[1]
    file2name = sys.argv[2]
    file1 = open(file1name)
    file2 = open(file2name)

    file1evts = set(get_fields(file1))
    file2evts = set(get_fields(file2))

    print "%s has %i events" % (file1name, len(file1evts))
    print "%s has %i events" % (file2name, len(file2evts))

    both = file1evts.intersection(file2evts)

    print "There are %i common events" % len(both)

    file1only = file1evts - file2evts
    file2only = file2evts - file1evts

    if file1only:
        print "Events in %s only:" % file1name
        for run, lumi, evt in sorted(file1only):
            #print "run: %i lumi: %s evt: %i" % (run, lumi, evt)
            print run, lumi, evt

    if file2only:
        print "Events in %s only:" % file2name
        for run, lumi, evt in sorted(file2only):
            #print "run: %i lumi: %s evt: %i" % (run, lumi, evt)
            print run, lumi, evt

