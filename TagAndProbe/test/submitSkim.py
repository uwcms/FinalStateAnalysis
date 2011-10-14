#!/bin/env python
from FinalStateAnalysis.TagAndProbe.datadefs import datadefs

samplesToAnalyze = [
    'data_SingleMu_Run2011A_May10ReReco_v1',
    'data_SingleMu_Run2011A_PromptReco_v4',
    'Ztautau_pythia',
    #'Ztautau_embedded_part1',
    #'Ztautau_embedded_part2'
    'Zmumu_pythia',
    'Zmumu_M20_pythia',
    #'Zmumu_powheg',
    'PPmuXptGt20Mu15',
    'WplusJets_madgraph',
    'TTplusJets_madgraph'
]

jobId = '2011-09-14-TauIdEffSkim'
cfg = 'tauID_skim_cfg.py'

# Process 3 GB per job
target_size = 3000.0

for sample, sample_info in datadefs.iteritems():

    options = []
    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    n_jobs_target = int(target_size/sample_info['size'] + 0.5)
    assert(n_jobs_target > 0)

    if 'data' not in sample:
        options.append('isMC=1')
    else:
        options.append('isMC=0')
        options.append('lumiMask=%s' % sample_info['lumi_mask'])
        farmout_options.append('--lumi-mask=%s' % sample_info['lumi_mask'])
        if 'firstRun' in sample_info:
            farmout_options.append(
                '--input-runs=%i-%i' %
                (sample_info['firstRun'], sample_info['lastRun']))

    if 'hlt' in sample_info:
        options.append('hltProcess=%s' % sample_info['hlt'].getProcessName())

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        #'--job-count=20',
        '--input-files-per-job=%i' % n_jobs_target
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
