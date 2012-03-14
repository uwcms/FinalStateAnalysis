import ROOT

import os

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.muonPt > 20,
    meta.electronPt > 10,
    meta.tauDecayFinding > 0.5,
    meta.tauPt > 20,
    #meta.mu17ele8 > 0.5,
    meta.tauAbsEta < 2.3,
    meta.muonAbsEta < 2.1,
    meta.electronAbsEta < 2.5,

    meta.electronMuOverlap < 1,
    meta.muVetoPt5 < 1,
    meta.eVetoWP95Iso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    meta.muonPixHits > 0,
    meta.electronJetBtag < 3.3,
    meta.muonJetBtag < 3.3,

    meta.electronMissingHits < 1,
    meta.electronHasConversion < 1,

    meta.electronDZ < 0.2,
    meta.muonDZ < 0.2,
    meta.tauDZ < 0.2,

    meta.tauJetBtag < 3.3,
    meta.tauAntiElectronMedium > 0.5,
    meta.tauAntiElectronMVA > 0.5,
    meta.tauElecOverlap < 0.5,
    meta.tauAntiMuonTight > 0.5,
    meta.tauMuOverlap < 0.5,
]


hadronic_tau_id = [
    meta.tauLooseIso > 0.5,
]

e_id = [
    meta.electronRelIso < 0.3,
    meta.electronMITID > 0.5,
]

mu_id = [
    meta.muonRelPFIsoDB < 0.3,
    meta.muonWWID > 0.5,
]

histograms = [
    (lambda x: x.muonPt, 'muonPt', 'Muon pt', 100, 0, 100),
    (lambda x: x.muonAbsEta, 'muonAbsEta', 'Muon |#eta|', 100, 0, 100),
]

def muon_fake_weight(x):
    return 1
def electron_fake_weight(x):
    return 1

class AnalyzeEMT(MegaBase):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeEMT, self).__init__(tree, output, **kwargs)
        for histogram in histograms:
            self.book('muon_fakes', *histogram[1:])
            self.book('electron_fakes', *histogram[1:])
            self.book('double_fakes', *histogram[1:])
            self.book('triple_fakes', *histogram[1:])
            # Histograms w/o weights
            self.book('muon_fakes_nowt', *histogram[1:])
            self.book('electron_fakes_nowt', *histogram[1:])
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
        passes_mu_id = all(select(tree) for select in mu_id)
        passes_e_id = all(select(tree) for select in e_id)

        category = (passes_mu_id, passes_e_id, passes_tau_id)

        if category == (True, True, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[os.path.join('final', histo[1])].Fill(value)
        elif category == (False, True, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('muon_fakes_nowt', histo[1])].Fill(value)
                weight = muon_fake_weight(tree.muonPt)
                self.histograms[
                    os.path.join('muon_fakes', histo[1])].Fill(value, weight)
        elif category == (True, False, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('electron_fakes_nowt', histo[1])].Fill(value)
                weight = electron_fake_weight(tree.electronPt)
                self.histograms[
                    os.path.join('electron_fakes', histo[1])].Fill(value, weight)
        elif category == (False, False, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('double_fakes_nowt', histo[1])].Fill(value)
                weight = electron_fake_weight(tree.electronPt)*muon_fake_weight(tree.muonPt)
                self.histograms[
                    os.path.join('double_fakes', histo[1])].Fill(value, weight)

        return True

    def finish(self):
        self.write_histos()
