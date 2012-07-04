'''

Measure fake rates in the E+Mu channel

We measure in QCD (anti-iso mu) and W+jet (iso mu) control regions.

The layout of output is:
    region/denom_tag/var1
    region/denom_tag/var2
    region/denom_tag/num_tag/var1
    region/denom_tag/num_tag/var2

Author: Evan K. Friis, UW

'''

import EMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import os

def control_region(row):
    # Figure out what control region we are in.
    if row.muonRelPFIsoDB < 0.15 and row.muonMtToMET > 50:
        return 'wjets'
    elif row.muonRelPFIsoDB > 0.3 and row.metSignificance < 3:
        return 'qcd'
    else:
        return None

class FakeRatesEM(MegaBase):
    tree = 'emu/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesEM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = EMuTree.EMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}

    def begin(self):
        for region in ['wjets', 'qcd']:
            for denom in ['pt10']:
                denom_key = (region, denom)
                denom_histos = {}
                self.histograms[denom_key] = denom_histos

                for numerator in ['mvaid', 'iso03', 'mvaidiso03',
                                  'mvaidiso01']:
                    num_key = (region, denom, numerator)
                    num_histos = {}
                    self.histograms[num_key] = num_histos

                    def book_histo(name, *args):
                        # Helper to book a histogram
                        if name not in denom_histos:
                            denom_histos[name] = self.book(os.path.join(
                                region, denom), name, *args)
                        num_histos[name] = self.book(os.path.join(
                            region, denom, numerator), name, *args)

                    book_histo('electronPt', 'Electron Pt', 100, 0, 100)
                    book_histo('electronJetPt', 'Electron Jet Pt', 100, 0, 100)
                    book_histo('electronAbsEta', 'Electron Abs Eta', 100, -2.5, 2.5)
                    book_histo('metSignificance', 'MET sig.', 100, 0, 10)
                    book_histo('muonMtToMET', 'Muon MT', 100, 0, 200)

    def process(self):
        base_selection = ' && '.join([
            'electron_muon_SS',
            'mu17ele8Pass',
            'muonPt > 20',
            'electronPt > 10',
            'muonAbsEta < 2.4',
            'electronAbsEta < 2.5',
            '!muVetoPt5',
            '!electronHasConversion',
            '!electronMissingHits',
        ])

        def fill(the_histos, row):
            the_histos['electronPt'].Fill(row.electronPt)
            the_histos['electronJetPt'].Fill(row.electronJetPt)
            the_histos['electronAbsEta'].Fill(row.electronAbsEta)
            the_histos['metSignificance'].Fill(row.metSignificance)
            the_histos['muonMtToMET'].Fill(row.muonMtToMET)

        histos = self.histograms
        for row in self.tree.where(base_selection):
            region = control_region(row)
            if region is None:
                continue
            # This is a QCD or Wjets
            fill(histos[(region, 'pt10')], row)

            if row.electronMVAIDH2TauWP:
                fill(histos[(region, 'pt10', 'mvaid')], row)

            if row.electronRelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'iso03')], row)

            if row.electronMVAIDH2TauWP and row.electronRelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'mvaidiso03')], row)

            if row.electronMVAIDH2TauWP and row.electronRelPFIsoDB < 0.1:
                fill(histos[(region, 'pt10', 'mvaidiso01')], row)

    def finish(self):
        self.write_histos()
