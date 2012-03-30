#!/usr/bin/env python
'''

Stupid script to check the number of entries in an Ntuple

Usage: get_ntuple_entries.py [tree] file1 [file2] ...

'''

import sys
import ROOT

treename = sys.argv[1]
files = sys.argv[2:]

chain = ROOT.TChain(treename)
for file in files:
    chain.Add(file)

print "Added %i files" % len(files)

print chain.GetEntries()
