'''

Analysis class for selecting the numerator and denominators
for the mu-fake rate in Z->mu mu events.

'''

import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree

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

class FakeRatesMMM(object):
    def __init__(self, tree, output, **kwargs):
        self.tree = tree
        self.output = output
        self.opts = kwargs
        self.output.cd()
        self.histo = ROOT.TH1F("adsf", "adsf", 100, 0, 100)
        self.histo.SetDirectory(self.output)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        for selection in base_selections:
            if not selection(tree):
                return True

        self.histo.Fill(tree.muon1_muon2_Mass)

        return True
    def finish(self):
        self.histo.Write()
