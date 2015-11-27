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
#muon iso: NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1




def correct_muiso15_mva(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 1.006
 	elif pt < 30:
	   return 1.002
 	elif pt < 40 :
	   return 1.001
	elif pt < 50:
	   return 1.001
	elif pt < 60:
	   return 0.998
	else:
	   return 1.001
    elif abseta<1.2:
        if pt <25.0:
           return 0.995
 	elif pt < 30:
	   return 0.999
 	elif pt < 40 :
	   return 1.000
	elif pt < 50:
	   return 1.002
	elif pt < 60:
	   return 1.001
	else:
	   return 1.005
    elif abseta<2.1:
        if pt <25.0:
           return 0.995
 	elif pt < 30:
	   return 1.001
 	elif pt < 40 :
	   return 1.001
	elif pt < 50:
	   return 1.001
	elif pt < 60:
	   return 0.997
	else:
	   return 1.001
    elif abseta<2.4:
        if pt <25.0:
           return 0.971
 	elif pt < 30:
	   return 0.992
 	elif pt < 40 :
	   return 1.000
	elif pt < 50:
	   return 1.004
	elif pt < 60:
	   return 1.003
	else:
	   return 1.001






def correct_muiso15_p1s_mva(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 1.012
 	elif pt < 30:
	   return 1.005
 	elif pt < 40 :
	   return 1.002
	elif pt < 50:
	   return 1.003
	elif pt < 60:
	   return 0.999
	else:
	   return 1.003
    elif abseta<1.2:
        if pt <25.0:
           return 1.003
 	elif pt < 30:
	   return 1.004
 	elif pt < 40 :
	   return 1.002
	elif pt < 50:
	   return 1.003
	elif pt < 60:
	   return 1.003
	else:
	   return 1.007
    elif abseta<2.1:
        if pt <25.0:
           return 0.999
 	elif pt < 30:
	   return 1.004
 	elif pt < 40 :
	   return 1.002
	elif pt < 50:
	   return 1.001
	elif pt < 60:
	   return 0.998
	else:
	   return 1.002
    elif abseta<2.4:
        if pt <25.0:
           return 0.979
 	elif pt < 30:
	   return 0.998
 	elif pt < 40 :
	   return 1.003
	elif pt < 50:
	   return 1.004
	elif pt < 60:
	   return 1.005
	else:
	   return 1.004







def correct_muiso15_m1s_mva(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 1.001
 	elif pt < 30:
	   return 0.999
 	elif pt < 40 :
	   return 1.000
	elif pt < 50:
	   return 0.999
	elif pt < 60:
	   return 0.997
	else:
	   return 1.000
    elif abseta<1.2:
        if pt <25.0:
           return 0.987
 	elif pt < 30:
	   return 0.994
 	elif pt < 40 :
	   return 0.998
	elif pt < 50:
	   return 1.001
	elif pt < 60:
	   return 1.000
	else:
	   return 1.003
    elif abseta<2.1:
        if pt <25.0:
           return 0.991
 	elif pt < 30:
	   return 0.998
 	elif pt < 40 :
	   return 1.000
	elif pt < 50:
	   return 1.000
	elif pt < 60:
	   return 0.996
	else:
	   return 1.000
    elif abseta<2.4:
        if pt <25.0:
           return 0.963
 	elif pt < 30:
	   return 0.987
 	elif pt < 40 :
	   return 0.998
	elif pt < 50:
	   return 1.003
	elif pt < 60:
	   return 1.000
	else:
	   return 0.999









#p2 currently is for single muon trigger ,run under 257819
def correct_mutrig15_mva_p2(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 0.875
 	elif pt < 30:
	   return 0.921
 	elif pt < 40 :
	   return 0.958
	elif pt < 50:
	   return 0.977
	elif pt < 60:
	   return 0.985
	else:
	   return 0.976
    elif abseta<1.2:
        if pt <25.0:
           return 0.930
 	elif pt < 30:
	   return 0.966
 	elif pt < 40 :
	   return 0.972
	elif pt < 50:
	   return 0.981
	elif pt < 60:
	   return 0.989
	else:
	   return 0.981
    elif abseta<2.1:
        if pt <25.0:
           return 0.968
 	elif pt < 30:
	   return 0.981
 	elif pt < 40 :
	   return 0.973
	elif pt < 50:
	   return 0.977
	elif pt < 60:
	   return 0.979
	else:
	   return 0.981
    elif abseta<2.4:
        if pt <25.0:
           return 0.989
 	elif pt < 30:
	   return 1.001
 	elif pt < 40 :
	   return 1.001
	elif pt < 50:
	   return 1.003
	elif pt < 60:
	   return 1.006
	else:
	   return 1.004



def correct_mutrig15_p1s_mva_p2(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 0.882
 	elif pt < 30:
	   return 0.925
 	elif pt < 40 :
	   return 0.959
	elif pt < 50:
	   return 0.978
	elif pt < 60:
	   return 0.987
	else:
	   return 0.979
    elif abseta<1.2:
        if pt <25.0:
           return 0.942
 	elif pt < 30:
	   return 0.973
 	elif pt < 40 :
	   return 0.975
	elif pt < 50:
	   return 0.983
	elif pt < 60:
	   return 0.993
	else:
	   return 0.987
    elif abseta<2.1:
        if pt <25.0:
           return 0.975
 	elif pt < 30:
	   return 0.985
 	elif pt < 40 :
	   return 0.975
	elif pt < 50:
	   return 0.980
	elif pt < 60:
	   return 0.982
	else:
	   return 0.985
    elif abseta<2.4:
        if pt <25.0:
           return 1.007
 	elif pt < 30:
	   return 1.011
 	elif pt < 40 :
	   return 1.006
	elif pt < 50:
	   return 1.008
	elif pt < 60:
	   return 1.015
	else:
	   return 1.015



def correct_mutrig15_m1s_mva_p2(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 0.868
 	elif pt < 30:
	   return 0.917
 	elif pt < 40 :
	   return 0.957
	elif pt < 50:
	   return 0.976
	elif pt < 60:
	   return 0.983
	else:
	   return 0.974
    elif abseta<1.2:
        if pt <25.0:
           return 0.917
 	elif pt < 30:
	   return 0.959
 	elif pt < 40 :
	   return 0.969
	elif pt < 50:
	   return 0.979
	elif pt < 60:
	   return 0.985
	else:
	   return 0.975
    elif abseta<2.1:
        if pt <25.0:
           return 0.961
 	elif pt < 30:
	   return 0.977
 	elif pt < 40 :
	   return 0.971
	elif pt < 50:
	   return 0.974
	elif pt < 60:
	   return 0.976
	else:
	   return 0.977
    elif abseta<2.4:
        if pt <25.0:
           return 0.971
 	elif pt < 30:
	   return 0.991
 	elif pt < 40 :
	   return 0.996
	elif pt < 50:
	   return 0.999
	elif pt < 60:
	   return 0.998
	else:
	   return 0.993







def correct_mutrig15_mva_p3(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 1.013 
 	elif pt < 30:
	   return 1.013
 	elif pt < 40 :
	   return 1.002
	elif pt < 50:
	   return 1.000
	elif pt < 60:
	   return 0.998
	else:
	   return 0.991
    elif abseta<1.2:
        if pt <25.0:
           return 1.035
 	elif pt < 30:
	   return 1.020
 	elif pt < 40 :
	   return 1.009
	elif pt < 50:
	   return 0.999
	elif pt < 60:
	   return 1.003
	else:
	   return 0.985
    elif abseta<2.1:
        if pt <25.0:
           return 1.008
 	elif pt < 30:
	   return 1.004
 	elif pt < 40 :
	   return 0.998
	elif pt < 50:
	   return 0.995
	elif pt < 60:
	   return 0.994
	else:
	   return 0.993
    elif abseta<2.4:
        if pt <25.0:
           return 1.031
 	elif pt < 30:
	   return 1.024
 	elif pt < 40 :
	   return 1.027
	elif pt < 50:
	   return 1.017
	elif pt < 60:
	   return 1.025
	else:
	   return 1.017




def correct_mutrig15_p1s_mva_p3(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 1.017 
 	elif pt < 30:
	   return 1.015
 	elif pt < 40 :
	   return 1.003
	elif pt < 50:
	   return 1.001
	elif pt < 60:
	   return 1.000
	else:
	   return 0.993
    elif abseta<1.2:
        if pt <25.0:
           return 1.044
 	elif pt < 30:
	   return 1.025
 	elif pt < 40 :
	   return 1.011
	elif pt < 50:
	   return 1.001
	elif pt < 60:
	   return 1.006
	else:
	   return 0.989
    elif abseta<2.1:
        if pt <25.0:
           return 1.013
 	elif pt < 30:
	   return 1.007
 	elif pt < 40 :
	   return 0.999
	elif pt < 50:
	   return 0.998
	elif pt < 60:
	   return 0.996
	else:
	   return 0.996
    elif abseta<2.4:
        if pt <25.0:
           return 1.044
 	elif pt < 30:
	   return 1.031
 	elif pt < 40 :
	   return 1.030
	elif pt < 50:
	   return 1.020
	elif pt < 60:
	   return 1.031
	else:
	   return 1.026




def correct_mutrig15_m1s_mva_p3(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 1.009 
 	elif pt < 30:
	   return 1.011
 	elif pt < 40 :
	   return 1.002
	elif pt < 50:
	   return 0.999
	elif pt < 60:
	   return 0.997
	else:
	   return 0.989
    elif abseta<1.2:
        if pt <25.0:
           return 1.027
 	elif pt < 30:
	   return 1.016
 	elif pt < 40 :
	   return 1.007
	elif pt < 50:
	   return 0.998
	elif pt < 60:
	   return 1.000
	else:
	   return 0.981
    elif abseta<2.1:
        if pt <25.0:
           return 1.004
 	elif pt < 30:
	   return 1.001
 	elif pt < 40 :
	   return 0.996
	elif pt < 50:
	   return 0.992
	elif pt < 60:
	   return 0.992
	else:
	   return 0.990
    elif abseta<2.4:
        if pt <25.0:
           return 1.019
 	elif pt < 30:
	   return 1.016
 	elif pt < 40 :
	   return 1.023
	elif pt < 50:
	   return 1.014
	elif pt < 60:
	   return 1.018
	else:
	   return 1.009





def correct_muid15_tight_mva(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 0.972
 	elif pt < 30:
	   return 0.979
 	elif pt < 40 :
	   return 0.987
	elif pt < 50:
	   return 0.987
	elif pt < 60:
	   return 0.982
	else:
	   return 0.981
    elif abseta<1.2:
        if pt <25.0:
           return 0.973
 	elif pt < 30:
	   return 0.981
 	elif pt < 40 :
	   return 0.981
	elif pt < 50:
	   return 0.981
	elif pt < 60:
	   return 0.980
	else:
	   return 0.975
    elif abseta<2.1:
        if pt <25.0:
           return 1.002
 	elif pt < 30:
	   return 0.993
 	elif pt < 40 :
	   return 0.993
	elif pt < 50:
	   return 0.993
	elif pt < 60:
	   return 0.991
	else:
	   return 0.987
    elif abseta<2.4:
        if pt <25.0:
           return 0.995
 	elif pt < 30:
	   return 0.980
 	elif pt < 40 :
	   return 0.980
	elif pt < 50:
	   return 0.977
	elif pt < 60:
	   return 0.980
	else:
	   return 0.930
	 




def correct_muid15_tight_p1s_mva(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 0.976
 	elif pt < 30:
	   return 0.981
 	elif pt < 40 :
	   return 0.988
	elif pt < 50:
	   return 0.987
	elif pt < 60:
	   return 0.984
	else:
	   return 0.983
    elif abseta<1.2:
        if pt <25.0:
           return 0.979
 	elif pt < 30:
	   return 0.984
 	elif pt < 40 :
	   return 0.982
	elif pt < 50:
	   return 0.982
	elif pt < 60:
	   return 0.982
	else:
	   return 0.979
    elif abseta<2.1:
        if pt <25.0:
           return 1.005
 	elif pt < 30:
	   return 0.995
 	elif pt < 40 :
	   return 0.994
	elif pt < 50:
	   return 0.994
	elif pt < 60:
	   return 0.992
	else:
	   return 0.990
    elif abseta<2.4:
        if pt <25.0:
           return 1.002
 	elif pt < 30:
	   return 0.984
 	elif pt < 40 :
	   return 0.982
	elif pt < 50:
	   return 0.979
	elif pt < 60:
	   return 0.985
	else:
	   return 0.940





def correct_muid15_tight_m1s_mva(pt,abseta):
    if abseta< 0.9:
        if pt <25.0:
           return 0.968
 	elif pt < 30:
	   return 0.977
 	elif pt < 40 :
	   return 0.986
	elif pt < 50:
	   return 0.986
	elif pt < 60:
	   return 0.981
	else:
	   return 0.978
    elif abseta<1.2:
        if pt <25.0:
           return 0.967
 	elif pt < 30:
	   return 0.977
 	elif pt < 40 :
	   return 0.979
	elif pt < 50:
	   return 0.980
	elif pt < 60:
	   return 0.977
	else:
	   return 0.971
    elif abseta<2.1:
        if pt <25.0:
           return 0.999
 	elif pt < 30:
	   return 0.991
 	elif pt < 40 :
	   return 0.992
	elif pt < 50:
	   return 0.992
	elif pt < 60:
	   return 0.989
	else:
	   return 0.984
    elif abseta<2.4:
        if pt <25.0:
           return 0.989
 	elif pt < 30:
	   return 0.976
 	elif pt < 40 :
	   return 0.978
	elif pt < 50:
	   return 0.975
	elif pt < 60:
	   return 0.975
	else:
	   return 0.920
	 


  
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
