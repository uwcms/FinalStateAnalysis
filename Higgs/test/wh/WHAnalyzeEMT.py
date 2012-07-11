'''

Analyze EMT events for the WH analysis

'''

import WHAnalyzerBase
from EMuTauTree import EMuTauTree
import os
from PUWeighting import pu_weight
from FinalStateAnalysis.StatTools.RooFunctorFromWS import build_roofunctor
import ROOT

# Get fitted fake rate functions
frfit_dir = os.path.join('results', os.environ['jobid'], 'fakerate_fits')
highpt_mu_fr = build_roofunctor(
    frfit_dir + '/m_wjets_pt20_pfidiso03_muonJetPt-data_mm.root',
    'fit_efficiency', # workspace name
    'efficiency'
)
lowpt_e_fr = build_roofunctor(
    frfit_dir + '/e_wjets_pt10_mvaidiso03_eJetPt-data_em.root',
    'fit_efficiency', # workspace name
    'efficiency'
)
tau_fr = build_roofunctor(
    frfit_dir + '/t_ztt_pt20_mvaloose_tauPt-data_mm.root',
    'fit_efficiency', # workspace name
    'efficiency'
)

# Get correction functions
ROOT.gSystem.Load("Corrector_C")

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

        self.book(folder, "emMass", "Electron-Muon Mass", 200, 0, 200)
        self.book(folder, "etMass", "Electron-Tau Mass", 200, 0, 200)
        self.book(folder, "subMass", "Subleading Mass", 200, 0, 200)
        self.book(folder, "bCSVVeto", "BjetCSV", 10, -0.5, 9.5)
        self.book(folder, "metSig", "MET significance", 100, 0, 15)
        self.book(folder, "tLeadDR", "DR between leading lepton and tau",
                  100, 0, 5)
        self.book(folder, "tSubDR", "DR between subleading lepton and tau",
                  100, 0, 5)

    def fill_histos(self, histos, folder, row, weight):
        def fill(name, value):
            histos['/'.join(folder + (name,))].Fill(value, weight)
        fill('mPt', row.mPt)
        fill('ePt', row.ePt)
        fill('mPt', row.mPt)
        fill('eAbsEta', row.eAbsEta)
        fill('mAbsEta', row.mAbsEta)
        fill('tAbsEta', row.tAbsEta)

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
        if row.tCiCTightElecOverlap:
            return False
        if not row.tAntiElectronMVA:
            return False
        if not row.tAntiMuonTight:
            return False
        #'t_ElectronOverlapWP95 < 0.5',

        return True

    def sign_cut(self, row):
        ''' Returns true if muons are SS '''
        return bool(row.e_m_SS)

    def obj1_id(self, row):
        return bool(row.mPFIDTight) and bool(row.mRelPFIsoDB < 0.3)

    def obj2_id(self, row):
        return bool(row.eMVAIDH2TauWP) and bool(row.eRelPFIsoDB < 0.3)

    def obj3_id(self, row):
        return bool(row.tLooseMVAIso)

    def event_weight(self, row):
        # fixme
        weight = pu_weight(row)
        if row.run < 10:
            weight *= ROOT.Cor_Total_Mu_Lead(row.mPt, row.mAbsEta)
            weight *= ROOT.Cor_Total_Ele_SubLead(row.ePt, row.eAbsEta)
        return weight

    def obj1_weight(self, row):
        return highpt_mu_fr(row.mJetPt)

    def obj2_weight(self, row):
        return lowpt_e_fr(row.eJetPt)

    def obj3_weight(self, row):
        return tau_fr(row.tPt)
