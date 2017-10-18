#! /bin/env python

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
from RecoLuminosity.LumiDB import argparse
from pdb import set_trace
import glob
import os
import ROOT
ROOT.gROOT.SetBatch(True)

def rows_diff(r1, r2, to_check):
    ret = []
    for attr in to_check:
        if isinstance(attr, tuple):
            attr_name1, attr_name2 = attr
        else:
            attr_name1 = attr_name2 = attr
        a1 = getattr(r1, attr_name1)
        a2 = getattr(r2, attr_name2)
        if a1 <> a2:
            ret.append('%s: %.4f --> %.4f' % (attr, a1, a2))
    return ret

parser = argparse.ArgumentParser()
parser.add_argument('file1')
parser.add_argument('file2')
parser.add_argument('--map', type=str, default="", help='remaps the branches')
    
args = parser.parse_args()

#Load files and trees
fname1  = args.file1.split(':')[0]
tname1  = args.file1.split(':')[1]
tfile1  = ROOT.TFile.Open(fname1)
tree1   = tfile1.Get(tname1)
branch1 = set(branch.GetName() for branch in tree1.GetListOfBranches())

fname2  = args.file2.split(':')[0]
tname2  = args.file2.split(':')[1]
tfile2  = ROOT.TFile.Open(fname2)
tree2   = tfile2.Get(tname2)
branch2 = set(branch.GetName() for branch in tree2.GetListOfBranches())

#check branches naming to avoid crash
branches_to_check = branch1.intersection(branch2)
missing_branches1 = list(branch1.difference(branches_to_check))
missing_branches2 = list(branch2.difference(branches_to_check))
branches_to_check = list(branches_to_check)

if missing_branches1 or missing_branches2:
    print 'mismatching found in branch naming'
    print '+%s: ' % fname1 + ', '.join(missing_branches1)
    print '+%s: ' % fname2 + ', '.join(missing_branches2)
    print 'use option --map to remap at will these names'

if tree1.GetEntries() <> tree2.GetEntries():
    logging.warning('tree lenghts does not match!')

branch_map = None
if args.map:
    branch_map = eval(args.map)

if branch_map:
    branches_to_check.extend(branch_map.items())

for entry, rows in enumerate( zip(tree1, tree2) ):
    row1, row2 = rows
    diffs = rows_diff(row1, row2, branches_to_check)
    if diffs:
        print 'entry #%i:' % entry
        print '\n'.join(diffs)

                
