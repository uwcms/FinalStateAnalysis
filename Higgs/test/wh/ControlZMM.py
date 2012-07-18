'''

Make control plots of Z->mumu events.

Author: Evan K. Friis, UW

'''

import MuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import glob
import os
import FinalStateAnalysis.TagAndProbe.MuonPOGCorrections as MuonPOGCorrections
import FinalStateAnalysis.TagAndProbe.PileupWeight as PileupWeight
import ROOT

################################################################################
#### MC-DATA and PU corrections ################################################
################################################################################

# Determine MC-DATA corrections
is7TeV = bool('7TeV' in os.environ['jobid'])
print "Is 7TeV:", is7TeV

# Make PU corrector from expected data PU distribution
# PU corrections .root files from pileupCalc.py
pu_distributions = glob.glob(os.path.join(
    'inputs', os.environ['jobid'], 'data_DoubleMu*pu.root'))
pu_corrector = PileupWeight.PileupWeight(
    'S6' if is7TeV else 'S7', *pu_distributions)

muon_pog_PFTight_2011 = MuonPOGCorrections.make_muon_pog_PFTight_2011()
muon_pog_PFTight_2012 = MuonPOGCorrections.make_muon_pog_PFTight_2012()

muon_pog_PFRelIsoDB012_2011 = MuonPOGCorrections.make_muon_pog_PFRelIsoDB012_2011()
muon_pog_PFRelIsoDB012_2012 = MuonPOGCorrections.make_muon_pog_PFRelIsoDB012_2012()

muon_pog_Mu17Mu8_Mu17_2012 = MuonPOGCorrections.make_muon_pog_Mu17Mu8_Mu17_2012()
muon_pog_Mu17Mu8_Mu8_2012 = MuonPOGCorrections.make_muon_pog_Mu17Mu8_Mu8_2012()

# takes etas of muons
muon_pog_Mu17Mu8_2011 = MuonPOGCorrections.muon_pog_Mu17Mu8_eta_eta_2011

# Get object ID and trigger corrector functions
def mc_corrector_2011(row):
    if row.run > 2:
        return 1
    pu = pu_corrector(row.nTruePU)
    #pu = 1
    m1id = muon_pog_PFTight_2011(row.m1Pt, row.m1Eta)
    m2id = muon_pog_PFTight_2011(row.m2Pt, row.m2Eta)
    m1iso = muon_pog_PFRelIsoDB012_2011(row.m1Pt, row.m1Eta)
    m2iso = muon_pog_PFRelIsoDB012_2011(row.m2Pt, row.m2Eta)
    trigger = muon_pog_Mu17Mu8_2011(row.m1Eta, row.m2Eta)
    return pu*m1id*m2id*m1iso*m2iso*trigger

def mc_corrector_2012(row):
    if row.run > 2:
        return 1
    pu = pu_corrector(row.nTruePU)
    m1id = muon_pog_PFTight_2012(row.m1Pt, row.m1Eta)
    m2id = muon_pog_PFTight_2012(row.m2Pt, row.m2Eta)
    m1iso = muon_pog_PFRelIsoDB012_2012(row.m1Pt, row.m1Eta)
    m2iso = muon_pog_PFRelIsoDB012_2012(row.m2Pt, row.m2Eta)
    m1Trig = muon_pog_Mu17Mu8_Mu17_2012(row.m1Pt, row.m1Eta)
    m2Trig = muon_pog_Mu17Mu8_Mu8_2012(row.m2Pt, row.m2Eta)
    return pu*m1id*m2id*m1iso*m2iso*m1Trig*m2Trig

# Determine which set of corrections to use
mc_corrector = mc_corrector_2011
if not is7TeV:
    mc_corrector = mc_corrector_2012

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
        return mc_corrector(row)

    def fill_histos(self, row):
        histos = self.histograms
        weight = self.correction(row)
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
