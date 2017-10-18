#!/usr/bin/env python
'''

Dump the runs from a CMS good-run JSON file .

Author: Evan K. Friis

'''

import json
import sys
import errno

def get_runs(json_str):
    run_dictionary = json.loads(json_str)
    for run in sorted(int(x) for x in run_dictionary.keys()):
        # allow us to break the pipe
        try:
            sys.stdout.write('%i\n' % run)
        except IOError, e:
            if e.errno == errno.EPIPE:
                sys.exit(0)
            else:
                raise

if __name__ == "__main__":
    file = None
    if len(sys.argv) > 1:
        file = open(sys.argv[1], 'r')
    else:
        file = sys.stdin
    get_runs(file.read())
