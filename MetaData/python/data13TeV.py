'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli
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
    'datasetpath': 'GluGlu_LFV_HToETau_M120_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748,#xs(14,125,'vbf')[0],
}
datadefs["GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 43.92 ,
}
datadefs["VBF_LFV_HToETau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748 ,
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
    'x_sec': -999. ,
}

datadefs["WZ_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}
datadefs["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 6025.2 ,
}
datadefs["ZZ_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}
datadefs["WW_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}
datadefs["WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}
datadefs["TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}
datadefs["GluGluHToTauTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-AsymptFlat10to50bx25Raw_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 43.92*yellowhiggs.br(125, 'tautau')[0] ,
}
datadefs["VBFHToTauTau_M125_13TeV_powheg_pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': 3.748*yellowhiggs.br(125, 'tautau')[0],
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



datadefs["WZ_TuneCUETP8M1_13TeV-pythia8"] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}
datadefs[""] = {
    'analyses': ['4L'],
    'datasetpath': '',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': -999. ,
}

datadefs["DYJets_M50-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 6025.2*picobarns,
}
datadefs["TTJets-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 689.1*picobarns, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}
datadefs["ggHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 43.62*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["ZZTo4L-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 15.4*picobarns,
}
datadefs["WZTo3LNu-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': -999,
}


if __name__=="__main__":
    query_cli(datadefs)
