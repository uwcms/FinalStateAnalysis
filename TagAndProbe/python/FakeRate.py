import os
import re
import ROOT
from graphReader import GraphReaderTrackingEta
from correctionloader import CorrectionLoader

_DATA_DIR = os.path.join(os.environ['CMSSW_BASE'], 'src',
                         "FinalStateAnalysis", "TagAndProbe", "data")

_DATA_FILES = {
    'Tau' : {
        'frEBDM0'   : os.path.join(_DATA_DIR, 'frEBDM0.root'),
        'frEBDM1'   : os.path.join(_DATA_DIR, 'frEBDM1.root'),
        'frEBDM10'   : os.path.join(_DATA_DIR, 'frEBDM10.root'),
        'frEEDM0'   : os.path.join(_DATA_DIR, 'frEBDM0.root'),
        'frEEDM1'   : os.path.join(_DATA_DIR, 'frEEDM1.root'),
        'frEEDM10'   : os.path.join(_DATA_DIR, 'frEEDM10.root')
        },
    'Muon' : {
        'frMuon'   : os.path.join(_DATA_DIR, 'frMuonPt.root')
        },
    }


def FakeRateWeight():
    return FakeRateWeight_ReReco(
        _DATA_FILES['Tau'],
        "fakerate"
    )


def FakeRateMuonWeight():
    return FakeRateMuonWeight_ReReco(
        _DATA_FILES['Muon'],
        "fakerate"
    )


class FakeRateWeight_ReReco(object):

    def __init__(self, files, frHisto):
        self.histopath = frHisto

        self.filenameEBDM0 = files['frEBDM0']
        self.fileEBDM0 = ROOT.TFile.Open(self.filenameEBDM0)
        self.keyEBDM0 = self.fileEBDM0.Get(self.histopath)

        self.filenameEBDM1 = files['frEBDM1']
        self.fileEBDM1 = ROOT.TFile.Open(self.filenameEBDM1)
        self.keyEBDM1 = self.fileEBDM1.Get(self.histopath)

        self.filenameEBDM10 = files['frEBDM10']
        self.fileEBDM10 = ROOT.TFile.Open(self.filenameEBDM10)
        self.keyEBDM10 = self.fileEBDM10.Get(self.histopath)

        self.filenameEEDM0 = files['frEEDM0']
        self.fileEEDM0 = ROOT.TFile.Open(self.filenameEEDM0)
        self.keyEEDM0 = self.fileEEDM0.Get(self.histopath)

        self.filenameEEDM1 = files['frEEDM1']
        self.fileEEDM1 = ROOT.TFile.Open(self.filenameEEDM1)
        self.keyEEDM1 = self.fileEEDM1.Get(self.histopath)

        self.filenameEEDM10 = files['frEEDM10']
        self.fileEEDM10 = ROOT.TFile.Open(self.filenameEEDM10)
        self.keyEEDM10 = self.fileEEDM10.Get(self.histopath)
      
    def __call__(self, pt, eta, DM):
        if pt < 30:
            bin = 1
        elif pt < 60:
            bin = 2
        elif pt < 90:
            bin = 3
        elif pt < 120:
            bin = 4
        else:
            bin = 5
        if abs(eta) < 1.5:
            if DM == 0:
                f = self.keyEBDM0.GetEfficiency(bin)
            elif DM == 1:
                f = self.keyEBDM1.GetEfficiency(bin)
            elif DM == 10:
                f = self.keyEBDM10.GetEfficiency(bin)
        else:
            if DM == 0:
                f = self.keyEEDM0.GetEfficiency(bin)
            elif DM == 1:
                f = self.keyEEDM1.GetEfficiency(bin)
            elif DM == 10:
                f = self.keyEEDM10.GetEfficiency(bin)
        if f == 1:
            return 0
        return f/(1-f)


class FakeRateMuonWeight_ReReco(object):

    def __init__(self, files, frHisto):
        self.filename = files['frMuon']
        self.file = ROOT.TFile.Open(self.filename)
        self.histopath = frHisto
        self.key = self.file.Get(self.histopath)

    def __call__(self, pt):
        if pt < 30:
            bin = 1
        elif pt < 60:
            bin = 2
        elif pt < 90:
            bin = 3
        elif pt < 120:
            bin = 4
        else:
            bin = 5
        f = self.key.GetEfficiency(bin)
        if f == 1:
            return 0
        return (f/(1-f))


if __name__ == "__main__":
    FakeRateWeight()
    FakeRateMuonWeight()
