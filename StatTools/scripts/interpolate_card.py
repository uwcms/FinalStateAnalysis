#!/usr/bin/env python
'''

Apply horizontal morphing to .txt DataCards

Assumes that only the signal yields are mass dependent.

Author: Evan K. Friis

'''

from RecoLuminosity.LumiDB import argparse
import logging
from FinalStateAnalysis.StatTools.interpolator import interpolate_card
import sys

parser = argparse.ArgumentParser()

parser.add_argument('lowcard', help='Low mass input card')
parser.add_argument('lowmass', type=int, help='Lower mass')
parser.add_argument('highcard', help='High mass input card')
parser.add_argument('highmass', type=int, help='Higher mass')
parser.add_argument('target', type=int, help='Target mass')
parser.add_argument('processes', nargs='+',
                    help = 'Which processes to morph.'
                    ' The tag {mass} will be replaced by the mass')

if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    interpolate_card(sys.stdout, args.lowcard, args.lowmass,
                     args.highcard, args.highmass, args.target, args.processes)
