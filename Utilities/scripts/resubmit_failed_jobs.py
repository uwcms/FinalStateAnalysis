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


def submit_jobid(sample, dryrun=False, verboseInfo={}):
    """
    Check the dag status file of the sample for failed jobs. If any, submit 
    the rescue dag files to farmoutAnalysisJobs. 
    Sample should be a path to the submit directory.
    """
    verbose = bool(verboseInfo)

    # FSA ntuples and PAT tuples use a different naming convention for the
    # status dag files. Try both.
    status_dag1 = '%s/dags/dag.status' % sample
    status_dag2 = '%s/dags/dag.dag.status' % sample

    # look for failed jobs
    errors = []
    try:
        if verbose: dagStatus, nodeStatuses, endStatus = parse_dag_state(status_dag1)
        with open(status_dag1, 'r') as dagfile:
            errors = [re.search('STATUS_ERROR', line) for line in dagfile]
        with open(status_dag1, 'r') as dagfile:
            submitted = [re.search('"STATUS_SUBMITTED"', line) for line in dagfile]
    except IOError:
        try:
            if verbose: dagStatus, nodeStatuses, endStatus = parse_dag_state(status_dag2)
            with open(status_dag2, 'r') as dagfile:
                errors = [re.search('STATUS_ERROR', line) for line in dagfile]
            with open(status_dag2, 'r') as dagfile:
                submitted = [re.search('STATUS_SUBMITTED', line) for line in dagfile]
        except IOError:
            print "    Skipping: %s" % sample
            return

    # verbose details
    if verbose:
        total = dagStatus['NodesTotal']
        verboseInfo["jobTotal"] += total
        done = dagStatus['NodesDone']
        verboseInfo["jobDone"] += done
        queued = dagStatus['NodesQueued']
        verboseInfo["jobQueued"] += queued
        failed = dagStatus['NodesFailed']
        verboseInfo["jobFailed"] += failed
        if not queued and failed:
            verboseInfo["doneTotal"] += total
            verboseInfo["doneDone"] += done
            verboseInfo["doneQueued"] += queued
            verboseInfo["doneFailed"] += failed
            verboseInfo["doneSamples"] += [sample]
        statusString = "        Total: {0} Done: {1} Queued: {2} Failed: {3}".format(total,done,queued,failed)
        errors = []
        for node in nodeStatuses:
            if 'status' in node['StatusDetails']:
                errors.append(int(node['StatusDetails'].split()[-1]))
        verboseInfo["jobErrors"].extend(errors)
        counts = [[x,errors.count(x)] for x in set(errors)]
        counts = sorted(counts, key=lambda error: error[0])
        #statusString += "\n        Errors:"
        #for c in counts:
        #    statusString += "\n            Error {0:d}: {1:d} times".format(c[0],c[1])

    # Do not try to resubmit jobs if jobs are still running
    if any(submitted):
        print "    %s not done, try again later" % sample
        if verbose: print statusString
        return

    # if there are any errors, submit the rescue dag files
    if any(errors):
        print "    Resubmit: %s" % sample
        if verbose: print statusString
        rescue_dag = max(glob.glob('%s/dags/*dag.rescue[0-9][0-9][0-9]' % sample))
        if verbose: print '        Rescue file: {0}'.format(rescue_dag)
        if not dryrun:
            cmd = 'farmoutAnalysisJobs --rescue-dag-file=%s' % rescue_dag
            os.system(cmd)
    else:
        #print "    %s successful, nothing to do"%sample
        pass


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
    parser = argparse.ArgumentParser(description='Resubmit failed Condor jobs',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('jobids', nargs='+', help='Provide the FSA sample(s) in'
                        ' one of the following formats (UNIX wildcards allowed):\n'
                        'jobID \n'
                        'jobID/sample \n'
                        '/path/to/job/or/submit/directory')

    parser.add_argument('--dry-run', dest='dryrun', action='store_true',
                        help='Show samples to submit without submitting them')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Show detailed information about the jobs')

    args = parser.parse_args(argv)

    return args

def generate_submit_dirs(jobids):
    '''
    Make a list of submit directories from an input argument. 
    If two or more forward slashes ('/') appear in a jobid, it is interpreted 
    as a path to a submit directory (which is resubmitted) or directory 
    containing submit directories, all of which are resubmitted.
    If there are no forward slashes, it is interpreted as a jobid, and its
    submit directories are found in /<submit_base>/<username>/jobid, where
    <submit_base> is '/data' on UWLogin and '/nfs_scratch' on login0*, and 
    all subdirectories are resubmitted.
    If there is exactly one forward slash, it is considered a jobid/sample pair
    and the sample is resubmitted.
    Either way, UNIX-style wildcards are allowed. 
    '''
    dirs = []

    if 'uwlogin' in gethostname():
        scratch = '/data'
    else:
        #scratch = '/nfs_scratch'
        scratch = '/scratch'

    user = os.environ['USER']

    for job in jobids:
        if job.count('/') > 1: # full path
            unixPath = job
        else: # jobid or jobid/sample
            unixPath = os.path.join(scratch, user, job)

        subdirs = glob.glob('%s/*' % unixPath)
        if any('dags' in s for s in subdirs): # this is a sample
            dirs += glob.glob(unixPath)
        else:
            dirs += subdirs

    return dirs


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    samples = generate_submit_dirs(args.jobids)

    verboseInfo = {}
    if args.verbose:
        verboseInfo["jobTotal"] = 0
        verboseInfo["jobDone"] = 0
        verboseInfo["jobQueued"] = 0
        verboseInfo["jobFailed"] = 0
        verboseInfo["jobErrors"] = []
        verboseInfo["doneTotal"] = 0
        verboseInfo["doneDone"] = 0
        verboseInfo["doneQueued"] = 0
        verboseInfo["doneFailed"] = 0
        verboseInfo["doneSamples"] = []

    for s in samples:
        submit_jobid(s, dryrun=args.dryrun, verboseInfo=verboseInfo)

    if args.verbose:
        statusString = "    Job Total: {0} Done: {1} Queued: {2} Failed: {3}".format(verboseInfo["jobTotal"],
                                                                                     verboseInfo["jobDone"],
                                                                                     verboseInfo["jobQueued"],
                                                                                     verboseInfo["jobFailed"])
        counts = [[x,verboseInfo["jobErrors"].count(x)] for x in set(verboseInfo["jobErrors"])]
        counts = sorted(counts, key=lambda error: error[0])
        #statusString += "\n    Job Errors:"
        #for c in counts:
        #    statusString += "\n        Job Error {0:d}: {1:d} times".format(c[0],c[1])
        print statusString

        doneStatusString = "    Resubmit Total: {0} Done: {1} Failed: {2}".format(verboseInfo["doneTotal"],
                                                                                  verboseInfo["doneDone"],
                                                                                  verboseInfo["doneFailed"])
        if verboseInfo["doneTotal"] and verboseInfo["doneFailed"]:
            print doneStatusString
            print "    Samples to resubmit:"
            for sample in verboseInfo["doneSamples"]:
                print "        {0}".format(sample)
        else:
            print "    None can be resubmitted at the moment"

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
