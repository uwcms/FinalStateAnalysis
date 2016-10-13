'''
Interface to official corrections from the EGamma  POG
===================================================
Adapted from MuonPOGcorrections.py
https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPOG

'''

import os
import re
#from FinalStateAnalysis.Utilities.rootbindings import ROOT
import ROOT

_DATA_DIR = os.path.join(os.environ['CMSSW_BASE'], 'src',
                         "FinalStateAnalysis", "TagAndProbe", "data")

_DATA_FILES = {
    'ICHEP2016ID' : {
        'nontrigWP90'   : os.path.join(_DATA_DIR, 'electronID_ICHEP2016_fulldataset_nontrigWP90_SF2D.root '),
        'nontrigWP80'   : os.path.join(_DATA_DIR, 'electronID_ICHEP2016_fulldataset_nontrigWP80_SF2D.root '),
    }
}


def make_egamma_pog_electronID_ICHEP2016(wp):
    ''' Make PFTight DATA/MC corrector for 2016 BCD '''
    return EGammaPOGCorrection2D(
        _DATA_FILES['ICHEP2016ID'][wp],    
        "EGamma_SF2D"
    )


class EGammaPOGCorrection2D(object):
    def __init__(self, file, eta_pt):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        #self.pt_thr  = pt_thr
        self.histopath = eta_pt
        self.correct_by_eta_pt = {}
        self.key = self.file.Get(self.histopath)

    def __call__(self, eta, pt):
        if pt >= 180: pt = 180.
        if pt < 5. : pt = 5.
        self.correct_by_eta_pt =self.key.GetBinContent(self.key.FindFixBin(eta, pt))
#        print 'E ID correction :', pt, eta,  self.correct_by_eta_pt
        return self.correct_by_eta_pt
