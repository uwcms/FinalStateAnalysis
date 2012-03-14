'''

Analysis class for selecting the numerator and denominators
for the mu-fake rate in Z->mu mu events.

'''

import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    #meta.doublemu > 0.5,
    meta.muon1Pt > 20,
    meta.muon2Pt > 10,
    meta.muon1RelPFIsoDB < 0.15,
    meta.muon2RelPFIsoDB < 0.15,
    meta.muon1WWID > 0.5,
    meta.muon2WWID > 0.5,

    # Now require that the first two muons make the best Z
    meta.muon1_muon2_Zcompat < meta.muon1_muon3_Zcompat,
    meta.muon1_muon2_Zcompat < meta.muon2_muon3_Zcompat,

    # Make sure the muons are within 10 GeV of the Z
    meta.muon1_muon2_Zcompat < 10,

    # Make sure we only get one candidate per event
    meta.muon1Pt > meta.muon2Pt,

    meta.muon1AbsEta < 2.1,
    meta.muon2AbsEta < 2.1,

    # Make sure this isn't a ZZ event
    meta.muVetoPt5 < 0.5,
    meta.eVetoWP95Iso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # Make sure they all come from the same vertex
    meta.muon1DZ < 0.2,
    meta.muon2DZ < 0.2,
    meta.muon3DZ < 0.2,
]

variables = [
    ('Zmass', 'Mass of Z muons', 60, 60, 120),
    ('muonJetPt', 'Mu Jet Pt', 60, 60, 120),
    ('muonPt', 'Mu Pt', 60, 60, 120),
]

class FakeRatesMMM(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMMM, self).__init__(tree, output, **kwargs)
        for var in variables:
            self.book('pass', *var)
            self.book('all', *var)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        for selection in base_selections:
            if not selection(tree):
                return True
        histograms = self.histograms

        histograms['all/Zmass'].Fill(tree.muon1_muon2_Mass)
        histograms['all/muonJetPt'].Fill(tree.muon3JetPt)
        histograms['all/muonPt'].Fill(tree.muon3Pt)

        if tree.muon3WWID > 0.5 and tree.muon3RelPFIsoDB < 0.3:
            histograms['pass/Zmass'].Fill(tree.muon1_muon2_Mass)
            histograms['pass/muonJetPt'].Fill(tree.muon3JetPt)
            histograms['pass/muonPt'].Fill(tree.muon3Pt)

        return True

    def finish(self):
        self.write_histos()
