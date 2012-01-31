#/usr/bin/env python

'''

Filters input list given lumi filter list

'''

import sys
import re

# Replace any nonnumeric w/ spaces
replacer = re.compile(r'[^\d]+')

evt_list = open(sys.argv[1])
lumi_list = open(sys.argv[2])

lumis = set([])

def get_fields(stream):
    for line in stream:
        line = line.strip()
        if not line:
            continue
        whitespace_only = replacer.sub(' ', line)
        yield tuple( int(x) for x in whitespace_only.split() )

for line in get_fields(lumi_list):
    lumis.add(line[0])

for line in get_fields(evt_list):
    run, lumi, evt = tuple(line)
    if lumi in lumis:
        print run, lumi, evt
