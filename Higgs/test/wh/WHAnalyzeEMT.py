'''

Analyze EMT events for the WH analysis

'''

import WHAnalyzerBase
from EMuTauTree import EMuTauTree
import glob
import os
import FinalStateAnalysis.TagAndProbe.MuonPOGCorrections as MuonPOGCorrections
import FinalStateAnalysis.TagAndProbe.H2TauCorrections as H2TauCorrections
import FinalStateAnalysis.TagAndProbe.PileupWeight as PileupWeight
from FinalStateAnalysis.StatTools.RooFunctorFromWS import build_roofunctor
import ROOT

################################################################################
#### Fitted fake rate functions ################################################
################################################################################

frfit_dir = os.path.join('results', os.environ['jobid'], 'fakerate_fits')
highpt_mu_fr = build_roofunctor(
    frfit_dir + '/m_wjets_pt20_pfidiso02_muonJetPt.root',
    'fit_efficiency', # workspace name
    'efficiency'
)
lowpt_e_fr = build_roofunctor(
    frfit_dir + '/e_wjets_pt10_mvaidiso01_eJetPt.root',
    'fit_efficiency', # workspace name
    'efficiency'
)
tau_fr = build_roofunctor(
    frfit_dir + '/t_ztt_pt20_mvaloose_tauPt.root',
    'fit_efficiency', # workspace name
    'efficiency'
)

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

class WHAnalyzeEMT(WHAnalyzerBase.WHAnalyzerBase):
    tree = 'emt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(WHAnalyzeEMT, self).__init__(tree, outfile, EMuTauTree, **kwargs)
        self.is7TeV = '7TeV' in os.environ['jobid']

    def book_histos(self, folder):
        self.book(folder, "mPt", "Muon Pt", 100, 0, 100)
        self.book(folder, "ePt", "Electron Pt", 100, 0, 100)
        self.book(folder, "tPt", "Tau Pt", 100, 0, 100)
        self.book(folder, "mAbsEta", "Muon AbsEta", 100, 0, 2.4)
        self.book(folder, "eAbsEta", "Electron AbsEta", 100, 0, 2.5)
        self.book(folder, "tAbsEta", "Tau AbsEta", 100, 0, 2.3)

        self.book(folder, "nTruePU", "NPU", 62, -1.5, 60.5)
        self.book(folder, "emMass", "Electron-Muon Mass", 200, 0, 200)
        self.book(folder, "eChargeIdTight", "Elec charge ID tight", 2, -0.5, 1.5)
        self.book(folder, "eChargeIdMedium", "Elec charge ID medium", 2, -0.5, 1.5)
        self.book(folder, "etMass", "Electron-Tau Mass", 200, 0, 200)
        self.book(folder, "subMass", "Subleading Mass", 200, 0, 200)
        self.book(folder, "bCSVVeto", "BjetCSV", 10, -0.5, 9.5)
        self.book(folder, "metSig", "MET significance", 100, 0, 15)
        self.book(folder, "tLeadDR", "DR between leading lepton and tau",
                  100, 0, 5)
        self.book(folder, "tSubDR", "DR between subleading lepton and tau",
                  100, 0, 5)

    def fill_histos(self, histos, folder, row, weight):
        histos['/'.join(folder + ('nTruePU',))].Fill(row.nTruePU)
        def fill(name, value):
            histos['/'.join(folder + (name,))].Fill(value, weight)
        fill('mPt', row.mPt)
        fill('ePt', row.ePt)
        fill('eAbsEta', row.eAbsEta)
        fill('mAbsEta', row.mAbsEta)
        fill('tAbsEta', row.tAbsEta)

        fill('eChargeIdTight', row.eChargeIdTight)
        fill('eChargeIdMedium', row.eChargeIdMed)

        fill('emMass', row.e_m_Mass)
        fill('etMass', row.e_t_Mass)
        fill('bCSVVeto', row.bjetCSVVeto)
        fill('metSig', row.metSignificance)
        if row.ePt < row.mPt:
            fill('subMass', row.e_t_Mass)
            fill('tLeadDR', row.m_t_DR)
            fill('tSubDR', row.e_t_DR)
        else:
            fill('subMass', row.m_t_Mass)
            fill('tLeadDR', row.e_t_DR)
            fill('tSubDR', row.m_t_DR)

    def preselection(self, row):
        ''' Preselection applied to events.

        Excludes FR object IDs and sign cut.
        '''
        if not row.mu17ele8Pass:
            return False
        if row.mPt < 20:
            return False
        if row.ePt < 10:
            return False
        if row.tPt < 20:
            return False
        if row.mAbsEta > 2.4:
            return False
        if row.eAbsEta > 2.5:
            return False
        if row.tAbsEta > 2.3:
            return False
        if row.muVetoPt5:
            return False
        if row.bjetVeto:
            return False
        if row.tauVetoPt20:
            return False
        if row.eVetoCicTightIso:
            return False
        if not row.mPixHits:
            return False
        if row.eMissingHits:
            return False
        if row.eHasConversion:
            return False
        if not row.eChargeIdTight:
            return False
        if row.LT < 80:
            return False
        # Fixme use CSV
        if row.mJetBtag > 3.3:
            return False
        if row.eJetBtag > 3.3:
            return False
        if abs(row.mDZ) > 0.2:
            return False
        if abs(row.eDZ) > 0.2:
            return False
        if abs(row.tDZ) > 0.2:
            return False
        if row.tMuOverlap:
            return False
        if not row.tAntiMuonTight:
            return False
        #'t_ElectronOverlapWP95 < 0.5',
        return True

    def sign_cut(self, row):
        ''' Returns true if muons are SS '''
        return bool(row.e_m_SS)

    def obj1_id(self, row):
        return bool(row.mPFIDTight) and bool(row.mRelPFIsoDB < 0.2)

    def obj2_id(self, row):
        return bool(row.eMVAIDH2TauWP) and bool(row.eRelPFIsoDB < 0.1)

    def obj3_id(self, row):
        return bool(row.tLooseMVAIso)

    def anti_wz(self, row):
        if row.tCiCTightElecOverlap:
            return False
        if row.e_t_Zcompat < 20:
            if not row.tAntiElectronMVA:
                return False
        elif not row.tAntiElectronLoose:
            return False
        return True

    def enhance_wz(self, row):
        if row.e_t_Zcompat < 15 and not row.tAntiElectronMVA:
            return True
        return False

    def event_weight(self, row):
        return mc_corrector(row)

    def obj1_weight(self, row):
        return highpt_mu_fr(row.mJetPt)

    def obj2_weight(self, row):
        return lowpt_e_fr(row.eJetPt)

    def obj3_weight(self, row):
        return tau_fr(row.tPt)
