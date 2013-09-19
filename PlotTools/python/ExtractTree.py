''' Mega analyzer class that just copies over a single tree to the outputfile.

Used for merging metadata information in batch.

Author: Evan K. Friis, UW Madison

'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase


class ExtractTree(MegaBase):
    def __init__(self, tree, outfile, **kwargs):
        super(ExtractTree, self).__init__(tree, outfile, **kwargs)

    def begin(self):
        pass

    def process(self):
        # Just copy over the tree into the output file
        self.output.cd()
        self.newtree = self.tree.CloneTree()

    def finish(self):
        # Make sure the Tree is flushed to the outfile
        self.newtree.Write()
