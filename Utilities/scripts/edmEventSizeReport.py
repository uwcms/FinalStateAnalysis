#!/usr/bin/env python
'''

A version of edmEventSize which gives more information

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import os
from FinalStateAnalysis.Utilities.prettytable import PrettyTable
import subprocess


def query_file(file):
    ''' Returns [ (file1, unc_size, comp_size), ... ] '''
    file = file.replace('root://cmsxrootd.hep.wisc.edu/', '/hdfs/')
    p = subprocess.Popen(['edmEventSize', '-v', file],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    output = []
    events = None
    for line in stdout.split('\n'):
        if not line:
            continue
        if line.startswith('File'):
            # Number of events in file
            events = int(line.split()[3])
            continue
        if line.startswith('Branch'):
            continue
        fields = line.split()
        info = (fields[0].strip(), float(fields[1]), float(fields[2]))
        output.append(info)
    output.sort(key=lambda x: x[2])
    statinfo = os.stat(file)
    return {
        'products': output,
        'size': statinfo.st_size,
        'events': events
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='AOD file')
    parser.add_argument('--wrt', default=None, help='Original to compare to')

    args = parser.parse_args()

    file_info = query_file(args.file)
    total = sum(x[2] for x in file_info['products'])

    table = PrettyTable(['Branch', 'Uncompress', 'Compressed', 'Percent'])
    for  branch, unc, comp in file_info['products']:
        percent = 100. * comp / total
        table.add_row([branch, unc, comp, '%0.f%%' % percent])

    print "Branches"
    print table

    print "Events: %i" % file_info['events']
    print "Total size: %i kb" % (file_info['size'] / 1000.)
    print "=> %0.0f kb/evt" % (file_info['size'] / 1000. / file_info['events'])

    if args.wrt:
        wrt_info = query_file(args.wrt)
        print ""
        print "===SOURCE FILE==="
        print "Events: %i" % wrt_info['events']
        print "Total size: %i kb" % (wrt_info['size'] / 1000.)
        print "=> %0.0f kb/evt" % (
            wrt_info['size'] / 1000. / wrt_info['events'])

        print "Skim eff: %0.3f" % (
            float(file_info['events']) / wrt_info['events'])
        print "Size eff: %0.2f" % (
            float(file_info['size']) / wrt_info['size'])
