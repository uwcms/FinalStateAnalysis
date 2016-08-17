from correctionloader import CorrectionLoader
from graphReader import GraphReader
import os

single_ele_2016 = GraphReader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/Electron_Ele25eta2p1WPTight_eff.root')
)


def correct_eid13_mva(pt, abseta):
    if abseta  < 1.479:
        if pt<30:
            return 0.8999
        else:
            return 0.9486
    else:
        if pt<30:
            return 0.7945
        else :
            return 0.8866

def correct_eiso13_mva(pt, abseta):
    if abseta  < 1.479:
        if pt<30:
            return 0.9417
        else:
            return 0.9804
    else:
        if pt<30:
            return 0.9471
        else :
            return 0.9900

def correct_eid13_p1s_mva(pt, abseta): # uncertainty from  https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID_Isolation_ETau_Chann
    if abseta  < 1.479:
        if pt<30:
            return 0.9017
        else:
            return 0.9489
    else:
        if pt<30:
            return 0.8
        else :
            return 0.8867


def correct_eiso13_p1s_mva(pt, abseta):
    if abseta  < 1.479:
        if pt<30:
            return 0.9436
        else:
            return 0.9807
    else:
        if pt<30:
            return 0.9508
        else :
            return 0.9902

def correct_eid13_m1s_mva(pt, abseta):
    if abseta  < 1.479:
        if pt<30:
            return 0.8981
        else:
            return 0.9483
    else:
        if pt<30:
            return 0.789
        else :
            return 0.8865

def correct_eiso13_m1s_mva(pt, abseta):
    if abseta  < 1.479:
        if pt<30:
            return 0.9398
        else:
            return 0.9801
    else:
        if pt<30:
            return 0.9434
        else :
            return 0.9898

            
    


def correct_etaufake(abseta, isTauTight):
    if abseta  < 1.460:
        if isTauTight:
            return 1.322
        else:
            return 1.253
    else:
        if isTauTight:
            return 1.319
        else:
            return 1.046
def correct_etaufake_p1s(abseta, isTauTight):
    if abseta  < 1.460:
        if isTauTight:
            return 1.536
        else:
            return 1.294
    else:
        if isTauTight:
            return 1.624
        else:
            return 1.100
def correct_etaufake_m1s(abseta, isTauTight):
    if abseta  < 1.460:
        if isTauTight:
            return 1.108
        else:
            return 1.212
    else:
        if isTauTight:
            return 1.014
        else:
            return 0.992


       
def correct_eid15_mva(pt, eta):
    if eta  < -1.566:
        if pt<30:
            return 0.98
        elif pt<40: 
            return 0.97
        elif pt < 50 :
            return 0.99
        else:
            return 0.98
    elif eta  < -0.8 and eta > -1.4442:
        if pt<30:
            return 0.91
        elif pt<40: 
            return 0.97
        elif pt < 50 :
            return 0.98
        else:
            return 0.96
    elif eta  < 0 and eta > -0.80:
        if pt<30:
            return 0.95
        elif pt<40: 
            return 0.95
        elif pt < 50 :
            return 0.97
        else:
            return 0.97
    elif eta  < 0.8 and eta > 0:
        if pt<30:
            return 0.99
        elif pt<40: 
            return 0.97
        elif pt < 50 :
            return 0.97
        else:
            return 0.99
    elif eta >0.8 and eta < 1.4442:
        if pt<30:
            return 0.99
        elif pt<40: 
            return 0.95
        elif pt < 50 :
            return 0.98
        else:
            return 0.97
    elif eta >1.566 :
        if pt<30:
            return 0.95
        elif pt<40: 
            return 0.96
        elif pt < 50 :
            return 0.99
        else:
            return 0.99
    else:
        return 1.


def correct_eid15_p1s_mva(pt, eta):
    
    if eta  < -1.566:
        if pt<30:
            return 1.
        elif pt<40: 
            return 0.98
        elif pt < 50 :
            return 1.
        else:
            return 1.
    elif eta  < -0.8 and eta > -1.4442:
        if pt<30:
            return 0.93
        elif pt<40: 
            return 0.98
        elif pt < 50 :
            return 0.99
        else:
            return 0.97
    elif eta  < 0 and eta > -0.80:
        if pt<30:
            return 0.97
        elif pt<40: 
            return 0.98
        elif pt < 50 :
            return 0.98
        else:
            return 0.98
    elif eta  < 0.8 and eta > 0:
        if pt<30:
            return 1.01
        elif pt<40: 
            return 0.98
        elif pt < 50 :
            return 0.98
        else:
            return 1.
    elif eta >0.8 and eta < 1.4442:
        if pt<30:
            return 1.01
        elif pt<40: 
            return 0.96
        elif pt < 50 :
            return 0.99
        else:
            return 0.98
    elif eta >1.566 :
        if pt<30:
            return 0.97
        elif pt<40: 
            return 0.97
        elif pt < 50 :
            return 1.0
        else:
            return 1.01
    else:
        return 1.


def correct_eid15_m1s_mva(pt, eta):
    if eta  < -1.566:
        if pt<30:
            return 0.96
        elif pt<40: 
            return 0.96
        elif pt < 50 :
            return 0.98
        else:
            return 0.96
    elif eta  < -0.8 and eta > -1.4442:
        if pt<30:
            return 0.89
        elif pt<40: 
            return 0.96
        elif pt < 50 :
            return 0.97
        else:
            return 0.95
    elif eta  < 0 and eta > -0.80:
        if pt<30:
            return 0.93
        elif pt<40: 
            return 0.92
        elif pt < 50 :
            return 0.96
        else:
            return 0.96
    elif eta  < 0.8 and eta > 0:
        if pt<30:
            return 0.97
        elif pt<40: 
            return 0.96
        elif pt < 50 :
            return 0.96
        else:
            return 0.98
    elif eta >0.8 and eta < 1.4442:
        if pt<30:
            return 0.97
        elif pt<40: 
            return 0.94
        elif pt < 50 :
            return 0.97
        else:
            return 0.96
    elif eta >1.566 :
        if pt<30:
            return 0.93
        elif pt<40: 
            return 0.95
        elif pt < 50 :
            return 0.98
        else:
            return 0.98
    else:
        return 1.
