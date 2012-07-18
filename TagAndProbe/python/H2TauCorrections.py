'''

Compilation of MC-DATA corrections provided by the H2Tau group.

For now just the and electron ID & ISO measured by Valentina.

See: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012

'''

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
    if abseta < 0.8:
        if pt < 15:
            return 1.0
        if pt < 20:
            return 1.0
        if pt < 25:
            return 1.01
        if pt < 30:
            return 1.0
        return 1.07
    elif abseta < 1.2:
        if pt < 15:
            return 0.99
        if pt < 20:
            return 1.04
        if pt < 25:
            return 0.98
        if pt < 30:
            return 1.06
        return 1.12
    else:
        if pt < 15:
            return 0.98
        if pt < 20:
            return 1.02
        if pt < 25:
            return 0.96
        if pt < 30:
            return 1.02
        return 1.12

def correct_mueg_e_2012(pt, abseta):
    ''' Get DATA-MC correction factor electron leg of MuEG trigger '''
    if abseta < 0.8:
        if pt < 15:
            return 0.99
        if pt < 20:
            return 0.99
        if pt < 25:
            return 0.98
        if pt < 30:
            return 1.0
        return 1.00
    elif abseta < 1.479:
        if pt < 15:
            return 0.82
        if pt < 20:
            return 1.00
        if pt < 25:
            return 0.96
        if pt < 30:
            return 0.98
        return 0.99
    else:
        if pt < 15:
            return 0.96
        if pt < 20:
            return 1.07
        if pt < 25:
            return 1.01
        if pt < 30:
            return 1.01
        return 0.97

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
    ''' Get DATA-MC correction factor electron ID and Iso '''
    if abseta < 0.8:
        if pt < 15:
            return 0.84
        if pt < 20:
            return 0.926
        return 0.959
    elif abseta < 1.479:
        if pt < 15:
            return 0.837
        if pt < 20:
            return 0.853
        return 0.954
    else:
        if pt < 15:
            return 0.722
        if pt < 20:
            return 0.838
        return 0.968

