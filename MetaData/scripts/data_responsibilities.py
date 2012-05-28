#!/usr/bin/env python
'''

Print out the size and number of events for each sample, and a summary for each
responible.


Author: Evan K. Friis, UW Madison

'''

from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.MetaData.datatools import query_das

people = {}

for dataset in sorted(datadefs.keys()):
    dataset_info =  datadefs[dataset]
    result = query_das(dataset_info['datasetpath'])
    print " ".join([
        dataset,
        'Files: %i' % result['nfiles'],
        'Events: %s' % result['nevents'],
        'Size: %0.f GB' % result['size'],
        'Resp: %s' % dataset_info['responsible']
    ])
    sofar = people.setdefault(dataset_info['responsible'], 0)
    people[dataset_info['responsible']] += result['size']

print ""
print "Job summary"
print "==========="
for k, v in people.iteritems():
    print "%s has %0.f GB of data to process"

