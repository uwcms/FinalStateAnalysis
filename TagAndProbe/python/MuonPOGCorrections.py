import os
import re
#from FinalStateAnalysis.Utilities.rootbindings import ROOT
import ROOT
from graphReader import GraphReaderTrackingEta
from correctionloader import CorrectionLoader

mu_trackingEta_2017 = GraphReaderTrackingEta(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/fits_muon_trk_2017.root'),'ratio_eff_eta3_dr030e030_corr'
)

_DATA_DIR = os.path.join(os.environ['CMSSW_BASE'], 'src',
                         "FinalStateAnalysis", "TagAndProbe", "data")

_DATA_FILES = {
    '2017ReReco' : {
        'PFID'   : os.path.join(_DATA_DIR, 'RunBCDEF_SF_ID.root'),
        'Iso'    : os.path.join(_DATA_DIR, 'RunBCDEF_SF_ISO.root'),
        'Trigger': os.path.join(_DATA_DIR, 'EfficienciesAndSF_RunBtoF_Nov17Nov2017.root')
        },
    }


def make_muon_pog_IsoMu27_2017ReReco():
    return MuonPOGCorrectionTrig2D_ReReco(
        _DATA_FILES['2017ReReco']['Trigger'],
        "IsoMu27_PtEtaBins/pt_abseta_ratio"
    )
def make_muon_pog_PFLoose_2017ReReco():
    return MuonPOGCorrectionID2D_ReReco(
        _DATA_FILES['2017ReReco']['PFID'],
        "NUM_LooseID_DEN_genTracks_pt_abseta"
    )
def make_muon_pog_PFMedium_2017ReReco():
    return MuonPOGCorrectionID2D_ReReco(
        _DATA_FILES['2017ReReco']['PFID'],
        "NUM_MediumID_DEN_genTracks_pt_abseta"
    )
def make_muon_pog_PFTight_2017ReReco():
    return MuonPOGCorrectionID2D_ReReco(
        _DATA_FILES['2017ReReco']['PFID'],
        "NUM_TightID_DEN_genTracks_pt_abseta"
    )
def make_muon_pog_LooseIso_2017ReReco(MuonID):
    return MuonPOGCorrectionLooseIso2D_ReReco(
        MuonID,
        _DATA_FILES['2017ReReco']['Iso'],
        ["NUM_LooseRelIso_DEN_LooseID_pt_abseta",
         "NUM_LooseRelIso_DEN_MediumID_pt_abseta",
         "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
    )
def make_muon_pog_TightIso_2017ReReco(MuonID):
    if MuonID=='Loose':
        raise ValueError('Tight Iso corrections are not available for Loose ID WP, use either medium or tight ID with tight Iso')
    return MuonPOGCorrectionIso2D_ReReco(
        MuonID,
        _DATA_FILES['2017ReReco']['Iso'],
        ["NUM_TightRelIso_DEN_MediumID_pt_abseta",
         "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"]
    )


class MuonPOGCorrectionTrig2D_ReReco(object):

    def __init__(self, file, pt_abseta):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        self.histopath = pt_abseta
        self.correct_by_pt_abseta = {}
        self.key = self.file.Get(self.histopath)
      
    def __call__(self, pt, eta):
        if pt >= 499.: pt = 499.
        if pt < 20. : pt = 20.
        self.correct_by_pt_abseta =self.key.GetBinContent(self.key.FindFixBin(pt, eta))

        return self.correct_by_pt_abseta


class MuonPOGCorrectionID2D_ReReco(object):

    def __init__(self, file, pt_abseta):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        self.histopath = pt_abseta
        self.correct_by_pt_abseta = {}
        self.key = self.file.Get(self.histopath)
      
    def __call__(self, pt, eta):
        if pt >= 119.: pt = 119.
        if pt < 20. : pt = 20.
        self.correct_by_pt_abseta =self.key.GetBinContent(self.key.FindFixBin(pt, eta))

        return self.correct_by_pt_abseta


class MuonPOGCorrectionIso2D_ReReco(object):

    def __init__(self, MuonID, file, pt_abseta):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        if MuonID not in ['Tight','Medium','Loose']:
            raise ValueError('Muon ID has to be a string - "Tight","Medium","Loose"')
        if MuonID=='Tight':
            self.histopath=pt_abseta[1]
        if MuonID=='Medium':
            self.histopath=pt_abseta[0]
        self.correct_by_pt_abseta = {}
        self.key = self.file.Get(self.histopath)
      
    def __call__(self, pt, eta):
        if pt >= 119.: pt = 119.
        if pt < 20. : pt = 20.
        self.correct_by_pt_abseta =self.key.GetBinContent(self.key.FindFixBin(pt, eta))

        return self.correct_by_pt_abseta

class MuonPOGCorrectionLooseIso2D_ReReco(object):

    def __init__(self, MuonID, file, pt_abseta):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        if MuonID not in ['Tight','Medium','Loose']:
            raise ValueError('Muon ID has to be a string - "Tight","Medium","Loose"')
        if MuonID=='Tight':
            self.histopath=pt_abseta[2]
        if MuonID=='Medium':
            self.histopath=pt_abseta[1]
        if MuonID=='Loose':
            self.histopath=pt_abseta[0]
        self.correct_by_pt_abseta = {}
        self.key = self.file.Get(self.histopath)
      
    def __call__(self, pt, eta):
        if pt >= 119.: pt = 119.
        if pt < 20. : pt = 20.
        self.correct_by_pt_abseta =self.key.GetBinContent(self.key.FindFixBin(pt, eta))

        return self.correct_by_pt_abseta


if __name__ == "__main__":
    make_muon_pog_IsoMu27_2017ReReco()
    make_muon_pog_PFTight_2017ReReco()
    make_muon_pog_TightIso_2017ReReco(MuonID)
    make_muon_pog_PFMedium_2017ReReco()
    make_muon_pog_LooseIso_2017ReReco(MuonID)
