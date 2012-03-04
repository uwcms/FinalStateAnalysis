import ROOT
from FinalStateAnalysis.TMegaSelector.megaselect import MegaPySelector

class AnalyzeEMT(MegaPySelector):

    def __init__(self):
        self.setup = False

    def Version(self):
        return 2

    def MegaInit(self, tree):
        print "megaInit"
        if not self.setup:
            self.setup = True
            self.MakeFloatCut("asdf", "MuPt", ">", 20)
        print "done"
        return True

    def MegaSlaveBegin(self, tree):
        print "megaSlave"
        self.TauPt = ROOT.TH1F("TauPt", "TauPt", 100, 0, 100)
        self.MuPt = ROOT.TH1F("MuPt", "MuPt", 100, 0, 100)
        self.BytesRead = ROOT.TH1F("BytesRead", "BytesRead", 1000, 0, 10000)
        self.DisableBranch('*')
        self.EnableBranch('TauPt')
        self.EnableBranch('MuPt')
        #self.SetFilterSelection("Base")
        return True

    def MegaProcess(self, entry):
        print entry
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
        return True
