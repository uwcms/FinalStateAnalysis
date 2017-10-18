#! /bin/env python

import FinalStateAnalysis.Utilities.prettyjson as prettyjson
from optparse import OptionParser
import logging

parser = OptionParser()
parser.add_option('--tag', '-t', type=str, default = None,
                  help='value of the tag to be added',dest='tag')
parser.add_option('--label', '-l', type=str, default = 'tag',
                  help='label of the tag to be added',dest='label')

(options,jsons) = parser.parse_args()

tagVal = options.tag

for jfile in jsons:
    json = prettyjson.loads( open(jfile).read() )
    json[options.label] = tagVal
    with open(jfile,'w') as out:
        out.write(prettyjson.dumps(json))
