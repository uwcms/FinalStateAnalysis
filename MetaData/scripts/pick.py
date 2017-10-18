#!/usr/bin/env python

'''

Pick events

Usage:
    pick.py primds json_file1 json_file2 --output output_name

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import sys
import logging
import os
import json
from subprocess import Popen, PIPE, STDOUT
from FinalStateAnalysis.MetaData.datadefs import datadefs
import FinalStateAnalysis.MetaData.datatools as datatools

if __name__ == "__main__":
    log = logging.getLogger("pick")
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset',
                        help="Dataset - either full DBS path or PrimDS")
    parser.add_argument('json_file', nargs='+',
                        help="JSON run-lumi-event files")
    parser.add_argument('--output', default = "{dataset}",
                        help="Name of output file.  Default: {dataset}")

    args = parser.parse_args()

    # Group by DBS datasets
    data_sets_to_pick = {}

    is_data = '/' not in args.dataset
    if is_data:
        log.info("DATA MODE")
    else:
        log.info("MC MODE")

    event_list = []
    for json_input_name in args.json_file:
        log.info("Getting events from %s", json_input_name)
        with open(json_input_name, 'r') as json_input:
            this_event_list = json.load(json_input)
            log.info("=> got %i events", len(this_event_list))
            event_list.extend(this_event_list)

    log.info("Determining which event belongs to which dataset")

    for event in event_list:
        if not 'evt' in event:
            log.error("Couldn't get the 'evt' key from event %s", event)
            sys.exit(1)
        run, lumi, evt = event['evt']
        dataset = args.dataset
        if is_data:
            dataname = datatools.find_data_for_run(run,dataset)
            dataset = datatools.map_data_to_dataset(dataname)

        dataset_dict = data_sets_to_pick.setdefault(dataset, [])
        dataset_dict.append((run, lumi, evt))

    log.info("Generating pickEvents commands")
    for real_dataset, runevts in data_sets_to_pick.iteritems():
        command = ['fsaPickEvents.py']
        clean_dataset = real_dataset.strip('/').replace('/', '-')
        command.append('--output=%s' % args.output.format(dataset=clean_dataset))
        command.append('--printInteractive')
        command.append(real_dataset)
        log.info('Picking events for dataset: %s' % (real_dataset))
        if not runevts:
            log.info('==> no events, skipping!')
            continue
        else:
            log.info('==> picking %i events' % len(runevts))
        for item in runevts:
            command.append(':'.join('%i' % x for x in item))
        log.info('Running: ' + ' '.join(command))
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = p.communicate()
        log.info(stderrdata)
        sys.stdout.write(stdoutdata)
