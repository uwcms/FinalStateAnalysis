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
    'datasetpath': '/VBF_LFV_HToMuTau_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 3.782*0.01,#xs(14,125,'vbf')[0],            
}

datadefs["GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
      'datasetpath': '/GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 48.57*0.01,
}
datadefs["GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
      'datasetpath': '/GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
      'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 48.57*0.01 ,
}
datadefs["VBF_LFV_HToETau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
      'datasetpath': '/VBF_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
      'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 3.782*0.01 ,
}
datadefs["VBF_LFV_HToEMu_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToEMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.782*0.01 ,
}
datadefs["GluGlu_LFV_HToEMu_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToEMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 48.57*0.01 ,
}

datadefs["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
      'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec':  5765.4,
}
datadefs["DYJetsToTauTau_ForcedMuDecay_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToTauTau_ForcedMuDecay_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec':  6025.2,
}

datadefs["WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
      'datasetpath': '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
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
      'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 6025.2 ,
}
datadefs["DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 18610.0 ,
}
###new stuff

datadefs["DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptoptic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 1245.38 ,
}



datadefs["DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptoptic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec':409.34,
}


datadefs["DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptoptic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec':125.21 ,
}



datadefs["DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptoptic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 67.40,
}


datadefs["DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec':181.30, 
}
#147.40*1.23(k-fac)

datadefs["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 50.42,
}
#40.99*1.23(k-fac)

datadefs["DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec':6.98, 
    
}
#5.678*1.23(k-fac)

datadefs["DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec':2.70, 
}
#2.198*1.23(k-fac)
datadefs["ZZ_TuneCUETP8M1_13TeV-pythia8"]={
      'analyses':['LFV'],
      'datsetpath':'/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM',
      'pu':'asymptotic_2016',
      'calibrationTarget': 'PUSpring16',
      'x_sec': 16.523,
      }
datadefs["WZ_TuneCUETP8M1_13TeV-pythia8"] = {
      'analyses': ['4L'],
      'datasetpath': '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
      'pu':'asymptotic_2016',
      'calibrationTarget': 'PUSpring16',
      'x_sec':  47.13, #from https://cmsweb.cern.ch/das/request?input=mcm%20prepid=TOP-RunIISummer15GS-00001
}

datadefs["WW_TuneCUETP8M1_13TeV-pythia8"] = {
      'analyses': ['4L'],
      'datasetpath': '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
      'pu':'asymptotic_2016',
      'calibrationTarget': 'PUSpring16',
      'x_sec':  118.7, #from https://cmsweb.cern.ch/das/request?input=mcm%20prepid=TOP-RunIISummer15GS-00001
}
datadefs["WWTo2L2Nu_13TeV-powheg"] = {
    'analyses': ['4L'],
    'datasetpath': '/WWTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec':  12.178, #from https://cmsweb.cern.ch/das/request?input=mcm%20prepid=TOP-RunIISummer15GS-00001
}

datadefs["WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 61526.7 ,
}

datadefs["W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': 'W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 11699.85 ,
}

datadefs["W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath':'W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3804.85 ,
}

datadefs["W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath':'W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM', 
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 1155.31 ,
}

datadefs["W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath':'W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM', 
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 587.57 ,
}



datadefs["TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 809
}
datadefs["TT_TuneCUETP8M1_13TeV-powheg-pythia8-evtgen"] = {
    'analyses': ['4L'],
    'datasetpath': '/TT_TuneCUETP8M1_13TeV-powheg-pythia8-evtgen/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 809,
}
datadefs["TT_TuneCUETP8M1_13TeV-powheg-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext*-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 809,
}
datadefs["TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 809,
}
datadefs["TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 809,
}
datadefs["TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 0.009103,
}
datadefs["WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph"] = {
    'analyses': ['4L'],
    'datasetpath': '/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 0.009103,#wrong***
}

datadefs["WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 495.36,# needs to be cross checked
}

datadefs["WGstarToLNuEE_012Jets_13TeV-madgraph"] = {
    'analyses': ['4L'],
    'datasetpath': '/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 11.7,#needs to be cross checked
}

datadefs["WGstarToLNuMuMu_012Jets_13TeV-madgraph"] = {
    'analyses': ['4L'],
    'datasetpath': '/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 3.8,#neeeds to be cross checked
}

datadefs["WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph"] = {
    'analyses': ['4L'],
    'datasetpath': '/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'ICHEP2016',
    'x_sec': 0.009103,#wrong******
}
datadefs["GluGluHToTauTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 44.14*0.0627,
}
datadefs["VBFHToTauTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
      'datasetpath': '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
    'pu': 'asymptotic_2016',
    'calibrationTarget': 'RunIISpring16MiniAODv1',
    'x_sec': 3.782*0.0627,
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
datadefs['data_SingleMuon_Run2016B_PromptReco-v2_25ns'] = {
   'datasetpath' : "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-273450_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
   'firstRun' : 272007,
   'lastRun' : 273450,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2015'
   }
datadefs['data_SingleMuon_Run2016C'] = {
      'datasetpath' : "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.tx",
      'firstRun' : 275420,
      'lastRun' : 276283,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleMuon_Run2016D'] = {
      'datasetpath' : "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.tx",
      'firstRun' : 276315,
      'lastRun' : 276811,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleMuon_Run2016E'] = {
      'datasetpath' : "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 276830,
      'lastRun' : 277420,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleMuon_Run2016F'] = {
      'datasetpath' : "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 277856,
      'lastRun' : 278349,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleMuon_Run2016G'] = {
      'datasetpath' : "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 278802,
      'lastRun' : 280385,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016H'] = {
      'datasetpath' : "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 280919,
      'lastRun' : 284044,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }



datadefs['data_SingleElectron_Run2016B'] = {
      'datasetpath' : "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.tx",
      'firstRun' : 273150,
      'lastRun' : 273450,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016C'] = {
      'datasetpath' : "/SingleElectron/Run2016C-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.tx",
      'firstRun' : 275420,
      'lastRun' : 276283,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016D'] = {
      'datasetpath' : "/SingleElectron/Run2016D-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.tx",
      'firstRun' : 276315,
      'lastRun' : 276811,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016E'] = {
      'datasetpath' : "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 276830,
      'lastRun' : 277420,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016F'] = {
      'datasetpath' : "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 277856,
      'lastRun' : 278349,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016G'] = {
      'datasetpath' : "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 278802,
      'lastRun' : 280385,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
   }
datadefs['data_SingleElectron_Run2016H'] = {
      'datasetpath' : "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD",
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt",
      'firstRun' : 280919,
      'lastRun' : 284044,
      'analyses' : ['HET'],
      'calibrationTarget':'ICHEP2016'
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
    'x_sec': 48.57*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
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
    'x_sec': 35.6, ##put the correctnumber
}
datadefs["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
      'analyses': ['mutau'],
      'datasetpath': '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
      'pu': 'asymptotic_2016',
      'calibrationTarget': 'Phys14DR',
      'x_sec': 35.6 , ##put the correctnumber
}
datadefs["ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = {
      'analyses': ['mutau'],
      'datasetpath': '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
      'pu': 'asymptotic_2016',
      'calibrationTarget': 'Phys14DR',
      'x_sec': 35.6 , ##put the correctnumber
}

if __name__=="__main__":
    query_cli(datadefs)
