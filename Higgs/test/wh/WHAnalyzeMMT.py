'''

Analyze MMT events for the WH analysis

'''

import WHAnalyzerBase
from MuMuTauTree import MuMuTauTree

class WHAnalyzeMMT(WHAnalyzerBase.WHAnalyzerBase):
    tree = 'mmt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(WHAnalyzeMMT, self).__init__(tree, outfile, MuMuTauTree, **kwargs)

    def book_histos(self, folder):
        self.book(folder, "m1Pt", "Muon 1 Pt", 100, 0, 100)
        self.book(folder, "m2Pt", "Muon 2 Pt", 100, 0, 100)
        self.book(folder, "m1m2Mass", "Muon 1-2 Mass", 120, 0, 120)

    def fill_histos(self, histos, folder, row, weight):
        def fill(name, value):
            histos['/'.join(folder + (name,))].Fill(value, weight)
        fill('m1Pt', row.m1Pt)
        fill('m2Pt', row.m2Pt)
        fill('m1m2Mass', row.m1_m2_Mass)

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
        if not row.muVetoPt5:
            return False
        if row.m1_m2_Mass < 20:
            return False
        if not row.bjetCSVVeto:
            return False
        if not row.tauVetoPt20:
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
        #fixme
        return 1

    def obj1_weight(self, row):
        #fixme
        return 1e-2

    def obj2_weight(self, row):
        #fixme
        return 1e-2

    def obj3_weight(self, row):
        #fixme
        return 1e-2
