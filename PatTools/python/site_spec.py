import os
import sys

_host_name = os.environ['HOSTNAME']
_log_name  = os.environ['LOGNAME']

submit_dir_root = '/nfs_scratch/%s'%_log_name
output_dir_root = '/hdfs/store/user/%s'%_log_name
output_dir_srm  = 'cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN='

if 'fnal.gov' in _host_name:
    output_dir_srm  = 'cmssrm.fnal.gov:8443/srm/managerv2?SFN='
    output_dir_root = '/11/store/user/%s'%_log_name
    submit_dir_root = '/storage/local/data1/condor/execute/%s'%_log_name

if 'hep.wisc.edu' in _host_name and 'lgray' in _log_name:
    output_dir_srm  = 'cmssrm.fnal.gov:8443/srm/managerv2?SFN='
    output_dir_root = '/11/store/user/lagray'
    submit_dir_root = '/nfs_scratch/%s'%_log_name
