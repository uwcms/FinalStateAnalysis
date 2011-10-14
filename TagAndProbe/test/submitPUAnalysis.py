import os
from FinalStateAnalysis.PatTools.datadefs import datadefs

cfg = 'analyze_PU_cfg.py'
jobId = '2011-10-03-v1-TauPUAnalyze'

patJobId = '2011-09-30-EWKPatTuple'
patCfg = 'patTuple_cfg'

def get_dir(sample):
    dir_name = '-'.join([patJobId, sample, patCfg])
    base_dir = '--input-dir=root://cmsxrootd.hep.wisc.edu//store/user/efriis/'
    return base_dir + dir_name

for sample, sample_info in datadefs.iteritems():
    #if 'QCD' in sample or 'data' in sample:
        #continue
    we_like_it = False
    if 'SingleMu' in sample:
        we_like_it = True
    if 'Zjets_M50' in sample:
        we_like_it = True
    if 'WplusJets' in sample:
        we_like_it = True
    we_like_it = False
    if '2011B' in sample and 'SingleMu' in sample:
        we_like_it = True
    if not we_like_it:
        continue

    options = []
    farmout_options = []
    farmout_options.append(get_dir(sample))

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        '--fwklite',
        #'--no-submit',
        '--job-count=60',
        #'--input-files-per-job=%i' % (sample_info['ana_group']*2),
        ' --exclude-input-files="*plots.root"'
        '--input-files-per-job=%i' % 5,
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append('/afs/hep.wisc.edu/user/efriis/cmssw/TagAndProbe/bin/slc5_amd64_gcc434/analyzeFinalStates')
    command.append(os.path.abspath(cfg))
    command.extend(options)
    print ' '.join(command)
