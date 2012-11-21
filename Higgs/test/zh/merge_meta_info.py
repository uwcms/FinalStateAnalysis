#!/usr/bin/env python

'''

Merge a bunch of JSON files with meta information into a big dictionary.

The key generated for each file is basename(file).replace('.meta.json', '')

Author: Evan K. Friis

'''

from RecoLuminosity.LumiDB import argparse
import json
import logging
import os

if __name__ == "__main__":
    log = logging.getLogger("merge_meta_info")

    parser = argparse.ArgumentParser()

    parser.add_argument('output', help='Output JSON file')
    parser.add_argument('inputs', metavar='file', nargs='+',
                        help='Input JSON files to merge')

    args = parser.parse_args()

    output = {}

    for input in args.inputs:
        sample = os.path.basename(input).replace('.meta.json', '')
        log.info("Merging sample %s from file %s", sample, input)
        with open(input) as input_file:
            output[sample] = json.load(input_file)

    log.info("Writing merged JSON output to %s", args.output)
    with open(args.output, 'w') as output_file:
        output_file.write(json.dumps(output, sort_keys=True, indent=2))
