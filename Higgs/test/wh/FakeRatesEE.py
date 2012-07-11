'''

Measure fake rates in dielectron events.

NB that the triggers we are using always have the same iso on the leading
and subleading legs.

We measure W+jet (iso electron) control regions.

The layout of output is:

    region/denom_tag/var1
    region/denom_tag/var2
    region/denom_tag/num_tag/var1
    region/denom_tag/num_tag/var2

Author: Evan K. Friis, UW

'''

import EETree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import os

def control_region(row):
    # Figure out what control region we are in.
    if row.e1_e2_SS and row.e1RelPFIsoDB < 0.15 and row.e1MtToMET > 50 and row.metSignificance > 3:
        return 'wjets'
    elif row.e1_e2_SS and row.e1RelPFIsoDB > 0.3 and row.metSignificance < 3:
        return 'qcd'
    elif row.e1RelPFIsoDB < 0.3 and row.e2RelPFIsoDB < 0.3 and row.e2MVAIDH2TauWP:
        return 'zee'
    else:
        return None

class FakeRatesEE(MegaBase):
    tree = 'ee/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesEE, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = EETree.EETree(tree)
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

                    book_histo('e2Pt', 'e Pt', 100, 0, 100)
                    book_histo('e2JetPt', 'e Jet Pt', 100, 0, 100)
                    book_histo('e2AbsEta', 'e Abs Eta', 100, -2.5, 2.5)
                    book_histo('metSignificance', 'MET sig.', 100, 0, 10)
                    book_histo('e1MtToMET', 'm MT', 100, 0, 200)
                    book_histo('e1e2Mass', 'DiElectron Mass', 100, 0, 200)
                    book_histo('doubleEPrescale', 'prescale', 10, -0.5, 9.5)
        # Charge mis-ID measurements
        self.book('charge', 'e1e2MassOS', 'DiEle mass OS', 60, 60, 120)
        self.book('charge', 'e1e2MassSS', 'DiEle mass SS', 60, 60, 120)

    def process(self):

        def preselection(row):
            if not row.doubleEPass: return False
            if not row.e1Pt > 20: return False
            if not row.e1MVAIDH2TauWP: return False
            if not row.e2Pt > 10: return False
            if not row.e1AbsEta < 2.5: return False
            if not row.e2AbsEta < 2.5: return False
            if not row.e1JetBtag < 3.3: return False
            if not row.e2JetBtag < 3.3: return False
            if not row.e1ChargeIdTight: return False
            if not row.e2ChargeIdTight: return False
            if row.eVetoCicTightIso: return False
            if row.muVetoPt5: return False
            if row.bjetCSVVeto: return False
            if row.tauVetoPt20: return False
            if row.e2HasConversion: return False
            if row.e2MissingHits: return False
            if row.e1HasConversion: return False
            if row.e1MissingHits: return False
            if not abs(row.e1DZ) < 0.2: return False
            if not abs(row.e2DZ) < 0.2: return False
            return True

        def fill(the_histos, row):
            the_histos['e2Pt'].Fill(row.e2Pt)
            the_histos['e2JetPt'].Fill(row.e2JetPt)
            the_histos['e2AbsEta'].Fill(row.e2AbsEta)
            the_histos['metSignificance'].Fill(row.metSignificance)
            the_histos['e1MtToMET'].Fill(row.e1MtToMET)
            the_histos['e1e2Mass'].Fill(row.e1_e2_Mass)
            the_histos['doubleEPrescale'].Fill(row.doubleEPrescale)

        histos = self.histograms
        for row in self.tree:
            if not preselection(row):
                continue

            region = control_region(row)
            if region is None:
                continue

            if region == 'zee':
                if row.e1_e2_SS:
                    histos['charge/e1e2MassSS'].Fill(row.e1_e2_Mass)
                else:
                    histos['charge/e1e2MassOS'].Fill(row.e1_e2_Mass)
                continue

            # This is a QCD or Wjets
            fill(histos[(region, 'pt10')], row)

            if row.e2MVAIDH2TauWP:
                fill(histos[(region, 'pt10', 'mvaid')], row)

            if row.e2RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'iso03')], row)

            if row.e2MVAIDH2TauWP and row.e2RelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'mvaidiso03')], row)

            if row.e2MVAIDH2TauWP and row.e2RelPFIsoDB < 0.1:
                fill(histos[(region, 'pt10', 'mvaidiso01')], row)

            if row.e2Pt > 20:
                fill(histos[(region, 'pt20')], row)
                if row.e2MVAIDH2TauWP:
                    fill(histos[(region, 'pt20', 'mvaid')], row)

                if row.e2RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'iso03')], row)

                if row.e2MVAIDH2TauWP and row.e2RelPFIsoDB < 0.3:
                    fill(histos[(region, 'pt20', 'mvaidiso03')], row)

                if row.e2MVAIDH2TauWP and row.e2RelPFIsoDB < 0.1:
                    fill(histos[(region, 'pt20', 'mvaidiso01')], row)

    def finish(self):
        self.write_histos()
