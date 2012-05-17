'''

Functions for interpolating data cards.

Author: Evan K. Friis, UW

'''

import copy
import logging
import FinalStateAnalysis.StatTools.morph as morph
from FinalStateAnalysis.StatTools.cardreader import read_card
from FinalStateAnalysis.StatTools.cardwriter import write_card
import sys

log = logging.getLogger('interpolate')

def interpolate_card(output_stream,
                     lowcardfile, lowmass,
                     highcardfile, highmass,
                     target, processes):
    ''' Interpolate between two data cards

    The output card (with mass=target) is written to output_stream.

    The [processes] are interpolated.  The processes can contain
    the format string {mass}
    '''

    log.info("Parsing %s m:%i", lowcardfile, lowmass)
    lowcard = read_card(lowcardfile)
    log.info("Parsing %s m:%i", highcardfile, highmass)
    highcard = read_card(highcardfile)

    assert(lowcard.bins == highcard.bins)

    newcard = copy.deepcopy(lowcard)

    for process in processes:
        targetlabel = process.format(mass=target)
        log.info("Interpolating %s process" % targetlabel)
        lowlabel = process.format(mass=lowmass)
        highlabel = process.format(mass=highmass)

        # Check the yield for this process in each bin
        for bin in lowcard.bins:
            try:
                low_yield = lowcard.exp[bin][lowlabel]
            except KeyError:
                log.error("Error reading bin: %s process: %s from file: %s",
                          bin, lowlabel, lowcardfile)
                raise

            try:
                high_yield = highcard.exp[bin][highlabel]
            except KeyError:
                log.error("Error reading bin: %s process: %s from file: %s",
                          bin, highlabel, highcardfile)
                raise

            target_yield = morph.interpolate(
                lowmass, low_yield,
                highmass, high_yield,
                target
            )
            #log.info("in bin", bin, "low yield is", low_yield,
                    #"high yield is", high_yield, "=> target is ", target_yield)
            # We use the same label as lowlabel, and replace it later
            newcard.exp[bin][lowlabel] = target_yield

    log.info("Writing new card to output")
    write_card(output_stream, newcard)
