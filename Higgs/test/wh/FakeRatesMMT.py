'''

Measure fake rates in mu+mu+tau events

Author: Evan K. Friis, UW Madison

'''

import MMTTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

class FakeRatesMMT(MegaBase):
    tree = 'mmt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesMMT, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MMTTree.MMTTree(tree)
        self.out = outfile

    def begin(self):
        # Book histograms
        # Denominator tau PT histogram
        self.tPt = self.book('plots', 'tPtAll', 'Tau Pt', 100, 0, 100)
        # Numerator (passing MVA) histogram
        self.tPtLooseMVA = self.book('plots', 'tPtLooseMVA', 'Tau Pt', 100, 0, 100)
        # Numerator (passing regular iso) histogram
        self.tPtLooseIso = self.book('plots', 'tPtLooseIso', 'Tau Pt', 100, 0, 100)

    def process(self):
        # Analyze data.  Select events with a good Z.
        for row in self.tree.where(
            'm1RelPFIsoDB < 0.25 && '
            'm2RelPFIsoDB < 0.25 && '
            'abs(m1_m2_Mass-91.2) < 10'):
            # Fill denominator
            self.tPt.Fill(row.tPt)
            # Check if passes tau ID, if so, fill numerator
            if row.tLooseMVAIso:
                self.tPtLooseMVA.Fill(row.tPt)
            if row.tLooseIso:
                self.tPtLooseIso.Fill(row.tPt)

    def finish(self):
        self.write_histos()
