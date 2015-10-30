#!/usr/bin/env python
'''

Parses the CSV output of lumi calc to get the total luminosity.

Prints the recorded int. lumi. (in pb-1) to STDOUT

Usage:

    lumicalc_parser.py lumiCalc_output.csv

Author: Evan K. Friis, UW Madison

'''

from FinalStateAnalysis.Utilities.lumitools import parse_lumicalc_output

if __name__ == "__main__":
    import sys
    print "cannot parse lumi yet"
#    print parse_lumicalc_output(sys.argv[1])
