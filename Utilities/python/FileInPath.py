'''

A "File-In-Path" object for python.

Searches with respect to:
    local directory
    $CMSSW_BASE/src

Author: Evan K. Friis, UW Madison

>>> import os
>>> fip = FileInPath("FinalStateAnalysis/RecoTools/data/masks/update.sh")
>>> os.environ['CMSSW_BASE'] in fip.full_path()
True
>>> os.path.exists(fip.full_path())
True

'''

import os

class FileInPath(object):
    def __init__(self, path):
        self.path = path

    def full_path(self):
        wrt_local = self.path
        wrt_base = os.path.join(os.environ['CMSSW_BASE'], 'src', self.path)
        if os.path.exists(wrt_local):
            return wrt_local
        elif os.path.exists(wrt_base):
            return wrt_base
        else:
            raise IOError("Couldn't find %s in search path!" % self.path)


if __name__ == "__main__":
    import doctest; doctest.testmod()
