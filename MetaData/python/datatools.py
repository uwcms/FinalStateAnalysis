'''

Various functions for getting information about the data samples defined in
datadefs.py

Author: Evan K. Friis, UW Madison

'''

from datadefs import datadefs
from FinalStateAnalysis.Utilities.das_client import get_data
from FinalStateAnalysis.Utilities.lumitools import json_summary
import logging
import json

log = logging.getLogger("datatools")

def find_data_for_run(run, primds):
    '''
    Get the appropriate dataset alias for a given run.
    This depends on the valid run ranges specified for each dataset.
    '''
    matching_datasets = []
    for dataset, dataset_info in datadefs.iteritems():
        if primds in dataset_info['datasetpath']:
            if run == 1 or (run >= dataset_info['firstRun'] and
                            run <= dataset_info['lastRun']):
                matching_datasets.append(dataset)

    if len(matching_datasets) != 1:
        raise ValueError("0 or multiple matching datasets found! %s"
                         % matching_datasets)
    return matching_datasets[0]

def map_data_to_dataset(data):
    '''
    Get the DBS name given the data nice name
    '''
    return datadefs[data]['datasetpath']

def query_das(dataset):
    ''' Get information about the dataset from DAS

    Returns a dictionary with nfiles, nevents, and size (GB).

    '''
    result = get_data(
        'https://cmsweb.cern.ch',
        'file dataset=%s | count(file), sum(file.nevents), sum(file.size)' % dataset,
        0, #idx
        0, #limit
        False
    )
    result = json.loads(result)
    output = {
        'nfiles' : result['data'][0]['result']['value'],
        'nevents' : result['data'][1]['result']['value'],
        'size' : result['data'][2]['result']['value']/1e9,
    }

    return output

def query_pattuple(dataset):
    ''' Get information about a pat tuple dataset from DAS

    Returns a dictionary with nfiles, nevents, nlumis

    '''
    output = {}
    pat_result = get_data(
        'https://cmsweb.cern.ch',
        'file dataset=%s  instance=cms_dbs_ph_analysis_01 | count(file), sum(file.nevents)' % dataset,
        0, #idx
        0, #limit
        False
    )
    pat_result = json.loads(pat_result)
    output['nfiles'] = pat_result['data'][0]['result']['value']
    output['nevents'] = pat_result['data'][1]['result']['value']

    parent_result = get_data(
        'https://cmsweb.cern.ch',
        'parent dataset=%s  instance=cms_dbs_ph_analysis_01' % dataset,
        0, #idx
        0, #limit
        False
    )
    parent_result = json.loads(parent_result)
    output['parent'] = parent_result['data'][0]['parent'][0]['name']

    return output

def query_files(dataset):
    ''' Get the list of files from a dataset '''
    log.info("Getting files from dataset %s:", dataset)
    files = []
    result = get_data(
        'https://cmsweb.cern.ch',
        'file dataset=%s  instance=cms_dbs_ph_analysis_01' % dataset,
        0, #idx
        0, #limit
        False
    )
    result = json.loads(result)
    for file_result in result['data']:
        files.append(file_result['file'][0]['name'])
    log.info("Found %i files", len(files))
    return files

def query_lumis(file):
    ''' Get the list of lumis in a file

    Returns a list of (run, lumi) tuples.

    '''
    log.info("Getting lumis from file: %s" % file)
    lumis = set([])
    result = get_data(
        'https://cmsweb.cern.ch',
        'lumi file=%s  instance=cms_dbs_ph_analysis_01' % file,
        0, #idx
        0, #limit
        False
    )
    result = json.loads(result)
    for lumi_result in result['data']:
        lumis.add((
            lumi_result['lumi'][0]['run_number'],
            lumi_result['lumi'][0]['id'],
        ))
    log.info("Found %i lumis", len(lumis))
    return lumis

def query_lumis_in_dataset(dataset):
    ''' Get all lumis in a dataset '''
    lumis = set([])
    for file in query_files(dataset):
        lumis |= query_lumis(file)
    return json_summary(lumis)

if __name__ == "__main__":
    #print query_pattuple('/WH_ZH_TTH_HToTauTau_M-115_8TeV-pythia6-tauola/friis-VH_H2Tau_M-115_2012-05-29-8TeV-PatTuple-67c1f94-4729152ae17d7e4009729a1d0d9e952d/USER')
    #files = query_files('/WH_ZH_TTH_HToTauTau_M-115_8TeV-pythia6-tauola/friis-VH_H2Tau_M-115_2012-05-29-8TeV-PatTuple-67c1f94-4729152ae17d7e4009729a1d0d9e952d/USER')
    #import pprint
    #pprint.pprint(files)
    #lumis = query_lumis('/store/user/friis/WH_ZH_TTH_HToTauTau_M-115_8TeV-pythia6-tauola/VH_H2Tau_M-115_2012-05-29-8TeV-PatTuple-67c1f94//4729152ae17d7e4009729a1d0d9e952d/output_10_1_UKO.root')
    import sys
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    lumis = query_lumis_in_dataset('/WH_ZH_TTH_HToTauTau_M-115_8TeV-pythia6-tauola/friis-VH_H2Tau_M-115_2012-05-29-8TeV-PatTuple-67c1f94-4729152ae17d7e4009729a1d0d9e952d/USER')

