'''

Dataset definitions for 8TeV

Author: Evan K. Friis, UW Madison

'''

from datacommon import square, cube, quad, picobarns, br_w_leptons

# Figure this out later.
data_name_map = {}

datadefs = {
   'WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },
   
   'WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_v2' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_v1' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball' : {
   'analyses': ['HTT'],
   'datasetpath' : "/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

   'TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'responsible' : 'Josh',
   },

}

############################################################################
#### Signal datasets                    ####################################
############################################################################
for mass in range(80,150, 10) + range(160, 220, 20) + range(250, 550, 50) + range(600, 1100, 100) :
   datadefs['SUSYGluGluToHToTauTau_M-%i_8TeV-pythia6-tauola' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/SUSYGluGluToHToTauTau_M-%i_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
      'responsible' : 'Josh',
      }
   datadefs['SUSYBBHToTauTau_M-%i_8TeV-pythia6-tauola' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/SUSYBBHToTauTau_M-%i_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
      'responsible' : 'Josh',
      }

for mass in range(110, 165, 5) :
   datadefs['GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
      'responsible' : 'Josh',
      }
   datadefs['VBF_HToTauTau_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/VBF_HToTauTau_M-%i_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
      'responsible' : 'Josh',
      }
   datadefs['WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
      'responsible' : 'Josh',
      }

for mass in range(115, 131) + range(145, 155, 5) + range(180, 220, 20) + range(250, 300, 50) + range(300, 375, 25) + range(400, 650, 50) :
   datadefs['GluGluToHToZZTo4L_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HZZ'],
      'datasetpath': "/GluGluToHToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM" % mass,
      'pu' : 'S7',
      'x_sec' : -999,
      'responsible' : 'Austin',
      }


# Add data files
def build_data_set(pd, analyses, who):
   subsample_dict = {
      'data_%s_Run2012A_13Jul2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012A-13Jul2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON.txt",
      'firstRun' : 190456,
      'lastRun' : 193621,
      'analyses' : analyses,
      'responsible' : who,
      },
      'data_%s_Run2012B_13Jul2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012B-13Jul2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON.txt",
      'firstRun' : 193834,
      'lastRun' : 196531,
      'analyses' : analyses,
      'responsible' : who,
      },
      'data_%s_Run2012C_PromptReco_v2_Run198934_201264' % pd : {
      'datasetpath' : "/%s/Run2012C-PromptReco-v2/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
      'firstRun' : 198934,
      'lastRun' : 201264,
      'analyses' : analyses,
      'responsible' : who,
      },
      'data_%s_Run2012C_24Aug2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012C-24Aug2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
      'firstRun' : 198022,
      'lastRun' : 198523,
      'analyses' : analyses,
      'responsible' : who,
      },
    }
   sample_dict = {
      'data_%s' % pd : subsample_dict.keys()
      }
   return subsample_dict, sample_dict

# Build all the PDs we use
data_DoubleMu, list_DoubleMu = build_data_set('DoubleMu', ['VH', 'Mu','4L'], 'tapas')
datadefs.update(data_DoubleMu)
data_name_map.update(list_DoubleMu)

data_MuEG, list_MuEG = build_data_set('MuEG', ['VH', 'HTT', 'Mu'], 'tapas')
datadefs.update(data_MuEG)
data_name_map.update(list_MuEG)

data_DoubleE, list_DoubleE = build_data_set('DoubleElectron', ['VH','4L'], 'Ian')
datadefs.update(data_DoubleE)
data_name_map.update(list_DoubleE)

data_SingleMu, list_SingleMu = build_data_set('SingleMu', ['Tau', 'Mu', 'Wbb'], 'tapas')
datadefs.update(data_SingleMu)
data_name_map.update(list_SingleMu)

data_SingleElectron, list_SingleElectron = build_data_set('SingleElectron', ['Tau', 'E', 'Wjets'], 'Maria')
datadefs.update(data_SingleElectron)
data_name_map.update(list_SingleElectron)

data_TauPlusX, list_TauPlusX = build_data_set('TauPlusX', ['HTT', ], 'Josh')
datadefs.update(data_TauPlusX)
data_name_map.update(list_TauPlusX)
