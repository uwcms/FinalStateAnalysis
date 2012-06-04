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

    cmsrun_group.add_argument('analysis', type=str,
                        help='Which analysis to use - this determines'
                        ' which samples in datadefs to run over.')

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

    args = parser.parse_args()

    log.info("Getting samples for analysis %s", args.analysis)
    sys.stdout.write('# Condor submission script\n')
    sys.stdout.write('# Generated with submit_job.py at %s\n'
                     % datetime.datetime.now())
    sys.stdout.write('# The command was: %s\n' % ' '.join(sys.argv))

    sys.stdout.write('export TERMCAP=screen\n')
    for sample, sample_info in reversed(
        sorted(datadefs.iteritems(), key=lambda (x,y): x)):
        if args.analysis not in sample_info['analyses']:
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
                # Remap from tuple DBS -> parent DBS to parent DBS -> tuple
                reversed = {}
                for k, v in tuple_info.iteritems():
                    reversed[v['parent']] = k
                if sample_info['datasetpath'] not in reversed:
                    log.warning("Dataset %s not found in %s, skipping!",
                                sample_info['datasetpath'], args.tuplelist)
                    continue
                input_commands.append('--input-dbs-path=%s' %
                                     reversed[sample_info['datasetpath']])
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
