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
    meta.m1Pt > 20,
    meta.m2Pt > 10,
    meta.m1RelPFIsoDB < 0.15,
    meta.m2RelPFIsoDB < 0.15,
    meta.m1WWID > 0.5,
    meta.m2WWID > 0.5,
    meta.tPt > 20,

    meta.m3_t_SS > 0.5,

    # Now require that the first two muons make the best Z
    meta.m1_m2_Zcompat < meta.m1_m3_Zcompat,
    meta.m1_m2_Zcompat < meta.m2_m3_Zcompat,

    # Make sure the muons are within 10 GeV of the Z
    meta.m1_m2_Zcompat < 10,

    # Make sure we only get one candidate per event
    meta.m1Pt > meta.m2Pt,

    meta.m3MtToMET < 30,

    meta.m3PixHits > 0.5,

    meta.m1AbsEta < 2.1,
    meta.m2AbsEta < 2.1,
    meta.m3AbsEta < 2.1,

    # Make sure this isn't a ZZ event
    meta.muVetoPt5 < 0.5,
    meta.eVetoWP95Iso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # Make sure they all come from the same vertex
    meta.m1DZ < 0.2,
    meta.m2DZ < 0.2,
    meta.m3DZ < 0.2,
    meta.tDZ < 0.2,
]

variables = [
    ('Zmass', 'Mass of Z muons', 60, 60, 120),
    ('muonJetPt', 'Mu Jet Pt', 200, 0, 200),
    ('muonPt', 'Mu Pt', 200, 0, 200),
]

probe_pt_cuts = [('pt10', 10), ('pt20', 20)]
probe_iso_cuts = [('iso15', 0.15), ('iso30', 0.30)]

class FakeRatesMMMT(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMMMT, self).__init__(tree, output, **kwargs)
        for var in variables:
            for pt, _ in probe_pt_cuts:
                for iso, _ in probe_iso_cuts:
                    self.book('zmm_tau20/%s/%s/all' % (pt, iso), *var)
                    self.book('zmm_tau20/%s/%s/pass' % (pt, iso), *var)
        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('m3WWID')
        self.enable_branch('m3RelPFIsoDB')
        self.enable_branch('m3Pt')
        self.enable_branch('m3JetPt')
        self.enable_branch('m1_m2_Mass')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        for selection in base_selections:
            if not selection(tree):
                return True
        histograms = self.histograms

        jetpt = tree.m3JetPt
        pt = tree.m3Pt
        pt10 = pt > 10
        pt20 = pt > 20
        wwid = tree.m3WWID > 0.5

        if pt10:
            histograms['zmm_tau20/pt10/iso15/all/muonJetPt'].Fill(jetpt)
            histograms['zmm_tau20/pt10/iso15/all/muonPt'].Fill(pt)
            histograms['zmm_tau20/pt10/iso30/all/muonJetPt'].Fill(jetpt)
            histograms['zmm_tau20/pt10/iso30/all/muonPt'].Fill(pt)
            if wwid and tree.m3RelPFIsoDB < 0.15:
                histograms['zmm_tau20/pt10/iso15/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm_tau20/pt10/iso15/pass/muonPt'].Fill(pt)
            if wwid and tree.m3RelPFIsoDB < 0.3:
                histograms['zmm_tau20/pt10/iso30/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm_tau20/pt10/iso30/pass/muonPt'].Fill(pt)
        if pt20:
            histograms['zmm_tau20/pt20/iso15/all/muonJetPt'].Fill(jetpt)
            histograms['zmm_tau20/pt20/iso15/all/muonPt'].Fill(pt)
            histograms['zmm_tau20/pt20/iso30/all/muonJetPt'].Fill(jetpt)
            histograms['zmm_tau20/pt20/iso30/all/muonPt'].Fill(pt)
            if wwid and tree.m3RelPFIsoDB < 0.15:
                histograms['zmm_tau20/pt20/iso15/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm_tau20/pt20/iso15/pass/muonPt'].Fill(pt)
            if wwid and tree.m3RelPFIsoDB < 0.3:
                histograms['zmm_tau20/pt20/iso30/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm_tau20/pt20/iso30/pass/muonPt'].Fill(pt)

        return True

    def finish(self):
        self.write_histos()
