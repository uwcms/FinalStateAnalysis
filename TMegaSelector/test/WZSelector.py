import ROOT
from FinalStateAnalysis.TMegaSelector.megaselect import TMegaPySelector

class WZSelector(TMegaPySelector):
    def Version(self):
        return 2
    def MegaSlaveBegin(self, tree):
        self.TauPt = ROOT.TH1F("TauPt", "TauPt", 100, 0, 100)
        self.MuPt = ROOT.TH1F("MuPt", "MuPt", 100, 0, 100)
        self.BytesRead = ROOT.TH1F("BytesRead", "BytesRead", 1000, 0, 10000)
        self.DisableBranch('*')
        self.EnableBranch('TauPt')
        self.EnableBranch('MuPt')
        #self.fOutput.Add(self.histo)
    def MegaProcess(self, entry):
        read = self.chain.GetEntry(entry)
        # Should be 8 bytes each time
        self.BytesRead.Fill(read)
        self.TauPt.Fill(self.chain.TauPt)
        self.MuPt.Fill(self.chain.MuPt)
        return True
    def MegaSlaveTerminate(self):
        print 'Adding output'
        self.AddToOutput(self.TauPt)
        self.AddToOutput(self.MuPt)
        self.AddToOutput(self.BytesRead)
