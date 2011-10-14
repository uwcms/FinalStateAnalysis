#!/bin/env python
from TauAnalysis.TauIdEfficiency.recoSampleDefinitionsTauIdEfficiency_7TeV_grid_cfi import recoSampleDefinitionsTauIdEfficiency_7TeV

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

jobId = '2011-07-20-TauIdEffSkim'
cfg = 'skimTauIdEffSample2_cfg.py'

script_string = ''

for sample in samplesToAnalyze:
    sample_info = recoSampleDefinitionsTauIdEfficiency_7TeV['RECO_SAMPLES'][sample]

    options = []
    farmout_options = []
    farmout_options.append(
        '--input-dbs-path=%s' % sample_info['datasetpath'])

    if sample_info['type'] != 'Data':
        options.append('isMC=1')
    else:
        options.append('isMC=0')
        options.append('lumiMask=%s' % sample_info['lumi_mask'])
        farmout_options.append('--lumi-mask=%s' % sample_info['lumi_mask'])
        if 'runselection' in sample_info:
            farmout_options.append('--input-runs=%s' % sample_info['runselection'])


    if 'hlt' in sample_info:
        options.append('hltProcess=%s' % sample_info['hlt'].getProcessName())

    if sample_info.get('applyZrecoilCorrection', False):
        options.append('applyZrecoilCorrection=1')

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        #'--job-count=20',
        '--input-files-per-job=3'
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
