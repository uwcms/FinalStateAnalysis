'''

Analysis class for selecting the numerator and denominators
for the mu-fake rate in W->mu nu and QCD (anti-iso mu events)

'''

import ROOT

from FinalStateAnalysis.PlotTools.megautil import MetaTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.muon1_muon2_SS > 0.5,

    # Muon 2 is the leading muon as defined in the ntuple production.
    meta.doubleMuPass > 0.5,
    meta.muon1Pt > 10,
    meta.muon2Pt > 20,
    meta.muon2WWID > 0.5,

    # Make sure we only get one candidate per event
    # we measure the subleading muon
    meta.muon1Pt < meta.muon2Pt,

    meta.muon1AbsEta < 2.1,
    meta.muon2AbsEta < 2.1,

    # Make sure this isn't a ZZ event
    meta.muGlbIsoVetoPt10 < 0.5,
    meta.eVetoCicTightIso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # Make sure they all come from the same vertex
    meta.muon1DZ < 0.2,
    meta.muon2DZ < 0.2,
]

# Selections to get Wjets
wselections = [
    meta.muon2RelPFIsoDB < 0.15,
    meta.muon2MtToMET > 50,
]

qcdselections = [
    meta.muon2RelPFIsoDB > 0.3,
    meta.metEt < 20,
]

variables = [
    ('muonJetPt', 'Mu Jet Pt', 50, 0, 200),
    ('muonPt', 'Mu Pt', 50, 0, 200),
]

probe_pt_cuts = [('pt10', 10), ('pt20', 20)]
probe_iso_cuts = [('iso15', 0.15), ('iso30', 0.30)]

class FakeRatesMM(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(FakeRatesMM, self).__init__(tree, output, **kwargs)
        for var in variables:
            for pt, _ in probe_pt_cuts:
                self.book('wjets/%s/denominator/' % (pt), *var)
                self.book('qcd/%s/denominator/' % (pt), *var)
                for iso, _ in probe_iso_cuts:
                    self.book('wjets/%s/%s/' % (pt, iso), *var)
                    self.book('qcd/%s/%s/' % (pt, iso), *var)
        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('muon1WWID')
        self.enable_branch('muon1RelPFIsoDB')
        self.enable_branch('muon1Pt')
        self.enable_branch('muon1JetPt')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        if not all(selection(tree) for selection in base_selections):
            return True

        histograms = self.histograms

        passes_wjets = all(selection(tree) for selection in wselections)
        passes_qcd = all(selection(tree) for selection in qcdselections)
        jetpt = tree.muon1JetPt
        pt = tree.muon1Pt
        pt10 = pt > 10
        pt20 = pt > 20
        wwid = tree.muon1WWID > 0.5

        # Fill histograms.  There is a lot of copy paste, but I'm not sure how
        # else to do it in a performant way
        if passes_wjets:
            if pt10:
                histograms['wjets/pt10/denominator/muonJetPt'].Fill(jetpt)
                histograms['wjets/pt10/denominator/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.15:
                    histograms['wjets/pt10/iso15/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt10/iso15/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.3:
                    histograms['wjets/pt10/iso30/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt10/iso30/muonPt'].Fill(pt)
            if pt20:
                histograms['wjets/pt20/denominator/muonJetPt'].Fill(jetpt)
                histograms['wjets/pt20/denominator/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.15:
                    histograms['wjets/pt20/iso15/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt20/iso15/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.3:
                    histograms['wjets/pt20/iso30/muonJetPt'].Fill(jetpt)
                    histograms['wjets/pt20/iso30/muonPt'].Fill(pt)

        if passes_qcd:
            if pt10:
                histograms['qcd/pt10/denominator/muonJetPt'].Fill(jetpt)
                histograms['qcd/pt10/denominator/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.15:
                    histograms['qcd/pt10/iso15/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt10/iso15/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.3:
                    histograms['qcd/pt10/iso30/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt10/iso30/muonPt'].Fill(pt)
            if pt20:
                histograms['qcd/pt20/denominator/muonJetPt'].Fill(jetpt)
                histograms['qcd/pt20/denominator/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.15:
                    histograms['qcd/pt20/iso15/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt20/iso15/muonPt'].Fill(pt)
                if wwid and tree.muon1RelPFIsoDB < 0.3:
                    histograms['qcd/pt20/iso30/muonJetPt'].Fill(jetpt)
                    histograms['qcd/pt20/iso30/muonPt'].Fill(pt)

        return True

    def finish(self):
        self.write_histos()
