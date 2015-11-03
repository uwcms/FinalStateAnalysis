#from FinalStateAnalysis.Utilities.rootbindings import ROOT
from correctionloader import CorrectionLoader
import os
#ROOT.gSystem.Load("libFinalStateAnalysisTagAndProbe")


def correct_hamburg_e(pt, abseta):

    if abseta > 0.000000 and abseta <= 0.800000 :
        if pt > 10 and pt<= 15 :
            return 0.834832 
            
        if pt > 15 and pt<= 20 :
            return 0.951007 
            
        if pt > 20 and pt<= 25 :
            return 0.985581 
                
        if pt > 25 and pt<= 30 :
            return 0.949936 

        if pt > 30 and pt<= 35 :
            return 0.966418 

        if pt > 35 :
            return 0.989763 

    if abseta > 0.800000 and abseta <= 1.500000 :
        if pt > 10 and pt<= 15 :
            return 0.921214 

        if pt > 15 and pt<= 20 :
            return 1.006625 

        if pt > 20 and pt<= 25 :
            return 0.936736 

        if pt > 25 and pt<= 30 :
            return 0.924828 

        if pt > 30 and pt<= 35 :
            return 0.952658 

        if pt > 35 :
            return 0.962767 

    if abseta > 1.500000 and abseta <= 2.300000 :
        if pt > 10 and pt<= 15 :
            return 0.937268 
            
        if pt > 15 and pt<= 20 :
            return 1.037564 

        if pt > 20 and pt<= 25 :
            return 0.975177 

        if pt > 25 and pt<= 30 :
            return 0.962375 

        if pt > 30 and pt<= 35 :
            return 0.962669 

        if pt > 35 :
            return 0.975031 

single_ele_wp80 = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/efficiency-Run2012ABCD-WP80ToHLTEle.txt')
)
single_ele_mva = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/ScaleFactors_MySelToHLT_efficiency.txt')
)
correct_eEmb = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/electronEmbeddedScaleFactor.txt')
)
single_ele_eff_mva = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/EfficiencySingleElectron_MySelToHLT_efficiency.txt')
)

scale_eleId_hww = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/scaleFactor-Run2012ABCD-GsfElectronToId.txt')
)
scale_eleIso_hww = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/scaleFactor-Run2012ABCD-RecoToIso.txt')
)

scale_elereco_hww = CorrectionLoader(
    os.path.join(os.environ['fsa'], 'TagAndProbe/data/scaleFactor-Run2012ABCD-SCToElectron.txt')
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


       
