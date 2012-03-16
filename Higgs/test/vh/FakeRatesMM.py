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

probe_pt_cuts = [('pt10', 10), ('pt20', 20)]
probe_iso_cuts = [('iso15', 0.15), ('iso30', 0.30)]

class FakeRatesMM(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMM, self).__init__(tree, output, **kwargs)
        for var in variables:
            for pt, _ in probe_pt_cuts:
                for iso, _ in probe_iso_cuts:
                    self.book('wjets/%s/%s/all' % (pt, iso), *var)
                    self.book('wjets/%s/%s/pass' % (pt, iso), *var)
                    self.book('qcd/%s/%s/all' % (pt, iso), *var)
                    self.book('qcd/%s/%s/pass' % (pt, iso), *var)
        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('muon2WWID')
        self.enable_branch('muon2RelPFIsoDB')
        self.enable_branch('muon2Pt')
        self.enable_branch('muon2JetPt')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        if not all(selection(tree) for selection in base_selections):
            return True

        histograms = self.histograms

        passes_wjets = all(selection(tree) for selection in wselections)
        passes_qcd = all(selection(tree) for selection in qcdselections)
        jetpt = tree.muon2JetPt
        pt = tree.muon2Pt
        pt10 = pt > 10
        pt20 = pt > 20
        wwid = tree.muon2WWID > 0.5

        # Fill histograms.  There is a lot of copy paste, but I'm not sure how
        # else to do it in a performant way
        if passes_wjets:
            if pt10:
                histograms['wjets/pt10/iso15/all/muonJetPt'].Fill(jetpt)
                histograms['wjets/pt10/iso15/all/muonPt'].Fill(pt)
                histograms['wjets/pt10/iso30/all/muonJetPt'].Fill(jetpt)
                histograms['wjets/pt10/iso30/all/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.15:
                    histograms['wjets/pt10/iso15/pass/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt10/iso15/pass/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.3:
                    histograms['wjets/pt10/iso30/pass/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt10/iso30/pass/muonPt'].Fill(pt)
            if pt20:
                histograms['wjets/pt20/iso15/all/muonJetPt'].Fill(jetpt)
                histograms['wjets/pt20/iso15/all/muonPt'].Fill(pt)
                histograms['wjets/pt20/iso30/all/muonJetPt'].Fill(jetpt)
                histograms['wjets/pt20/iso30/all/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.15:
                    histograms['wjets/pt20/iso15/pass/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt20/iso15/pass/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.3:
                    histograms['wjets/pt20/iso30/pass/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt20/iso30/pass/muonPt'].Fill(pt)

        if passes_qcd:
            if pt10:
                histograms['qcd/pt10/iso15/all/muonJetPt'].Fill(jetpt)
                histograms['qcd/pt10/iso15/all/muonPt'].Fill(pt)
                histograms['qcd/pt10/iso30/all/muonJetPt'].Fill(jetpt)
                histograms['qcd/pt10/iso30/all/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.15:
                    histograms['qcd/pt10/iso15/pass/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt10/iso15/pass/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.3:
                    histograms['qcd/pt10/iso30/pass/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt10/iso30/pass/muonPt'].Fill(pt)
            if pt20:
                histograms['qcd/pt20/iso15/all/muonJetPt'].Fill(jetpt)
                histograms['qcd/pt20/iso15/all/muonPt'].Fill(pt)
                histograms['qcd/pt20/iso30/all/muonJetPt'].Fill(jetpt)
                histograms['qcd/pt20/iso30/all/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.15:
                    histograms['qcd/pt20/iso15/pass/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt20/iso15/pass/muonPt'].Fill(pt)
                if wwid and tree.muon2RelPFIsoDB < 0.3:
                    histograms['qcd/pt20/iso30/pass/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt20/iso30/pass/muonPt'].Fill(pt)

        return True

    def finish(self):
        self.write_histos()
