""" Representation of a Condor DAG file.

Has various utility for querying status and parameters of the job.

Author: Evan K. Friis

"""

import collections
import os
import re
import logging
import linecache
log = logging.getLogger("__dags__")


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
        self.status = ("UNKNOWN", "")

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
            'JOB\s+(?P<jobid>\S+)\s+(?P<status>\S+)\s+\((?P<info>.*)\)') 
        dagmatcher = re.compile(r'NodeStatus\s\S\s\S+\s\S+\s\S(?P<status>\w+)')
                                           
        dagstatusfile = self.dagfile + '.status'

        if not os.path.exists(dagstatusfile):
            return self.status

        with open(dagstatusfile, 'r') as statusfile:
            lines = statusfile.readlines()
            for i,line in enumerate(lines):
                
                if not 'Node = ' and not 'DagStatus =' in line:
                    continue
                if 'Node =' in line :
                    #log.info("line %s  and line %s" %(line, lines[i+1]))
                    jobidmatch = re.search('Node\s\S\s\S(?P<jobid>\S+)\S\S\n', line)
                    jobmatch =  re.search('NodeStatus\s\S\s\S+\s\S+\s\S(?P<status>\w+)', lines[i+1])
                    #log.info("jobid %s  and jobstatus %s" %(jobidmatch.group('jobid'), jobmatch.group('status')))
                    if jobidmatch:
                        self.nodes[jobidmatch.group('jobid')].status = (
                            jobmatch.group('status'), "")
                        
                        jobreport = re.search('StatusDetails\s\S\s\S(?P<info>\S+)\S\S\n', lines[i+2])    
                        if jobreport:
                            self.nodes[jobidmatch.group('jobid')].status = (
                                jobmatch.group('status'),jobreport.group('info'))
                        continue
                dagmatch = dagmatcher.match(line)
                if 'DagStatus =' in line:
                    m = re.search('DagStatus\s\S\s\S+\s\S+\s\S(?P<status>\w+)\s(?P<info>\S+)', line)
                    if m:
                        self.status = (m.group('status'), m.group('info')) 
                     
        return self.status

    def failing_nodes(self):
        """ Generate all jobs which have failed. """
        self.update_status()
        for nodeid, node in self.nodes.iteritems():
            if node.status[0] == "STATUS_ERROR":
                yield (nodeid, node.status[1])

    def job_statistics(self):
        """ Returns a collection.Counter of jobs in various states. """
        counts = collections.defaultdict(int)
        self.update_status()
        for job, node in self.nodes.iteritems():
            counts[node.status[0]] += 1
        return counts
