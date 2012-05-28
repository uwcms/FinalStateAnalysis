'''
File: submit_tuplization_crab.py

Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison

Description: submit UW pattuple jobs via crab. Makes a crab.cfg and
multicrab.cfg (populated by datasets with filter provided by user) Based on
submit_tuplization.py

'''


from FinalStateAnalysis.MetaData.datadefs import datadefs
from FinalStateAnalysis.PatTools.pattuple_option_configurator import \
        configure_pat_tuple
import os
import sys

cfg = 'patTuple_cfg.py'
jobId = '2012-05-15-PatTuple'

if len(sys.argv)==1:
	print "Hey, I need some help. What datasets do you want to look for?"
	sys.exit()
searchTerm = sys.argv[1]

os.system('mkdir -p '+jobId)

#Write a simple crab.cfg
f=open('crab.cfg','w')
f.write('[CRAB]\njobtype = cmssw\nscheduler = glidein\nuse_server = 1\n')
f.write('[USER]\nreturn_data = 0\ncopy_data = 1\nstorage_element = T2_US_Wisconsin\npublish_data = 1\ndbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet')
f.write('[GRID]\nrb = CERN\nmaxtarballsize = 250\n')
f.close()

#make multicrab.cfg
f=open('multicrab.cfg','w')
f.write('[MULTICRAB]\ncfg = crab.cfg\n')
f.write('[COMMON]\nCMSSW.total_number_of_lumis = -1\nCMSSW.lumis_per_job = 40\nCMSSW.get_edm_output = 1\n\n')
for sample in sorted(datadefs.keys()):
    if sample.find(searchTerm) == -1:
        continue

    f.write('[')
    f.write(sample)
    f.write(']\n')
    sample_info = datadefs[sample]

    #cmsRun parameters
    options = configure_pat_tuple(sample, sample_info)

    f.write('CMSSW.datasetpath = '+sample_info['datasetpath']+'\n')
    f.write('CMSSW.pset = ')
    f.write(jobId+'/'+sample+'_cfg.py\n')
    options.append('dumpCfg='+jobId+'/'+sample+'_cfg.py')
    opts= ' '.join(options)
    print "python patTuple_cfg.py "+opts
    os.system("python patTuple_cfg.py "+opts)

    if 'dbs' in sample_info:
        f.write('CMSSW.dbs_url =http://cmsdbsprod.cern.ch/'+sample_info['dbs']+'/servlet/DBSServlet\n')
	f.write('USER.publish_data_name = ',sample+"_TUPLE\n")

f.write('\n\n')
f.close()
