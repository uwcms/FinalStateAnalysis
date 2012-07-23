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
    if row.mRelPFIsoDB < 0.15 and row.mMtToMET > 40 and row.eMtToMET < 30:
        return 'wjets'
    elif row.mRelPFIsoDB > 0.3 and row.metSignificance < 3:
        return 'qcd'
    else:
        return None

class FakeRatesEM(MegaBase):
    tree = 'em/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(FakeRatesEM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = EMuTree.EMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}
        self.is7TeV = '7TeV' in os.environ['jobid']

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

                    book_histo('ePt', 'e Pt', 100, 0, 100)
                    book_histo('eJetPt', 'e Jet Pt', 100, 0, 100)
                    book_histo('eAbsEta', 'e Abs Eta', 100, -2.5, 2.5)
                    book_histo('metSignificance', 'MET sig.', 100, 0, 10)
                    book_histo('mMtToMET', 'm MT', 100, 0, 200)

    def process(self):

        def preselection(row):
            if not row.mu17ele8Pass: return False
            if not row.e_m_SS: return False
            if not row.mPt > 20: return False
            if not row.ePt > 10: return False
            if not row.mAbsEta < 2.4: return False
            if not row.eAbsEta < 2.5: return False
            if row.muVetoPt5: return False
            if row.bjetCSVVeto: return False
            if row.eVetoCicTightIso: return False
            if not row.eChargeIdTight: return False
            if row.tauVetoPt20: return False
            if row.eHasConversion: return False
            if row.eMissingHits: return False
            if not abs(row.mDZ) < 0.2: return False
            if not abs(row.eDZ) < 0.2: return False
            return True
        #if self.is7TeV:
            #base_selection = 'mu17ele8Pass && ' + base_selection

        def fill(the_histos, row):
            the_histos['ePt'].Fill(row.ePt)
            the_histos['eJetPt'].Fill(row.eJetPt)
            the_histos['eAbsEta'].Fill(row.eAbsEta)
            the_histos['metSignificance'].Fill(row.metSignificance)
            the_histos['mMtToMET'].Fill(row.mMtToMET)

        histos = self.histograms
        for row in self.tree:
            if not preselection(row):
                continue
            region = control_region(row)
            if region is None:
                continue
            # This is a QCD or Wjets
            fill(histos[(region, 'pt10')], row)

            if row.eMVAIDH2TauWP:
                fill(histos[(region, 'pt10', 'mvaid')], row)

            if row.eRelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'iso03')], row)

            if row.eMVAIDH2TauWP and row.eRelPFIsoDB < 0.3:
                fill(histos[(region, 'pt10', 'mvaidiso03')], row)

            if row.eMVAIDH2TauWP and row.eRelPFIsoDB < 0.1:
                fill(histos[(region, 'pt10', 'mvaidiso01')], row)

    def finish(self):
        self.write_histos()
