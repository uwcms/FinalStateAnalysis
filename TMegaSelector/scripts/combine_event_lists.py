#!/usr/bin/env python
'''

Combine multiple output megaevents output.  The combined list
ist written to stdout.  The total nubmer of events is written to stderr

Usage: combine_event_lists.py file [file [file] ]]

'''

from RecoLuminosity.LumiDB import argparse
import json
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='file', nargs='+',
                        help = 'Event list json files')
    parser.add_argument('--count', default=False, action='store_true',
                        help = 'If supplied, just count the events.')

    args = parser.parse_args()

    full_event_list = []
    unique_events = set([])

    for filename in args.files:
        with open(filename) as file:
            event_list = json.load(file)
            full_event_list.extend(event_list)
            for event in event_list:
                unique_events.add(tuple(event['evt']))

    if not args.count:
        json.dump(full_event_list, sys.stdout, indent=2, sort_keys=True)
        sys.stderr.write(
            'Combined %i events [%i unique]\n'
            % (len(full_event_list), len(unique_events))
        )
    else:
        sys.stderr.write(
            '%i[%i unique]' % (len(full_event_list), len(unique_events)) )
