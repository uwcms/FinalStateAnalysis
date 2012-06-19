#!/usr/bin/env python

'''

Create a script file to submit jobs to condor.  The script is written to stdout,
some logging information is sent to stderr.

Example to make submit script for VH analysis:

    submit_job.py VH 2012-03-14-Trileptons trilepton_ntuples_cfg.py \
            "--input-dir={myhdfs}/2012-03-05-EWKPatTuple/{sample}"

'''

from RecoLuminosity.LumiDB import argparse
import datetime
import fnmatch
import json
import logging
import os
import sys
from FinalStateAnalysis.MetaData.datadefs import datadefs

log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    cmsrun_group = parser.add_argument_group('Analysis and cmsRun options')

    cmsrun_group.add_argument('jobid', type=str,
                        help='String description of job')

    cmsrun_group.add_argument('cfg', type=str, help='Config file to run')

    cmsrun_group.add_argument(
        'cmsargs', metavar='arg', nargs='*',
        help = 'VarParsing arguments passed to cmsRun.'
        ' Note that inputFiles and outputFiles are always passed.'
    )

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        '--input-dir', dest='inputdir',
        help = 'Input dir argument passed to farmout.'
    )

    input_group.add_argument(
        '--tuple-file', dest='tuplelist',
        help = 'JSON file mapping datasets to DBS paths.'
        ' Generally kept in MetaData/tuples'
    )

    filter_group = parser.add_argument_group('Sample Filters')
    filter_group.add_argument('--analysis', type=str, default='',
                              help='Which analysis to use - this determines'
                              ' which samples in datadefs to run over.')

    filter_group.add_argument('--samples', nargs='+', type=str, required=False,
                        help='Filter samples using list of patterns (shell style)')

    farmout_group = parser.add_argument_group("farmout",
                                              description="Farmout options")

    farmout_group.add_argument(
        '--output-dag-file', dest='dagdir',
        default='/scratch/{user}/{jobid}/{sample}/dags/dag',
        help = 'Where to put dag files',
    )

    farmout_group.add_argument(
        '--submit-dir', dest='subdir',
        default='/scratch/{user}/{jobid}/{sample}/submit',
        help = 'Where to put submit files. Default: %s(default)s',
    )

    farmout_group.add_argument(
        '--output-dir', dest='outdir',
        default='srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/{user}/{jobid}/{sample}/',
        help = 'Where to put the output.  Default: %(default)s'
    )

    farmout_group.add_argument('--input-files-per-job', type=int, dest='filesperjob',
                        default=1, help='Files per job')

    farmout_group.add_argument('--clean-crab-dupes', action='store_true',
                               default=False, dest='cleancrab',
                               help='Clean crab dupes')

    args = parser.parse_args()

    sys.stdout.write('# Condor submission script\n')
    sys.stdout.write('# Generated with submit_job.py at %s\n'
                     % datetime.datetime.now())
    sys.stdout.write('# The command was: %s\n' % ' '.join(sys.argv))

    sys.stdout.write('export TERMCAP=screen\n')
    for sample, sample_info in reversed(
        sorted(datadefs.iteritems(), key=lambda (x,y): x)):

        passes_filter = True
        # Filter by analysis
        if args.analysis:
            passes_ana = sample_info['analysis'] == args.analysis
            passes_filter = passes_filter and passes_ana
        # Filter by sample wildcards
        if args.samples:
            passes_wildcard = False
            for pattern in args.samples:
                if fnmatch.fnmatchcase(sample, pattern):
                    passes_wildcard = True
            passes_filter = passes_wildcard and passes_filter
        if not passes_filter:
            continue

        submit_dir = args.subdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = sample
        )
        if os.path.exists(submit_dir):
            sys.stdout.write('# Submission directory for %s already exists\n'
                            % sample)
            log.warning("Submit directory for sample %s exists, skipping",
                       sample)
            continue

        log.info("Building submit files for sample %s", sample)
        sys.stdout.write('# Submit file for sample %s\n' % sample)

        dag_dir = args.dagdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = sample
        )
        sys.stdout.write('mkdir -p %s\n' % os.path.dirname(dag_dir))

        output_dir = args.outdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = sample
        )

        input_commands = []

        if args.inputdir:
            input_dir = args.inputdir.format(
                user = os.environ['LOGNAME'],
                jobid = args.jobid,
                sample = sample,
                dataset = sample_info['datasetpath'],
                myhdfs = 'root://cmsxrootd.hep.wisc.edu//store/user/%s/' % os.environ['LOGNAME']
            )
            input_commands.append('"--input-dir=%s"' % input_dir)
        else:
            with open(args.tuplelist) as tuple_file:
                # Parse info about PAT tuples
                tuple_info = json.load(tuple_file)
                # Find the matching pat tuple DBS name
                #import pdb; pdb.set_trace();
                matching_datasets = []
                for pat_tuple, pat_tuple_info in tuple_info.iteritems():
                    if sample in pat_tuple:
                        matching_datasets.append(pat_tuple)
                if len(matching_datasets) != 1:
                    log.error("No or multiple matching datasets found "
                              " for sample %s, matches: [%s]",
                              sample, ", ".join(matching_datasets))
                    continue
                datasetpath = matching_datasets[0]

                input_commands.append(
                    '--input-dbs-path=%s' % datasetpath)
                input_commands.append(
                    '--dbs-service-url=http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet'
                )

        command = [
            'farmoutAnalysisJobs',
            '--infer-cmssw-path',
            '"--submit-dir=%s"' % submit_dir,
            '"--output-dag-file=%s"' % dag_dir,
            '"--output-dir=%s"' % output_dir,
            '--input-files-per-job=%i' % args.filesperjob,
        ]
        if args.cleancrab:
            command.append('--clean-crab-dupes')
        command.extend(input_commands)
        command.extend([
            # The job ID
            '%s-%s' % (args.jobid, sample),
            args.cfg
        ])

        command.extend(args.cmsargs)
        command.append("'inputFiles=$inputFileNames'")
        command.append("'outputFile=$outputFileName'")

        sys.stdout.write(' '.join(command) + '\n')
