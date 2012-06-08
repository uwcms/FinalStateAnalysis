'''

Measure fake rates in dimuon events.

We measure in QCD (anti-iso mu) and W+jet (iso mu) control regions.

The layout of output is:

    region/denom_tag/var1
    region/denom_tag/var2
    region/denom_tag/num_tag/var1
    region/denom_tag/num_tag/var2

Author: Evan K. Friis, UW

'''

import MuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import os

def control_region(row):
    # Figure out what control region we are in.
    if row.muon1RelPFIsoDB < 0.15 and row.muon1MtToMET > 50:
        return 'wjets'
    elif row.muon1RelPFIsoDB > 0.3 and row.metSignificance < 3:
        return 'qcd'
    else:
        return None

class FakeRatesMM(MegaBase):
    tree = 'mumu/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesMM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuMuTree.MuMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}

    def begin(self):
        for region in ['wjets', 'qcd']:
            for denom in ['pt10', 'pt20']:
                denom_key = (region, denom)
                denom_histos = {}
                self.histograms[denom_key] = denom_histos

                for numerator in ['pfid', 'iso03', 'pfidiso03',
                                  'pfidiso01']:
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

                    book_histo('muonPt', 'Muon Pt', 100, 0, 100)
                    book_histo('muonAbsEta', 'Muon Abs Eta', 100, -2.5, 2.5)
                    book_histo('metSignificance', 'MET sig.', 100, 0, 10)
                    book_histo('muon1MtToMET', 'Muon 1 MT', 100, 0, 200)

    def process(self):
        base_selection = ' && '.join([
            'muon1_muon2_SS',
            'doubleMuPass',
            'muon1Pt > 20',
            'muon1PFIDTight',
            'muon2Pt > 10',
            'muon1AbsEta < 2.4',
            'muon2AbsEta < 2.4',
            'muon2PixHits',
            '!muVetoPt5',
        ])

        def fill(the_histos, row):
            the_histos['muonPt'].Fill(row.muon2Pt)
            the_histos['muonAbsEta'].Fill(row.muon2AbsEta)
            the_histos['metSignificance'].Fill(row.metSignificance)
            the_histos['muon1MtToMET'].Fill(row.muon1MtToMET)

        histos = self.histograms
        for row in self.tree.where(base_selection):
            region = control_region(row)
            if region is None:
                continue
            # This is a QCD or Wjets
            fill(histos[(region, 'pt10')], row)

            if row.muon2PFIDTight:
                fill(histos[(region, 'pt10', 'pfid')], row)

            if row.muon2RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'iso03')], row)

            if row.muon2PFIDTight and row.muon2RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'pfidiso03')], row)

            if row.muon2PFIDTight and row.muon2RelPFIsoDB < 0.1:
                fill(histos[(region, 'pt10', 'pfidiso01')], row)

            if row.muon2Pt > 20:
                fill(histos[(region, 'pt20')], row)
                if row.muon2PFIDTight:
                    fill(histos[(region, 'pt20', 'pfid')], row)

                if row.muon2RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'iso03')], row)

                if row.muon2PFIDTight and row.muon2RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'pfidiso03')], row)

                if row.muon2PFIDTight and row.muon2RelPFIsoDB < 0.1:
                    fill(histos[(region, 'pt20', 'pfidiso01')], row)

    def finish(self):
        self.write_histos()
