import ROOT

import os

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.muon1Pt > 20,
    meta.muon2Pt > 10,

    meta.muon1AbsEta < 2.1,
    meta.muon2AbsEta < 2.1,

    meta.muon1WWID > 0.5,
    meta.muon2WWID > 0.5,

    #meta.muVetoPt5 < 1,
    #meta.eVetoWP95Iso < 1,
    #meta.bjetVeto < 1,
    #meta.tauVetoPt20 < 1,
    meta.muon1_muon2_SS < 0.5,

    meta.muon2DZ < 0.2,
    meta.muon1DZ < 0.2,
]

class ZMuMuControl(MegaBase):

    def __init__(self, tree, output, **kwargs):
        super(ZMuMuControl, self).__init__(tree, output, **kwargs)
        self.book('plots', 'muon1RelIso', "Muon 1 Rel. Iso after mass cut", 100, 0, 100)
        self.book('plots', 'muon2RelIso', "Muon 1 Rel. Iso after mass cut", 100, 0, 100)
        self.book('plots', 'zMass', "Dimuon mass", 200, 0, 200)
        self.book('plots', 'zMassFinal', "Dimuon mass after all cuts", 200, 0, 200)
        self.book('plots', 'rhoBeforeIso', "Rho (before muon isolation)", 50, 0, 50)
        self.book('plots', 'nvtxBeforeIso',
                  "Number Reco. Vertices (before muon isolation)",
                  40, -0.5, 39.5)
        self.book('plots', 'rhoAfterIso', "Rho (after muon isolation)", 50, 0, 50)
        self.book('plots', 'nvtxAfterIso',
                  "Number Reco. Vertices (after muon isolation)",
                  40, -0.5, 39.5)
        self.book('plots', 'muon1Pt', "Muon 1 Pt", 100, 0, 100)
        self.book('plots', 'muon2Pt', "Muon 2 Pt", 100, 0, 100)
        self.book('plots', 'muon1Eta', "Muon 1 Eta", 100, -2.5, 2.5)
        self.book('plots', 'muon2Eta', "Muon 2 Eta", 100, -2.5, 2.5)

        self.disable_branch('*')

        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('muon1Pt')
        self.enable_branch('muon2Pt')
        self.enable_branch('muon1Eta')
        self.enable_branch('muon2Eta')
        self.enable_branch('muon1RelPFIsoDB')
        self.enable_branch('muon2RelPFIsoDB')
        self.enable_branch('muon1_muon2_SS')
        self.enable_branch('rho')
        self.enable_branch('nvtx')
        self.enable_branch('muon1_muon2_Mass')
        self.enable_branch('metEt')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)

        # Check if we pass the base selection
        if not all(select(tree) for select in base_selections):
            return True

        histograms = self.histograms
        #print self.histograms.keys()
        histograms['plots/zMass'].Fill(tree.muon1_muon2_Mass)

        if tree.muon1_muon2_Mass < 80 or tree.muon1_muon2_Mass > 100:
            return True

        histograms['plots/rhoBeforeIso'].Fill(tree.rho)
        histograms['plots/nvtxBeforeIso'].Fill(tree.nvtx)


        histograms['plots/muon1RelIso'].Fill(tree.muon1RelPFIsoDB)
        histograms['plots/muon2RelIso'].Fill(tree.muon2RelPFIsoDB)

        if tree.muon1RelPFIsoDB < 0.2:
            return True

        if tree.muon2RelPFIsoDB < 0.2:
            return True

        histograms['plots/rhoAfterIso'].Fill(tree.rho)
        histograms['plots/nvtxAfterIso'].Fill(tree.nvtx)

        histograms['plots/muon1Pt'].Fill(tree.muon1Pt)
        histograms['plots/muon2Pt'].Fill(tree.muon2Pt)
        histograms['plots/muon1Eta'].Fill(tree.muon1Eta)
        histograms['plots/muon2Eta'].Fill(tree.muon2Eta)

        histograms['plots/zMassFinal'].Fill(tree.muon1_muon2_Mass)

        return True

    def finish(self):
        self.write_histos()
