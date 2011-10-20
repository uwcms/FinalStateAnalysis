#!/usr/bin/env python

'''

Add numbers in quadrature.

Usage: quad.py 10 2

Author: Evan K. Friis

'''

import math
import sys

def quad(*xs):
    return math.sqrt(sum(float(x)*float(x) for x in xs))

if __name__ == "__main__":
    print quad(*sys.argv[1:])
