'''

Make control plots of Z and ttbar -> emu events.

Author: Evan K. Friis, UW

'''

import EMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import glob
import os
import FinalStateAnalysis.TagAndProbe.MuonPOGCorrections as MuonPOGCorrections
import FinalStateAnalysis.TagAndProbe.H2TauCorrections as H2TauCorrections
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
    'inputs', os.environ['jobid'], 'data_MuEG*pu.root'))
pu_corrector = PileupWeight.PileupWeight(
    'S6' if is7TeV else 'S7', *pu_distributions)

muon_pog_PFTight_2011 = MuonPOGCorrections.make_muon_pog_PFTight_2011()
muon_pog_PFTight_2012 = MuonPOGCorrections.make_muon_pog_PFTight_2012()

muon_pog_PFRelIsoDB02_2011 = MuonPOGCorrections.make_muon_pog_PFRelIsoDB02_2011()
muon_pog_PFRelIsoDB02_2012 = MuonPOGCorrections.make_muon_pog_PFRelIsoDB02_2012()

# Get object ID and trigger corrector functions
def mc_corrector_2011(row):
    if row.run > 2:
        return 1
    pu = pu_corrector(row.nTruePU)
    #pu = 1
    m1id = muon_pog_PFTight_2011(row.mPt, row.mEta)
    m1iso = muon_pog_PFRelIsoDB02_2011(row.mPt, row.mEta)
    e2idiso = H2TauCorrections.correct_e_idiso_2011(row.ePt, row.eAbsEta)
    m_trg = H2TauCorrections.correct_mueg_mu_2011(row.mPt, row.mAbsEta)
    e_trg = H2TauCorrections.correct_mueg_e_2011(row.ePt, row.eAbsEta)
    return pu*m1id*m1iso*e2idiso*m_trg*e_trg

def mc_corrector_2012(row):
    if row.run > 2:
        return 1
    pu = pu_corrector(row.nTruePU)
    m1id = muon_pog_PFTight_2012(row.mPt, row.mEta)
    m1iso = muon_pog_PFRelIsoDB02_2012(row.mPt, row.mEta)
    e2idiso = H2TauCorrections.correct_e_idiso_2012(row.ePt, row.eAbsEta)
    m_trg = H2TauCorrections.correct_mueg_mu_2012(row.mPt, row.mAbsEta)
    e_trg = H2TauCorrections.correct_mueg_e_2012(row.ePt, row.eAbsEta)
    return pu*m1id*m1iso*e2idiso*m_trg*e_trg

# Determine which set of corrections to use
mc_corrector = mc_corrector_2011
if not is7TeV:
    mc_corrector = mc_corrector_2012

class ControlEM(MegaBase):
    tree = 'em/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(ControlEM, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = EMuTree.EMuTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}
        self.is7TeV = '7TeV' in os.environ['jobid']

    def begin(self):
        self.book('em', "weight", "Event weight", 100, 0, 5)
        self.book('em', "weight_nopu", "Event weight without PU", 100, 0, 5)

        self.book('em', "rho", "Fastjet #rho", 100, 0, 25)
        self.book('em', "nvtx", "Number of vertices", 31, -0.5, 30.5)
        self.book('em', "prescale", "HLT prescale", 21, -0.5, 20.5)

        self.book('em', "mPt", "Muon 1 Pt", 100, 0, 100)
        self.book('em', "ePt", "Muon 2 Pt", 100, 0, 100)
        self.book('em', "mAbsEta", "Muon 1 eta", 100, -2.5, 2.5)
        self.book('em', "eAbsEta", "Muon 2 eta", 100, -2.5, 2.5)
        self.book('em', "emMass", "m_{e#mu} (GeV)", 240, 0, 240)

        self.book('em', 'mPixHits', 'Mu 1 pix hits', 10, -0.5, 9.5)

        self.book('em', 'mJetBtag', 'Mu 1 JetBtag', 100, -5.5, 9.5)
        self.book('em', 'eJetBtag', 'Mu 2 JetBtag', 100, -5.5, 9.5)

        # Vetoes
        self.book('em', 'bjetVeto', 'Number of b-jets', 5, -0.5, 4.5)
        self.book('em', 'bjetCSVVeto', 'Number of b-jets', 5, -0.5, 4.5)
        self.book('em', 'muVetoPt5', 'Number of extra muons', 5, -0.5, 4.5)
        self.book('em', 'tauVetoPt20', 'Number of extra taus', 5, -0.5, 4.5)
        self.book('em', 'eVetoCicTightIso', 'Number of extra CiC tight electrons', 5, -0.5, 4.5)

    def correction(self, row):
        return mc_corrector(row)

    def fill_histos(self, row):
        histos = self.histograms
        weight = self.correction(row)
        histos['em/weight'].Fill(weight)
        histos['em/weight_nopu'].Fill(self.correction(row))
        histos['em/rho'].Fill(row.rho, weight)
        histos['em/nvtx'].Fill(row.nvtx, weight)
        histos['em/prescale'].Fill(row.doubleMuPrescale, weight)
        histos['em/ePt'].Fill(row.ePt, weight)
        histos['em/mPt'].Fill(row.mPt, weight)
        histos['em/eAbsEta'].Fill(row.eAbsEta, weight)
        histos['em/mAbsEta'].Fill(row.mAbsEta, weight)
        histos['em/mPixHits'].Fill(row.mPixHits, weight)
        histos['em/eJetBtag'].Fill(row.eJetBtag, weight)
        histos['em/mJetBtag'].Fill(row.mJetBtag, weight)
        histos['em/emMass'].Fill(row.e_m_Mass, weight)

        histos['em/bjetVeto'].Fill(row.bjetVeto, weight)
        histos['em/bjetCSVVeto'].Fill(row.bjetCSVVeto, weight)
        histos['em/muVetoPt5'].Fill(row.muVetoPt5, weight)
        histos['em/tauVetoPt20'].Fill(row.tauVetoPt20, weight)
        histos['em/eVetoCicTightIso'].Fill(row.eVetoCicTightIso, weight)

    def preselection(self, row):
        ''' Preselection applied to events.

        Excludes FR object IDs and sign cut.
        '''
        if not row.mu17ele8Pass:
            return False
        if row.e_m_SS:
            return False
        if row.mPt < 20:
            return False
        if row.ePt < 10:
            return False
        if row.mAbsEta > 2.4:
            return False
        if row.eAbsEta > 2.5:
            return False
        if abs(row.eDZ) > 0.2:
            return False
        if abs(row.mDZ) > 0.2:
            return False
        return True

    def obj1_id(self, row):
        return bool(row.mPFIDTight) and bool(row.mRelPFIsoDB < 0.2)

    def obj2_id(self, row):
        return bool(row.eMVAIDH2TauWP) and bool(row.eRelPFIsoDB < 0.1)

    def process(self):
        for row in self.tree:
            if not self.preselection(row):
                continue
            if not self.obj1_id(row) or not self.obj2_id(row):
                continue
            self.fill_histos(row)

    def finish(self):
        self.write_histos()
