#!/usr/bin/env python

'''

Usage:
    crosscheck.py event_file tree_file channel charge_cat obj1 obj2 obj3

    Where obj1,2,3 are the names of the objects - Mu, Elec, etc.

'''

import ROOT
import rootpy.io as io
from rootpy.utils import asrootpy
import sys
import re

print "Run me from test/plotting"
sys.path.append('.')
from analysis_cfg import cfg

event_filename = sys.argv[1]
tree_file = sys.argv[2]
channel = sys.argv[3]
charge_cat = sys.argv[4]
obj1 = sys.argv[5]
obj2 = sys.argv[6]
obj3 = sys.argv[7]

#file = io.open(tree_file)
#ntuple = getattr(file, channel)
#tree = asrootpy(ntuple.final.Ntuple)

tree = ROOT.TChain("%s/final/Ntuple" % channel)
files_added = tree.Add(tree_file)
print "Added %i files" % files_added

print "Total %i entries" % tree.GetEntries()

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

#events = list(run_evt_only(get_fields(event_file)))
events = list(get_fields(event_file))

all_cuts = cfg[channel]['baseline'] + \
        cfg[channel]['charge_categories'][charge_cat]['object1']['pass'] +\
        cfg[channel]['charge_categories'][charge_cat]['object2']['pass'] +\
        cfg[channel]['charge_categories'][charge_cat]['object3']['pass'] +\
        cfg[channel]['charge_categories'][charge_cat]['selections']['final']['cuts']


good_events = 0
good_events_list = []
bad_events = []
for event_info in events:
    run, event, lumi = None, None, None
    if len(event_info) == 2:
        run, event = event_info
    elif len(event_info) == 3:
        run, lumi, event = event_info

    run_evt = [
        'evt == %i' % event,
        'run == %i' % run,
    ]
    pass_topo = tree.GetEntries(' && '.join(run_evt))
    print "\nRUN: %i LUMI: %i EVENT: %i" % (run, lumi, event)
    if not pass_topo:
        print "- has no loose WH candidates!"
        continue
    else:
        print "- has %i loose WH candidates:" % pass_topo
    good_cands = 0
    for i in range(pass_topo):
        idx_cut = ['idx == %i' % i]
        bad_cuts = 0

        object_pts = []
        object_etas = []

        for obj in [obj1, obj2, obj3]:
            histo_name_pt = "htemp_%i_%i_%s_pt" % (event, i, obj)
            histo_name_eta = "htemp_%i_%i_%s_eta" % (event, i, obj)
            #print objstr
            selector = run_evt + idx_cut

            objstr_pt = '%sPt>>%s' % (obj, histo_name_pt)
            objstr_eta = '%sEta>>%s' % (obj, histo_name_eta)
            tree.Draw(objstr_pt, '&&'.join(selector))
            obj_pt_hist = ROOT.gDirectory.Get(histo_name_pt)
            tree.Draw(objstr_eta, '&&'.join(selector))
            obj_eta_hist = ROOT.gDirectory.Get(histo_name_eta)
            #print obj_pt_hist.GetMaximumBin()
            #print obj_pt_hist.GetEntries(), obj_pt_hist.GetMean()
            object_pts.append(obj_pt_hist.GetMean())
            object_etas.append(obj_eta_hist.GetMean())

        topo_str = "[%s][%s]" % (
            ",".join("%0.1f" % x for x in object_pts),
            ",".join("%0.1f" % x for x in object_etas)
        )

        for cut in all_cuts:
            #if 'MuCharge' in cut:
                #continue
            #if 'vtx' in cut:
                #continue
            #if 'DoubleMus_HLT' in cut:
                #continue
            to_test = run_evt + idx_cut + [cut]
            to_test_str = ' && '.join(to_test)

            passes_cut = tree.GetEntries(to_test_str)
            if not passes_cut:
                print "-- [cand %i %s] fails cut: %s" % (i, topo_str, cut)
                bad_cuts += 1

        if not bad_cuts:
            print "-- [cand %i %s] passes all cuts" % (i, topo_str)
            good_cands += 1
    if good_cands:
        good_events += 1
        good_events_list.append((run, lumi, event))
    else:
        bad_events.append((run, lumi, event))
    print "- has %i WH candidates which pass all cuts" % good_cands

print "After all cuts %i/%i events remain" % (good_events, len(events))
print "The following events passed:"
for run_lumi_event in good_events_list:
    print ' '.join(str(x) for x in run_lumi_event)
print "The following events failed:"
for run_lumi_event in bad_events:
    print ' '.join(str(x) for x in run_lumi_event)
