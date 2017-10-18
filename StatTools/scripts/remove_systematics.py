#!/usr/bin/env python

from RecoLuminosity.LumiDB import argparse
import fnmatch
import logging
from FinalStateAnalysis.StatTools.cardreader import read_card
from FinalStateAnalysis.StatTools.cardwriter import write_card
import sys

parser = argparse.ArgumentParser()

parser.add_argument('card', help='Input card')
parser.add_argument('toremove', nargs='+', metavar='systematic', type=str,
                    help='Systematics to remove.  Can specify wildcards.')

log = logging.getLogger('remove_systematics')

if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    input = read_card(args.card)

    clean_systematics = []

    filters_applied = set([])

    for syst in input.systs:
        is_clean = True
        for filter in args.toremove:
            if fnmatch.fnmatchcase(syst[0], filter):
                is_clean = False
                filters_applied.add(filter)
                break
        if not is_clean:
            log.info("Removing systematic: %s", syst[0])
        else:
            clean_systematics.append(syst)

    for filter in args.toremove:
        if filter not in filters_applied:
            log.warning("Filter %s did not match any systematics!", filter)

    input.systs = clean_systematics
    log.info("Writing new card to stdout")
    write_card(sys.stdout, input)
