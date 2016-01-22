'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli
from string import Template

try:
      from yellowhiggs import xs, br, xsbr
      br(130.,'WW')
except:
      #print "warning: yellowhiggs error"
      #define / override functions to avoid crashes
      def br(*args, **kwargs):
            return -99
      def xs(*args, **kwargs):
            return -99, (-99, 99)
      def xsbr(*args, **kwargs):
            return -99, (-99, 99)

data_name_map = {}

datadefs = {}

datadefs["VBF_LFV_HToMuTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': 'GluGlu_LFV_HToMuTau_M120_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748*0.01,#xs(14,125,'vbf')[0],
}
datadefs["GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 43.92*0.01,
}
datadefs["GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 43.92*0.01 ,
}
datadefs["VBF_LFV_HToETau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748*0.01 ,
}
datadefs["VBF_LFV_HToEMu_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToEMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748*0.01 ,
}
datadefs["GluGlu_LFV_HToEMu_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToEMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 43.92*0.01 ,
}

datadefs["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec':  6025.2,
}
datadefs["WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 61526.7 ,
}

datadefs["WZ_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 22.82 , #from https://cmsweb.cern.ch/das/request?input=mcm%20prepid=TOP-RunIISummer15GS-00002
}
datadefs["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 6025.2 ,
}
datadefs["DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 18610.0 ,
}
datadefs["ZZ_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': 10.32 , #from https://cmsweb.cern.ch/das/request?input=mcm%20prepid=TOP-RunIISummer15GS-00003
}
datadefs["WW_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec':  63.21, #from https://cmsweb.cern.ch/das/request?input=mcm%20prepid=TOP-RunIISummer15GS-00001
}
datadefs["WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 61526.7 ,
}
datadefs["TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 831.76,
}
datadefs["TT_TuneCUETP8M1_13TeV-powheg-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 831.76,
}
datadefs["TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 831.76,
}
datadefs["TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 831.76,
}
datadefs["TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 0.009103,
}
datadefs["GluGluHToTauTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-AsymptFlat10to50bx25Raw_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 43.92*br(125, 'tautau')[0] ,
}
datadefs["VBFHToTauTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748*br(125, 'tautau')[0],
}
datadefs['data_SingleElectron_Run2015C_05Oct2015_25ns'] = {
   'datasetpath' : "/SingleElectron/Run2015C_25ns-05Oct2015-v1/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt",
   'firstRun' : 254227,
   'lastRun' : 254914,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }

datadefs['data_SingleElectron_Run2015D_05Oct2015_25ns'] = {
   'datasetpath' : "/SingleElectron/Run2015D-05Oct2015-v1/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt",
   'firstRun' : 256630,
   'lastRun' : 258158,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }

datadefs['data_SingleElectron_Run2015D_PromptReco-v4_25ns'] = {
   'datasetpath' : "/SingleElectron/Run2015D-PromptReco-v4/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt",
   'firstRun' : 258486,
   'lastRun' : 260403,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }

datadefs['data_SingleMuon_Run2015C_05Oct2015_25ns'] = {
   'datasetpath' : "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt",
   'firstRun' : 254227,
   'lastRun' : 254914,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }

datadefs['data_SingleMuon_Run2015D_05Oct2015_25ns'] = {
   'datasetpath' : "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt",
   'firstRun' : 256630,
   'lastRun' : 258158,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }

datadefs['data_SingleMuon_Run2015D_PromptReco-v4_25ns'] = {
   'datasetpath' : "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt",
   'firstRun' : 258486,
   'lastRun' : 260403,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }



datadefs["DYJets_M50-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 6025.2,
}
datadefs["TTJets-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 689.1, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}
datadefs["ggHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 43.62*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["ZZTo4L-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 15.4,
}
datadefs["WZTo3LNu-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': -999,
}

datadefs["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"] = {
    'analyses': ['mutau'],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 0.1, ##put the correctnumber
}
datadefs["ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"] = {
    'analyses': ['mutau'],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 216.99, ##put the correctnumber
}
datadefs["ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
    'analyses': ['mutau'],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 80.95, ##put the correctnumber
}
datadefs["ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
    'analyses': ['mutau'],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 103.2, ##put the correctnumber
}

datadefs["ST_tW_antitop_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
      'analyses': ['mutau'],
      'datasetpath': '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
      'pu': '20bx25',
      'calibrationTarget': 'Phys14DR',
      'x_sec': 38.09, ##put the correctnumber
}
datadefs["ST_tW_top_5f_DS_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
    'analyses': ['mutau'],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 38.09, ##put the correctnumber
}
datadefs["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
    'analyses': ['mutau'],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 38.09
      , ##put the correctnumber
}

if __name__=="__main__":
    query_cli(datadefs)
