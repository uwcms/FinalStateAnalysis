import os
import sys

_host_name = os.environ['HOSTNAME']

submit_dir_root = '/scratch'
output_dir_root = '/hdfs/store/user/'
output_dir_srm  = 'cmssrm.hep.wisc.edu:8443'

if 'fnal.gov' in _host_name:
    output_dir_srm  = 'cmssrm.fnal.gov:8443'
    output_dir_root = '/pnfs/cms/WAX/11/store/user/'
    submit_dir_root = '/storage/local/data1/condor/execute'

