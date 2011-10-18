#!/usr/bin/env python

# combine limits in a dumb way

import sys
import math

if __name__ == "__main__":
    vals = [float(x) for x in sys.argv[1:]]
    denominator = sum(1/(x*x) for x in vals)
    print 1/math.sqrt(denominator)

