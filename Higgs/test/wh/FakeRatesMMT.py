'''

Measure fake rates in mu+mu+tau events

Author: Evan K. Friis, UW Madison

'''

import MMTTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

class FakeRatesMMT(MegaBase):
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesMMT, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MMTTree.MMTTree(tree)
        self.out = outfile

    def begin(self):
        self.out.cd()
        self.tPt = self.book('plots', 'tPt', 'Tau Pt', 100, 0, 100)

    def process(self):
        for row in self.tree:
            self.tPt.Fill(row.tPt)

    def finish(self):
        self.write_histos()
