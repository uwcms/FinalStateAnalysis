'''

Analysis class for selecting the numerator and denominators
for the e-fake rate in W->mu nu and QCD (anti-iso mu events)

'''

import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    #meta.mu17ele8 > 0.5,
    meta.muonPt > 25,
    meta.muonWWID > 0.5,
    meta.electron_muon_SS > 0.5,

    meta.muonAbsEta < 2.1,

    # Make sure this isn't a ZZ event
    meta.muGlbIsoVetoPt10 < 0.5,
    meta.eVetoCicTightIso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # Make sure they all come from the same vertex
    meta.muonDZ < 0.2,
    meta.electronDZ < 0.2,
]

# Selections to get Wjets
wselections = [
    meta.muonRelPFIsoDB < 0.15,
    #meta.muonMtToMET > 40,
]

qcdselections = [
    meta.muonRelPFIsoDB > 0.3,
    meta.metEt < 20,
]

variables = [
    ('electronJetPt', 'Electron Jet Pt', 60, 60, 120),
    ('electronPt', 'Electron Pt', 60, 60, 120),
]


class FakeRatesME(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesME, self).__init__(tree, output, **kwargs)
        for var in variables:
            for pt in ['pt10', 'pt20']:
                for id_type = ['cic_iso15', 'mit_iso15']:
                    self.book('wjets/%s/%s/pass', *var)
                    self.book('wjets/%s/all', *var)
                    self.book('qcd/%s/%s/pass', *var)
                    self.book('qcd/%s/%s/all', *var)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        if not all(selection(tree) for selection in base_selections):
            return True

        histograms = self.histograms

        passes_eid = tree.electronMITID > 0.5 and tree.electronRelPFIsoDB < 0.3

        if all(selection(tree) for selection in wselections):
            histograms['wjets/all/electronJetPt'].Fill(tree.electronJetPt)
            histograms['wjets/all/electronPt'].Fill(tree.electronPt)
            if passes_eid:
                histograms['wjets/all/electronJetPt'].Fill(tree.electronJetPt)
                histograms['wjets/all/electronPt'].Fill(tree.electronPt)

        if all(selection(tree) for selection in qcdselections):
            histograms['qcd/all/electronJetPt'].Fill(tree.electronJetPt)
            histograms['qcd/all/electronPt'].Fill(tree.electronPt)
            if passes_eid:
                histograms['qcd/all/electronJetPt'].Fill(tree.electronJetPt)
                histograms['qcd/all/electronPt'].Fill(tree.electronPt)

        return True

    def finish(self):
        self.write_histos()
