#!/usr/bin/env python

'''
File: submit_tuplization.py

Author: Evan Friis, UW Madison

Description: submit UW pattuple jobs via condor.

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.Utilities.version import fsa_version
from FinalStateAnalysis.PatTools.pattuple_option_configurator import \
        configure_pat_tuple
import os
import sys

parser = argparse.ArgumentParser(description='Build PAT Tuple CRAB submission')
parser.add_argument('jobid', help='Job ID identifier')
parser.add_argument('--samples', nargs='+', type=str, required=False,
                    help='Filter samples using list of patterns (shell style)')
args = parser.parse_args()

cfg = 'patTuple_cfg.py'
jobId = args.jobid

print " # Job ID: %s Version: %s" % (jobId, fsa_version())
print 'export TERMCAP=screen'
for sample in sorted(datadefs.keys()):
    sample_info = datadefs[sample]

    passes_filter = True

    # Filter by sample wildcards
    if args.samples:
        passes_wildcard = False
        for pattern in args.samples:
            if fnmatch.fnmatchcase(sample, pattern):
                passes_wildcard = True
        passes_filter = passes_wildcard and passes_filter
    if not passes_filter:
        continue

    submit_dir_base = "/scratch/{logname}/{jobid}/{sample}".format(
        logname = os.environ['LOGNAME'],
        jobid = jobId,
        sample = sample
    )
    dag_directory = os.path.join(submit_dir_base, 'dags')
    # Create the dag directory
    print "mkdir -p %s" % dag_directory

    submit_dir = os.path.join(submit_dir_base, 'submit')

    sys.stderr.write('Building sample submit dir %s\n' % (sample))
    if os.path.exists(submit_dir):
        sys.stderr.write('=> skipping existing submit directory for %s\n' % sample)
        continue

    options = configure_pat_tuple(sample, sample_info)
    options.append("'inputFiles=$inputFileNames'")
    options.append("'outputFile=$outputFileName'")

    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    if 'lumi_mask' in sample_info:
        farmout_options.append('--lumi-mask=%s' % lumi_mask_fip)
        if 'firstRun' in sample_info:
            farmout_options.append(
                '--input-runs=%i-%i' %
                (sample_info['firstRun'], sample_info['lastRun']))
    # Check if we need to use a different DBS
    if 'dbs' in sample_info:
        farmout_options.append(
            '--dbs-service-url=http://cmsdbsprod.cern.ch/%s/servlet/DBSServlet'
            % sample_info['dbs']
        )

    command = [
        'farmoutAnalysisJobs',
        #'--no-shared-fs', # Copy libs to submit dir so we don't kill AFS
        '--infer-cmssw-path',
        '--vsize-limit=30000',
        '--input-files-per-job=1',
        '"--output-dir=srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/%s/%s/%s/"' % (os.environ['LOGNAME'], jobId, sample),
        '--submit-dir=%s' % submit_dir,
        '--output-dag-file=%s/dag.dag' % dag_directory,
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
