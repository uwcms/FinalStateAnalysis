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
        base_selection = ' && '.join([
            'doubleEPass',
            'e1Pt > 20',
            'e1MVAIDH2TauWP',
            'e2Pt > 10',
            'e1AbsEta < 2.5',
            'e2AbsEta < 2.5',
            'e1JetBtag < 3.3',
            'e2JetBtag < 3.3',

            'e1ChargeIdTight',
            'e2ChargeIdTight',

            # NEEDS E VETO!
            '!muVetoPt5',
            '!bjetCSVVeto',
            '!tauVetoPt20',
            '!e2HasConversion',
            '!e2MissingHits',
            '!e1HasConversion',
            '!e1MissingHits',

            'abs(e1DZ) < 0.2',
            'abs(e2DZ) < 0.2',
        ])

        def fill(the_histos, row):
            the_histos['e2Pt'].Fill(row.e2Pt)
            the_histos['e2JetPt'].Fill(row.e2JetPt)
            the_histos['e2AbsEta'].Fill(row.e2AbsEta)
            the_histos['metSignificance'].Fill(row.metSignificance)
            the_histos['e1MtToMET'].Fill(row.e1MtToMET)
            the_histos['e1e2Mass'].Fill(row.e1_e2_Mass)
            the_histos['doubleEPrescale'].Fill(row.doubleEPrescale)

        histos = self.histograms
        for row in self.tree.where(base_selection):
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
