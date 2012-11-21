import ROOT

import os

from FinalStateAnalysis.PlotTools.megautil import MetaTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.muon1Pt > 20,
    meta.muon2Pt > 10,

    meta.tauDecayFinding > 0.5,
    meta.tauPt > 20,

    #meta.mu17ele8 > 0.5,
    meta.tauAbsEta < 2.3,
    meta.muon1AbsEta < 2.1,
    meta.muon2AbsEta < 2.1,

    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    meta.muon1PixHits > 0,
    meta.muon2PixHits > 0,
    meta.muon1JetBtag < 3.3,
    meta.muon2JetBtag < 3.3,

    meta.muon2DZ < 0.2,
    meta.muon1DZ < 0.2,
    meta.tauDZ < 0.2,

    meta.tauJetBtag < 3.3,
    meta.tauAntiElectronMVA > 0.5,
    meta.tauAntiElectronMedium > 0.5,
    meta.tauElecOverlap < 0.5,
    meta.tauAntiMuonTight > 0.5,
    meta.tauMuOverlap < 0.5,
]


hadronic_tau_id = [
    meta.tauLooseIso > 0.5,
]

muon2_id = [
    meta.muon2RelPFIsoDB < 0.3,
    meta.muon2WWID > 0.5,
]

muon1_id = [
    meta.muon1RelPFIsoDB < 0.3,
    meta.muon1WWID > 0.5,
]

histograms = [
    (lambda x: x.muon1Pt, 'muon1Pt', 'muon1 pt', 100, 0, 100),
    (lambda x: x.muon1AbsEta, 'muon1AbsEta', 'muon1 |#eta|', 100, 0, 100),
]

def muon1_fake_weight(x):
    return 1
def muon2_fake_weight(x):
    return 1

class AnalyzeMMT(MegaBase):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeMMT, self).__init__(tree, output, **kwargs)
        for histogram in histograms:
            self.book('muon1_fakes', *histogram[1:])
            self.book('muon2_fakes', *histogram[1:])
            self.book('double_fakes', *histogram[1:])
            self.book('triple_fakes', *histogram[1:])
            # Histograms w/o weights
            self.book('muon1_fakes_nowt', *histogram[1:])
            self.book('muon2_fakes_nowt', *histogram[1:])
            self.book('double_fakes_nowt', *histogram[1:])
            self.book('triple_fakes_nowt', *histogram[1:])
            self.book('final', *histogram[1:])
        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)

        # Check if we pass the base selection
        if not all(select(tree) for select in base_selections):
            return True

        # figure out which objects pass
        passes_tau_id = all(select(tree) for select in hadronic_tau_id)
        passes_muon1_id = all(select(tree) for select in muon1_id)
        passes_muon2_id = all(select(tree) for select in muon2_id)

        category = (passes_muon1_id, passes_muon2_id, passes_tau_id)

        if category == (True, True, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[os.path.join('final', histo[1])].Fill(value)
        elif category == (False, True, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('muon1_fakes_nowt', histo[1])].Fill(value)
                weight = muon1_fake_weight(tree.muon1Pt)
                self.histograms[
                    os.path.join('muon1_fakes', histo[1])].Fill(value, weight)
        elif category == (True, False, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('muon2_fakes_nowt', histo[1])].Fill(value)
                weight = muon2_fake_weight(tree.muon2Pt)
                self.histograms[
                    os.path.join('muon2_fakes', histo[1])].Fill(value, weight)
        elif category == (False, False, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('double_fakes_nowt', histo[1])].Fill(value)
                weight = muon2_fake_weight(tree.muon2Pt)*muon1_fake_weight(tree.muon1Pt)
                self.histograms[
                    os.path.join('double_fakes', histo[1])].Fill(value, weight)

        return True

    def finish(self):
        self.write_histos()
