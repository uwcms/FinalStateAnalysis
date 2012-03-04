import ROOT
from FinalStateAnalysis.TMegaSelector.megaselect import TMegaPySelector

class TestSelector(TMegaPySelector):
    def Version(self):
        return 2
    def MegaSlaveBegin(self, tree):
        self.histo = ROOT.TH1F("adsf", "asdf", 100, 0, 100)
        #self.fOutput.Add(self.histo)
        self.MakeFloatCut("Base", "MuEta", "<", 0.5, True)
    def MegaProcess(self, entry):
        self.chain.GetEntry(entry)
        print self.chain.intBranch
        self.histo.Fill(entry)
        return True
    def MegaSlaveTerminate(self):
        print 'Adding output'
        self.AddToOutput(self.histo)
