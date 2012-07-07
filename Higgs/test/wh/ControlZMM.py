'''

Make control plots of Z->mumu events.

Author: Evan K. Friis, UW

'''

import MuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import os

import ROOT
ROOT.gSystem.Load("Corrector_C")

class ControlZMM(MegaBase):
    tree = 'mm/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(ControlZMM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuMuTree.MuMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}
        self.is7TeV = '7TeV' in os.environ['jobid']

    def begin(self):
        self.book('zmm', "weight", "Event weight", 100, 0, 5)
        self.book('zmm', "weight_nopu", "Event weight without PU", 100, 0, 5)

        self.book('zmm', "rho", "Fastjet #rho", 100, 0, 25)
        self.book('zmm', "nvtx", "Number of vertices", 31, -0.5, 30.5)
        self.book('zmm', "prescale", "HLT prescale", 21, -0.5, 20.5)

        self.book('zmm', "m1Pt", "Muon 1 Pt", 100, 0, 100)
        self.book('zmm', "m2Pt", "Muon 2 Pt", 100, 0, 100)
        self.book('zmm', "m1AbsEta", "Muon 1 eta", 100, -2.5, 2.5)
        self.book('zmm', "m2AbsEta", "Muon 2 eta", 100, -2.5, 2.5)
        self.book('zmm', "m1m2Mass", "Muon 1-2 Mass", 120, 0, 120)

        self.book('zmm', 'm1PixHits', 'Mu 1 pix hits', 10, -0.5, 9.5)
        self.book('zmm', 'm2PixHits', 'Mu 2 pix hits', 10, -0.5, 9.5)

        self.book('zmm', 'm1JetBtag', 'Mu 1 JetBtag', 100, -5.5, 9.5)
        self.book('zmm', 'm2JetBtag', 'Mu 2 JetBtag', 100, -5.5, 9.5)

    def correction(self, row):
        weight = 1.0
        if row.run < 10:
            weight *= ROOT.Cor_Total_Mu_Lead(row.m1Pt, row.m1AbsEta)
            weight *= ROOT.Cor_Total_Mu_SubLead(row.m2Pt, row.m2AbsEta)
        return weight

    def pu_weight(self, row):
        #fixme
        return row.puWeightData2011AB

    def fill_histos(self, row):
        histos = self.histograms
        weight = self.correction(row)*self.pu_weight(row)
        histos['zmm/weight'].Fill(weight)
        histos['zmm/weight_nopu'].Fill(self.correction(row))
        histos['zmm/rho'].Fill(row.rho)
        histos['zmm/nvtx'].Fill(row.nvtx)
        histos['zmm/prescale'].Fill(row.doubleMuPrescale)
        histos['zmm/m1Pt'].Fill(row.m1Pt)
        histos['zmm/m2Pt'].Fill(row.m2Pt)
        histos['zmm/m1AbsEta'].Fill(row.m1AbsEta)
        histos['zmm/m2AbsEta'].Fill(row.m2AbsEta)
        histos['zmm/m1PixHits'].Fill(row.m1PixHits)
        histos['zmm/m2PixHits'].Fill(row.m2PixHits)
        histos['zmm/m1JetBtag'].Fill(row.m1JetBtag)
        histos['zmm/m2JetBtag'].Fill(row.m2JetBtag)
        histos['zmm/m1m2Mass'].Fill(row.m1_m2_Mass)

    def preselection(self, row):
        ''' Preselection applied to events.

        Excludes FR object IDs and sign cut.
        '''
        if not row.doubleMuPass:
            return False
        if row.m1Pt < 20:
            return False
        if row.m2Pt < 10:
            return False
        if row.m1AbsEta > 2.4:
            return False
        if row.m2AbsEta > 2.4:
            return False
        if row.muVetoPt5:
            return False
        if row.m1_m2_Mass < 20:
            return False

        if row.bjetCSVVeto:
            return False
        if row.tauVetoPt20:
            return False
        #if not row.m1PixHits:
            #return False
        #if not row.m2PixHits:
            #return False
        # Fixme use CSV
        #if row.m1JetBtag > 3.3:
            #return False
        #if row.m2JetBtag > 3.3:
            #return False
        if abs(row.m1DZ) > 0.2:
            return False
        if abs(row.m2DZ) > 0.2:
            return False

        return True

    def obj1_id(self, row):
        return bool(row.m1PFIDTight) and bool(row.m1RelPFIsoDB < 0.3)

    def obj2_id(self, row):
        return bool(row.m2PFIDTight) and bool(row.m2RelPFIsoDB < 0.3)

    def process(self):
        for row in self.tree:
            if not self.preselection(row):
                continue
            if not self.obj1_id(row) or not self.obj2_id(row):
                continue
            self.fill_histos(row)

    def finish(self):
        self.write_histos()
