#!/usr/bin/env python
'''

Get information about published PAT tuple datasets

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
from FinalStateAnalysis.MetaData.datadefs import datadefs
import logging
import json
import os
from FinalStateAnalysis.MetaData.datatools import query_pattuple
from FinalStateAnalysis.MetaData.dbslumis import query_lumis_in_dataset
import sys

log = logging.getLogger("get_tuple_info")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tuple_list',
                        help='Txt file with list of published PAT tuples')
    parser.add_argument('output', help='Output json file')
    parser.add_argument('--update-all', dest='update', action='store_true',
                        help='Rebuild the output json from scratch')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='Increase verbosity')

    args = parser.parse_args()

    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level, stream=sys.stderr)

    tuple_info = {}
    # If desired, don't repeat calls
    if not args.update and os.path.exists(args.output):
        with open(args.output, 'r') as existing:
            tuple_info = json.load(existing)

    try:
        with open(args.tuple_list, 'r') as input:
            for line in input.readlines():
                dataset = line.strip()
                if dataset not in tuple_info:
                    log.info("Querying DAS for %s" % dataset)
                    info = query_pattuple(dataset)
                    tuple_info[dataset] = info

        log.info("Checking if we need to compute lumi results")
        for sample, sample_info in tuple_info.iteritems():
            if sample_info['parent'].endswith('AOD'):
                log.info("Getting lumis for sample %s", sample)
                # Ony update the files we don't have
                current_lumimask = sample_info.setdefault('lumimask', {})
                lumis = query_lumis_in_dataset(sample, current_lumimask)
                sample_info['lumimask'] = lumis

    finally:
        # Always clean up and write what we wrote at the end
        with open(args.output, 'w') as output:
            json.dump(tuple_info, output, indent=2, sort_keys=True)
