'''

Tasks a list of files and runs a py selector on it.

Takes Selector like type, a list of input files, and an input tree.

Objects are written to an output file.

'''

import ROOT


class ChainProcessor(object):
    def __init__(self, files, treename, selector, output_file, log, **kwargs):
        self.log = log
        self.tree = ROOT.TChain(treename)
        self.nfiles = len(files)
        for file in files:
            self.tree.Add(file)
        # Setup cache
        ROOT.TTreeCache.SetLearnEntries(100)
        self.tree.SetCacheSize(10000000)
        self.outfilename = output_file
        self.out = ROOT.TFile(output_file, "RECREATE")
        if not self.out:
            raise IOError("Can't open output ROOT file %s for writing"
                          % output_file)
        self.log.debug("ChainProcessor creating selector")
        # Create our selector instance
        self.selector = selector(self.tree, self.out, **kwargs)

    def process(self):
        self.selector.begin()
        self.selector.process()
        self.selector.finish()
        # Cleanup files
        self.out.Close()
        return (self.nfiles, self.outfilename)
