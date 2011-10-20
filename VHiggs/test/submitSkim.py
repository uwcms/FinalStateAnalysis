import os
import sys
from FinalStateAnalysis.PatTools.datadefs import datadefs

cfg = 'analyze_cfg.py'
jobId = '2011-10-07-WHReSkim'

patJobId = '2011-10-06-EWKPatTuple'
patCfg = 'patTuple_cfg'

def get_dir(sample):
    dir_name = '-'.join([patJobId, sample, patCfg])
    base_dir = '--input-dir=root://cmsxrootd.hep.wisc.edu//store/user/efriis/'
    return base_dir + dir_name

for sample, sample_info in datadefs.iteritems():
    if 'TauPlusX' in sample:
        continue
    if 'MuHad' in sample:
        continue
    #if 'DoubleElectron' in sample:
        #continue
    #if 'QCD' in sample or 'data' in sample:
        #continue
    path_name = os.path.join(os.environ['scratch'], '-'.join(
        [jobId, sample, cfg.replace('.py', '')]))
    sys.stderr.write('Building sample submit dir %s\n' % (sample))
    if os.path.exists(path_name):
        sys.stderr.write('Skipping existing submit directory for %s\n' % sample)
        continue

    options = []
    farmout_options = []
    farmout_options.append(get_dir(sample))

    command = [
        'farmoutAnalysisJobs2',
        '--varparsing',
        #'--no-submit',
        #'--job-count=20',
        #'--input-files-per-job=%i' % (sample_info['ana_group']*2),
        '--input-files-per-job=%i' % 10,
        #'--quick-test'
    ]

    command.extend(farmout_options)

    command.append('-'.join([jobId, sample]))
    command.append(os.path.abspath(cfg))
    command.extend(options)
    print ' '.join(command)
