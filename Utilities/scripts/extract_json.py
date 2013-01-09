#!/usr/bin/env python
'''

Extract a given key from a JSON object stream on stdin and write it to stdout.

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import sys
import json

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="Key to extract")
    args = parser.parse_args()
    input = json.load(sys.stdin)
    if args.key not in input:
        sys.stderr.write("Key %s is not in input JSON!\n" % args.key)
        sys.stderr.write("JSON content: !\n")
        sys.stderr.write(str(input) + '\n')
        sys.exit(1)

    sys.stdout.write(json.dumps(input[args.key]) + '\n')
