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
import FinalStateAnalysis.PatTools.site_spec as site_spec

parser = argparse.ArgumentParser(description='Build PAT Tuple CRAB submission')
parser.add_argument('jobid', help='Job ID identifier')
parser.add_argument('--samples', nargs='+', type=str, required=False,
                    help='Filter samples using list of patterns (shell style)')
parser.add_argument('--lumimask', type=str, required=False,
                    help='Optionally override the lumi mask used.')
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

    submit_dir_base = "{root}/{jobid}/{sample}".format(
        root=site_spec.submit_dir_root,
        jobid=jobId,
        sample=sample
    )
    dag_directory = os.path.join(submit_dir_base, 'dags')
    # Create the dag directory
    print "mkdir -p %s" % dag_directory

    submit_dir = os.path.join(submit_dir_base, 'submit')

    sys.stderr.write('Building sample submit dir %s\n' % (sample))
    if os.path.exists(submit_dir):
        sys.stderr.write(
            '=> skipping existing submit directory for %s\n' % sample)
        continue

    if args.lumimask:
        sys.stderr.write("=> overriding lumi mask with %s\n" % args.lumimask)
        if not args.lumimask.startswith(
                "FinalStateAnalysis/RecoTools/data/masks/"):
            sys.stderr.write("ERROR: Lumimasks must be placed in "
                             "FinalStateAnalysis/RecoTools/data/masks/ "
                             " and the path relative to $CMSSW_BASE"
                             " must be given.\n")
            sys.exit(1)
        sample_info['lumi_mask'] = args.lumimask

    options = configure_pat_tuple(sample, sample_info)
    options.append("'inputFiles=$inputFileNames'")
    options.append("'outputFile=$outputFileName'")

    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    if 'lumi_mask' in sample_info:
        # This path goes to farmout, and should be absolute.
        lumi_mask_fip = sample_info['lumi_mask']
        lumi_mask_path = os.path.join(
            os.environ['CMSSW_BASE'], 'src', lumi_mask_fip)
        farmout_options.append('--lumi-mask=%s' % lumi_mask_path)
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

    output_dir = os.path.join(
        site_spec.output_dir_root + sample_info['datasetpath'],
        jobId
    )

    print site_spec.output_dir_root, output_dir

    command = [
        'farmoutAnalysisJobs',
        #'--no-shared-fs', # Copy libs to submit dir so we don't kill AFS
        '--infer-cmssw-path',
        '--vsize-limit=30000',
        '--input-files-per-job=1',
        '"--output-dir=srm://%s%s"' % (site_spec.output_dir_srm, output_dir),
        '--submit-dir=%s' % submit_dir,
        '--output-dag-file=%s/dag.dag' % dag_directory,
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
