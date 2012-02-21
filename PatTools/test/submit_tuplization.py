from FinalStateAnalysis.PatTools.datadefs import datadefs
import os
import sys

cfg = 'patTuple_cfg.py'
jobId = '2011-12-13-EWKPatTuple'

dag_directory = "/scratch/efriis/dags/%s" % jobId
if not os.path.exists(dag_directory):
    os.mkdir(dag_directory)

print 'export TERMCAP=screen'
for sample in sorted(datadefs.keys()):
    sample_info = datadefs[sample]
    if 'VH' not in sample_info['analyses'] and 'Tau' not in sample_info['analyses']:
        continue

    path_name = os.path.join(os.environ['scratch'], '-'.join(
        [jobId, sample, cfg.replace('.py', '')]))
    sys.stderr.write('Building sample submit dir %s\n' % (sample))
    if os.path.exists(path_name):
        sys.stderr.write('Skipping existing submit directory for %s\n' % sample)
        continue

    options = []
    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    if 'data' not in sample:
        options.append('isMC=1')
        options.append('globalTag=START42_V15B::All')
        options.append('xSec=%0.4f' % sample_info['x_sec'])
    else:
        options.append('isMC=0')
        options.append('globalTag=GR_R_42_V21::All')
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
        '--infer-cmssw-path',
        '--output-dag-file=%s/%s-%s.dag' % (dag_directory, jobId, sample),
        '--input-files-per-job=1',
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
