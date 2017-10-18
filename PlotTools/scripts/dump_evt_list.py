#! /bin/env python

import ROOT
import sys
from pdb import set_trace

tree_path  = sys.argv[1]

tree = ROOT.TChain(tree_path) #tfile.Get(tree_path)

for fname in sys.argv[2:]:
    tree.Add(fname)

for row in tree:
    print '%i:%i:%i' % (row.run, row.lumi, row.evt)


