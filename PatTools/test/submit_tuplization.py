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
from FinalStateAnalysis.Utilities.dbsinterface import get_das_info
from FinalStateAnalysis.PatTools.pattuple_option_configurator import \
    configure_pat_tuple
import os
import sys
import FinalStateAnalysis.PatTools.site_spec as site_spec
import time
from pdb import set_trace
from hashlib import md5

parser = argparse.ArgumentParser(description='Build PAT Tuple CRAB submission')
parser.add_argument('jobid', help='Job ID identifier')
parser.add_argument('--samples', nargs='+', type=str, required=False,
                    help='Filter samples using list of patterns (shell style)')
parser.add_argument('--dbsnames', nargs='+', type=str, required=False,
                    help='use full DBS names')
parser.add_argument('--lumimask', type=str, required=False,
                    help='Optionally override the lumi mask used.')
parser.add_argument('--xrootd', action='store_true', required=False, default=False,
                    help='fetch files from remote tiers using xrootd')
parser.add_argument('--ignoreRunRange', action='store_true', required=False, default=False,
                    help='ignores the run range passed from datadefs')
args = parser.parse_args()

cfg = 'patTuple_cfg.py'
jobId = args.jobid

print " # Job ID: %s Version: %s" % (jobId, fsa_version())
print 'export TERMCAP=screen'

def any_matches(regexes, string):
    for regex in regexes:
        if fnmatch.fnmatchcase(string, regex):
            return True
    return False

to_be_used = []
for key, info in datadefs.iteritems():
    if args.samples:
        if any_matches(args.samples, key):
            to_be_used.append(key)
    if 'datasetpath' in info and args.dbsnames:
        dbs = info['datasetpath']
        if any_matches(args.dbsnames, dbs):
            to_be_used.append(key)            

production_info = {}

for sample in sorted(to_be_used):

    sample_info = datadefs[sample]
    if args.ignoreRunRange and 'firstRun' in sample_info:
        del sample_info['firstRun']
        del sample_info['lastRun']

    submit_dir_base = "{root}/{jobid}/{sample}".format(
        root=site_spec.submit_dir_root,
        jobid=jobId,
        sample=sample
    )
    dag_directory = os.path.join(submit_dir_base, 'dags')
    # Create the dag directory
    mkdir_cmd = "mkdir -p %s" % dag_directory
    print mkdir_cmd

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
    if args.xrootd:
        #query DBS to get the filenames
        files = get_das_info('file dataset=%s' % sample_info['datasetpath'])
        os.system(mkdir_cmd) #make the directory now, we need to
        input_txt = '%s_inputfiles.txt' % sample
        input_txt_path = os.path.join(dag_directory, input_txt)
        with open(input_txt_path, 'w') as txt:
            txt.write('\n'.join(files))
        farmout_options.extend([
            '--input-file-list=%s' % input_txt_path,
            '--assume-input-files-exist', 
            '--input-dir=root://xrootd.unl.edu/',
        ])
    else:
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

    info = {
        'creator' : '%s' % site_spec._log_name,
        'jobid' : jobId,
        'production date' : time.strftime("%c"),
        'FSA Version' : fsa_version(),
        'DBS Name' : sample_info['datasetpath'],
        'PAT Location' : output_dir,
    }
    hasher = md5()
    hasher.update(info.__repr__())

    production_info[hasher.hexdigest()] = info


import FinalStateAnalysis.Utilities.prettyjson as prettyjson

hasher = md5()
hasher.update(production_info.__repr__())

with open(hasher.hexdigest() + '.json', 'w') as json:
    json.write( 
        prettyjson.dumps( 
            production_info
            )
        )
