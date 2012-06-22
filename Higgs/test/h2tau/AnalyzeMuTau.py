'''

Run the Mu-Tau analysis

'''

import MuTauTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

def category(row):
    taupt = row.tauPt
    njets = row.jetVeto40
    return 'boosted_low'

def region(row):
    return 'os_signal'

class AnalyzeMuTau(MegaBase):
    def __init__(self, tree, outfile, **kwargs):
        super(AnalyzeMuTau, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuTauTree.MuTauTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}

    def begin(self):
        categories = [
            'boosted_low', 'boosted_high',
            '0jet_low', '0jet_high',
            '1jet_low', '1jet_high',
            '1bjet_low', '1bjet_high',
            'vbf', 'vjj'
        ]
        regions = [
            'os_signal', 'ss_signal',
            'os_mt', 'ss_mt',
        ]

        for category in categories:
            for region in regions:
                key = (category, region)
                histos = {}
                self.histograms[key] = histos
                def book_histo(name, *args):
                    # Helper to book a histogram
                    histos[name] = self.book(category + '/' + region, name, *args)
                book_histo('tauPt', 'Tau Pt', 100, 0, 100)
                book_histo('tauAbsEta', 'Tau Abs Eta', 100, -2.5, 2.5)

    def process(self):
        base_selection = ' && '.join([
            'muonRelPFIsoDB < 0.1',
            'tauLooseMVAIso',
            'muonPFIDTight',
            'abs(muonDZ) < 0.1',
            'abs(muonD0) < 0.045',
        ])
        for row in self.tree.where(base_selection):
            category_key = category(row), region(row)
            self.histograms[category_key]['tauPt'].Fill(row.tauPt)

    def finish(self):
        self.write_histos()
