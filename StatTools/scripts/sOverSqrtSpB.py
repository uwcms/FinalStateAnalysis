#!/usr/bin/env python

'''
Stupid calculator to print out s/sqrt(s+b)

Usage:
    sOverSqrtSpB.py [s] [b]
'''

import math
import sys

s = float(sys.argv[1])
b = float(sys.argv[2])
sys.stdout.write(str(s/math.sqrt(s+b)) + '\n')
