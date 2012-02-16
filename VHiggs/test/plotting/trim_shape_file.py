#!/usr/bin/env python
'''

Remove unneeded histograms from a shape file

'''

import logging
import os
from RecoLuminosity.LumiDB import argparse

log = logging.getLogger("trimmer")
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs=1, help='Limit file')
    parser.add_argument('folders', nargs='*', help='Folders to keep')
    parser.add_argument('--mass', type=int, required=True, help='Higgs mass to keep')
    parser.add_argument('--out', type=str, required=True, help='Output file')
    args = parser.parse_args()
    from rootpy.io import open, cp, rm
    import ROOT

    input = open(args.data[0], 'read')
    output = open(args.out, 'recreate')

    def exclude(path, histo):
        ''' Predicate to kill unwanted histograms '''
        if 'VH' in histo and str(args.mass) not in histo:
            return True
        return False

    for folder in args.folders:
        log.info("Copying folder: %s" % folder)
        cp(input.Get(folder), output, exclude=exclude)

    output.Write()
