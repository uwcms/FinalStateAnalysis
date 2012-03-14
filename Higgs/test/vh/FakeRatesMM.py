'''

Analysis class for selecting the numerator and denominators
for the mu-fake rate in W->mu nu and QCD (anti-iso mu events)

'''

import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    #meta.doublemu > 0.5,
    meta.muon1Pt > 20,
    meta.muon2Pt > 10,
    meta.muon1WWID > 0.5,

    meta.muon1_muon2_SS > 0.5,

    # Make sure we only get one candidate per event
    # we measure the subleading muon
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
]

# Selections to get Wjets
wselections = [
    meta.muon1RelPFIsoDB < 0.15,
    meta.muon1MtToMET > 40,
]

qcdselections = [
    meta.muon1RelPFIsoDB > 0.3,
    meta.metEt < 20,
]

variables = [
    ('muonJetPt', 'Mu Jet Pt', 60, 60, 120),
    ('muonPt', 'Mu Pt', 60, 60, 120),
]

class FakeRatesMM(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMM, self).__init__(tree, output, **kwargs)
        for var in variables:
            self.book('wjets/pass', *var)
            self.book('wjets/all', *var)
            self.book('qcd/pass', *var)
            self.book('qcd/all', *var)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        if not all(selection(tree) for selection in base_selections):
            return True

        histograms = self.histograms

        passes_muid = tree.muon2WWID > 0.5 and tree.muon2RelPFIsoDB < 0.3

        if all(selection(tree) for selection in wselections):
            histograms['wjets/all/muonJetPt'].Fill(tree.muon2JetPt)
            histograms['wjets/all/muonPt'].Fill(tree.muon2Pt)
            if passes_muid:
                histograms['wjets/all/muonJetPt'].Fill(tree.muon2JetPt)
                histograms['wjets/all/muonPt'].Fill(tree.muon2Pt)

        if all(selection(tree) for selection in qcdselections):
            histograms['qcd/all/muonJetPt'].Fill(tree.muon2JetPt)
            histograms['qcd/all/muonPt'].Fill(tree.muon2Pt)
            if passes_muid:
                histograms['qcd/all/muonJetPt'].Fill(tree.muon2JetPt)
                histograms['qcd/all/muonPt'].Fill(tree.muon2Pt)

        return True

    def finish(self):
        self.write_histos()
