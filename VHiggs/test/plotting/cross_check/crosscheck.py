#!/usr/bin/env python

'''

Usage:
    crosscheck.py event_file tree_file channel charge_cat

'''

import rootpy.io as io
import sys
import re

print "Run me from test/plotting"
sys.path.append('.')
from analysis_cfg import cfg

event_filename = sys.argv[1]
tree_file = sys.argv[2]
channel = sys.argv[3]
charge_cat = sys.argv[4]

file = io.open(tree_file)

ntuple = getattr(file, channel)

tree = ntuple.final.Ntuple
print tree

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

event_file = open(event_filename, 'r')

events = list(run_evt_only(get_fields(event_file)))

all_cuts = cfg[channel]['baseline'] + \
        cfg[channel]['charge_categories'][charge_cat]['object1']['pass'] +\
        cfg[channel]['charge_categories'][charge_cat]['object2']['pass'] +\
        cfg[channel]['charge_categories'][charge_cat]['object3']['pass'] +\
        cfg[channel]['charge_categories'][charge_cat]['selections']['final']['cuts']


good_events = 0
for event_info in events:
    run, event, lumi = None, None, None
    if len(event_info) == 2:
        run, event = event_info
    elif len(event_info) == 3:
        run, lumi, event = event_info

    run_evt = [
        'run == %i' % run,
        'evt == %i' % event
    ]
    pass_topo = tree.GetEntries(' && '.join(run_evt))
    print "\nRUN: %i EVENT: %i" % (run, event)
    if not pass_topo:
        print "- has no loose e-mu-tau candidates!"
        continue
    else:
        print "- has %i loose e-mu-tau candidates:" % pass_topo
    for i in range(pass_topo):
        idx_cut = ['idx == %i' % i]
        bad_cuts = 0
        good_cands = 0
        for cut in all_cuts:
            if 'MuCharge' in cut:
                continue
            to_test = run_evt + idx_cut + [cut]
            to_test_str = ' && '.join(to_test)
            passes_cut = tree.GetEntries(to_test_str)
            if not passes_cut:
                print "-- [cand %i] fails cut: %s" % (i, cut)
                bad_cuts += 1
        if not bad_cuts:
            print "-- [cand %i] passes all cuts" % i
            good_cands += 1
    if good_cands:
        good_events += 1
    print "- has %i e-mu-tau candidates which pass all cuts" % good_cands

print "After all cuts %i/%i events remain" % (good_events, len(events))


