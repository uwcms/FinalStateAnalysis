#! /bin/env python

import os
import sys
from RecoLuminosity.LumiDB import argparse
import ROOT
import re
from pdb import set_trace

ROOT.gROOT.SetBatch(True)

def txt2tuple(line):
    return tuple([ int(i.strip()) for i in line.split(':') ])

def row2tuple(row):
    return int(row.run), int(row.lumi), int(row.evt)

def group(branch_lists):
    groupable = re.compile('(?P<group>[emt]\d?)[A-Z]')
    ret = {} #{'misc' : []}
    for branch in branch_lists:
        m = groupable.match(branch)
        if m:
            gr = m.group('group')
            if gr in ret:
                ret[gr].append(branch)
            else:
                ret[gr] = [branch]
        else:
            gr = 'misc'
            if gr in ret:
                ret[gr].append(branch)
            else:
                ret[gr] = [branch]
    return ret

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('events')
parser.add_argument('treepath')
parser.add_argument('scan', help='supports python regex')
#parser.add_argument('--filter', type=str, default="", help='filters the events')
parser.add_argument('--by-combination', dest='combos', action='store_true')

args = parser.parse_args()

event  = txt2tuple(args.events) #[txt2tuple(i) for i in args.events]
tfile  = ROOT.TFile.Open(args.file)
tree   = tfile.Get(args.treepath)

branches = [branch.GetName() for branch in tree.GetListOfBranches()]
regexes  = [re.compile(i+'$') for i in args.scan.split(',')]
branches_to_monitor = [ i for i in branches if any(regex.match(i) for regex in regexes)]
#set_trace()
grouped = group(branches_to_monitor)
monitor = dict((i,[]) for i in branches_to_monitor)

for row in tree:
    if row2tuple(row) == event: 
        for i in branches_to_monitor:
            monitor[i].append( getattr(row, i) )

by_option = {}
for gr, branches in grouped.iteritems():
    values_by_option = zip(*[monitor[i] for i in branches])
    group_options = []
    for values in values_by_option:
        to_append = '-- '
        for info in zip([i.replace(gr,'', 1) for i in branches], values):
            to_append += '%s: %.4f   ' % info
        #to_append += '\n'
        group_options.append(to_append)

    if not args.combos:
        print '%s:' % gr
        for opt in set(group_options): #remove duplicates
            print opt
        print
    else:
        by_option[gr] = group_options

if args.combos:
    for i in range( len(by_option[grouped.keys()[0]]) ):
        print "\nCombination #%i" % i
        for key in by_option:
            print '%s:' % key
            print by_option[key][i]
