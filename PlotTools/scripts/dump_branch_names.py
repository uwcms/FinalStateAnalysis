#! /bin/env python

import sys
if len(sys.argv) < 3 or '-h' in sys.argv or '--help' in sys.argv:
    print 'Usage dump_branch_names.py file.root path/to/Tree'
    sys.exit(1)

#Open sample file
import ROOT
ROOT.gROOT.SetBatch(True)
tfile = ROOT.TFile.Open(sys.argv[-2])

tree = tfile.Get(sys.argv[-1])
#Get All the branches
print '\n'.join([branch.GetName() for branch in tree.GetListOfBranches()])
tfile.Close()
