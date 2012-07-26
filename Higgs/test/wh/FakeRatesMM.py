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
    if row.m1RelPFIsoDB < 0.15 and row.m1MtToMET > 40 and row.m2MtToMET < 30:
        return 'wjets'
    elif row.m1RelPFIsoDB > 0.3 and row.metSignificance < 3:
        return 'qcd'
    else:
        return None

class FakeRatesMM(MegaBase):
    tree = 'mm/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesMM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuMuTree.MuMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}
        self.is7TeV = '7TeV' in os.environ['jobid']

    def begin(self):
        for region in ['wjets', 'qcd']:
            for denom in ['pt10', 'pt20']:
                denom_key = (region, denom)
                denom_histos = {}
                self.histograms[denom_key] = denom_histos

                for numerator in ['pfid', 'iso03', 'pfidiso03',
                                  'pfidiso02', 'pfidiso01']:
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

                    book_histo('muonPt', 'Muon Pt', 16, 10, 50)
                    book_histo('muonJetPt', 'Muon Jet Pt', 100, 0, 100)
                    book_histo('muonAbsEta', 'Muon Abs Eta', 100, -2.5, 2.5)
                    book_histo('metSignificance', 'MET sig.', 100, 0, 10)
                    book_histo('m1MtToMET', 'Muon 1 MT', 100, 0, 200)


    def process(self):

        def preselection(row):
            if not row.m1_m2_SS: return False
            if not row.doubleMuPass: return False
            if row.m1Pt < row.m2Pt: return False
            if not row.m1Pt > 20: return False
            if not row.m1PFIDTight: return False
            if not row.m2Pt > 10: return False
            if not row.m1AbsEta < 2.4: return False
            if not row.m2AbsEta < 2.4: return False
            if not row.m2JetBtag < 3.3: return False
            if not row.m2PixHits: return False
            if row.eVetoCicTightIso: return False
            if row.muVetoPt5: return False
            if row.bjetCSVVeto: return False
            if row.tauVetoPt20: return False
            if not abs(row.m1DZ) < 0.2: return False
            if not abs(row.m2DZ) < 0.2: return False
            return True

        def fill(the_histos, row):
            # Get PU weight - fix me
            weight = 1
            the_histos['muonPt'].Fill(row.m2Pt, weight)
            the_histos['muonJetPt'].Fill(max(row.m2JetPt, row.m2Pt), weight)
            the_histos['muonAbsEta'].Fill(row.m2AbsEta, weight)
            the_histos['metSignificance'].Fill(row.metSignificance, weight)
            the_histos['m1MtToMET'].Fill(row.m1MtToMET, weight)

        histos = self.histograms
        for row in self.tree:
            if not preselection(row):
                continue
            region = control_region(row)
            if region is None:
                continue
            # This is a QCD or Wjets
            fill(histos[(region, 'pt10')], row)

            if row.m2PFIDTight:
                fill(histos[(region, 'pt10', 'pfid')], row)

            if row.m2RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'iso03')], row)

            if row.m2PFIDTight and row.m2RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'pfidiso03')], row)

            if row.m2PFIDTight and row.m2RelPFIsoDB < 0.2:
                fill(histos[(region, 'pt10', 'pfidiso02')], row)

            if row.m2PFIDTight and row.m2RelPFIsoDB < 0.1:
                fill(histos[(region, 'pt10', 'pfidiso01')], row)

            if row.m2Pt > 20:
                fill(histos[(region, 'pt20')], row)
                if row.m2PFIDTight:
                    fill(histos[(region, 'pt20', 'pfid')], row)

                if row.m2RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'iso03')], row)

                if row.m2PFIDTight and row.m2RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'pfidiso03')], row)

                if row.m2PFIDTight and row.m2RelPFIsoDB < 0.2:
                    fill(histos[(region, 'pt20', 'pfidiso02')], row)

                if row.m2PFIDTight and row.m2RelPFIsoDB < 0.1:
                    fill(histos[(region, 'pt20', 'pfidiso01')], row)

    def finish(self):
        self.write_histos()
