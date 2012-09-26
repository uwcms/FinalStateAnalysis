'''

Stupid library to get CMSSW version

'''

import os
import subprocess
import re

_fsa_directory = os.path.join(
    os.environ['CMSSW_BASE'], 'src', 'FinalStateAnalysis')

def cmssw_version():
    return os.getenv('CMSSW_VERSION')

def cmssw_major_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[1])

def cmssw_minor_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[2])

def fsa_version_unsafe():
    ''' Get commit hash of FSA '''
    result = subprocess.Popen(
        ['git', 'log', '-1', '--format=%h'],
        cwd=_fsa_directory, stdout=subprocess.PIPE).communicate()[0]
    return result.strip()

def fsa_version():
    ''' Get the current commit hash of FSA, without using the git command

    Reads the information directly from the .git repository folder.

    '''
    HEAD_file = os.path.join(
        _fsa_directory, '.git', 'HEAD')
    # Get current HEAD ref
    with open(HEAD_file, 'r') as head:
        head_ref = head.readline().split(':')[1].strip()
        commit_file = os.path.join(
            _fsa_directory, '.git', head_ref)
        # Read commit ID for current HEAD
        with open(commit_file, 'r') as commit:
            return commit.readline().strip()[0:7]

def repo_status():
    ''' Get status of FSA repository '''
    result = subprocess.Popen(
        ['git', 'status', '-s'],
        cwd=_fsa_directory, stdout=subprocess.PIPE).communicate()[0]
    return result.strip()

if __name__ == "__main__":
    print "Version info:"
    print "CMSSW: %s - major = %i" % (cmssw_version(), cmssw_major_version())
    print "Commit: %s" % fsa_version_unsafe()
    print "Commit (safe mode): %s" % fsa_version()
    print "Repo Status:\n%s" % repo_status()

