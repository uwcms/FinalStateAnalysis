'''

Analyzer for measuring the VBF selection efficiency in Z->mumu events.

Author: Evan K. Friis, UW Madison

'''

import MuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

class VBFEfficiency(MegaBase):
    tree = 'mumu/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(VBFEfficiency, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuMuTree.MuMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}

    def begin(self):
        self.book('incl', 'zPt', 'Z Pt', 100, 0, 200)
        self.book('incl', 'zMass', 'Z Mass', 60, 60, 120)
        self.book('vbf', 'zPt', 'Z Pt', 100, 0, 200)
        self.book('vbf', 'zMass', 'Z Mass', 60, 60, 120)

    def process(self):
        z_selection = ' && '.join([
            '!m1_m2_SS',
            'doubleMuPass',
            'm1RelPFIsoDB < 0.2',
            'm2RelPFIsoDB < 0.2',
            'm1Pt > 20',
            'm2Pt > 15',
            'm1AbsEta < 2.4',
            'm2AbsEta < 2.4',
            'm1_m2_Mass > 60',
            'm1_m2_Mass < 120',
        ])

        histos = self.histograms
        for row in self.tree.where(z_selection):
            histos['incl/zPt'].Fill(row.m1_m2_Pt)
            histos['incl/zMass'].Fill(row.m1_m2_Mass)

            if row.vbfNJets > 1.5 and !row.vbfJetVeto30 and row.vbfMVA > 0.5:
                histos['vbf/zPt'].Fill(row.m1_m2_Pt)
                histos['vbf/zMass'].Fill(row.m1_m2_Mass)

    def finish(self):
        self.write_histos()
