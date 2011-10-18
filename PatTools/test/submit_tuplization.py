from FinalStateAnalysis.PatTools.datadefs import datadefs
import os
import sys

cfg = 'patTuple_cfg.py'
jobId = '2011-10-06-EWKPatTuple'

for sample, sample_info in datadefs.iteritems():

    #if 'TauPlusX' in sample:
        #continue
    #if 'DoubleElectron' in sample:
        #continue
    #if 'SingleMu' in sample:
        #continue
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
        options.append('globalTag=START42_V13::All')
    else:
        options.append('isMC=0')
        options.append('globalTag=GR_R_42_V19::All')
        options.append('lumiMask=%s' % sample_info['lumi_mask'])
        farmout_options.append('--lumi-mask=%s' % sample_info['lumi_mask'])
        if 'firstRun' in sample_info:
            farmout_options.append(
                '--input-runs=%i-%i' %
                (sample_info['firstRun'], sample_info['lastRun']))
            options.append('firstRun=%s' % sample_info['firstRun'])
            options.append('lastRun=%s' % sample_info['lastRun'])

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        '--input-files-per-job=1',
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
