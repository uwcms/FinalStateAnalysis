from FinalStateAnalysis.MetaData.datadefs import datadefs
import os
import sys

cfg = 'patTuple_cfg.py'
jobId = '2012-05-10-PatTuple'

print 'export TERMCAP=screen'
for sample in sorted(datadefs.keys()):
    sample_info = datadefs[sample]

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

    options = []
    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    # Figure out dataset - the EGamma electron calibrator needs to know
    # if we are using a ReReco, etc.
    dataset=None
    for tag in ['Fall11', 'Summer11', 'Prompt', 'ReReco', 'Jan16ReReco']:
        if tag in sample_info['datasetpath']:
            dataset = tag
    if dataset is None and '05Aug2011' in sample_info['datasetpath']:
        dataset = 'ReReco'
    if dataset is None and 'crab_reco' in sample_info['datasetpath']:
        dataset = 'Fall11'
    if not dataset:
        raise ValueError("Couldn't determine dataset for sample: "
                        + sample_info['datasetpath'])
    options.append('dataset=%s' % dataset)

    # Figure out which target - the EGamma/Muon effective areas need to know
    # this
    target=None
    if 'Fall11' in sample_info['datasetpath']:
        target = 'Fall11MC'
    elif 'crab_reco' in sample_info['datasetpath']: # special case, private prod
        target = 'Fall11MC'
    elif 'Summer11' in sample_info['datasetpath']:
        target = 'Summer11MC'
    elif 'data' in sample and '2011' in sample_info['datasetpath']:
        target = '2011Data'
    elif 'data' in sample and '2012' in sample_info['datasetpath']:
        target = '2012Data'
    if not target:
        raise ValueError("Couldn't determine target for sample: "
                         + sample_info['datasetpath'])
    options.append('target=%s' % target)

    # Check if we need to use a different DBS
    if 'dbs' in sample_info:
        farmout_options.append(
            '--dbs-service-url=http://cmsdbsprod.cern.ch/%s/servlet/DBSServlet' % sample_info['dbs']
        )

    if 'data' not in sample:
        options.append('isMC=1')
        options.append('globalTag=$mcgt')
        options.append('xSec=%0.4f' % sample_info['x_sec'])
        options.append('puTag=%s' % sample_info['pu'])
    else:
        options.append('isMC=0')
        options.append('globalTag=$datagt')
        options.append('puTag=data')
        lumi_mask_fip = sample_info['lumi_mask']
        lumi_mask_path = os.path.join(
            os.environ['CMSSW_BASE'], 'src', lumi_mask_fip)
        options.append('lumiMask=%s' % lumi_mask_path)
        farmout_options.append('--lumi-mask=%s' % lumi_mask_path)
        if 'firstRun' in sample_info:
            farmout_options.append(
                '--input-runs=%i-%i' %
                (sample_info['firstRun'], sample_info['lastRun']))
            options.append('firstRun=%s' % sample_info['firstRun'])
            options.append('lastRun=%s' % sample_info['lastRun'])

    options.append("'inputFiles=$inputFileNames'")
    options.append("'outputFile=$outputFileName'")

    command = [
        'farmoutAnalysisJobs',
        #'--no-shared-fs', # Copy libs to submit dir so we don't kill AFS
        '--infer-cmssw-path',
        '--vsize-limit=30000',
        '--input-files-per-job=1',
        '"--output-dir=srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/efriis/%s/%s/"' % (jobId, sample),
        '--submit-dir=%s' % submit_dir,
        '--output-dag-file=%s/dag.dag' % dag_directory,
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
