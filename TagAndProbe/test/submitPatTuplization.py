from FinalStateAnalysis.TagAndProbe.datadefs import datadefs

cfg = 'tauID_patTuple_cfg.py'
jobId = '2011-09-14-v1-TauIdPatTuple'

skimJobId = '2011-09-14-TauIdEffSkim'
skimCfg = 'tauID_skim_cfg'

def get_dir(sample):
    dir_name = '-'.join([skimJobId, sample, skimCfg])
    base_dir = '--input-dir=root://cmsxrootd.hep.wisc.edu//store/user/efriis/'
    return base_dir + dir_name

for sample, sample_info in datadefs.iteritems():

    options = []
    farmout_options = []
    farmout_options.append(get_dir(sample))

    if 'data' not in sample:
        options.append('isMC=1')
        options.append('globalTag=START42_V13::All')
    else:
        options.append('isMC=0')
        options.append('globalTag=GR_R_42_V19::All')

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        '--input-files-per-job=1',
        ' --exclude-input-files="*_plots.root"'
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(cfg)
    command.extend(options)
    print ' '.join(command)
