#!/usr/bin/env python

'''

Stupid script to calculator the delta R between two numberso

deltaR.py eta1,phi1 eta2,phi2

'''

import sys
import math

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'Usage:\n    deltaR.py eta1,phi1 eta2,phi2 '
        sys.exit(0)
    pair1 = sys.argv[1]
    pair2 = sys.argv[2]

    eta1, phi1 = tuple(float(x) for x in pair1.split(','))
    eta2, phi2 = tuple(float(x) for x in pair2.split(','))

    deta = eta1-eta2
    dphi = phi1-phi2

    print "%0.3f" % math.sqrt( deta*deta + dphi*dphi )
