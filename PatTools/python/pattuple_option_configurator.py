'''

Figures out which options should be passed to patTuple_cfg.py depending
on the dataset.

Author: Evan K. Friis, UW Madison

'''

from FinalStateAnalysis.MetaData.datadefs import datadefs
import os

def configure_pat_tuple(sample, sample_info):
    options = []

    # Figure out dataset - the EGamma electron calibrator needs to know
    # if we are using a ReReco, etc.
    dataset=None
    for tag in ['Fall11', 'Summer11', 'Prompt', 'ReReco', 'Jan16ReReco']:
        if tag in sample_info['datasetpath']:
            dataset = tag
    if dataset is None and '05Aug2011' in sample_info['datasetpath']:
        dataset = 'ReReco'
    if dataset is None and '16Jan2012' in sample_info['datasetpath']:
        dataset = 'Jan16ReReco'
    if dataset is None and 'crab_reco' in sample_info['datasetpath']:
        dataset = 'Fall11'
    if dataset is None and 'Summer12' in sample_info['datasetpath']:
        # Not determined yet
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
    elif 'Summer12' in sample_info['datasetpath']:
        target = '2011Data'

    if not target:
        raise ValueError("Couldn't determine target for sample: "
                         + sample_info['datasetpath'])
    options.append('target=%s' % target)

    if 'data' not in sample:
        options.append('isMC=1')
        options.append('globalTag=%s' % os.environ['mcgt'])
        if 'x_sec' in sample_info:
            options.append('xSec=%0.4f' % sample_info['x_sec'])
        else:
            options.append('xSec=0')
        options.append('puTag=%s' % sample_info['pu'])
    else:
        options.append('isMC=0')
        options.append('globalTag=%s' % os.environ['datagt'])
        options.append('puTag=data')
        lumi_mask_fip = sample_info['lumi_mask']
        lumi_mask_path = os.path.join(
            os.environ['CMSSW_BASE'], 'src', lumi_mask_fip)
        options.append('lumiMask=%s' % lumi_mask_path)
        if 'firstRun' in sample_info:
            options.append('firstRun=%s' % sample_info['firstRun'])
            options.append('lastRun=%s' % sample_info['lastRun'])

    return options

