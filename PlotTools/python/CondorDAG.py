""" Representation of a Condor DAG file

Author: Evan K. Friis

"""

import os
import re


def get_jobs(dagfile):
    """ Generate a list of (jobid, submitfile) from the DAG file. """
    with open(dagfile, 'r') as dag:
        for line in dag:
            if line.startswith('JOB'):
                fields = line.strip().split(' ')
                yield (fields[1], fields[2])


def get_edges(dagfile):
    """ Generate list of (parentid, childid) dependencies in the DAG file. """
    with open(dagfile, 'r') as dag:
        for line in dag:
            if line.startswith('PARENT'):
                fields = line.strip().split(' ')
                yield (fields[1], fields[3])


class CondorDAGJob(object):
    """ Representation of a single CondorDAG job. """
    def __init__(self, jobname, submitfile):
        self.jobname = jobname
        self.submitfile = submitfile
        self.daughters = []
        self.parents = []

    def __hash__(self):
        """ The jobname is always unique. """
        return hash(self.jobname)

    def repr(self):
        return "CondorDAGJob(%s, %s)" % (self.jobname, self.submitfile)

    def leaves(self):
        """ Generate the leaves of this subtree.

        A leaf may appear more than once

        """
        if not self.daughters:
            yield self
        else:
            for daughter in self.daughters:
                for leaf in daughter.leaves():
                    yield leaf

    def output_file(self):
        """ Get the output root file of this job. """
        with open(self.submitfile, 'r') as submitfile:
            print submitfile
            for line in submitfile:
                # the output is stored like:
                # # DAG_OUTPUT_FILENAME THE_FILE.root
                if 'DAG_OUTPUT_FILENAME' in line:
                    thefile = line.strip().replace(
                        '# DAG_OUTPUT_FILENAME ', '')
                    return thefile


class CondorDAG(object):
    """ Representation of a full batch processing DAG """
    def __init__(self, dagfile):
        self.nodes = {}
        self.status = ("UNKNOWN", "")
        self.dagfile = dagfile
        for jobid, submitfile in get_jobs(dagfile):
            self.nodes[jobid] = CondorDAGJob(jobid, submitfile)
        for parent, child in get_edges(dagfile):
            self.nodes[parent].daughters.append(self.nodes[child])
            self.nodes[child].parents.append(self.nodes[parent])

    def roots(self):
        """ Generate jobs which have no dependencies. """
        for jobid, dagjob in self.nodes.iteritems():
            if not dagjob.parents:
                yield dagjob

    def leaves(self):
        """ Return the set of jobs which have no children """
        jobs = set()
        # Get leafs of each root
        for root in self.roots():
            for leaf in root.leaves():
                jobs.add(leaf)
        return list(jobs)

    def update_status(self):
        """ Parse the dag status file.

        Returns a tuple with (STATUS, REASON) giving the overall status
        of the DAG.

        """
        jobmatcher = re.compile(
            'JOB\s+(?P<jobid>\S+)\s+(?P<status>\S+)\s+\((?P<info>\S*)\)')
        dagmatcher = re.compile(
            'DAG status:\s+(?P<status>\S+)\s+(?P<info>\S*)')

        dagstatusfile = self.dagfile + '.status'

        if not os.path.exists(dagstatusfile):
            return self.status

        with open(dagstatusfile, 'r') as statusfile:
            for line in statusfile:
                jobmatch = jobmatcher.match(line)
                if jobmatch:
                    self.nodes[jobmatch.group('jobid')] = (
                        jobmatch.group('status'), jobmatch.group('info'))
                    continue
                dagmatch = dagmatcher.match(line)
                if dagmatch:
                    self.status = (dagmatch.group('status'),
                                   dagmatch.group('info'))
        return self.status

    def failing_nodes(self):
        for nodeid, node in self.nodes.iteritems():
            if node.status[0] == "STATUS_ERROR":
                yield (nodeid, node.status[1])
