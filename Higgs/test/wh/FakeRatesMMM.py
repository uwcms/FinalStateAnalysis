'''

Measure fake rates in trimuon events.

We measure in Z + jets

The layout of output is:

    region/denom_tag/var1
    region/denom_tag/var2
    region/denom_tag/num_tag/var1
    region/denom_tag/num_tag/var2

Author: Evan K. Friis, UW

'''

import array
import MuMuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import os

def control_region(row):
    # Figure out what control region we are in.
    if row.m1RelPFIsoDB < 0.25 and row.m2RelPFIsoDB < 0.25 \
       and row.m1_m2_Zcompat < 20 and row.metSignificance < 3\
       and row.m3MtToMET < 20:
        return 'zmm'
    else:
        return None

class FakeRatesMMM(MegaBase):
    tree = 'mmm/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesMMM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuMuMuTree.MuMuMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}
        self.is7TeV = '7TeV' in os.environ['jobid']

    def begin(self):
        for region in ['zmm']:
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

                    #pt_bins = array.array('d', [10, 12.5, 15, 17.5, 20, 30, 50, 100])

                    #book_histo('muonPt', 'Muon Pt', 100, 0, 100)
                    book_histo('muonPt', 'Muon Pt', 16, 10, 50)
                    #book_histo('muonPt', 'Muon Pt', len(pt_bins)-1, pt_bins)
                    book_histo('muonJetPt', 'Muon Jet Pt', 100, 0, 100)
                    book_histo('muonAbsEta', 'Muon Abs Eta', 100, -2.5, 2.5)
                    book_histo('metSignificance', 'MET sig.', 100, 0, 10)
                    book_histo('m1MtToMET', 'Muon 1 MT', 100, 0, 200)
                    book_histo('m3MtToMET', 'Muon 3 MT', 100, 0, 200)


    def process(self):

        def preselection(row):
            if row.m1_m2_SS: return False
            if not row.doubleMuPass: return False
            if not row.m1Pt > 20: return False
            if not row.m1PFIDTight: return False
            if not row.m2Pt > 10: return False
            if not row.m3Pt > 10: return False
            if row.m1Pt < row.m2Pt: return False
            if not row.m1AbsEta < 2.4: return False
            if not row.m2AbsEta < 2.4: return False
            if not row.m2JetBtag < 3.3: return False
            if not row.m3JetBtag < 3.3: return False
            if not row.m3PixHits: return False
            if not row.m3AbsEta < 2.4: return False
            if row.muVetoPt5: return False
            if row.bjetCSVVeto: return False
            if row.tauVetoPt20: return False
            if not abs(row.m1DZ) < 0.2: return False
            if not abs(row.m2DZ) < 0.2: return False
            if not abs(row.m3DZ) < 0.2: return False
            return True

        def trigger_match(row):
            if row.m3DiMuonL3p5PreFiltered8  > 0 or \
               row.m3DiMuonL3PreFiltered7  > 0 or \
               row.m3SingleMu13L3Filtered13  > 0 or \
               row.m3SingleMu13L3Filtered17  > 0 or \
               row.m3DiMuonMu17Mu8DzFiltered0p2  > 0:
                return True

        def fill(the_histos, row):
            # Get PU weight - FIXME
            weight = 1
            the_histos['muonPt'].Fill(row.m3Pt, weight)
            the_histos['muonJetPt'].Fill(max(row.m3JetPt, row.m3Pt), weight)
            the_histos['muonAbsEta'].Fill(row.m3AbsEta, weight)
            the_histos['metSignificance'].Fill(row.metSignificance, weight)
            the_histos['m1MtToMET'].Fill(row.m1MtToMET, weight)
            the_histos['m3MtToMET'].Fill(row.m3MtToMET, weight)

        histos = self.histograms
        for row in self.tree:
            if not preselection(row):
                continue
            if not trigger_match(row):
                continue
            region = control_region(row)
            if region is None:
                continue
            # This is a QCD or Wjets
            fill(histos[(region, 'pt10')], row)

            if row.m3PFIDTight:
                fill(histos[(region, 'pt10', 'pfid')], row)

            if row.m3RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'iso03')], row)

            if row.m3PFIDTight and row.m3RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'pfidiso03')], row)

            if row.m3PFIDTight and row.m3RelPFIsoDB < 0.2:
                fill(histos[(region, 'pt10', 'pfidiso02')], row)

            if row.m3PFIDTight and row.m3RelPFIsoDB < 0.1:
                fill(histos[(region, 'pt10', 'pfidiso01')], row)

            if row.m3Pt > 20:
                fill(histos[(region, 'pt20')], row)
                if row.m3PFIDTight:
                    fill(histos[(region, 'pt20', 'pfid')], row)

                if row.m3RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'iso03')], row)

                if row.m3PFIDTight and row.m3RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'pfidiso03')], row)

                if row.m3PFIDTight and row.m3RelPFIsoDB < 0.2:
                    fill(histos[(region, 'pt20', 'pfidiso02')], row)

                if row.m3PFIDTight and row.m3RelPFIsoDB < 0.1:
                    fill(histos[(region, 'pt20', 'pfidiso01')], row)

    def finish(self):
        self.write_histos()
