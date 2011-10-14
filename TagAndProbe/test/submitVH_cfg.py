import os

from FinalStateAnalysis.TagAndProbe.datadefs import datadefs

cfg = 'analyzeZHnunutautau_cfg.py'
jobId = '2011-09-02-v4-VHAnalyze'

patJobId = '2011-08-16-v2-TauIdPatTuple'
patCfg = 'tauID_patTuple_cfg'

def get_dir(sample):
    dir_name = '-'.join([patJobId, sample, patCfg])
    base_dir = '--input-dir=root://cmsxrootd.hep.wisc.edu//store/user/efriis/'
    return base_dir + dir_name

for sample, sample_info in datadefs.iteritems():

    options = []
    if 'VH' in sample:
        options.append('isSignal=1')
    farmout_options = []
    farmout_options.append(get_dir(sample))

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        #'--fwklite',
        #'--job-count=20',
        '--input-files-per-job=%i' % (sample_info['ana_group']*2),
        ' --exclude-input-files="*_plots.root"'
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    #command.append('/afs/hep.wisc.edu/user/efriis/cmssw/TagAndProbe/bin/slc5_amd64_gcc434/fwliteTagAndProbe')
    #command.append('/afs/hep.wisc.edu/user/efriis/cmssw/TagAndProbe/bin/slc5_amd64_gcc434/fwliteTagAndProbe')
    command.append(os.path.abspath(cfg))
    command.extend(options)
    print ' '.join(command)

