'''

Figures out which options should be passed to patTuple_cfg.py depending
on the dataset.

Author: Evan K. Friis, UW Madison

'''

import os

def configure_pat_tuple(sample, sample_info):
    options = []

    #if the HLT process happens to not be 'HLT'
    if 'hlt_process' in sample_info:
        options.append('HLTprocess=%s'%(sample_info['hlt_process']))

    if 'calibrationTarget' in sample_info:
        options.append('calibrationTarget=%s'%sample_info['calibrationTarget'])

    if 'data' not in sample and 'embedded' not in sample:
        options.append('isMC=1')
        options.append('globalTag=%s' % os.environ['mcgt'])
        if 'x_sec' in sample_info:
            options.append('xSec=%0.5e' % sample_info['x_sec'])
        else:
            options.append('xSec=0')
        options.append('puTag=%s' % sample_info['pu'])
    elif 'embedded' in sample:
        options.append('isMC=1')
        options.append('embedded=1')
        options.append('globalTag=%s' % os.environ['datagt'])
        if 'x_sec' in sample_info:
            options.append('xSec=%0.5e' % sample_info['x_sec'])
        else:
            options.append('xSec=0')
        options.append('puTag=%s' % sample_info['pu'])
    else:
        options.append('isMC=0')
        options.append('globalTag=%s' % os.environ['datagt'])
        options.append('puTag=data')
        # This path goes to cmsRun, and should be relative (i.e.
        # edm::FileInPath)
        lumi_mask_fip = sample_info['lumi_mask']
        options.append('lumiMask=%s' % lumi_mask_fip)
        if 'firstRun' in sample_info:
            options.append('firstRun=%s' % sample_info['firstRun'])
            options.append('lastRun=%s' % sample_info['lastRun'])

    return options

