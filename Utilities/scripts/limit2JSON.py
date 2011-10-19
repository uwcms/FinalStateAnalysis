#!/usr/bin/env python

'''

Convert a limit calculation to a JSON string

Example

>> combine cards/mmt_channels_115.card  -t 50 | limit2JSON.py
{"ntoys": 50, "median": 13.8759, "+2": 36.808199999999999, "+1": 21.918299999999999, "-1": 10.664, "-2": 7.6471299999999998}

Author: Evan K. Friis, UW Madison

'''

import sys
import re
import json

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

if __name__ == "__main__":
    last_lines = []
    for line in sys.stdin:
        last_lines.append(line)
        while len(last_lines) > 10:
            last_lines.pop(0)

    # Detect if this is the observed limit
    if last_lines[-1].startswith('Done in'):
        match = obs_re.match(last_lines[-2])
        assert(match)
        output = {'obs' : float(match.group('limit'))}
        sys.stdout.write(json.dumps(output) + '\n')
    # Detect if this is a toys
    elif last_lines[-1].strip().startswith('95'):
        match95 = band95_re.match(last_lines[-1].strip())
        match68 = band68_re.match(last_lines[-2].strip())
        median = med_re.match(last_lines[-3].strip())
        assert(match95)
        assert(match68)
        assert(median)
        output = {
            'median' : float(median.group('limit')),
            'ntoys' : int(median.group('ntoys')),
            '-1' : float(match68.group('lo68')),
            '-2' : float(match95.group('lo95')),
            '+1' : float(match68.group('hi68')),
            '+2' : float(match95.group('hi95')),
        }
        sys.stdout.write(json.dumps(output) + '\n')
