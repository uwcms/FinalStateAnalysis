'''

Stupid library to get CMSSW version

'''

import os

def cmssw_version():
    return os.getenv('CMSSW_VERSION')

def cmssw_major_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[1])
