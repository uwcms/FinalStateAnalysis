'''

Analysis class for selecting the numerator and denominators
for the mu-fake rate in Z->mu mu events.

'''

import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.doubleMuPass > 0.5,
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

    meta.muon3MtToMET < 30,

    # Make sure we only get one candidate per event
    meta.muon1Pt > meta.muon2Pt,

    meta.muon3PixHits > 0.5,

    meta.muon1AbsEta < 2.1,
    meta.muon2AbsEta < 2.1,
    meta.muon3AbsEta < 2.1,

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
    ('muonJetPt', 'Mu Jet Pt', 200, 0, 200),
    ('muonPt', 'Mu Pt', 200, 0, 200),
]

probe_pt_cuts = [('pt10', 10), ('pt20', 20)]
probe_iso_cuts = [('iso15', 0.15), ('iso30', 0.30)]

class FakeRatesMMM(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMMM, self).__init__(tree, output, **kwargs)
        for var in variables:
            for pt, _ in probe_pt_cuts:
                for iso, _ in probe_iso_cuts:
                    self.book('zmm/%s/%s/all' % (pt, iso), *var)
                    self.book('zmm/%s/%s/pass' % (pt, iso), *var)
        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('muon3WWID')
        self.enable_branch('muon3RelPFIsoDB')
        self.enable_branch('muon3Pt')
        self.enable_branch('muon3JetPt')
        self.enable_branch('muon1_muon2_Mass')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        for selection in base_selections:
            if not selection(tree):
                return True
        histograms = self.histograms

        jetpt = tree.muon3JetPt
        pt = tree.muon3Pt
        pt10 = pt > 10
        pt20 = pt > 20
        wwid = tree.muon3WWID > 0.5

        if pt10:
            histograms['zmm/pt10/iso15/all/muonJetPt'].Fill(jetpt)
            histograms['zmm/pt10/iso15/all/muonPt'].Fill(pt)
            histograms['zmm/pt10/iso30/all/muonJetPt'].Fill(jetpt)
            histograms['zmm/pt10/iso30/all/muonPt'].Fill(pt)
            if wwid and tree.muon3RelPFIsoDB < 0.15:
                histograms['zmm/pt10/iso15/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm/pt10/iso15/pass/muonPt'].Fill(pt)
            if wwid and tree.muon3RelPFIsoDB < 0.3:
                histograms['zmm/pt10/iso30/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm/pt10/iso30/pass/muonPt'].Fill(pt)
        if pt20:
            histograms['zmm/pt20/iso15/all/muonJetPt'].Fill(jetpt)
            histograms['zmm/pt20/iso15/all/muonPt'].Fill(pt)
            histograms['zmm/pt20/iso30/all/muonJetPt'].Fill(jetpt)
            histograms['zmm/pt20/iso30/all/muonPt'].Fill(pt)
            if wwid and tree.muon3RelPFIsoDB < 0.15:
                histograms['zmm/pt20/iso15/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm/pt20/iso15/pass/muonPt'].Fill(pt)
            if wwid and tree.muon3RelPFIsoDB < 0.3:
                histograms['zmm/pt20/iso30/pass/muonJetPt'].Fill(jetpt)
                histograms['zmm/pt20/iso30/pass/muonPt'].Fill(pt)

        return True

    def finish(self):
        self.write_histos()
