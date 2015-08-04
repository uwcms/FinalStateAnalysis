#!/usr/bin/env python
"""
Allows the resubmission of failed Condor jobs provided they have a rescue dag
file.

Author: D. Austin Belknap, UW-Madison
"""

import os
import re
import sys
import glob
import argparse
from socket import gethostname


def submit_jobid(jobid, dryrun=False, verbose=False):
    """
    Scan through the samples of a given job id, and check the dag status file
    for failed jobs. If any, submit the rescue dag files to farmoutAnalysisJobs
    """
    if 'uwlogin' in gethostname():
        scratch = '/data'
    else:
        scratch = '/nfs_scratch'

    user = os.environ['USER']

    path = os.path.join(scratch, user, jobid)

    samples = glob.glob('%s/*' % path)

    print "Job: %i samples in %s" % (len(samples),path)

    if verbose:
        jobTotal = 0
        jobDone = 0
        jobQueued = 0
        jobFailed = 0
        jobErrors = []

    for s in samples:
        # FSA ntuples and PAT tuples use a different naming convention for the
        # status dag files. Try both.
        status_dag1 = '%s/dags/dag.status' % s
        status_dag2 = '%s/dags/dag.dag.status' % s

        # look for failed jobs
        errors = []
        try:
            if verbose: dagStatus, nodeStatuses, endStatus = parse_dag_state(status_dag1)
            with open(status_dag1, 'r') as dagfile:
                errors = [re.search('STATUS_ERROR', line) for line in dagfile]
            with open(status_dag1, 'r') as dagfile:
                submitted = [re.search('STATUS_SUBMITTED', line) for line in dagfile]
        except IOError:
            try:
                if verbose: dagStatus, nodeStatuses, endStatus = parse_dag_state(status_dag2)
                with open(status_dag2, 'r') as dagfile:
                    errors = [re.search('STATUS_ERROR', line) for line in dagfile]
                with open(status_dag2, 'r') as dagfile:
                    submitted = [re.search('STATUS_SUBMITTED', line) for line in dagfile]
            except IOError:
                print "    Skipping: %s" % s
                continue

        # verbose details
        if verbose:
            total = dagStatus['NodesTotal']
            jobTotal += total
            done = dagStatus['NodesDone']
            jobDone += done
            queued = dagStatus['NodesQueued']
            jobQueued += queued
            failed = dagStatus['NodesFailed']
            jobFailed += failed
            statusString = "        Total: {0} Done: {1} Queued: {2} Failed: {3}".format(total,done,queued,failed)
            errors = []
            for node in nodeStatuses:
                if 'status' in node['StatusDetails']:
                    errors.append(int(node['StatusDetails'].split()[-1]))
            jobErrors.extend(errors)
            counts = [[x,errors.count(x)] for x in set(errors)]
            counts = sorted(counts, key=lambda error: error[0])
            statusString += "\n        Errors:"
            for c in counts:
                statusString += "\n            Error {0:d}: {1:d} times".format(c[0],c[1])

        # Do not try to resubmit jobs if jobs are still running
        if any(submitted):
            print "    Not done: %s" % s
            if verbose: print statusString
            continue

        # if there are any errors, submit the rescue dag files
        if any(errors):
            if dryrun:
                print "    Resubmit: %s" % s
                if verbose: print statusString
            else:
                print "    Resubmit: %s" % s
                if verbose: print statusString
                rescue_dags = glob.glob('%s/dags/*dag.rescue[0-9][0-9][0-9]' % s)
                cmd = 'farmoutAnalysisJobs --rescue-dag-file=%s' % max(rescue_dags)
                os.system(cmd)

    if verbose:
        statusString = "    Job Total: {0} Done: {1} Queued: {2} Failed: {3}".format(jobTotal,jobDone,jobQueued,jobFailed)
        counts = [[x,jobErrors.count(x)] for x in set(jobErrors)]
        counts = sorted(counts, key=lambda error: error[0])
        statusString += "\n    Job Errors:"
        for c in counts:
            statusString += "\n        Job Error {0:d}: {1:d} times".format(c[0],c[1])
        print statusString


def parse_dag_state(filename):
    with open(filename,'r') as dagfile:
        lines = dagfile.readlines()
    dagStatus = {}
    nodeStatuses = []
    endStatus = {}
    currentNode = {}
    keyvalString = ''
    for line in lines:
        if '[' in line: # new object
            currentNode = {}
        elif ']' in line: # end object
            if currentNode['Type'] == "DagStatus":
                dagStatus = currentNode
            elif currentNode['Type'] == "NodeStatus":
                nodeStatuses.append(currentNode)
            elif currentNode['Type'] == "StatusEnd":
                endStatus = currentNode
            else:
                print 'Error: unknown type "%s"' % currentNode['Type']
        elif ';' in line: # end of key val pair
            keyvalString += line
            keyvalString = ' '.join(keyvalString.split())
            keyval = keyvalString.split(';')[0]
            strings = [x.strip() for x in keyval.split('=')]
            key = strings[0]
            if '{' in strings[1]: # create a python list
                val = [x.strip('') for x in strings[1].strip('{}').split('"') if x]
            elif '"' in strings[1]: # its a python string
                val = strings[1].strip('"')
            else: # its a number
                val =  int(strings[1]) 
            currentNode[key] = val
            keyvalString = ''
        else:
            keyvalString += line
    return dagStatus, nodeStatuses, endStatus

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Resubmit failed Condor jobs')

    parser.add_argument('jobids', nargs='+', help='Provide the FSA job ID(s) (UNIX wildcards allowed) the original jobs were run with')

    parser.add_argument('--dry-run', dest='dryrun', action='store_true',
                        help='Show samples to submit without submitting them')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Show detailed information about the jobs')

    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    jobids = [directory
              for string in args.jobids
              for directory in glob.glob(string)]

    for jobid in jobids:
        submit_jobid(jobid, dryrun=args.dryrun, verbose=args.verbose)

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
