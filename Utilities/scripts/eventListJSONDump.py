#!/usr/bin/env python

'''
Convert an json style event list info a CSV list

Usage:
    eventListDumpJSON.py my_list.json [format]

Format can be python or colons

'''

import json
import sys

formats = {
    'python' : '(%i, %i, %i),\n',
    'colons' : '%i:%i:%i\n',
}

if __name__ == "__main__":
    json_file = open(sys.argv[1], 'r')
    info = json.load(json_file)
    format_type = 'python'
    if len(sys.argv) > 2:
        format_type = sys.argv[2]
    format = formats[format_type]
    all_events = []
    for data_set, events in info.iteritems():
        all_events.extend(events)
    for event in sorted(tuple(x) for x in all_events):
        sys.stdout.write(format % event)
