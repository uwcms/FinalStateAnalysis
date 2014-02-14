'''

Compilation of MC-DATA corrections provided by the H2Tau group.

For now just the trigger and electron ID & ISO measured by Valentina.

See: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012

'''

from FinalStateAnalysis.Utilities.rootbindings import ROOT
#ROOT.gSystem.Load("libFinalStateAnalysisTagAndProbe")


def correct_mueg_mu_2011(pt, abseta):
    ''' Get DATA-MC correction factor mu leg of MuEG trigger '''
    if abseta < 1.2:
        if pt < 15:
            return 1.01
        if pt < 20:
            return 0.99
        if pt < 30:
            return 0.99
        return 0.992
    else:
        if pt < 15:
            return 1.03
        if pt < 20:
            return 1.07
        if pt < 30:
            return 1.04
        return 1.06


def correct_mueg_e_2011(pt, abseta):
    ''' Get DATA-MC correction factor electron leg of MuEG trigger '''
    if abseta < 1.5:
        if pt < 15:
            return 0.98
        if pt < 20:
            return 1.0
        if pt < 30:
            return 1.001
        return 1.003
    else:
        if pt < 15:
            return 0.97
        if pt < 20:
            return 1.05
        if pt < 30:
            return 1.00
        return 1.008


def correct_mueg_mu_2012(pt, abseta):
    ''' Get DATA-MC correction factor muon leg of MuEG trigger '''
    return ROOT.muTrigScale_MuEG_2012_53X(pt, abseta)


def correct_mueg_e_2012(pt, abseta):
    ''' Get DATA-MC correction factor electron leg of MuEG trigger '''
    return ROOT.eleTrigScale_MuEG_2012_53X(pt, abseta)


def correct_e_idiso_2011(pt, abseta):
    ''' Get DATA-MC correction factor electron ID and Iso '''
    if abseta < 1.479:
        if pt < 15:
            return 1.04
        if pt < 20:
            return 0.962
        return 0.985
    else:
        if pt < 15:
            return 0.976
        if pt < 20:
            return 1.148
        return 1.012


def correct_mu_idiso_2011(pt, abseta):
    ''' Get DATA-MC correction factor muon ID and Iso '''
    if abseta < 1.5:
        if pt < 15:
            return 0.99
        if pt < 20:
            return 1.02
        return 1.01
    else:
        if pt < 15:
            return 1.03
        if pt < 20:
            return 1.025
        return 1.01


def correct_e_idiso_2012(pt, abseta):
    ''' Get DATA-MC correction factor electron ID and Iso

    Twiki: HiggsToTauTauWorkingHCP2012#Electron_ID_Isolation_EMu_Channe

    '''
    return ROOT.eleIDscale_MuEG_2012_53X(pt, abseta)


def correct_mu_idiso_2012(pt, abseta):
    ''' Get DATA-MC correction for 53X data from inclusive E-Mu

    Twiki: HiggsToTauTauWorkingHCP2012#Muon_ID_Isolation_EMu_Channel
    '''
    return ROOT.muIDscale_MuEG_2012_53X(pt, abseta)


def correct_mu_trg_2012(pt, abseta):
    ''' Get DATA-MC correction for 53X data from inclusive E-Mu

    Twiki: HiggsToTauTauWorkingHCP2012#Muon_ID_Isolation_EMu_Channel

    Remarks from Alexei R:

        The muon legs in these electron-muon cross triggers are identical to
        the HLT_Mu17_Mu8 trigger.

        To be in synchronization with the e-mu channel we just used the numbers
        obtained by Valentina.

        If one requires simulation of HLT_Mu17_Mu8 (and we do require now
        simulation of HLT_Mu17_Mu8 trigger), then one has to apply the
        following trigger weight to MC event :

        trigger_weight = SF(pt2,eta2)*SF(pt1,eta),

        where SF(pt,eta) - are pt and eta dependent scale factors
        derived by Valentina.

    '''
    return correct_mueg_mu_2012(pt, abseta)


def correct_double_electron_trg_2012(ept1, eabseta1, ept2, eabseta2):
    return ROOT.Trg_DoubleEle_2012(ept1, eabseta1, ept2, eabseta2)

def correct_double_electron_trg_2011(ept1, eabseta1, ept2, eabseta2):
    return ROOT.Trg_DoubleEle_2011(ept1, eabseta1, ept2, eabseta2)

def correct_double_muon_trg_2012(mupt1, muabseta1, mupt2, muabseta2):
    return ROOT.Trg_DoubleMu_2012(mupt1, muabseta1, mupt2, muabseta2)


def correct_e_TIGHTidiso_2012(pt, abseta):
    return ROOT.eleTIGHTIDscale_2012_53X(pt, abseta)

def correct_e_TIGHTidiso_2011(pt, abseta):
    return ROOT.eleTIGHTIDscale_2011(pt, abseta)
