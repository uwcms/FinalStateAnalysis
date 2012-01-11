#!/usr/bin/env python

'''
Convert an json style event list info a CSV list

Usage:
    eventListDumpJSON.py my_list.json

'''

import json
import sys

if __name__ == "__main__":
    json_file = open(sys.argv[1], 'r')
    info = json.load(json_file)
    all_events = []
    for data_set, events in info.iteritems():
        all_events.extend(events)
    for event in sorted(tuple(x) for x in all_events):
        sys.stdout.write('(%i, %i, %i),\n' % event)
