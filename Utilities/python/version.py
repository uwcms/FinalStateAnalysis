'''

Stupid library to get CMSSW version

'''

from functools import wraps
import os
import subprocess
import sys
import warnings


def diaper(f):
    # Decorator to make sure a function never crashes.
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            # Just catch all the shit.
            print "version.py - exception caught and discarded"
            print "Unexpected error:", str(sys.exc_info()[0])
            return "UNKNOWN"
    return wrapper

_fsa_directory = os.path.join(
    os.environ['CMSSW_BASE'], 'src', 'FinalStateAnalysis')


@diaper
def cmssw_version():
    return os.getenv('CMSSW_VERSION')


@diaper
def cmssw_major_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[1])


@diaper
def cmssw_minor_version():
    return int(os.getenv('CMSSW_VERSION').split('_')[2])


@diaper
def fsa_version_unsafe():
    ''' Get commit hash of FSA '''
    result = subprocess.Popen(
        ['git', 'log', '-1', '--format=%h'],
        cwd=_fsa_directory, stdout=subprocess.PIPE).communicate()[0]
    return result.strip()


@diaper
def fsa_version():
    ''' Get the current commit hash of FSA, without using the git command

    Reads the information directly from the .git repository folder.

    '''
    HEAD_file = os.path.join(
        _fsa_directory, '.git', 'HEAD')
    if not os.path.exists(HEAD_file):
        warnings.warn("Could not extract git commit information!")
        return 'NO_IDEA'
    # Get current HEAD ref
    with open(HEAD_file, 'r') as head:
        head_ref = head.readline().split(':')[1].strip()
        commit_file = os.path.join(
            _fsa_directory, '.git', head_ref)
        # Read commit ID for current HEAD
        with open(commit_file, 'r') as commit:
            return commit.readline().strip()[0:7]


@diaper
def get_user():
    ''' Get the user name in a safe way '''
    if 'dboard_user' in os.environ:
        return os.environ['dboard_user']
    elif 'LOGNAME' in os.environ:
        return os.environ['LOGNAME']
    return 'UNKNOWN'


@diaper
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
    print "User: %s" % get_user()
    print "Repo Status:\n%s" % repo_status()

    @diaper
    def test_diaper():
        raise ValueError("catch me")
    test_diaper()

