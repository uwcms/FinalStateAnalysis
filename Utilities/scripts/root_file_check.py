#!/usr/bin/env python

'''

Returns 1 if a ROOT file is missing/corrupt

Usage: root_file_check.py file

'''

import os
import sys
import ROOT

if __name__ == "__main__":
    file = sys.argv[1]
    if not os.path.exists(file):
        sys.exit(1)
    file = ROOT.TFile.Open(file, "READ")
    if not file:
        sys.exit(2)
    if file.TestBit(ROOT.TFile.kRecovered):
        sys.exit(3)
    sys.exit(0)
