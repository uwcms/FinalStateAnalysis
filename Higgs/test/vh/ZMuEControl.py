import ROOT

import os

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.muonPt > 20,
    meta.electronPt > 10,

    meta.muonAbsEta < 2.1,
    meta.electronAbsEta < 2.5,

    meta.muonWWID > 0.5,
    meta.electronMITID > 0.5,

    #meta.muGlbIsoVetoPt10 < 1,
    #meta.eVetoCicTightIso < 1,
    #meta.bjetVeto < 1,
    #meta.tauVetoPt20 < 1,
    meta.muon_electron_SS < 0.5,

    meta.muonDZ < 0.2,
    meta.electronDZ < 0.2,
]

class ZMuEControl(MegaBase):

    def __init__(self, tree, output, **kwargs):
        super(ZMuEControl, self).__init__(tree, output, **kwargs)
        self.book('plots', 'muonRelIso', "Muon 1 Rel. Iso after mass cut", 100, 0, 100)
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
        self.book('plots', 'muonPt', "Muon 1 Pt", 100, 0, 100)
        self.book('plots', 'muon2Pt', "Muon 2 Pt", 100, 0, 100)
        self.book('plots', 'muonEta', "Muon 1 Eta", 100, -2.5, 2.5)
        self.book('plots', 'muon2Eta', "Muon 2 Eta", 100, -2.5, 2.5)

        self.disable_branch('*')

        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('muonPt')
        self.enable_branch('muon2Pt')
        self.enable_branch('muonEta')
        self.enable_branch('muon2Eta')
        self.enable_branch('muonRelPFIsoDB')
        self.enable_branch('muon2RelPFIsoDB')
        self.enable_branch('muon_muon2_SS')
        self.enable_branch('rho')
        self.enable_branch('nvtx')
        self.enable_branch('muon_muon2_Mass')
        self.enable_branch('metEt')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)

        # Check if we pass the base selection
        if not all(select(tree) for select in base_selections):
            return True

        histograms = self.histograms
        #print self.histograms.keys()
        histograms['plots/zMass'].Fill(tree.muon_muon2_Mass)

        if tree.muon_muon2_Mass > 80 or tree.muon_muon2_Mass < 100:
            return True

        histograms['plots/rhoBeforeIso'].Fill(tree.rho)
        histograms['plots/nvtxBeforeIso'].Fill(tree.ntvtx)


        histograms['plots/muonRelIso'].Fill(tree.muonRelPFIsoDB)
        histograms['plots/muon2RelIso'].Fill(tree.muon2RelPFIsoDB)

        if tree.muonRelPFIsoDB < 0.2:
            return True

        if tree.muon2RelPFIsoDB < 0.2:
            return True

        histograms['plots/rhoAfterIso'].Fill(tree.rho)
        histograms['plots/nvtxAfterIso'].Fill(tree.ntvtx)

        histograms['plots/muonPt'].Fill(tree.muonPt)
        histograms['plots/muon2Pt'].Fill(tree.muon2Pt)
        histograms['plots/muonEta'].Fill(tree.muonEta)
        histograms['plots/muon2Eta'].Fill(tree.muon2Eta)

        histograms['plots/zMassFinal'].Fill(tree.muon_muon2_Mass)

        return True

    def finish(self):
        self.write_histos()
