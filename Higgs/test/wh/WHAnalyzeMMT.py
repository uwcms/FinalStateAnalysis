'''

Analyze MMT events for the WH analysis

'''

import WHAnalyzerBase
from MuMuTauTree import MuMuTauTree
import os
from FinalStateAnalysis.StatTools.RooFunctorFromWS import build_roofunctor
import ROOT

# Get fitted fake rate functions
frfit_dir = os.path.join('results', os.environ['jobid'], 'fakerate_fits')
highpt_mu_fr = build_roofunctor(
    frfit_dir + '/m_wjets_pt20_pfidiso03_muonJetPt-data_mm.root',
    'fit_efficiency', # workspace name
    'efficiency'
)
lowpt_mu_fr = build_roofunctor(
    frfit_dir + '/m_wjets_pt10_pfidiso03_muonJetPt-data_mm.root',
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

class WHAnalyzeMMT(WHAnalyzerBase.WHAnalyzerBase):
    tree = 'mmt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(WHAnalyzeMMT, self).__init__(tree, outfile, MuMuTauTree, **kwargs)

    def book_histos(self, folder):
        self.book(folder, "weight", "Event weight", 100, 0, 5)
        self.book(folder, "weight_nopu", "Event weight without PU", 100, 0, 5)
        self.book(folder, "rho", "Fastjet #rho", 100, 0, 25)
        self.book(folder, "nvtx", "Number of vertices", 31, -0.5, 30.5)
        self.book(folder, "prescale", "HLT prescale", 21, -0.5, 20.5)
        self.book(folder, "m1Pt", "Muon 1 Pt", 100, 0, 100)
        self.book(folder, "m2Pt", "Muon 2 Pt", 100, 0, 100)
        self.book(folder, "m1m2Mass", "Muon 1-2 Mass", 120, 0, 120)
        self.book(folder, "subMass", "subleadingMass", 200, 0, 200)
        self.book(folder, "m2Iso", "m2Iso", 100, 0, 0.3)

    def fill_histos(self, histos, folder, row, weight):
        def fill(name, value):
            histos['/'.join(folder + (name,))].Fill(value, weight)
        histos['/'.join(folder + ('weight',))].Fill(weight)
        histos['/'.join(folder + ('weight_nopu',))].Fill(
            weight/row.puWeightData2011AB if row.puWeightData2011AB else 0)

        fill('prescale', row.doubleMuPrescale)
        fill('rho', row.rho)
        fill('nvtx', row.nvtx)
        fill('m1Pt', row.m1Pt)
        fill('m2Pt', row.m2Pt)
        fill('m1m2Mass', row.m1_m2_Mass)
        fill('subMass', row.m2_t_Mass)
        fill('m2Iso', row.m2RelPFIsoDB)

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
        if row.tPt < 20:
            return False
        if row.m1AbsEta > 2.4:
            return False
        if row.m2AbsEta > 2.4:
            return False
        if row.tAbsEta > 2.3:
            return False
        if row.muVetoPt5:
            return False
        if row.m1_m2_Mass < 20:
            return False
        if row.LT < 80:
            return False

        if row.bjetCSVVeto:
            return False
        if row.tauVetoPt20:
            return False
        if not row.m1PixHits:
            return False
        if not row.m2PixHits:
            return False
        # Fixme use CSV
        if row.m1JetBtag > 3.3:
            return False
        if row.m2JetBtag > 3.3:
            return False
        if abs(row.m1DZ) > 0.2:
            return False
        if abs(row.m2DZ) > 0.2:
            return False
        if abs(row.tDZ) > 0.2:
            return False
        if not row.tAntiElectronMVA:
            return False
        if not row.tAntiMuonTight:
            return False
        if row.tMuOverlap:
            return False
        #'t_ElectronOverlapWP95 < 0.5',

        return True

    def sign_cut(self, row):
        ''' Returns true if muons are SS '''
        return bool(row.m1_m2_SS)

    def obj1_id(self, row):
        return bool(row.m1PFIDTight) and bool(row.m1RelPFIsoDB < 0.3)

    def obj2_id(self, row):
        return bool(row.m2PFIDTight) and bool(row.m2RelPFIsoDB < 0.3)

    def obj3_id(self, row):
        return bool(row.tLooseMVAIso)

    def event_weight(self, row):
        weight = row.puWeightData2011AB
        if row.run < 10:
            weight *= ROOT.Cor_Total_Mu_Lead(row.m1Pt, row.m1AbsEta)
            weight *= ROOT.Cor_Total_Mu_SubLead(row.m2Pt, row.m2AbsEta)
        return weight

    def obj1_weight(self, row):
        return highpt_mu_fr(row.m1JetPt)

    def obj2_weight(self, row):
        return lowpt_mu_fr(row.m2JetPt)

    def obj3_weight(self, row):
        return tau_fr(row.tPt)
