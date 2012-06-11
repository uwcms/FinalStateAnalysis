'''

Class which mimics PROOF functionality.

Processes a single file (with a single Tree in it)

Takes Selector like type, an input file, and an input tree.

Objects are written to an output file.

'''


import ROOT
import logging

class FileProcessor(object):
    def __init__(self, filename, treename, selector, output_file, **kwargs):
        self.file = ROOT.TFile.Open(filename, "READ")
        if not self.file:
            raise IOError("Can't open ROOT file: %s" % filename)
        self.tree = self.file.Get(treename)
        if not self.tree:
            raise IOError("Can't get tree: %s from file: %s" %
                          (treename, filename))
        # Setup cache
        ROOT.TTreeCache.SetLearnEntries(10)
        self.tree.SetCacheSize(10000000)
        self.outfilename = output_file
        self.out = ROOT.TFile(output_file, "RECREATE")
        if not self.file:
            raise IOError("Can't open output ROOT file %s for writing"
                          % output_file)
        # Create our selector instance
        self.selector = selector(self.tree, self.out, **kwargs)

    def process(self):
        self.selector.begin()
        self.selector.process()
        self.selector.finish()
        return (1, self.outfilename)
