'''

Analyze EET events for the WH analysis

'''

from EETauTree import EETauTree
from FinalStateAnalysis.StatTools.RooFunctorFromWS import build_roofunctor
import os
from PUWeighting import pu_weight
import ROOT
import WHAnalyzerBase

# Get fitted fake rate functions
frfit_dir = os.path.join('results', os.environ['jobid'], 'fakerate_fits')
highpt_ee_fr = build_roofunctor(
    frfit_dir + '/ee_wjets_pt20_mvaidiso03_e2JetPt-data_ee.root',
    'fit_efficiency', # workspace name
    'efficiency'
)
lowpt_ee_fr = build_roofunctor(
    frfit_dir + '/ee_wjets_pt10_mvaidiso03_e2JetPt-data_ee.root',
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

class WHAnalyzeEET(WHAnalyzerBase.WHAnalyzerBase):
    tree = 'eet/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(WHAnalyzeEET, self).__init__(tree, outfile, EETauTree, **kwargs)

    def book_histos(self, folder):
        self.book(folder, "weight", "Event weight", 100, 0, 5)
        self.book(folder, "weight_nopu", "Event weight without PU", 100, 0, 5)
        self.book(folder, "rho", "Fastjet #rho", 100, 0, 25)
        self.book(folder, "nvtx", "Number of vertices", 31, -0.5, 30.5)
        self.book(folder, "prescale", "HLT prescale", 21, -0.5, 20.5)
        self.book(folder, "e1Pt", "E 1 Pt", 100, 0, 100)
        self.book(folder, "e2Pt", "E 2 Pt", 100, 0, 100)
        self.book(folder, "e1e2Mass", "E 1-2 Mass", 120, 0, 120)
        self.book(folder, "e1tMass", "E 1-2 Mass", 120, 0, 120)
        self.book(folder, "subMass", "subleadingMass", 200, 0, 200)
        self.book(folder, "e2Iso", "e2Iso", 100, 0, 0.3)

    def fill_histos(self, histos, folder, row, weight):
        def fill(name, value):
            histos['/'.join(folder + (name,))].Fill(value, weight)
        histos['/'.join(folder + ('weight',))].Fill(weight)
        histos['/'.join(folder + ('weight_nopu',))].Fill(
            weight/row.puWeightData2011AB if row.puWeightData2011AB else 0)

        fill('prescale', row.doubleEPrescale)
        fill('rho', row.rho)
        fill('nvtx', row.nvtx)
        fill('e1Pt', row.e1Pt)
        fill('e2Pt', row.e2Pt)
        fill('e1e2Mass', row.e1_e2_Mass)
        fill('e1tMass', row.e1_t_Mass)
        fill('subMass', row.e2_t_Mass)
        fill('e2Iso', row.e2RelPFIsoDB)

    def preselection(self, row):
        ''' Preselection applied to events.

        Excludes FR object IDs and sign cut.
        '''
        if not row.doubleEPass:
            return False
        if row.e1Pt < 20:
            return False
        if row.e2Pt < 10:
            return False
        if row.tPt < 20:
            return False
        if row.e1AbsEta > 2.5:
            return False
        if row.e2AbsEta > 2.5:
            return False
        if row.tAbsEta > 2.3:
            return False
        if row.muVetoPt5:
            return False
        if row.e1_e2_Mass < 20:
            return False

        if not row.e1ChargeIdTight:
            return False
        if not row.e2ChargeIdTight:
            return False

        if row.e1_e2_Mass > 81 and row.e1_e2_Mass < 101:
            return False

        if row.LT < 80:
            return False

        if row.bjetCSVVeto:
            return False
        if row.tauVetoPt20:
            return False

        # Add e-veto!
        if row.e1MissingHits:
            return False
        if row.e2MissingHits:
            return False

        # Fixme use CSV
        if row.e1JetBtag > 3.3:
            return False
        if row.e2JetBtag > 3.3:
            return False
        if abs(row.e1DZ) > 0.2:
            return False
        if abs(row.e2DZ) > 0.2:
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
        return bool(row.e1_e2_SS)

    def obj1_id(self, row):
        return bool(row.e1MVAIDH2TauWP) and bool(row.e1RelPFIsoDB < 0.3)

    def obj2_id(self, row):
        return bool(row.e2MVAIDH2TauWP) and bool(row.e2RelPFIsoDB < 0.3)

    def obj3_id(self, row):
        return bool(row.tLooseMVAIso)

    def event_weight(self, row):
        weight = pu_weight(row)
        if row.run < 10:
            weight *= ROOT.Cor_Total_Ele_Lead(row.e1Pt, row.e1AbsEta)
            weight *= ROOT.Cor_Total_Ele_SubLead(row.e2Pt, row.e2AbsEta)
        return weight

    def obj1_weight(self, row):
        return highpt_ee_fr(row.e1JetPt)

    def obj2_weight(self, row):
        return lowpt_ee_fr(row.e2JetPt)

    def obj3_weight(self, row):
        return tau_fr(row.tPt)
