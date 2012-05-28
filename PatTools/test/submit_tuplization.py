from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.PatTools.pattuple_option_configurator import \
        configure_pat_tuple
import os
import sys

cfg = 'patTuple_cfg.py'
jobId = '2012-05-15-PatTuple'

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

    options = configure_pat_tuple(sample, sample_info)
    options.append("'inputFiles=$inputFileNames'")
    options.append("'outputFile=$outputFileName'")

    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    if 'data' in sample:
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
