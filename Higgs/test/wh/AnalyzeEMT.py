import ROOT

from FinalStateAnalysis.TMegaSelector.megautil import MetaTree
from FinalStateAnalysis.TMegaSelector.megaselect import MegaPySelector

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

class AnalyzeEMT(MegaPySelector):

    def __init__(self):
        super(AnalyzeEMT, self).__init__()

    def Version(self):
        return 1

    def MegaSlaveBegin(self, tree):
        # Book histograms
        self.MuPt = ROOT.TH1F("MuPt", "MuPt", 200, 0, 200)
        self.DisableBranch('*')
        for branch in meta.active_branches():
            self.EnableBranch(branch)
        return True

    def MegaProcess(self, entry):
        tree = self.chain
        read = tree.GetEntry(entry)

        # Check if we pass the base selection
        for select in base_selections:
            if not select(tree):
                return True

        self.MuPt.Fill(tree.muonPt)
        return True

    def MegaSlaveTerminate(self):
        self.AddToOutput(self.MuPt)
        return True
