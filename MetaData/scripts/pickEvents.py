#!/usr/bin/env python

'''

Pick events from different datasets using a special json specifier file.

Usage:

    pickEvents.py json_file [label]

The json file should have the following format:

{
    "DATASET_ALIAS" : [ [run1, lumi1, evt1], [run2, lumi2, evt] ],
    "ANOTHER_DATASET_ALIAS" : [ [run1, lumi1, evt1], [run2, lumi2, evt] ]
}

The actual dataset corresponding to a dataset alias is mapped in
MetaData.python.datadefs

The resulting edmPickEvents.py calls are written to stdout

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import sys
import os
import json
from subprocess import Popen, PIPE, STDOUT
from FinalStateAnalysis.MetaData.datadefs import datadefs
import warnings

if __name__ == "__main__":
    warnings.warn("This script is deprecated, using pick.py instead",
                  DeprecationWarning)
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', help="JSON run-lumi-event file")
    parser.add_argument('--output', default = "{dataset}",
                        help="Name of output file.  Default: {dataset}")

    args = parser.parse_args()

    filename = args.json_file
    if not os.path.exists(filename):
        sys.stderr.write("Input file %s does not exist!\n" % filename)
        sys.exit(2)

    file = open(filename, 'r')
    events = json.load(file)

    for dataset, runevts in events.iteritems():
        real_dataset = datadefs[dataset]['datasetpath']
        command = ['fsaPickEvents.py']
        command.append('--output=%s' % args.output.format(dataset=dataset))
        command.append('--printInteractive')
        command.append(real_dataset)
        sys.stderr.write('Picking events for dataset: %s = %s '
                         % (dataset, real_dataset))
        if not runevts:
            sys.stderr.write('==> no events, skipping!\n')
            continue
        else:
            sys.stderr.write('==> picking %i events\n' % len(runevts))
        for item in runevts:
            command.append(':'.join('%i' % x for x in item))
        sys.stderr.write('Running: ' + ' '.join(command) + '\n')
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = p.communicate()
        sys.stderr.write(stderrdata)
        sys.stdout.write(stdoutdata)
