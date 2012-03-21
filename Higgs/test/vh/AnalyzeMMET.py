import ROOT

import os

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    # Require the Z candidate within 10 GeV of m_Z
    meta.m1_m2_Zcompat < 10,

    # Require that the Higgs cand is OS
    meta.e_t_SS < 0.5,

    # Order the Z muons by PT so we only have one candidate per event
    meta.m1Pt > meta.m2Pt,

    meta.e_t_Mass < 80,
    meta.e_t_Mass > 30,

    meta.m1Pt > 20,
    meta.m2Pt > 10,
    meta.ePt > 10,

    meta.m1RelPFIsoDB < 0.25,
    meta.m2RelPFIsoDB < 0.25,

    meta.tPt > 20,

    meta.m1WWID > 0,
    meta.m2WWID > 0,

    meta.tDecayFinding > 0.5,

    #meta.mu17ele8 > 0.5,
    meta.tAbsEta < 2.3,
    meta.m1AbsEta < 2.4,
    meta.m2AbsEta < 2.4,

    meta.muVetoPt5 < 1,
    meta.eVetoWP95Iso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    meta.m1DZ < 0.2,
    meta.m2DZ < 0.2,
    meta.eDZ < 0.2,
    meta.tDZ < 0.2,

    #meta.tJetBtag < 3.3,
    meta.tAntiElectronLoose > 0.5,
    #meta.tAntiElectronMedium > 0.5,
    meta.tElecOverlap < 0.5,
    meta.tAntiMuonTight > 0.5,
    meta.tMuOverlap < 0.5,
]


hadronic_tau_id = [
    meta.tLooseIso > 0.5,
]

e_id = [
    meta.eRelPFIsoDB < 0.15,
    meta.eWWID > 0.5,
]

histograms = [
    (lambda x: x.m1Pt, 'm1Pt', 'm1 pt', 100, 0, 100),
    (lambda x: x.m1AbsEta, 'm1AbsEta', 'm1 |#eta|', 100, 0, 100),
]

def e_fake_weight(x):
    return 1
def tau_fake_weight(x):
    return 1

class AnalyzeMMET(MegaBase):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeMMET, self).__init__(tree, output, **kwargs)
        for histogram in histograms:
            self.book('e_fakes', *histogram[1:])
            self.book('tau_fakes', *histogram[1:])
            self.book('double_fakes', *histogram[1:])
            # Histograms w/o weights
            self.book('e_fakes_nowt', *histogram[1:])
            self.book('tau_fakes_nowt', *histogram[1:])
            self.book('double_fakes_nowt', *histogram[1:])
            self.book('final', *histogram[1:])
        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('run')
        self.enable_branch('evt')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)

        # Check if we pass the base selection
        if not all(select(tree) for select in base_selections):
            return True

        # figure out which objects pass
        passes_tau_id = all(select(tree) for select in hadronic_tau_id)
        passes_e_id = all(select(tree) for select in e_id)

        category = (passes_e_id, passes_tau_id)

        if category == (True, True):
            print tree.run, tree.evt
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[os.path.join('final', histo[1])].Fill(value)
        elif category == (False, True):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('e_fakes_nowt', histo[1])].Fill(value)
                weight = e_fake_weight(tree.ePt)
                self.histograms[
                    os.path.join('e_fakes', histo[1])].Fill(value, weight)
        elif category == (True, False):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('tau_fakes_nowt', histo[1])].Fill(value)
                weight = tau_fake_weight(tree.tPt)
                self.histograms[
                    os.path.join('tau_fakes', histo[1])].Fill(value, weight)
        elif category == (False, False):
            for histo in histograms:
                value = histo[0](tree)
                self.histograms[
                    os.path.join('double_fakes_nowt', histo[1])].Fill(value)
                weight = e_fake_weight(tree.ePt)*tau_fake_weight(tree.tPt)
                self.histograms[
                    os.path.join('double_fakes', histo[1])].Fill(value, weight)

        return True

    def finish(self):
        self.write_histos()
