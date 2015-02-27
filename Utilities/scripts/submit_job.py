#!/usr/bin/env python

'''

Create a script file to submit jobs to condor using farmoutAnalysisJobs. 
By default, the script is written to stdout, with some logging information 
sent to stderr. If --output_file (-o) is specified, a bash script is
created containing the ouput.


Example to make submit script for VH analysis:

    submit_job.py VH 2012-03-14-Trileptons trilepton_ntuples_cfg.py \
            "--input-dir={myhdfs}/2012-03-05-EWKPatTuple/{sample}"

'''

import argparse
import datetime
import fnmatch
import json
import logging
import os
import sys
from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.Utilities.dbsinterface import get_das_info

log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

def datasets_from_dbs():
    dbs_datasets = get_das_info('/*/%s/MINIAOD*' % args.campaignstring)
        # check sample wildcards
    for dataset in dbs_datasets:
        dataset_name = dataset.split('/')[1] 
        passes_filter = True
        if args.samples:
            passes_wildcard = False
            for pattern in args.samples:
                if args.dastuple: # check json for shorthand
                    with open(args.dastuple) as tuple_file:
                        tuple_info = json.load(tuple_file)
                        matching_datasets = []
                        for shorthand, fullname in tuple_info.iteritems():
                            if fullname in dataset_name:
                                if fnmatch.fnmatchcase(shorthand, pattern):
                                    passes_wildcard = True
                else: # check das directly
                    if fnmatch.fnmatchcase(dataset_name, pattern):
                        passes_wildcard = True
            passes_filter = passes_wildcard and passes_filter
        if not passes_filter:
            continue
        
        submit_dir = args.subdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = dataset_name
        )
        if os.path.exists(submit_dir):
            sys.stdout.write('# Submission directory for %s already exists\n'
                            % dataset_name)
            log.warning("Submit directory for sample %s exists, skipping",
                        dataset_name)
            continue

        log.info("Building submit files for sample %s", dataset_name)

        dag_dir = args.dagdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = dataset_name
        )

        output_dir = args.outdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = dataset_name
        )

        input_commands = []

        files = get_das_info('file dataset=%s' % dataset)
        mkdir_cmd = "mkdir -p %s" % (dag_dir+"inputs")
        os.system(mkdir_cmd)
        input_txt = '%s_inputfiles.txt' % dataset_name
        input_txt_path = os.path.join(dag_dir+"inputs", input_txt)
        with open(input_txt_path, 'w') as txt:
            txt.write('\n'.join(files))
        input_commands.extend([
            '--input-file-list=%s' % input_txt_path,
            '--assume-input-files-exist', 
            '--input-dir=root://xrootd.unl.edu/',
        ])

        command = [
            'farmoutAnalysisJobs',
            '--infer-cmssw-path',
            '"--submit-dir=%s"' % submit_dir,
            '"--output-dag-file=%s"' % dag_dir,
            '"--output-dir=%s"' % output_dir,
            '--input-files-per-job=%i' % args.filesperjob,
        ]
        if args.sharedfs:
            command.append('--shared-fs')
        command.extend(input_commands)
        command.extend([
            # The job ID
            '%s-%s' % (args.jobid, dataset_name),
            args.cfg
        ])

        command.extend(args.cmsargs)
        command.append("'inputFiles=$inputFileNames'")
        command.append("'outputFile=$outputFileName'")

        if args.apply_cms_lumimask and 'lumi_mask' in sample_info:
            lumi_mask_path = os.path.join(
                os.environ['CMSSW_BASE'], 'src', sample_info['lumi_mask'])
            command.append('lumiMask=%s' % lumi_mask_path)
            firstRun = sample_info.get('firstRun', -1)
            if firstRun > 0:
                command.append('firstRun=%i' % firstRun)
            lastRun = sample_info.get('lastRun', -1)
            if lastRun > 0:
                command.append('lastRun=%i' % lastRun)

        script_content = '# Submit file for sample %s\n' % dataset_name
        script_content += 'mkdir -p %s\n' % os.path.dirname(dag_dir)
        script_content += ' '.join(command) + '\n'
        return script_content
def datasets_from_datadefs():
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

        dag_dir = args.dagdir.format(
            user = os.environ['LOGNAME'],
            jobid = args.jobid,
            sample = sample
        )

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
            if args.cleancrab:
                input_commands.append('--clean-crab-dupes')
        elif args.tuplelist:
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
                datasetpath = tuple_info[matching_datasets[0]]

                if args.xrootd:
                    files = get_das_info('file dataset=%s' % datasetpath)
                    mkdir_cmd = "mkdir -p %s" % (dag_dir+"inputs")
                    os.system(mkdir_cmd)
                    input_txt = '%s_inputfiles.txt' % matching_datasets[0]
                    input_txt_path = os.path.join(dag_dir+"inputs", input_txt)
                    with open(input_txt_path, 'w') as txt:
                        txt.write('\n'.join(files))
                    input_commands.extend([
                        '--input-file-list=%s' % input_txt_path,
                        '--assume-input-files-exist', 
                        '--input-dir=root://xrootd.unl.edu/',
                    ])
                else:
                    input_commands.append(
                        '--input-dbs-path=%s' % datasetpath)
                    input_commands.append(
                        '--dbs-service-url=http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet')
        elif args.tupledirlist:
            with open(args.tupledirlist) as tuple_file:
                # Parse info about PAT tuples
                tuple_info = json.load(tuple_file)
                if sample not in tuple_info:
                    log.warning("No data directory for %s specified, skipping",
                                sample)
                    continue
                input_dir = tuple_info[sample]
                if '!' in input_dir:
                    # ! means it a DBS path
                    input_commands.append(
                        '--dbs-service-url=http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet'
                    )
                    input_commands.append(
                        '--input-dbs-path=%s' % input_dir.replace('!', ''))
                else:
                    input_commands.append('"--input-dir=%s"' % input_dir)
                    if args.cleancrab:
                        input_commands.append('--clean-crab-dupes')

        command = [
            'farmoutAnalysisJobs',
            '--infer-cmssw-path',
            '"--submit-dir=%s"' % submit_dir,
            '"--output-dag-file=%s"' % dag_dir,
            '"--output-dir=%s"' % output_dir,
            '--input-files-per-job=%i' % args.filesperjob,
        ]
        if args.sharedfs:
            command.append('--shared-fs')
        command.extend(input_commands)
        command.extend([
            # The job ID
            '%s-%s' % (args.jobid, sample),
            args.cfg
        ])

        command.extend(args.cmsargs)
        command.append("'inputFiles=$inputFileNames'")
        command.append("'outputFile=$outputFileName'")

        if args.apply_cms_lumimask and 'lumi_mask' in sample_info:
            lumi_mask_path = os.path.join(
                os.environ['CMSSW_BASE'], 'src', sample_info['lumi_mask'])
            command.append('lumiMask=%s' % lumi_mask_path)
            firstRun = sample_info.get('firstRun', -1)
            if firstRun > 0:
                command.append('firstRun=%i' % firstRun)
            lastRun = sample_info.get('lastRun', -1)
            if lastRun > 0:
                command.append('lastRun=%i' % lastRun)

        script_content = '# Submit file for sample %s\n' % sample
        script_content += 'mkdir -p %s\n' % os.path.dirname(dag_dir)
        script_content += ' '.join(command) + '\n'
    return script_content
def get_com_line_args():
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

    cmsrun_group.add_argument(
        '--apply-cmsRun-lumimask', dest='apply_cms_lumimask',
        action='store_true', help = 'If specified, pass the appropriate '
        'lumiMask=XXX.json and firstRun etc to cmsRun'
    )

    cmsrun_group.add_argument(
        '--xrootd', action='store_true', required=False, default=False,
        help='fetch files from remote tiers using xrootd'
    )

    cmsrun_group.add_argument(
        '--das-replace-tuple', dest='dastuple',
         help = 'JSON file listing shorthand names for DAS samples.'
    )

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        '--input-dir', dest='inputdir',
        help = 'Input dir argument passed to farmout.'
    )

    input_group.add_argument(
        '--tuple-dbs', dest='tuplelist',
        help = 'JSON file mapping datasets to DBS paths.'
        ' Generally kept in MetaData/tuples'
    )

    input_group.add_argument(
        '--tuple-dirs', dest='tupledirlist',
        help = 'JSON file mapping datasets to HDFS directories'
        ' Generally kept in MetaData/tuples'
    )

    input_group.add_argument(
        '--campaign-tag', dest='campaignstring',
        help = 'DAS production campaign string for query.'
               ' For a given DAS query, it is the second part'
               ' (dataset=/*/[campaign-tag]/MINIAODSIM).'
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
        default='/nfs_scratch/{user}/{jobid}/{sample}/dags/dag',
        help = 'Where to put dag files',
    )

    farmout_group.add_argument(
        '--shared-fs', dest='sharedfs', action='store_true',
        help = 'Use only nodes with access to AFS',
    )

    farmout_group.add_argument(
        '--submit-dir', dest='subdir',
        default='/nfs_scratch/{user}/{jobid}/{sample}/submit',
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

    parser.add_argument('--output_file', '-o', type=str, default="",
                        required=False, help="Create bash script OUTPUT_FILE file with ouput "
                        "rather than printing information to stdout")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    script_content = '# Condor submission script\n'
    script_content += '# Generated with submit_job.py at %s\n' % datetime.datetime.now()
    script_content += '# The command was: %s\n' % ' '.join(sys.argv)
    script_content += 'export TERMCAP=screen\n'
    args = get_com_line_args()
    # first, make DAS query for dataset if not using local dataset or hdfs/dbs tuple list
    if args.campaignstring:
        script_content += datasets_from_dbs()
    else:
        # this is the old version that uses datadefs
        script_content += datasets_from_datadefs()
    if args.output_file == "":
        sys.stdout.write(script_content)
    else:
        with open(args.output_file, "w") as file:
            file.write("#!/bin/bash")
            file.write(script_content)
        sys.stdout.write("\nWrote submit script %s\n" % args.output_file)

