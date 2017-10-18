'''
File: submit_tuplization_crab.py

Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison

Description: submit UW pattuple jobs via crab. Makes a crab.cfg and
multicrab.cfg (populated by datasets with filter provided by user) Based on
submit_tuplization.py

'''


from RecoLuminosity.LumiDB import argparse
import fnmatch
from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.Utilities.version import fsa_version
from FinalStateAnalysis.PatTools.pattuple_option_configurator import \
        configure_pat_tuple
import os
import sys

parser = argparse.ArgumentParser(description='Build PAT Tuple CRAB submission')
parser.add_argument('jobid', help='Job ID identifier')
parser.add_argument('--samples', nargs='+', type=str, required=False,
                    help='Filter samples using list of patterns (shell style)')
parser.add_argument('--no-whitelist', dest='nowhitelist', default=False,
                    action='store_true',
                    help='Disable the default T2_US, T3_US whitelist')
parser.add_argument('--glite', dest='glite', default=False,
                    action='store_true',
                    help='Use glite server')
args = parser.parse_args()

cfg = 'patTuple_cfg.py'
jobId = args.jobid

# Put in scratch then symlink it to the CWD
scratch_dir = os.path.join('/scratch', os.environ['LOGNAME'], jobId)
os.system('mkdir -p '+ scratch_dir)
if not os.path.exists(jobId):
    os.symlink(scratch_dir, jobId)

#Write a simple crab.cfg
f=open('%s/crab.cfg' % jobId, 'w')
f.write('[CRAB]\njobtype = cmssw\nscheduler = %s\nuse_server = 1\n' %
       'glidein' if not args.glite else 'glite')
f.write('[USER]\nreturn_data = 0\ncopy_data = 1\nstorage_element = T2_US_Wisconsin\n')
f.write('publish_data = 1\ndbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet\n')
f.write('[GRID]\nrb = CERN\nmaxtarballsize = 250\n')
if not args.nowhitelist:
    f.write('se_white_list = T2_US, T3_US\n')
f.close()

#make multicrab.cfg
f=open('%s/multicrab.cfg' % jobId, 'w')
f.write('[MULTICRAB]\ncfg = crab.cfg\n')
f.write('[COMMON]\nCMSSW.get_edm_output = 1\n\n')

# Loop over samples
for sample in sorted(datadefs.keys()):
    sample_info = datadefs[sample]
    passes_filter = True
    # Filter by sample wildcards
    if args.samples:
        passes_wildcard = False
        for pattern in args.samples:
            if fnmatch.fnmatchcase(sample, pattern):
                passes_wildcard = True
        passes_filter = passes_wildcard and passes_filter
    if not passes_filter:
        continue

    f.write('[')
    f.write(sample)
    f.write(']\n')

    #cmsRun parameters
    options = configure_pat_tuple(sample, sample_info)

    f.write('CMSSW.datasetpath = '+sample_info['datasetpath']+'\n')
    f.write('CMSSW.pset = ')
    f.write(sample+'_cfg.py\n')
    if 'data' not in sample and 'embedded' not in sample:
        f.write('CMSSW.total_number_of_events = -1\nCMSSW.events_per_job = 7000\n')
    else:
        f.write('CMSSW.total_number_of_lumis = -1\nCMSSW.lumis_per_job = 30\n')
        lumi_mask_fip = sample_info['lumi_mask']
        lumi_mask_path = os.path.join(os.environ['CMSSW_BASE'],
                                      'src', lumi_mask_fip)
        f.write('CMSSW.lumi_mask = %s\n' % lumi_mask_path)
        # Apply a run selection
        if 'firstRun' in sample_info:
            f.write('CMSSW.runselection = %i-%i\n' %
                    (sample_info['firstRun'], sample_info['lastRun']))

    options.append('dumpCfg='+jobId+'/'+sample+'_cfg.py')
    opts= ' '.join(options)
    print "python patTuple_cfg.py "+opts
    os.system("python patTuple_cfg.py "+opts)

    f.write('USER.publish_data_name = '+sample+"_%s-%s\n" % (jobId, fsa_version()))

    if 'dbs' in sample_info:
        f.write('CMSSW.dbs_url =http://cmsdbsprod.cern.ch/'+sample_info['dbs']+'/servlet/DBSServlet\n')

f.write('\n\n')
f.close()
