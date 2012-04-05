#!/usr/bin/env python

'''

Returns 1 if a ROOT file is missing/corrupt

Usage: cat list_of_files.txt | root_file_check.py > clean_list_of_files.txt

'''

import os
import sys
import ROOT

def is_gud(file):
    file = ROOT.TFile.Open(file, "READ")
    if not file:
        return False
    if file.TestBit(ROOT.TFile.kRecovered):
        file.Close()
        file.Delete()
        return False
    file.Close()
    file.Delete()
    return True

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if is_gud(line.strip()):
            sys.stdout.write(line + "\n")
        else:
            sys.stdout.write("# " + line + "\n")
