'''
File: submit_tuplization_crab.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: submit UW pattuple jobs via crab. Makes a crab.cfg and multicrab.cfg (populated by datasets with filter provided by user)
Based on submit_tuplization.py
'''


from FinalStateAnalysis.MetaData.datadefs import datadefs
import os
import sys

cfg = 'patTuple_cfg.py'
jobId = '2012-05-15-PatTuple'

if len(sys.argv)==1:
	print "Hey, I need some help. What datasets do you want to look for?"
	sys.exit()
searchTerm = sys.argv[1]

os.system('mkdir -p '+jobId)
print 'export TERMCAP=screen'

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

    submit_dir_base = "/scratch/{logname}/{jobid}/{sample}".format(
        logname = os.environ['LOGNAME'],
        jobid = jobId,
        sample = sample
    )

    submit_dir = os.path.join(submit_dir_base, 'submit')

    #cmsRun parameters
    options = []

    # Figure out dataset - the EGamma electron calibrator needs to know
    # if we are using a ReReco, etc.
    dataset=None
    for tag in ['Fall11', 'Summer11', 'Prompt', 'ReReco', 'Jan16ReReco']:
        if tag in sample_info['datasetpath']:
            dataset = tag
    if dataset is None and '05Aug2011' in sample_info['datasetpath']:
        dataset = 'ReReco'
    if dataset is None and 'crab_reco' in sample_info['datasetpath']:
        dataset = 'Fall11'
    if not dataset:
        raise ValueError("Couldn't determine dataset for sample: "
                        + sample_info['datasetpath'])
    options.append('dataset=%s' % dataset)

    # Figure out which target - the EGamma/Muon effective areas need to know
    # this
    target=None
    if 'Fall11' in sample_info['datasetpath']:
        target = 'Fall11MC'
    elif 'crab_reco' in sample_info['datasetpath']: # special case, private prod
        target = 'Fall11MC'
    elif 'Summer11' in sample_info['datasetpath']:
        target = 'Summer11MC'
    elif 'data' in sample and '2011' in sample_info['datasetpath']:
        target = '2011Data'
    elif 'data' in sample and '2012' in sample_info['datasetpath']:
        target = '2012Data'
    if not target:
        raise ValueError("Couldn't determine target for sample: "
                         + sample_info['datasetpath'])
    options.append('target=%s' % target)

    if 'data' not in sample:
        options.append('isMC=1')
        options.append('globalTag=$mcgt')
        options.append('xSec=%0.4f' % sample_info['x_sec'])
        options.append('puTag=%s' % sample_info['pu'])
    else:
        options.append('isMC=0')
        options.append('globalTag=$datagt')
        options.append('puTag=data')
        lumi_mask_fip = sample_info['lumi_mask']
        lumi_mask_path = os.path.join(
            os.environ['CMSSW_BASE'], 'src', lumi_mask_fip)
        options.append('lumiMask=%s' % lumi_mask_path)
        if 'firstRun' in sample_info:
            options.append('firstRun=%s' % sample_info['firstRun'])
            options.append('lastRun=%s' % sample_info['lastRun'])

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
