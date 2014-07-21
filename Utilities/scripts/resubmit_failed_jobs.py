#!/usr/bin/env python

import os
import re
import sys
import glob
import argparse


def submit_jobid(jobid):
    user = os.environ['USER']
    scratch = '/nfs_scratch'

    path = os.path.join(scratch, user, jobid)

    samples = glob.glob('%s/*' % path)

    for s in samples:
        status_dag1 = '%s/dags/dag.status' % s
        status_dag2 = '%s/dags/dag.dag.status' % s
        errors = []
        try:
            with open(status_dag1, 'r') as dagfile:
                errors = [True and re.search('ERROR', line) for line in dagfile]
        except IOError:
            try:
                with open(status_dag2, 'r') as dagfile:
                    errors = [True and re.search('ERROR', line) for line in dagfile]
            except IOError:
                print "Skipping: %s" % s
                continue

        if any(errors):
            rescue_dags = glob.glob('%s/dags/*dag.rescue[0-9][0-9][1-9]' % s)
            for dag in rescue_dags:
                cmd = 'farmoutAnalysisJobs --rescue-dag-file=%s' % dag
                print cmd
                os.system(cmd)


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('jobid', type=str, help='')

    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    submit_jobid(args.jobid)

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
