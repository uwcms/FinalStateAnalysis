import ROOT

import os

from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or

meta = MetaTree()

base_selections = And(
    # Pick the best Z candidate in the first two positions
    meta.m1_m2_Zcompat < meta.m1_m3_Zcompat,
    meta.m1_m2_Zcompat < meta.m2_m3_Zcompat,

    # Require the Z candidate within 10 GeV of m_Z
    meta.m1_m2_Zcompat < 10,

    # Require that the Higgs cand is OS
    meta.m3_t_SS < 0.5,

    # Order the Z muons by PT so we only have one candidate per event
    meta.m1Pt > meta.m2Pt,

    meta.m3_t_Mass < 80,
    meta.m3_t_Mass > 30,

    meta.m1Pt > 20,
    meta.m2Pt > 10,
    meta.m3Pt > 10,

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
    meta.m3DZ < 0.2,
    meta.tDZ < 0.2,

    #meta.tJetBtag < 3.3,
    meta.tAntiElectronLoose > 0.5,
    #meta.tAntiElectronMedium > 0.5,
    meta.tElecOverlap < 0.5,
    meta.tAntiMuonTight > 0.5,
    meta.tMuOverlap < 0.5,
)

hadronic_tau_id = meta.tLooseIso > 0.5

m3_id = And(
    meta.m3RelPFIsoDB < 0.15,
    meta.m3WWID > 0.5,
)

mt_cut = meta.m3MtToMET > 50

def unit_weight(x):
    return 1.

histograms = [
    (lambda x: x.m1Pt, unit_weight, '', ('m1Pt', 'm1 pt', 20, 0, 200)),
    (lambda x: x.m1AbsEta, unit_weight, '', ('m1AbsEta', 'm1 |#eta|', 10, 0, 2.5)),
]

class AnalyzeMMMT(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeMMMT, self).__init__(tree, output, **kwargs)

        self.define_region('base', base_selections, histograms)
        self.define_region('tau_pass',
                           base_selections & hadronic_tau_id & ~m3_id,
                           histograms)
        self.define_region('mu_pass',
                           base_selections & m3_id & ~hadronic_tau_id,
                           histograms)
        self.define_region('mu_pass_mt_pass',
                           base_selections & m3_id & ~hadronic_tau_id & mt_cut,
                           histograms)
        self.define_region('mu_pass_mt_fail',
                           base_selections & m3_id & ~hadronic_tau_id & ~mt_cut,
                           histograms)
        self.define_region('all_pass',
                           base_selections & m3_id & hadronic_tau_id,
                           histograms)
        self.define_region('none_pass',
                           base_selections & ~m3_id & ~hadronic_tau_id,
                           histograms)

        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('run')
        self.enable_branch('evt')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        self.analyze(tree)
        return True

    def finish(self):
        self.write_histos()
