#!/usr/bin/env python

'''

Parse the CSV output of lumicalc2.py and compute the average inst. luminosity.

The units are microbarns/second.

Author: Evan Friis, UW Madison

'''

import sys

def get_recorded(line):
    fields = line.strip().split(',')
    recorded = float(fields[-1])
    return recorded

def averageAndTotal(lines):
    total = 0.0
    nlines = 0
    for line in lines.splitlines():
        if 'Recorded' in line:
            continue
        total += get_recorded(line)
        nlines += 1
    return total/nlines, total*(1.0/0.0429)

if __name__ == "__main__":
    file = None
    if len(sys.argv) > 1:
        file = open(sys.argv[1], 'r')
    else:
        file = sys.stdin
    sys.stdout.write('%0.3f, %0.3f\n' % averageAndTotal(file.read()))
