'''

Analysis class for selecting the numerator and denominators
for the e-fake rate in Z->mu mu events.

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
    meta.electronDZ < 0.2,
]

variables = [
    ('Zmass', 'Mass of Z muons', 60, 60, 120),
    ('electronJetPt', 'Electron Jet Pt', 60, 60, 120),
    ('electronPt', 'Electron Pt', 60, 60, 120),
]

class FakeRatesMME(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMME, self).__init__(tree, output, **kwargs)
        for var in variables:
            self.book('zmm/pass', *var)
            self.book('zmm/all', *var)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        for selection in base_selections:
            if not selection(tree):
                return True
        histograms = self.histograms

        histograms['zmm/all/Zmass'].Fill(tree.muon1_muon2_Mass)
        histograms['zmm/all/electronJetPt'].Fill(tree.electronJetPt)
        histograms['zmm/all/electronPt'].Fill(tree.electronPt)

        if tree.electronMITID > 0.5 and tree.electronRelPFIsoDB < 0.3:
            histograms['zmm/pass/Zmass'].Fill(tree.muon1_muon2_Mass)
            histograms['zmm/pass/electronJetPt'].Fill(tree.electronJetPt)
            histograms['zmm/pass/electronPt'].Fill(tree.electronPt)

        return True

    def finish(self):
        self.write_histos()
