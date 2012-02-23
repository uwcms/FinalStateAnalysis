#!/usr/bin/env python

'''

Get the appropriate stat error for a histogram

Looks up the weight that was used, then divided the yield by the weight
to get the number of unweighted entries.  Error is sqrt(unweighted)/unweighted)


'''

import bisect
import logging
import json
import math
import re
from analysis import plotter

logging.basicConfig(
    filename='get_mc_weights.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("mc_weights")
stderr_log = logging.StreamHandler()
log.addHandler(stderr_log)

vh_points = [110, 115, 120, 130, 140, 150, 160]
vhww_points = [120, 130, 140, 150, 160]

vhtt_re = re.compile('VH(?P<mass>[0-9]+)(SM4|FF|)$')
vhww_re = re.compile('VH(?P<mass>[0-9]+)WW(SM4|FF|)$')

def get_stat_error(sample, weighted_yield):
    log.info("Getting weight for %s", sample)
    sample_to_use = sample
    vhtt_match = vhtt_re.match(sample)
    if vhtt_match:
        mass = int(vhtt_match.group('mass'))
        log.info("It's a VH sample, mass %i", mass)
        # Find closest mass
        closest_mass = vh_points[0]
        for vh_mass in vh_points:
            if abs(vh_mass - mass) < abs(closest_mass - mass):
                closest_mass = vh_mass
        sample = 'VH%i' % closest_mass
        log.info("Best mass match is %s", sample)

    vhww_match = vhww_re.match(sample)
    if vhww_match:
        mass = int(vhww_match.group('mass'))
        log.info("It's a VHWW sample, mass %i", mass)
        # Find closest mass
        closest_mass = vhww_points[0]
        for vh_mass in vhww_points:
            if abs(vh_mass - mass) < abs(closest_mass - mass):
                closest_mass = vh_mass
        sample = 'VH%iWW' % closest_mass
        log.info("Best mass match is %s", sample)

    log.info("Weighted yield is: %f", weighted_yield)
    weight = plotter.get_weight(sample)[0]
    log.info("Sample weight is %f", weight)
    total_yield = weighted_yield/weight
    log.info("Sample unweighted yield is %f", total_yield)

    stat_error = 0
    if total_yield > 0:
        stat_error = math.sqrt(total_yield)/total_yield
    log.info("Stat error is %f", stat_error)
    return stat_error

if __name__ == "__main__":
    print get_stat_error('VH121', 0.2)
