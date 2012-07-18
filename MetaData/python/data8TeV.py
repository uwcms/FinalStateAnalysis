'''

Dataset definitions for 8TeV

Author: Evan K. Friis, UW Madison

'''

from datacommon import square, cube, quad, picobarns, br_w_leptons

# Figure this out later.
data_name_map = {}

datadefs = {
    'WplusJets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'x_sec': 36257.2,
        'responsible' : 'Maria',
    },
    'Zjets_M50' : {
        'analyses': ['HTT'],
        'datasetpath': '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',
        'pu': 'S7',
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
        'x_sec': 3503.71,
        'responsible' : 'Josh',
    },
    'TTplusJets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/TTJets_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V5-v1/AODSIM',
        'pu': 'S7',
        'x_sec': 225.197,
        'responsible' : 'Evan',
    },
    'WZJetsTo3LNu_pythia' : {
        'analyses': ['HTT'],
        'datasetpath': '/WZTo3LNu_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'x_sec': 32.3161*3*0.03365*(0.1075+0.1057+0.1125) ,
        'responsible' : 'Evan',
    },
    'WWJetsTo2L2Nu_TuneZ2_7TeV' : {
        'analyses': ['HTT'],
        'datasetpath': '/WWTo2L2Nu_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'x_sec': -999,
        'responsible' : 'Josh',
    },
    'ZZJetsTo4L_pythia' : {
        'analyses': ['HTT'],
        'datasetpath': '/ZZTo4L_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'x_sec': 17.890*0.10096*0.10096,
        'responsible' : 'Ian',
    },
    'ZZ4LJetsTo4L_madgraph' : {
        'analyses': ['4L'],
        'datasetpath': '/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v3/AODSIM',
        'pu': 'S7',
        'x_sec': -999,
        'responsible' : 'Ian',
    },
	'ZZ4M_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo4mu_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
		'x_sec': 0.07691,
		'responsible' : 'Ian',
	},
	'ZZ4E_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo4e_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
		'x_sec': 0.07691,
		'responsible' : 'Ian',
	},
	'ZZ2E2M_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo2e2mu_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
		'x_sec': 0.1767,
		'responsible' : 'Ian',
	},
	'ZZ4T_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo4tau_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
		'x_sec': 0.07691,
		'responsible' : 'Ian',
	},
	'ZZ2M2T_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo2mu2tau_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
		'x_sec': 0.1767,
		'responsible' : 'Ian',
	},
	'ZZ2E2T_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo2e2tau_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
		'x_sec': 0.1767,
		'responsible' : 'Ian',
	},
    'WW_pythi6_tauola' :{
   'analyses': [''],
   'datasetpath': '/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S8_START52_V9-v1/AODSIM',
   'pu':'S7',
   'x_sec':-999,
   'responsible': 'Isobel',
   },
    'T_t_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v3/GEN',
   'pu':'S7',
   'x_sec':-999,
   'responsible': 'Isobel',
   },
    'T_s_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v4/GEN',
   'pu':'S7',
   'x_sec':-999,
   'responsible': 'Isobel',
   },
    'Tbar_t_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v1/GEN',
   'pu':'S7',
   'x_sec':-999,
   'responsible': 'Isobel',
   },
    'Tbar_s_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v4/GEN',
   'pu':'S7',
   'x_sec':-999,
   'responsible': 'Isobel',
   },
    'embedded_2012A_mutau' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012A_PromptReco_v1_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
        'x_sec' : -999,
        'pu' : 'data',
        'responsible' : 'Evan',
    },
    'embedded_2012A_etau' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012A_PromptReco_v1_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
        'x_sec' : -999,
        'pu' : 'data',
        'responsible' : 'Evan',
    },
    'embedded_2012B_mutau_193752_195135' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run193752to195135_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'pu' : 'data',
        'responsible' : 'Evan',
    },
    'embedded_2012B_etau_193752_195135' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run193752to195135_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'pu' : 'data',
        'responsible' : 'Evan',
    },
    'embedded_2012B_etau_195147_196070' : {
        'analyses': ['HTT'],
        'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run195147to196070_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'pu' : 'data',
        'responsible' : 'Evan',
    },
    'embedded_2012B_mutau_195147_196070' : {
        'analyses': ['HTT'],
        'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run195147to196070_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'pu' : 'data',
        'responsible' : 'Evan',
    },

}

# Add GGH H2Tau samples
for mass in range(110, 165, 5):
   datadefs['GGH_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT'],
        'datasetpath': '/GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'x_sec': -999,
        'responsible' : 'Josh',
    }

# Add VBF H2Tau samples - not all done.
for mass in [110, 115, 120, 125, 135, 145, 155]:
    datadefs['VBF_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT'],
        'datasetpath': '/VBF_HToTauTau_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'x_sec': -999,
        'responsible' : 'Josh',
    }

# Add ggHZZ4L samples
# https://cmsweb.cern.ch/das/request?view=list&limit=10&instance=cms_dbs_prod_global&input=dataset+dataset%3D%2FGluGluToHToZZTo4L_M-*_8TeV-powheg-pythia6%2FSummer12-PU_S7_START52_V9-v1%2FAODSIM+%7C+sort+dataset.name
# only 33 exist IAR 30.May.2012
for mass in[115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 135, 140, 145, 150, 160, 170, 180, 190, 200, 210, 220, 230, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 650, 700, 750, 800, 850, 900, 950, 1000]:
	datadefs['GGH_HZZ4L_M-%i' % mass] = {
        'analyses': ['4L'],
        'datasetpath': '/GluGluToHToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'x_sec': -999,
        'responsible': 'Ian',
        }

# Add VBF HZZ4L samples
# https://cmsweb.cern.ch/das/request?view=list&limit=10&instance=cms_dbs_prod_global&input=dataset+dataset%3D%2FVBF_HToZZTo4L_M-*_8TeV-powheg-pythia6%2FSummer12-PU_S7_START52_V9-v1%2FAODSIM+%7C+sort+dataset.name
# only 33 exist IAR 30.May.2012
for mass in[115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 135, 140, 145, 150, 160, 170, 180, 190, 200, 210, 220, 230, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 650, 700, 750, 800, 850, 900, 950, 1000]:
	datadefs['VBF_HZZ4L_M-%i' % mass] = {
        'analyses': ['4L'],
        'datasetpath': '/VBF_HToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'x_sec': -999,
        'responsible': 'Ian',
        }

# Add WH TauTau signal samples
for mass in [110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160]:
    datadefs['VH_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT', 'VH'],
        'datasetpath': '/WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola/Summer12-PU_S7_START52_V9-v2/AODSIM' % mass,
        'pu': 'S7',
        'x_sec': -999,
        'responsible' : 'Evan',
    }
    if mass == 110:
        # Special case use v3 instead of v2, which doesn't exist
        datadefs['VH_H2Tau_M-110']['datasetpath'] = datadefs['VH_H2Tau_M-110']['datasetpath'].replace(
            'V9-v2', 'V9-v3')

# Add the only one we are currently interested int
datadefs['VH_H2Tau_M-110']['x_sec'] = (1.060 + 0.5869 + 0.1887)*7.95E-02
datadefs['VH_H2Tau_M-120']['x_sec'] = (0.7966 + 0.4483 + 0.1470)*7.04E-02
datadefs['VH_H2Tau_M-130']['x_sec'] = (0.6095 + 0.3473 + 0.1157)*5.48E-02
datadefs['VH_H2Tau_M-140']['x_sec'] = (0.4713 + 0.2728 + 0.09207)*3.54E-02

# Add data files
def build_data_set(pd, analyses, who):
    subsample_dict = {
        'data_%s_Run2012A_PromptReco_v1' % pd : {
            'datasetpath' : "/%s/Run2012A-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 190450,
            'lastRun' : 193686,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012B_PromptReco_v1_a' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 193752,
            'lastRun' : 194479,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012B_PromptReco_v1_b' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195396_8TeV_PromptReco_Collisions12_JSON_v2.txt",
            'firstRun' : 194478,
            'lastRun' : 195396,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012B_PromptReco_v1_c' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
            'firstRun' : 195397,
            'lastRun' : 195947,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012B_PromptReco_v1_d' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196509_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 195948,
            'lastRun' : 196509,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012B_PromptReco_v1_e' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 196510,
            'lastRun' : 196531,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012A_PromptReco_v1_Run190456_193683' % pd : {
            'datasetpath' : "/%s/Run2012A-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 190456,
            'lastRun' : 193683,
            'analyses' : analyses,
            'responsible' : who,
        },
        'data_%s_Run2012B_PromptReco_v1_Run193752_196531' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 193752,
            'lastRun' : 196531,
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
