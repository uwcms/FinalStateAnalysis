#!/usr/bin/env python

'''

Convert the STDOUT of a limit calculation to a JSON string

Example

>> combine cards/mmt_channels_115.card  -t 50 | limit2JSON.py
{"ntoys": 50, "median": 13.8759, "+2": 36.808199999999999, "+1": 21.918299999999999, "-1": 10.664, "-2": 7.6471299999999998}

You can pass a mass parameter to --mass and add it as metadata.

Any alpha characters after the mass are added as a label.

Author: Evan K. Friis, UW Madison

'''

import json
import sys
import re
from RecoLuminosity.LumiDB import argparse

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

obs_re = re.compile(r'Limit: r < (?P<limit>[0-9\.]+) @ 95% CL')

#mean   expected limit: r < 15.209 +/- 4.68417 @ 95%CL (5 toyMC)
med_re = re.compile(
    r'median expected limit: r < (?P<limit>[0-9\.]+) @ 95%CL \((?P<ntoys>[0-9]+) toyMC\)')

band68_re = re.compile(
    r'68% expected band : (?P<lo68>[0-9\.]+) < r < (?P<hi68>[0-9\.]+)'
)
band95_re = re.compile(
    r'95% expected band : (?P<lo95>[0-9\.]+) < r < (?P<hi95>[0-9\.]+)'
)

# Asymptotic limit
ass_extractor = re.compile( # hee hee
    r'.*: r < (?P<value>[0-9\.]+)'
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mass', type=str, required=True,
                        help='Higgs mass')
    args = parser.parse_args()

    label_extractor = re.compile('(?P<mass>\d*)(?P<label>[a-zA-Z]*)')
    label_extraction = label_extractor.match(args.mass)
    mass = int(label_extraction.group('mass'))
    label = label_extraction.group('label')

    last_lines = []
    for line in sys.stdin:
        last_lines.append(line)
        while len(last_lines) > 10:
            last_lines.pop(0)

    # Detect if this is the observed limit
    if last_lines[-1].startswith('Done in') and 'Asymptotic' not in last_lines[-9]:
        match = obs_re.match(last_lines[-2])
        assert(match)
        output = {
            'method' : "unknown",
            'mass' : mass,
            'obs' : float(match.group('limit')),
            'label' : label
        }
        sys.stdout.write(json.dumps(output) + '\n')
    # Detect if this is using toys
    elif last_lines[-1].strip().startswith('95'):
        match95 = band95_re.match(last_lines[-1].strip())
        match68 = band68_re.match(last_lines[-2].strip())
        median = med_re.match(last_lines[-3].strip())
        assert(match95)
        assert(match68)
        assert(median)
        output = {
            'method' : "unknown",
            'mass' : mass,
            'exp' : float(median.group('limit')),
            'ntoys' : int(median.group('ntoys')),
            '-1' : float(match68.group('lo68')),
            '-2' : float(match95.group('lo95')),
            '+1' : float(match68.group('hi68')),
            '+2' : float(match95.group('hi95')),
            'label' : label,
        }
        sys.stdout.write(json.dumps(output) + '\n')
    # Detect asymptotic
    elif 'Asymptotic' in last_lines[-9]:
        #7 Observed Limit: r < 15.3322
        #6 Expected  2.5%: r < 5.5286
        #5 Expected 16.0%: r < 7.3538
        #4 Expected 50.0%: r < 10.1900
        #3 Expected 84.0%: r < 14.1539
        #2 Expected 97.5%: r < 18.8053
        #1
        #0 Done in 0.00 min (cpu), 0.00 min (real)
        obs = float(ass_extractor.match(last_lines[-8]).group('value'))
        expm2 = float(ass_extractor.match(last_lines[-7]).group('value'))
        expm1 = float(ass_extractor.match(last_lines[-6]).group('value'))
        exp = float(ass_extractor.match(last_lines[-5]).group('value'))
        expp1 = float(ass_extractor.match(last_lines[-4]).group('value'))
        expp2 = float(ass_extractor.match(last_lines[-3]).group('value'))
        output = {
            'method' : "asymp",
            'mass' : mass,
            'obs' : obs,
            'exp' : exp,
            '-1' : expm1,
            '-2' : expm2,
            '+1' : expp1,
            '+2' : expp2,
            'label' : label,
        }
        sys.stdout.write(json.dumps(output, indent=2, sort_keys=True) + '\n')

