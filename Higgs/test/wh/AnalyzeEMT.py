import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase

meta = MetaTree()

base_selections = [
    meta.muonPt > 20,
    meta.electronPt > 10,
    meta.tauPt > 20,
    #meta.mu17ele8 > 0.5,
    meta.tauAbsEta < 2.3,
    meta.muonAbsEta < 2.1,
    meta.electronAbsEta < 2.5,

    meta.electronMuOverlap < 1,
    meta.muVetoPt5 < 1,
    meta.eVetoWP95Iso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    meta.muonPixHits > 0,
    meta.electronJetBtag < 3.3,
    meta.muonJetBtag < 3.3,

    meta.electronMissingHits < 1,
    meta.electronHasConversion < 1,

    meta.electronDZ < 0.2,
    meta.muonDZ < 0.2,
    meta.tauDZ < 0.2,

    meta.tauJetBtag < 3.3,
    meta.tauAntiElectronMedium > 0.5,
    meta.tauAntiElectronMVA > 0.5,
    meta.tauElecOverlap < 0.5,
    meta.tauAntiMuonTight > 0.5,
    meta.tauMuOverlap < 0.5,
]


hadronic_tau_id = [
    meta.tauDecayFinding > 0.5,
    meta.tauLooseIso > 0.5,
]

e_id = [
    meta.electronRelIso < 0.3,
    meta.electronMITID > 0.5,
]

mu_id = [
    meta.muonRelIso < 0.3,
    meta.muWWID > 0.5,
]

class AnalyzeEMT(MegaBase):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeEMT, self).__init__(tree, output, **kwargs)
        self.book('final', 'MuPt', "Muon Pt", 100, 0, 100)

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)

        # Check if we pass the base selection
        if not all(select(tree) for select in base_selections):
            return True

        self.histograms['final/MuPt'].Fill(tree.muonPt)
        return True

    def finish(self):
        self.write_histos()
