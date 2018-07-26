"""
Data definitions for 13 TeV samples.
"""
from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli
from string import Template
try:
    from yellowhiggs import xs, br, xsbr
    br(130.0, 'WW')
except:

    def br(*args, **kwargs):
        return -99


    def xs(*args, **kwargs):
        return (-99, (-99, 99))


    def xsbr(*args, **kwargs):
        return (-99, (-99, 99))


data_name_map = {}
datadefs = {}


datadefs['GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
'analyses': ['LFV'],
 'datasetpath': '/GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAOD',
 'x_sec': 30.52*0.01
}
datadefs['VBF_LFV_HToMuTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
'analyses': ['LFV'],
 'datasetpath': '/VBF_LFV_HToMuTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAOD',
 'x_sec': 3.861*0.01
}


datadefs['DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 5343
}
datadefs['DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14_ext1-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 5343
}
datadefs['DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v2'] = {
 'analyses': ['LFV'],
 'datasetpath': '/DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 81880
}
datadefs['DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 877.8
}
datadefs['DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v2'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 877.8
}
datadefs['DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14_ext1-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 877.8
}
datadefs['DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 304.4
}
datadefs['DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14_ext1-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 304.4
}
datadefs['DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14_ext1-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 111.5
}
datadefs['DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': 'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 44.03
}


datadefs['WW_TuneCP5_13TeV-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datsetpath': '/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 75.8
}
datadefs['WZ_TuneCP5_13TeV-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datsetpath': '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 27.6
}
datadefs['ZZ_TuneCP5_13TeV-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datsetpath': '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 12.14
}


# datadefs['VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8_v6-v1'] = {'analyses': ['4L'],
#  'datasetpath': '/WWTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
#  'pu': 'Asympt25ns',
#  'calibrationTarget': 'ICHEP2016',
#  'x_sec': 11.95}
# datadefs['VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8_v6_ext1-v1'] = {'analyses': ['4L'],
#  'datasetpath': '/WWTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM',
#  'pu': 'Asympt25ns',
#  'calibrationTarget': 'ICHEP2016',
#  'x_sec': 11.95}


datadefs['WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_v14_ext1-v2'] = {
 'analyses': ['LFV'],
 'datasetpath': '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 52940
}
datadefs['WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v2'] = {
 'analyses': ['LFV'],
 'datasetpath': '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 52940
}
datadefs['W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v3'] = {
 'analyses': ['LFV'],
 'datasetpath': '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 8111
}
datadefs['W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v4'] = {
 'analyses': ['LFV'],
 'datasetpath': '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v4/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 2793
}
datadefs['W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 992.5
}
datadefs['W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 544.3
}


datadefs['TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 831.76 #687.1
}
datadefs['TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 88.29
}
datadefs['TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_v14-v2'] = {
 'analyses': ['LFV'],
 'datasetpath': '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 365.34
}
datadefs['TTToHadronic_TuneCP5_13TeV-powheg-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 377.96
}


datadefs['GluGluHToTauTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 30.52*0.0627
}
datadefs['VBFHToTauTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 3.861*0.0627
}


datadefs['ZHToTauTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/ZHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 0.7524*0.0627
}
datadefs['ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 0.5269*0.067
}
datadefs['WminusHToTauTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/WminusHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 0.5331*0.0627
}
datadefs['WplusHToTauTau_M125_13TeV_powheg_pythia8_v14-v1'] = {
 'analyses': ['LFV'],
 'datasetpath': '/WplusHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 0.851*0.0627
}


datadefs['data_SingleMuon_Run2015C_05Oct2015_25ns'] = {'datasetpath': '/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt',
 'firstRun': 254227,
 'lastRun': 254914,
 'analyses': ['HZZ'],
 'calibrationTarget': 'Moriond2015'}
datadefs['data_SingleMuon_Run2015D_05Oct2015_25ns'] = {'datasetpath': '/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt',
 'firstRun': 256630,
 'lastRun': 258158,
 'analyses': ['HZZ'],
 'calibrationTarget': 'Moriond2015'}
datadefs['data_SingleMuon_Run2015D_PromptReco-v4_25ns'] = {'datasetpath': '/SingleMuon/Run2015D-PromptReco-v4/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt',
 'firstRun': 258486,
 'lastRun': 260403,
 'analyses': ['HZZ'],
 'calibrationTarget': 'Moriond2015'}
datadefs['data_SingleMuon_Run2016B_PromptReco-v2_25ns'] = {'datasetpath': '/SingleMuon/Run2016B-PromptReco-v2/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_271036-273450_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt',
 'firstRun': 272007,
 'lastRun': 273450,
 'analyses': ['HZZ'],
 'calibrationTarget': 'Moriond2015'}
datadefs['data_SingleMuon_Run2016C'] = {'datasetpath': '/SingleMuon/Run2016C-PromptReco-v2/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt',
 'firstRun': 275420,
 'lastRun': 276283,
 'analyses': ['HET'],
 'calibrationTarget': 'ICHEP2016'}
datadefs['data_SingleMuon_Run2016D'] = {'datasetpath': '/SingleMuon/Run2016D-PromptReco-v2/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.tx',
 'firstRun': 276315,
 'lastRun': 276811,
 'analyses': ['HET'],
 'calibrationTarget': 'ICHEP2016'}
datadefs['data_SingleMuon_Run2016E'] = {'datasetpath': '/SingleMuon/Run2016E-PromptReco-v2/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt',
 'firstRun': 276830,
 'lastRun': 277420,
 'analyses': ['HET'],
 'calibrationTarget': 'ICHEP2016'}
datadefs['data_SingleMuon_Run2016F'] = {'datasetpath': '/SingleMuon/Run2016E-PromptReco-v2/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt',
 'firstRun': 277856,
 'lastRun': 278349,
 'analyses': ['HET'],
 'calibrationTarget': 'ICHEP2016'}
datadefs['data_SingleMuon_Run2016G'] = {'datasetpath': '/SingleMuon/Run2016E-PromptReco-v2/MINIAOD',
 'lumi_mask': 'FinalStateAnalysis/RecoTools/data/masks/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt',
 'firstRun': 278802,
 'lastRun': 280385,
 'analyses': ['HET'],
 'calibrationTarget': 'ICHEP2016'}



datadefs['ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_v14-v1'] = {
 'analyses': ['MuTau'],
 'datasetpath': '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 67.91
}
datadefs['ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_v14-v1'] = {
 'analyses': ['MuTau'],
 'datasetpath': '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 113.3
}
datadefs['ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_v14-v1'] = {
 'analyses': ['MuTau'],
 'datasetpath': '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 34.97
}
datadefs['ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_v14-v1'] = {
 'analyses': ['MuTau'],
 'datasetpath': '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
 'pu': '2017',
 'calibrationTarget': 'RunIIFall17MiniAODv2',
 'x_sec': 34.91
}


if __name__ == '__main__':
    query_cli(datadefs)
