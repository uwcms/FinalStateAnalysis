'''

Compilation of MC-DATA corrections provided by the H2Tau group.

For now just the trigger and electron ID & ISO measured by Valentina.

See: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012

'''

import ROOT
ROOT.gSystem.Load("libFinalStateAnalysisTagAndProbe")

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
    return ROOT.muTrigEff_MuEG_2012_53X(pt, abseta)

def correct_mueg_e_2012(pt, abseta):
    ''' Get DATA-MC correction factor electron leg of MuEG trigger '''
    return ROOT.eleTrigEff_MuEG_2012_53X(pt, abseta)

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

def correct_e_idiso_2012(pt, abseta):
    ''' Get DATA-MC correction factor electron ID and Iso

    https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingHCP2012#Electron_ID_Isolation_EMu_Channe

    '''
    if abseta < 0.8:
        if pt < 15:
            return 0.7893
        if pt < 20:
            return 0.8506
        return 0.9534
    elif abseta < 1.479:
        if pt < 15:
            return 0.7952
        if pt < 20:
            return 0.8661
        return 0.9481
    else:
        if pt < 15:
            return 0.6519
        if pt < 20:
            return 0.7816
        return 0.9378

def correct_mu_idiso_2012(pt, abseta):
    ''' Get DATA-MC correction for 53X data from inclusive E-Mu

    https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingHCP2012#Muon_ID_Isolation_EMu_Channel
    '''
    if abseta < 0.8:
        if pt < 15:
            return 0.9845
        if pt < 20:
            return 0.9644
        return 0.9884
    elif abseta < 1.2:
        if pt < 15:
            return 0.9869
        if pt < 20:
            return 0.9800
        return 0.9884
    else:
        if pt < 15:
            return 0.9927
        if pt < 20:
            return 0.9961
        return 0.9941

