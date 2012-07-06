'''

Analyze EMT events for the WH analysis

'''

import WHAnalyzerBase
from EMuTauTree import EMuTauTree

class WHAnalyzeEMT(WHAnalyzerBase.WHAnalyzerBase):
    tree = 'emt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(WHAnalyzeEMT, self).__init__(tree, outfile, EMuTauTree, **kwargs)

    def book_histos(self, folder):
        self.book(folder, "mPt", "Muon Pt", 100, 0, 100)
        self.book(folder, "ePt", "Electron Pt", 100, 0, 100)
        self.book(folder, "emMass", "Electron-Muon Mass", 120, 0, 120)

    def fill_histos(self, histos, folder, row, weight):
        def fill(name, value):
            histos['/'.join(folder + (name,))].Fill(value, weight)
        fill('mPt', row.mPt)
        fill('ePt', row.ePt)
        fill('emMass', row.e_m_Mass)

    def preselection(self, row):
        ''' Preselection applied to events.

        Excludes FR object IDs and sign cut.
        '''
        if not row.doubleMuPass:
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
        if not row.muVetoPt5:
            return False
        if not row.bjetCSVVeto:
            return False
        if not row.tauVetoPt20:
            return False
        if not row.mPixHits:
            return False
        if not row.eMissingHits > 0.5:
            return False
        if not row.eHasConversion > 0.5:
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
        return row.puWeightData2012AB

    def obj1_weight(self, row):
        #fixme
        return 1e-2

    def obj2_weight(self, row):
        #fixme
        return 1e-2

    def obj3_weight(self, row):
        #fixme
        return 1e-2
