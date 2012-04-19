import os
import sys
from FinalStateAnalysis.PatTools.datadefs import datadefs

cfg = 'analyze_cfg.py'
jobId = '2012-04-14-v1-MuonTP'

patJobId = '2011-12-13-EWKPatTuple'
patCfg = 'patTuple_cfg'

def get_dir(sample):
    dir_name = '-'.join([patJobId, sample, patCfg])
    base_dir = '--input-dir=root://cmsxrootd.hep.wisc.edu//store/user/efriis/'
    return base_dir + dir_name

dag_directory = "/scratch/efriis/%s/dags" % jobId
if not os.path.exists(dag_directory):
    os.makedirs(dag_directory)

print "export TERMCAP=screen"
for sample, sample_info in sorted(datadefs.iteritems(), key=lambda (x,y): x):
    if 'Mu' not in sample_info['analyses']:
        continue

    path_name = os.path.join(os.environ['scratch'], '-'.join(
        [jobId, sample, 'analyzeFinalStates']))
    sys.stderr.write(path_name + '\n')
    sys.stderr.write('Building sample submit dir %s\n' % (sample))
    if os.path.exists(path_name):
        sys.stderr.write('Skipping existing submit directory for %s\n' % sample)
        continue

    options = []
    if 'data' not in sample:
        options.append('isMC=1')
        options.append('puScenario=%s' % sample_info['pu'])
    else:
        options.append('isMC=0')

    options.append("'inputFiles=$inputFileNames'")
    options.append("'outputFile=$outputFileName'")

    farmout_options = []
    farmout_options.append(get_dir(sample))


    command = [
        'farmoutAnalysisJobs',
        '--fwklite',
        '--infer-cmssw-path',
        #'--express-queue',
        #'--no-submit',
        #'--job-count=2',
        #'--input-files-per-job=%i' % (sample_info['ana_group']*2),
        '--submit-dir=/scratch/efriis/%s/%s/' % (jobId, sample),
        '"--output-dir=srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/efriis/%s/%s/"' % (jobId, sample),
        '--output-dag-file=%s/%s-%s.dag' % (dag_directory, jobId, sample),
        ' --exclude-input-files="*plots.root"',
        '--input-files-per-job=%i' % 10,
    ]

    #if 'WplusJets' in sample:
        #command.append('--job-count=10')

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(os.path.join(
        os.environ['CMSSW_BASE'], 'bin',
        os.environ['SCRAM_ARCH'], 'analyzeFinalStates'))

    command.append(os.path.abspath(cfg))
    command.extend(options)
    print ' '.join(command)
