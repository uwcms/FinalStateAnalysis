#! /bin/env python

__doc__='''
gathers the limits produced and dumps the values into a json
Usage:
harvest_limits.py input_dir
'''

import os
import ROOT
from rootpy import io
import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
import glob
import FinalStateAnalysis.Utilities.prettyjson as prettyjson
import re

if len(sys.argv) < 2:
    print __doc__
    sys.exit(0)

def tree_to_quantile_map(tree):
    ret = {}
    for row in tree:
        #%.3f removes the approximation made in floats, that might (and it does)
        #differ between c++ and python
        ret[ '%.3f' % row.quantileExpected ] = row.limit
    return ret

def check_consistency(map, entry, value):
    if entry not in map:
        store[entry] = value
    else:
        #check if the channel is the same
        if map[entry] != value:
            raise KeyError('the %s does not match with the one of the previous files (%s)' % (value, map[entry]))
    

input_dir  = sys.argv[1]


root_files = glob.glob(os.path.join(input_dir,'*/*.root')) #FIXME: check if the name is correct*scr
file_regex = re.compile(r'higgsCombine-(?P<obs>exp|obs|sig)\.(?P<method>\w+)\.\w+\d+.root')
file_groups={}
for tfile_path in root_files:
    match   = file_regex.match(tfile_path.split('/')[-1])
    if not match:
        logging.info('%s does not match to a limit root file, skipping it...' % tfile_path)
        continue
    kind    = 'observed' if match.group('obs') == 'obs' else \
              'expected' if match.group('obs') == 'exp' else 'significance'
    method  = match.group('method')
    if (kind, method) not in file_groups:
        file_groups[(kind, method)] = []
    file_groups[(kind, method)].append(tfile_path)

for info, paths in file_groups.iteritems():
    store        = {}
    kind, method = info
    channel      = paths[0].split('/')[-3]
    store['kind']    = kind
    store['method']  = method
    store['channel'] = channel
    store['limits']  ={}
    for path in paths:
        print path
        mass     = path.split('/')[-2]
        store['limits'][mass]={}
        tfile = io.open(path)
        limit_tree = tfile.Get('limit')
        limit_map  = tree_to_quantile_map(limit_tree)
        if kind == 'expected':
            store['limits'][mass]['+2sigma'] = limit_map['0.975']
            store['limits'][mass]['+1sigma'] = limit_map['0.840']
            store['limits'][mass]['median']  = limit_map['0.500']
            store['limits'][mass]['-1sigma'] = limit_map['0.160']
            store['limits'][mass]['-2sigma'] = limit_map['0.025']
        else:
            store['limits'][mass]['median'] = limit_map['-1.000']
            
        tfile.Close()
    outfilename = '%s_%s_%s_limit.json' % (channel, method, kind)
    with open( os.path.join(input_dir,outfilename),'w') as outfile:
        outfile.write(prettyjson.dumps(store))





