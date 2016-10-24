#!/usr/bin/env python

'''

Create a script file to submit jobs to condor using farmoutAnalysisJobs.
(http://www.hep.wisc.edu/cms/comp/faq.html#how-can-i-use-farmoutanalysisjobs...)

By default, the script is written to stdout, with some logging information 
sent to stderr. If --output_file (-o) is specified, a bash script is
created containing the ouput.


Example to make submit script (stored in test.sh) for WZ analysis on Phys14 miniAOD:
(run from $fsa/NtupleTools/test or use full path to make_ntuples_cfg.py)
    
    submit_job.py 2015-02-26-WZ_ntuples_test make_ntuples_cfg.py \
    channels="eee,mmm,eem,emm" isMC=1 --campaign-tag="Phys14DR-PU20bx25_PHYS14_25_V*" \
    --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV.json \
    --samples "W*" "Z*" "D*" "T*" \
    -o test.sh

Note: It's a good idea to put your sample names with wildcards inside quotes,
    as otherwise the unix wildcard will be expanded before it is passed to the 
    program (so a file named 'Wsubmit.sh' in your folder would cause the 
    argument W* to become Wsubmit.sh, which you don't want)

'''

import argparse
import datetime
import fnmatch
import json
import logging
import os
import sys
from socket import gethostname
from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.Utilities.dbsinterface import get_das_info

log = logging.getLogger("submit_job")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

def getFarmoutCommand(args, dataset_name, full_dataset_name):
    ''' Builds the command to submit an ntuple job for the given dataset 

    Builds text for a bash script to submit ntuplization jobs to condor
    via FarmoutAnalysisJobs. Recieves the command line input (via the varialbe 
    args), the dataset shortname (dataset_name) and full name with path 
    (full_dataset_name) as input. Creates the directory dag_dir+"inputs", 
    where dag_dir is a command line argument.

    returns text for the bash script
    '''
    uname = os.environ['USER']

    if 'uwlogin' in gethostname():
        scratchDir = 'data'
    else:
        scratchDir = 'nfs_scratch'

    submit_dir = args.subdir.format(
        scratch = scratchDir,
        user = uname,
        jobid = args.jobid,
        sample = dataset_name
    )
    if os.path.exists(submit_dir):
        command = '# Submission directory for %s already exists\n' % dataset_name
        log.warning("Submit directory for sample %s exists, skipping",
                    dataset_name)
        return command

    log.info("Building submit files for sample %s", dataset_name)

    dag_dir = args.dagdir.format(
        scratch = scratchDir,
        user = uname,
        jobid = args.jobid,
        sample = dataset_name
    )

    output_dir = args.outdir.format(
        user = uname,
        jobid = args.jobid,
        sample = dataset_name
    )

    input_commands = []

    dasFilesCommand = 'file dataset={0}'.format(full_dataset_name)
    if args.instance: dasFilesCommand += ' instance={0}'.format(args.instance)
    files = get_das_info(dasFilesCommand)
    mkdir_cmd = "mkdir -p %s" % (dag_dir+"inputs")
    os.system(mkdir_cmd)
    input_txt = '%s_inputfiles.txt' % dataset_name
    input_txt_path = os.path.join(dag_dir+"inputs", input_txt)
    with open(input_txt_path, 'w') as txt:
        txt.write('\n'.join(files))
    input_commands.extend([
        '--input-file-list=%s' % input_txt_path,
        '--assume-input-files-exist', 
        '--input-dir=/',
    ])

    command = [
        'farmoutAnalysisJobs',
        '--infer-cmssw-path',
        '"--submit-dir=%s"' % submit_dir,
        '"--output-dag-file=%s"' % dag_dir,
        '"--output-dir=%s"' % output_dir,
        '--input-files-per-job=%i' % args.filesperjob,
        '--job-count=%i' % args.jobcount,
    ]
    paramLoc = 'src/FinalStateAnalysis/NtupleTools/python/parameters'
    if 'uwlogin' in gethostname() and not args.extraUserCodeFiles:
        command.append('--extra-usercode-files="%s"'%paramLoc)
    if args.extraUserCodeFiles:
        if paramLoc in args.extraUserCodeFiles:
            command.append('--extra-usercode-files="%s"'%(' '.join(args.extraUserCodeFiles)))
        else: 
            command.append('--extra-usercode-files="%s %s"'%(' '.join(args.extraUserCodeFiles), paramLoc))
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

    # temp hardcode
    if args.apply_cms_lumimask:
        filename = 'Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' # 20.1/fb
        #lumi_mask_path = os.path.join('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV',filename)
        #lumi_mask_path = os.path.join(os.environ['CMSSW_BASE'],'/src/FinalStateAnalysis/NtupleTools/python/parameters/',filename)
        lumi_mask_path = '/afs/hep.wisc.edu/cms/truggles/public/'+filename
        if args.lumimaskjson: 
            assert not (args.silver or args.goldenv2), "ERROR: Multiple lumimask jsons specified"
            lumi_mask_path = args.lumimaskjson
        command.append('lumiMask=%s' % lumi_mask_path)

    #if args.apply_cms_lumimask and 'lumi_mask' in sample_info:
    #    lumi_mask_path = os.path.join(
    #        os.environ['CMSSW_BASE'], 'src', sample_info['lumi_mask'])
    #    command.append('lumiMask=%s' % lumi_mask_path)
    #    firstRun = sample_info.get('firstRun', -1)
    #    if firstRun > 0:
    #        command.append('firstRun=%i' % firstRun)
    #    lastRun = sample_info.get('lastRun', -1)
    #    if lastRun > 0:
    #        command.append('lastRun=%i' % lastRun)

    farmout_command = '# Submit file for sample %s\n' % dataset_name
    farmout_command += 'mkdir -p %s\n' % os.path.dirname(dag_dir)
    farmout_command += ' '.join(command) + '\n'
    return farmout_command

def datasets_from_das(args):
    ''' Build submit script using datasets from DAS

    Builds text for a bash script to submit ntuplization jobs to condor
    via FarmoutAnalysisJobs. Recieves the command line input (via the varialbe 
    args) as input. The MINIAOD file to be ntuplized is found by searching for 
    files in DAS matching args.samples in the campaign args.campaignstring. If 
    args.dastuple is specified (a json file), this is used as a simpler lookup 
    method rather than searching through all of DAS. 

    If a submit folder already exists with the same name, it will not be
    recreated. A warning is written to the submit script.

    returns a string containing the text of the bash submit script.

    '''
    script_content = ""
    # this part searches for MC
    if args.campaignstring:
        dbs_datasets = get_das_info('/*/%s/MINIAODSIM' % args.campaignstring)
        # check sample wildcards
        for dataset in dbs_datasets:
            dataset_name = dataset.split('/')[1] 
            passes_filter = True
            passes_wildcard = False
            
            for pattern in args.samples:
                if args.dastuple: # check json for shorthand
                    with open(args.dastuple) as tuple_file:
                        tuple_info = json.load(tuple_file)
                        matching_datasets = []
                        for shorthand, fullname in tuple_info.iteritems():
                            if fullname in dataset:
                                if fnmatch.fnmatchcase(shorthand, pattern):
                                    passes_wildcard = True
                else: # check das directly
                    if fnmatch.fnmatchcase(dataset_name, pattern):
                        passes_wildcard = True
            passes_filter = passes_wildcard and passes_filter
            if passes_filter:
                script_content += getFarmoutCommand(args, dataset_name, dataset)
    # special handling for data
    elif args.isData:
        data_patterns = [x for x in args.samples if 'data_' in x]
        data_datasets = get_das_info('/*/*/MINIAOD')
        for dataset in data_datasets:
            passes_filter = True
            passes_wildcard = False
            name_to_use = 'data_' + '_'.join(dataset.split('/'))
            for pattern in data_patterns:
                if args.dastuple: # check json for shorthand, links to full dataset name
                    with open(args.dastuple) as tuple_file:
                        tuple_info = json.load(tuple_file)
                        matching_datasets = []
                        for shorthand, fullname in tuple_info.iteritems():
                            if fullname in dataset:
                                if fnmatch.fnmatchcase(shorthand, pattern):
                                    passes_wildcard = True
                                    name_to_use = shorthand
                else: # check das directly
                    if fnmatch.fnmatchcase(dataset, pattern):
                        passes_wildcard = True
            passes_filter = passes_wildcard and passes_filter
            if passes_filter:
                script_content += getFarmoutCommand(args, name_to_use, dataset)
    elif args.useDasName: # passed a full dataset name
        for dataset in args.samples:
            dataset_name = dataset.split('/')[1]
            script_content += getFarmoutCommand(args, dataset_name, dataset)
    else:
        print 'Unknown argument'
    if "Submit file" not in script_content:
        log.warning("No datasets found matching %s", args.samples)
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
        'lumiMask=XXX.json and firstRun etc to cmsRun. If no other JSON is '
        'specified, the most recent golden JSON is used.'
    )
    cmsrun_group.add_argument(
        '--lumimask-json', dest='lumimaskjson',
        default='',
        help = 'Custom lumimask json.',
    )
    cmsrun_group.add_argument(
        '--goldenv2', dest='goldenv2',
        action='store_true', help='Use older version of golden JSON.'
    )
    cmsrun_group.add_argument(
        '--silver', dest='silver',
        action='store_true', help='Use silver JSON.'
    )    
    cmsrun_group.add_argument(
        '--bunch-spacing', dest='bunchSpacing', type=int,
        default=25, choices=[25,50],
        help = 'Bunch spacing in ns.',
    )

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        '--input-dir', dest='inputdir',
        help = 'Input dir argument passed to farmout.'
    )
    input_group.add_argument(
        '--campaign-tag', dest='campaignstring',
        help = 'DAS production campaign string for query.'
               ' For a given DAS query, it is the second part'
               ' (dataset=/*/[campaign-tag]/MINIAODSIM).'
    )
    input_group.add_argument(
        '--data', dest='isData', action='store_true',
        help = 'Run over data',
    )
    input_group.add_argument(
        '--das-name', dest='useDasName', action='store_true',
        help = 'Run over DAS sample names',
    )

    filter_group = parser.add_argument_group('Sample Filters')
    filter_group.add_argument('--samples', nargs='+', type=str, required=False,
                        help='Filter samples using list of patterns (shell style)')
    filter_group.add_argument(
        '--instance', dest='instance',
        default='',
        help = 'DAS instance',
    )
    filter_group.add_argument(
        '--das-replace-tuple', dest='dastuple',
         help = 'JSON file listing shorthand names for DAS samples.'
    )

    farmout_group = parser.add_argument_group("farmout",
                                              description="Farmout options")

    farmout_group.add_argument(
        '--job-count', type=int, dest='jobcount',
        default=1000000,
        help = 'number of jobs',
    )
    farmout_group.add_argument(
        '--extra-usercode-files', nargs='*', type=str, dest='extraUserCodeFiles',
        help = 'Space-separated list of extra directories that need to be included '
               'in the user_code tarball sent with the job. Paths relative to $CMSSW_BASE.'
    )

    farmout_group.add_argument(
        '--output-dag-file', dest='dagdir',
        default='/{scratch}/{user}/{jobid}/{sample}/dags/dag',
        help = 'Where to put dag files',
    )

    farmout_group.add_argument(
        '--shared-fs', dest='sharedfs', action='store_true',
        help = 'Use only nodes with access to AFS',
    )

    farmout_group.add_argument(
        '--submit-dir', dest='subdir',
        default='/{scratch}/{user}/{jobid}/{sample}/submit',
        help = 'Where to put submit files. Default: %s(default)s',
    )

    farmout_group.add_argument(
        '--output-dir', dest='outdir',
        default='srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/{user}/{jobid}/{sample}/',
        help = 'Where to put the output.  Default: %(default)s'
    )

    farmout_group.add_argument('--input-files-per-job', type=int, dest='filesperjob',
                        default=1, help='Files per job')

    parser.add_argument('--output_file', '-o', type=str, default="",
                        required=False, help="Create bash script OUTPUT_FILE file with ouput "
                        "rather than printing information to stdout")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    script_content = '# Condor submission script\n'
    script_content += '# Generated with submit_job.py at %s\n' % datetime.datetime.now()
    script_content += '# The command was: %s\n\n' % ' '.join(sys.argv)
    args = get_com_line_args()
    # first, make DAS query for dataset if not using local dataset or hdfs/dbs tuple list
    if args.campaignstring or args.isData or args.useDasName:
        script_content += datasets_from_das(args)
    else:
        # this is the old version that uses datadefs
        script_content += datasets_from_datadefs(args)
    if args.output_file == "":
        sys.stdout.write(script_content)
    else:
        with open(args.output_file, "w") as file:
            file.write("#!/bin/bash\n")
            file.write(script_content)
        sys.stdout.write("\nWrote submit script %s\n\n" % args.output_file)

