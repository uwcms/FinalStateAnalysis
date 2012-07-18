'''

Interface to official corrections from the muon POG
===================================================

Interface: Evan K. Friis, UW Madison

https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffs

In general, there is a eta dependent correction for pt > 20, and a pt dependent
correction otherwise.

Available correctors::

    make_muon_pog_PFTight_2011()
    make_muon_pog_PFTight_2012()
    make_muon_pog_PFRelIsoDB012_2012()
    make_muon_pog_PFRelIsoDB02_2012()
    make_muon_pog_PFRelIsoDB02_2011()
    make_muon_pog_PFRelIsoDB012_2011()
    make_muon_pog_Mu17Mu8_Mu17_2012()
    make_muon_pog_Mu17Mu8_Mu8_2012()

which do what they say on the tin.  Each of these returns a corrector object
that has a method "correction(pt, eta)".  Note that the Mu17_Mu8 corrections are
only available for 2012.

The trigger efficiencies for 2011 are encoded in a C++ file::
    interface/MuonPOG2011HLTEfficiencies.h

They are available as python functions (taking the eta of both muons) as::

    muon_pog_Mu17Mu8_eta_eta_2011(eta1, eta2)
    muon_pog_Mu13Mu8_eta_eta_2011(eta1, eta2)

'''

import os
import ROOT

_DATA_DIR = os.path.join(os.environ['CMSSW_BASE'], 'src',
                         "FinalStateAnalysis", "TagAndProbe", "data")

_DATA_FILES = {
    '2011' : os.path.join(_DATA_DIR, 'MuonEfficiencies2011_42X_DataMC.root'),
    '2012' : os.path.join(_DATA_DIR, 'MuonEfficiencies_11June2012_52X.root')
}

# Load the 2011 muon HLT corrections and give the function a consistent name
ROOT.gSystem.Load("libFinalStateAnalysisTagAndProbe")
muon_pog_Mu13Mu8_eta_eta_2011 = ROOT.Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC
muon_pog_Mu17Mu8_eta_eta_2011 = ROOT.Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC

def make_muon_pog_PFTight_2011():
    ''' Make PFTight DATA/MC corrector for 2011 '''
    return MuonPOG2011Combiner(
        MuonPOGCorrection(
            _DATA_FILES['2011'],
            "DATA/MC_PFTIGHT_nH10_2011A_pt__abseta<1.2",
            "DATA/MC_PFTIGHT_nH10_2011A_pt__abseta>1.2",
            "DATA/MC_PFTIGHT_nH10_2011A_eta__pt>20",
        ),
        MuonPOGCorrection(
            _DATA_FILES['2011'],
            "DATA/MC_PFTIGHT_nH10_2011B_pt__abseta<1.2",
            "DATA/MC_PFTIGHT_nH10_2011B_pt__abseta>1.2",
            "DATA/MC_PFTIGHT_nH10_2011B_eta__pt>20",
        )
    )

def make_muon_pog_PFTight_2012():
    ''' Make PFTight DATA/MC corrector for 2012 '''
    return MuonPOGCorrection(
        _DATA_FILES['2012'],
        "DATA/MC_Tight_pt_abseta<1.2",
        "DATA/MC_Tight_pt_abseta>1.2",
        "DATA/MC_Tight_eta_pt20-100",
    )

def make_muon_pog_PFRelIsoDB012_2012():
    return MuonPOGCorrection(
        _DATA_FILES['2012'],
        'DATA/MC_combRelIsoPF04dBeta<012_Tight_pt_abseta<1.2',
        'DATA/MC_combRelIsoPF04dBeta<012_Tight_pt_abseta>1.2',
        'DATA/MC_combRelIsoPF04dBeta<012_Tight_eta_pt20-100',
    )

def make_muon_pog_PFRelIsoDB02_2012():
    return MuonPOGCorrection(
        _DATA_FILES['2012'],
        'DATA/MC_combRelIsoPF04dBeta<02_Tight_pt_abseta<1.2',
        'DATA/MC_combRelIsoPF04dBeta<02_Tight_pt_abseta>1.2',
        'DATA/MC_combRelIsoPF04dBeta<02_Tight_eta_pt20-100',
    )

def make_muon_pog_PFRelIsoDB02_2011():
    return MuonPOG2011Combiner(
        MuonPOGCorrection(
            _DATA_FILES['2011'],
            'DATA/MC_combRelPFISO20_2011A_pt__abseta<1.2',
            'DATA/MC_combRelPFISO20_2011A_pt__abseta>1.2',
            'DATA/MC_combRelPFISO20_2011A_eta__pt>20',
        ),
        MuonPOGCorrection(
            _DATA_FILES['2011'],
            'DATA/MC_combRelPFISO20_2011B_pt__abseta<1.2',
            'DATA/MC_combRelPFISO20_2011B_pt__abseta>1.2',
            'DATA/MC_combRelPFISO20_2011B_eta__pt>20',
        ),
    )

def make_muon_pog_PFRelIsoDB012_2011():
    return MuonPOG2011Combiner(
        MuonPOGCorrection(
            _DATA_FILES['2011'],
            'DATA/MC_combRelPFISO12_2011A_pt__abseta<1.2',
            'DATA/MC_combRelPFISO12_2011A_pt__abseta>1.2',
            'DATA/MC_combRelPFISO12_2011A_eta__pt>20',
        ),
        MuonPOGCorrection(
            _DATA_FILES['2011'],
            'DATA/MC_combRelPFISO12_2011B_pt__abseta<1.2',
            'DATA/MC_combRelPFISO12_2011B_pt__abseta>1.2',
            'DATA/MC_combRelPFISO12_2011B_eta__pt>20',
        ),
    )

# These are only measured in 2012
def make_muon_pog_Mu17Mu8_Mu17_2012():
    return MuonPOGCorrection(
        _DATA_FILES['2012'],
        'DATA/MC_DoubleMu17Mu8_Mu17_Tight_pt_abseta<1.2',
        'DATA/MC_DoubleMu17Mu8_Mu17_Tight_pt_abseta>1.2',
        'DATA/MC_DoubleMu17Mu8_Mu17_Tight_eta_pt20-100',
    )
def make_muon_pog_Mu17Mu8_Mu8_2012():
    return MuonPOGCorrection(
        _DATA_FILES['2012'],
        'DATA/MC_DoubleMu17Mu8_Mu8_Tight_pt_abseta<1.2',
        'DATA/MC_DoubleMu17Mu8_Mu8_Tight_pt_abseta>1.2',
        'DATA/MC_DoubleMu17Mu8_Mu8_Tight_eta_pt20-100',
    )

class MuonPOGCorrection(object):
    '''

    Muon POG corrections are generally by eta dependent for pt > 20,
    and pt dependent for pt < 20, split by barrel and endcap.

    '''

    def __init__(self, file, pt_barrel, pt_endcap, eta_pt20, abs_eta=False):
        self.filename = file
        self.file = ROOT.TFile.Open(file)
        self.abs_eta = abs_eta

        # Map the functions to the appropriate TGraphAsymmErrors
        self.correct_by_pt_barrel = self.load_graph_eval_func(pt_barrel)
        self.correct_by_pt_endcap = self.load_graph_eval_func(pt_endcap)
        self.corrector_by_eta_pt20 = self.load_graph_eval_func(eta_pt20)

    def load_graph_eval_func(self, name):
        ''' Load a graph with a given name form the file '''
        key = self.file.GetKey(name)
        if not key:
            raise IOError("Object with name %s d.n.e. in file %s" %
                          (name, self.filename))
        obj = key.ReadObj()
        if not obj:
            raise IOError("Object with key name %s d.n.e. can't be read" % name)
        return obj.Eval

    def __call__(self, pt, eta):
        if pt < 20:
            if abs(eta) < 1.2:
                return self.correct_by_pt_barrel(pt)
            else:
                return self.correct_by_pt_endcap(pt)
        else:
            if self.abs_eta:
                eta = abs(eta)
            return self.correct_by_eta_pt20(eta)


class MuonPOG2011Combiner(object):
    ''' They provide 2011 A and B separate, we have to combine them '''
    def __init__(self, corrector2011A, corrector2011B):
        self.corrA = corrector2011A
        self.corrB = corrector2011B

    def __call__(self, pt, eta):
        # Weighted average, by int. lumi
        return self.corrA(pt, eta)*(2.1/4.6) + \
                self.corrB(pt, eta)*(2.5/4.6)


if __name__ == "__main__":
    make_muon_pog_PFTight_2011()
    make_muon_pog_PFTight_2012()
    make_muon_pog_PFRelIsoDB012_2012()
    make_muon_pog_PFRelIsoDB02_2012()
    make_muon_pog_PFRelIsoDB02_2011()
    make_muon_pog_PFRelIsoDB012_2011()
    make_muon_pog_Mu17Mu8_Mu17_2012()
    make_muon_pog_Mu17Mu8_Mu8_2012()
