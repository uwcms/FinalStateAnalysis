#!/usr/bin/env python

''' Compute the percent difference between two numbers.

Usage:
    percentDiff.py 1 2

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('num1', type=float, help='First number')
    parser.add_argument('num2', type=float, help='Second number')

    args = parser.parse_args()

    diff = (args.num2 - args.num1)/args.num1

    sys.stdout.write('%0.4f\n' % diff)
