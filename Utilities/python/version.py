'''

Stupid library to get CMSSW version

'''

import os
import subprocess

def cmssw_version():
    return os.getenv('CMSSW_VERSION')

def cmssw_major_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[1])

def fsa_version():
    ''' Get commit hash of FSA '''
    result = subprocess.Popen(
        ['git', 'log', '-1', '--format=%h'],
        stdout=subprocess.PIPE).communicate()[0]
    return result.strip()
