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
    'ICHEP2016' : {
        'nontrigWP90'   : os.path.join(_DATA_DIR, 'electronID_ICHEP2016_fulldataset_nontrigWP90_SF2D.root '),
        'nontrigWP80'   : os.path.join(_DATA_DIR, 'electronID_ICHEP2016_fulldataset_nontrigWP80_SF2D.root '),
        'tracking':os.path.join(_DATA_DIR, 'ElectronTrackingEgammaPOG.root'),
    },
    'MORIOND2017' : {
        'nontrigWP90'   : os.path.join(_DATA_DIR, 'electronID_WP90_MORIOND17eGammaPOG.root '),
        'nontrigWP80'   : os.path.join(_DATA_DIR, 'electronID_WP80_MORIOND17eGammaPOG.root '),
        'recon':os.path.join(_DATA_DIR, 'electronReconEffiMORIOND17eGammaPOG.root'),
    }

}


def make_egamma_pog_electronID_ICHEP2016(wp):
    ''' Make PFTight DATA/MC corrector for 2016 BCD '''
    return EGammaPOGCorrection2D(
        _DATA_FILES['ICHEP2016'][wp],    
        "EGamma_SF2D"
    )


def make_egamma_pog_electronID_MORIOND2017(wp):
    ''' Make PFTight DATA/MC corrector for 2016 BCD '''
    return EGammaPOGCorrection2D(
        _DATA_FILES['MORIOND2017'][wp],    
        "EGamma_SF2D"
    )



def make_egamma_pog_tracking_ICHEP2016():
    ''' Make PFTight DATA/MC corrector for 2016 BCD '''
    return EGammaPOGCorrection2Dtrk(
        _DATA_FILES['ICHEP2016']['tracking'],    

        "EGamma_SF2D"
    )


def make_egamma_pog_recon_MORIOND17():
    ''' Make PFTight DATA/MC corrector for 2016 BCD '''
    return EGammaPOGCorrection2Dtrk(
        _DATA_FILES['MORIOND2017']['recon'],    
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
        if pt <= 10. : pt = 10.
        self.correct_by_eta_pt =self.key.GetBinContent(self.key.FindFixBin(eta, pt))
        #print 'E trk correction :', pt, eta,  self.correct_by_eta_pt
        return self.correct_by_eta_pt


class EGammaPOGCorrection2Dtrk(object):
    def __init__(self, file, eta_pt):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        #self.pt_thr  = pt_thr                                                                                                                
        self.histopath = eta_pt
        self.correct_by_eta_pt = {}
        self.key = self.file.Get(self.histopath)
    def __call__(self, eta, pt):
        if pt >= 180: pt = 180.
        if pt <=26. : pt = 26.#sf flat for low energy electrons
        self.correct_by_eta_pt =self.key.GetBinContent(self.key.FindFixBin(eta, pt))
        #print 'E trk correction :', pt, eta,  self.correct_by_eta_pt
        return self.correct_by_eta_pt


class EGammaPOGCorrection2Dtrk(object):
    def __init__(self, file, eta_pt):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        #self.pt_thr  = pt_thr                                                                                                                
        self.histopath = eta_pt
        self.correct_by_eta_pt = {}
        self.key = self.file.Get(self.histopath)

    def __call__(self, eta, pt):
        if pt >= 180: pt = 180.
        if pt < 20. : pt = 20.#sf flat for low energy electrons
        self.correct_by_eta_pt =self.key.GetBinContent(self.key.FindFixBin(eta, pt))
#        print 'E trk correction :', pt, eta,  self.correct_by_eta_pt
        return self.correct_by_eta_pt
