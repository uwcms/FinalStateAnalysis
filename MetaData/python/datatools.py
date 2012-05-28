'''

Various functions for getting information about the data samples defined in
datadefs.py

Author: Evan K. Friis, UW Madison

'''

from datadefs import datadefs
from FinalStateAnalysis.Utilities.das_client import get_data
import json

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
