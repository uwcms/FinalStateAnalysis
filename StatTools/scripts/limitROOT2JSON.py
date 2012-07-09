#!/usr/bin/env python
'''

Extract the limit information from a Higgs combine result(s) and write it to a JSON.

'''

from RecoLuminosity.LumiDB import argparse
import json
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('rootfiles', nargs='+')
    args = parser.parse_args()

    import ROOT

    tree = ROOT.TChain('limit')
    for file in args.rootfiles:
        tree.Add(file)

    def get_quantile(x):
        # Convert a float value to a string label
        if x < 0:
            return 'obs'
        elif 0.0 < x < 0.027:
            return '-2'
        elif 0.1 < x < 0.2:
            return '-1'
        elif 0.4 < x < 0.6:
            return 'exp'
        elif 0.8 < x < 0.85:
            return '+1'
        elif 0.97 < x < 0.976:
            return '+2'
        return None

    output = {}

    for row in tree:
        quantile = get_quantile(row.quantileExpected)
        limit = row.limit
        output[quantile] = limit
        output['mass'] = row.mh

    json.dump(output, sys.stdout, indent=2)
