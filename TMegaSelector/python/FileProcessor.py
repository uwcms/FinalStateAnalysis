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
        self.file = ROOT.TFile(filename, "READ")
        if not self.file:
            raise IOError("Can't open ROOT file: %s" % filename)
        self.tree = self.file.Get(treename)
        if not self.tree:
            raise IOError("Can't get tree: %s from file: %s" %
                          (treename, filename))
        self.outfilename = output_file
        self.out = ROOT.TFile(output_file, "RECREATE")
        if not self.file:
            raise IOError("Can't open output ROOT file %s for writing"
                          % output_file)
        # Create our selector instance
        self.selector = selector(self.tree, self.out, **kwargs)

    def process(self):
        nentries = self.tree.GetEntries()
        selector = self.selector
        for x in xrange(nentries):
            selector.process(x)
        # Tell the selector to clean up
        if hasattr(selector, 'finish'):
            selector.finish()
        return (nentries, self.outfilename)
