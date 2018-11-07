from correctionloader import CorrectionLoader
import os
import ROOT 

def make_DYreweight():
    return DYCorrection(
        os.path.join(os.environ['fsa'], 'TagAndProbe/data/dy_weights_2017.root'),    
        "zptmass_histo"   
    )

def make_DYreweight1D():
    return DYCorrection1D(
        os.path.join(os.environ['fsa'], 'TagAndProbe/data/zpt_weights_2017_1D.root'),
        "zpt_weight"
    )

class DYCorrection(object):
    def __init__(self, file, mass_pt):
        ROOT.TH1.AddDirectory(False)
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        self.histopath = mass_pt
        self.correct_by_mass_pt = {}
        self.key = self.file.Get(self.histopath)
        #ROOT.TH1.AddDirectory(True);
    def __call__(self, mass, pt):
        self.correct_by_mass_pt =self.key.GetBinContent(self.key.FindFixBin(mass, pt))
        return self.correct_by_mass_pt


class DYCorrection1D(object):
    def __init__(self, file, mass_pt):
        ROOT.TH1.AddDirectory(False)
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        self.histopath = mass_pt
        self.correct_by_pt = {}
        self.key = self.file.Get(self.histopath)
        ROOT.TH1.AddDirectory(True)
       
    def __call__(self, pt):
        self.correct_by_pt =self.key.GetBinContent(self.key.FindBin(pt))
        return self.correct_by_pt
