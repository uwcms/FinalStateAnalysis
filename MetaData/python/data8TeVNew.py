'''

Dataset definitions for 8TeV

You can query the information in this file at the command line.

Run

python data8TeVNew.py --help

for more information.

Author: Evan K. Friis, UW Madison

'''

from datacommon import square, cube, quad, picobarns, \
        br_w_leptons, br_z_leptons, query_cli, femtobarns

from data8TeV import datadefs as datadefs52

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


# Figure this out later.
data_name_map = {}

datadefs = {
   'WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 0.91*picobarns,
   'pu' : 'S10',
   'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 0.1296*picobarns,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 11.1,
   'pu' : 'S10',
   },

   'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 11.1,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/Tbar_t-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 30.7,
   'pu' : 'S10',
   },

   'T_t-channel_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/T_t-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 56.4,
   'pu' : 'S10',
   'calibrationTarget':'Summer12_DR53X_HCP2012'
   },
   'Zjets_M50_S10' : {
   'analyses': ['ET'],
   'datasetpath': '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
   'pu': 'S10',
   'calibrationTarget': 'Summer12',
   'xsec': -999,
   },
    'Z2jets_M50_S10' : {
        'analyses': ['ET'],
        'datasetpath': '/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12',
        'xsec': -999,
    },
    'Z3jets_M50' : {
        'analyses': ['ET'],
        'datasetpath': '/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12',
        'xsec': -999,
    },
    'Z4jets_M50' : {
        'analyses': ['ET'],
        'datasetpath': '/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12',
        'xsec': -999,
    },
    'Z1jets_M50' : {
        'analyses': ['ET'],
        'datasetpath': '/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12',
        'xsec': -999,
    },




   'Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/Tbar_s-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 1.56,
   'pu' : 'S10',
   },

   'T_s-channel_TuneZ2star_8TeV-powheg-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/T_s-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 3.79,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'TTJetsFullLepMGDecays' : {
         'analyses': ["ET"],
         'datasetpath' : "/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM",
         'x_sec' : -999,
         'pu' : 'S10',
         'calibrationTarget' : 'Summer12_DR53X',
   },
   'TTJetsSemiLepMGDecays' : {
         'analyses': ["ET"],
         'datasetpath' : "/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM",
         'x_sec' : -999,
         'pu' : 'S10',
         'calibrationTarget' : 'Summer12_DR53X',
   },
   'TTTo2L2Nu2B_8TeV-powheg-pythia6' : {
   'analyses': ['4L'],
   'datasetpath' : "/TTTo2L2Nu2B_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_v2' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_v1' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball' : {
   'analyses': ['HTT','HZG'],
   'datasetpath' : "/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
   'x_sec' : 3503.71*picobarns,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'DYJetsToLL_M-10To50filter_8TeV-madgraph' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : 915.0*picobarns,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph' : {
   'analyses': ['ZZ'],
   'datasetpath': '/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
   'x_sec': -999,
   'pu': 'S10',
   'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola' : {
   'analyses': ['HTT'],
   'datasetpath' : "/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   },

   'ZZTo2e2tau_8TeV-powheg-pythia6' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/ZZTo2e2tau_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZTo2e2mu_8TeV-powheg-pythia6' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/ZZTo2e2mu_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZTo2mu2tau_8TeV-powheg-pythia6' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/ZZTo2mu2tau_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZTo4mu_8TeV-powheg-pythia6' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/ZZTo4mu_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
   },

   'ZZTo4e_8TeV-powheg-pythia6' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/ZZTo4e_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ZZTo4tau_8TeV-powheg-pythia6' : {
   'analyses': ['ZZ'],
   'datasetpath' : "/ZZTo4tau_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'ggZZ4L' : {
   'analyses': ['4L'],
   'datasetpath': '/GluGluToZZTo4L_8TeV-gg2zz-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
   'pu': 'S7',
   'xsec': -999,
   'calibrationTarget': 'Summer12_DR53X_HCP2012',
   'responsible' : 'Ian',
   },

   'ggZZ2L2L' : {
   'analyses': ['4L'],
   'datasetpath': '/GluGluToZZTo2L2L_TuneZ2star_8TeV-gg2zz-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
   'pu': 'S7',
   'xsec': -999,
   'calibrationTarget': 'Summer12_DR53X_HCP2012',
   'responsible' : 'Ian',
   },

   'WbbJetsToLNu_Massive_TuneZ2star_8TeV-madgraph-pythia6_tauola' : {
   'analyses' : ['Wbb'],
   'datasetpath' : "/WbbJetsToLNu_Massive_TuneZ2star_8TeV-madgraph-pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

   'DoubleMu_Run2012B_13Jul2012_v4_embedded_trans1_tau116_ptmu1_13had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012B_13Jul2012_v4_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
    'calibrationTarget':'Moriond2013'
   },

   'DoubleMu_Run2012B_13Jul2012_v4_embedded_trans1_tau115_ptelec1_17had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012B_13Jul2012_v4_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'Moriond2013'
   },

   'DoubleMu_Run2012A_13Jul2012_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012A_13Jul2012_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'Moriond2013'
   },

   'DoubleMu_Run2012A_13Jul2012_v1_embedded_trans1_tau116_ptmu1_13had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012A_13Jul2012_v1_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'Moriond2013'
   },

   'DoubleMu_Run2012C_PromptReco_v2_embedded_trans1_tau116_ptmu1_13had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012C_PromptReco_v2_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'Moriond2013'
   },

   'DoubleMu_Run2012C_PromptReco_v2_embedded_trans1_tau115_ptelec1_17had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012C_PromptReco_v2_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'ICHEP2012'
   },

   'DoubleMu_Run2012C_24Aug2012_v1_embedded_trans1_tau116_ptmu1_13had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012C_24Aug2012_v1_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'ICHEP2012'
   },

   'DoubleMu_Run2012C_24Aug2012_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_Run2012C_24Aug2012_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'ICHEP2012'
   },

   'DoubleMu_Run2012D_22Jan2013_v1_RHembedded_trans1_tau115_ptelec1_20had1_18_v1' : {
   'analyses': ['HTauTau'],
   'datasetpath' : "/DoubleMuParked/StoreResults-Run2012D_22Jan2013_v1_RHembedded_trans1_tau115_ptelec1_20had1_18_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
   'pu' : 'data',
   'calibrationTarget':'ICHEP2012'
   },

    'WplusJets_madgraph_filtered' : {
# This is not a sample exactly... To combine 1-2-3-4 jets I have incorporated a filtered version of WJets (NUP==5) in my workflow
# I need the name in datadefs for UWHiggs to work
        'analyses': ['HTT'],
        'datasetpath': '/ThisIsNotARealSample/NeededForUWCMSToWork/Sorry/Maria',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 37509, # this is the W xsec in the StandardModelReference twiki
    },

   'WplusJets_madgraph_S10' : {
   'analyses': ['HTT'],
   'datasetpath' : "/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
   'x_sec' : -999,
   'pu' : 'S10',
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   },

    'Wplus1Jets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/W1JetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12',
        'x_sec': 6662.8,
    },
    'Wplus1Jets_madgraph_tapas' : {
        'analyses': ['ET'],
        'datasetpath': '/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12',
        'x_sec': 6662.8,
    },

    'Wplus2Jets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/W2JetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 2159.2,
    },
      'Wplus2Jets_madgraph_tapas' : {
            'analyses': ['HTT'],
            'datasetpath': '/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM',
            'pu': 'S10',
            'calibrationTarget': 'Summer12',
            'x_sec': 2159.2,
      },

    'Wplus3Jets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/W3JetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 640.4,
    },

    'Wplus4Jets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/W4JetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 264.,
    },


}



# SM Z\gamma 8 TeV
datadefs['ZGToLLG']= {
   'datasetpath' :'/ZGToLLG_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
   'pu' : 'S10',
   'x_sec' : 156.2*picobarns,
   'analyses' : ['HZG'],
   'calibrationTarget':'Summer12_DR53X_HCP2012'
   }

############################################################################
#### Signal datasets ####################################
############################################################################
for mass in range(80,150, 10) + range(160, 220, 20) + range(250, 550, 50) + range(600, 1100, 100) :
   datadefs['SUSYGluGluToHToTauTau_M-%i_8TeV-pythia6-tauola' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/SUSYGluGluToHToTauTau_M-%i_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
      'calibrationTarget':'Summer12_DR53X_HCP2012'
      }
   datadefs['SUSYBBHToTauTau_M-%i_8TeV-pythia6-tauola' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/SUSYBBHToTauTau_M-%i_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
       'calibrationTarget':'Summer12_DR53X_HCP2012'
      }

aTGC_path = Template('/ZZ4L_Sherpa_aTGC_f${i}_${f1}0_${f2}0_v2/iross-SUMMER12-AODSIM-START53_V7C_${i}_${f1}_${f2}-RECO-v2-6c2e8f83abf0ca43d500aa4162646310/USER')

for coup in ["4","5"]:
    for coup1 in ["0p015","0p000","m0p015"]:
        for coup2 in ["0p015","0p000","m0p015"]:
            datadefs['ZZ4L_f%s_%s0_%s0' % ( coup, coup1, coup2 )] = {
               'analyses': ['ZZ'],
               'datasetpath' : aTGC_path.substitute(i=coup,f1=coup1,f2=coup2),
               'dbs' : "cms_dbs_ph_analysis_01",
               'x_sec' : -999,
               'pu' : 'S10',
               'calibrationTarget':'Summer12_DR53X_HCP2012'
               }

datadefs['SUSYBBHToTauTau_M-300_8TeV-pythia6-tauola'] = {
   'analyses': ['HTT'],
   'datasetpath': "/SUSYBBHToTauTau_M-300_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM",
   'pu' : 'S10',
   'x_sec' : -999,
    'calibrationTarget':'Summer12_DR53X_HCP2012'
   }

for mass in range(110, 165, 5) :
   datadefs['GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
       'calibrationTarget':'Summer12_DR53X_HCP2012'
      }
   datadefs['VBF_HToTauTau_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/VBF_HToTauTau_M-%i_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
       'calibrationTarget':'Summer12_DR53X_HCP2012'
      }

# Double Charged Higgs Signal Samples
dblh_4l_xsec = {110: 8730.9,  130: 186.21,  150: 106.55,
                170: 64.641,  200: 33.209,  250: 12.724,
                300: 5.5458,  350: 2.6413,  400: 1.3414,
                450: 0.71531, 500: 0.39604, 600: 0.13271,
                700: 0.48382e-1}

for mass in [110, 130, 150, 170, 200, 250, 300, 350, 400, 450, 500, 600, 700]:
    if mass >= 170:
        datadefs['HPlusPlusHMinusHTo3L_M-%i_8TeV-calchep-pythia6' % mass] = {
            'analyses' : ['HPP'],
            'datasetpath' : '/HPlusPlusHMinusHTo3L_M-%i_8TeV-calchep-pythia6/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM' % mass,
            'pu' : 'S10',
            'x_sec' : -999,
            'calibrationTarget' : 'Summer12_DR53X_HCP2012'
            }

    datadefs['HPlusPlusHMinusMinusHTo4L_M-%i_8TeV-pythia6' % mass] = {
        'analyses' : ['HPP'],
        'datasetpath' : '/HPlusPlusHMinusMinusHTo4L_M-%i_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM' % mass,
        'pu' : 'S10',
        'x_sec' : dblh_4l_xsec[mass]*femtobarns,
        'calibrationTarget' : 'Summer12_DR53X_HCP2012'
        }


# HZZ4L Signal Samples
for mass in range(115,130) + range(130,150,5) + range(150,200,10) + [200,220] + range(250,600,25) + range(600,1001,50) :
   datadefs['GluGluToHToZZTo4L_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/GluGluToHToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
       'calibrationTarget':'Summer12_DR53X_HCP2012'
      }
   datadefs['VBF_HToZZTo4L_M-%i_8TeV-powheg-pythia6' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/VBF_HToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'x_sec' : -999,
       'calibrationTarget':'Summer12_DR53X_HCP2012'
      }

# HZZ4L Spin Parity Samples
datadefs['SMHiggs-126'] = {
        'analyses': ['4L'],
        'datasetpath': '/SMHiggsToZZTo4L_M-126_8TeV_ext-JHUgenV2-pythia6/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12_DR53X_HCP2012',
        'x_sec': -999,
        'globalTag': 'START53_V7G::All',
        'eleReg' : 1
        }

datadefs['Higgs0M-126'] = {
        'analyses': ['4L'],
        'datasetpath': '/Higgs0MToZZTo4L_M-126_8TeV_ext-JHUgenV2-pythia6/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12_DR53X_HCP2012',
        'x_sec': -999,
        'globalTag': 'START53_V7G::All',
        'eleReg' : 1
        }

datadefs['Higgs0PH-126'] = {
        'analyses': ['4L'],
        'datasetpath': '/Higgs0PHToZZTo4L_M-126_8TeV-JHUgenV2-pythia6/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12_DR53X_HCP2012',
        'x_sec': -999,
        'globalTag': 'START53_V7G::All',
        'eleReg' : 1
        }

datadefs['Graviton2PM-126'] = {
        'analyses': ['4L'],
        'datasetpath': '/Graviton2PMToZZTo4L_M-126_8TeV_ext-JHUgenV2-PYTHIA6_Tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12_DR53X_HCP2012',
        'x_sec': -999,
        'globalTag': 'START53_V7G::All',
        'eleReg' : 1
        }

datadefs['Graviton2PMqq-126'] = {
        'analyses': ['4L'],
        'datasetpath': '/Graviton2PMqqbarToZZTo4L_M-126_8TeV-JHUgenV2-PYTHIA6_Tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12_DR53X_HCP2012',
        'x_sec': -999,
        'globalTag': 'START53_V7G::All',
        'eleReg' : 1
        }



for mass in range(110, 165, 5) :
   if mass==135 :
      ver=2
   else :
      ver=1

   datadefs['WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola' % mass] = {
      'analyses': ['HTT'],
      'datasetpath': "/WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v%i/AODSIM" % (mass,ver),
      'pu' : 'S10',
      'x_sec' : -999,
       'calibrationTarget':'Summer12_DR53X_HCP2012'
      }

# H -> Z\gamma signal datasets
hzgMap = {'gg':['/GluGluToHToZG_M-','_8TeV-powheg-pythia6'],
          'VBF':['/VBF_HToZG_M-','_8TeV-powheg-pythia6'],
          'V':['/WH_ZH_HToZG_M-','_8TeV-pythia6'],
          'tt':['/TTH_HToZG_M-','_8TeV-pythia6']}
#all cross sections in picobarns
cs_hzg = {120.0:{'gg':21.13,'VBF':1.649,'V':0.7966+0.4483,'tt':0.1470},
          125.0:{'gg':19.52,'VBF':1.578,'V':0.6966+0.3943,'tt':0.1302},
          130.0:{'gg':18.07,'VBF':1.511,'V':0.6095+0.3473,'tt':0.1157},
          135.0:{'gg':16.79,'VBF':1.448,'V':0.5351+0.3074,'tt':0.1031},
          140.0:{'gg':15.63,'VBF':1.389,'V':0.4713+0.2728,'tt':0.09207},
          145.0:{'gg':14.59,'VBF':1.333,'V':0.4164+0.2424,'tt':0.08246},
          150.0:{'gg':13.65,'VBF':1.280,'V':0.3681+0.2159,'tt':0.07403}}
hbr_hzg = {120:1.12e-03,
           125:1.55e-03,
           130:1.96e-03,
           135:2.28e-03,
           140:2.46e-03,
           145:2.48e-03,
           150:2.31e-03}
zbr_hzg = {'gg':br_z_leptons,'VBF':br_z_leptons,'V':1.0,'tt':br_z_leptons}
for mass in range(120,155,5):
  ver=1
  for ch in cs_hzg[mass].keys():
    datadefs['%sHToZG_M-%i' %(ch,mass)]= {
      'datasetpath' :'%s%i%s/Summer12_DR53X-PU_S10_START53_V7A-v%i/AODSIM' % (hzgMap[ch][0],
                                                                              mass,
                                                                              hzgMap[ch][1],
                                                                              ver),
      'pu' : 'S10',
      'calibrationTarget':'Summer12_DR53X_HCP2012',
      'x_sec' : cs_hzg[mass][ch]*hbr_hzg[mass]*zbr_hzg[ch]*picobarns,
      'analyses' : ['HZG']
      }


# Add VH files
for mass in range(110, 165, 5):
   datadefs['VHtautau_lepdecay_%i' % mass] = {
      'analyses': ['VH'],
      'datasetpath': "/WH_ZH_TTH_HToTauTau_M-%i_lepdecay_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
       'calibrationTarget':'Summer12_DR53X_HCP2012',
      'x_sec' : xsbr(8,mass,'wh','tautau')[0]*br_w_leptons + xsbr(8,mass,'zh','tautau')[0]*br_z_leptons + xsbr(8,mass,'tth','tautau')[0]*br_w_leptons**2,
      }

for mass in range(110, 150, 10):
   datadefs['VHWW_lepdecay_%i' % mass] = {
      'analyses': ['VH'],
      'datasetpath': "/WH_ZH_TTH_HToWW_M-%i_lepdecay_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
       'calibrationTarget':'Summer12_DR53X_HCP2012',
      'x_sec' : (xs(8,mass,'wh')[0]*br_w_leptons+xs(8,mass,'zh')[0]*br_z_leptons+xs(8,mass,'tth')[0])*br(mass,'WW')*br_w_leptons**2,
      }



# We use the same name for the 53X lepdecay only samples (sigh)
for mass in range(90, 165, 5):
    datadefs['VH_H2Tau_M-%s' % mass] = {}
    datadefs['VH_H2Tau_M-%s' % mass]['x_sec'] = xsbr(8,mass,'wh','tautau')[0] + xsbr(8,mass,'zh','tautau')[0] + xsbr(8,mass,'tth','tautau')[0]

## datadefs['VH_H2Tau_M-120']['x_sec'] = (0.7966*br_w_leptons + 0.4483*br_z_leptons + 0.1470*square(br_w_leptons))*7.04E-02
## datadefs['VH_H2Tau_M-130']['x_sec'] = (0.6095*br_w_leptons + 0.3473*br_z_leptons + 0.1157*square(br_w_leptons))*5.48E-02
## datadefs['VH_H2Tau_M-140']['x_sec'] = (0.4713*br_w_leptons + 0.2728*br_z_leptons + 0.09207*square(br_w_leptons))*3.54E-02

# Add data files

datadefs['data_DoubleMu_Run2012B_13Jul2012_v4'] = {
   'datasetpath' : "/DoubleMu/Run2012B-13Jul2012-v4/AOD",
   'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt",
   'firstRun' : 193834,
   'lastRun' : 196531,
   'analyses' : ['HZZ'],
    'calibrationTarget':'Moriond2013'
   }

def build_data_set(pd, analyses):
   subsample_dict = {
      'data_%s_Run2012A_13Jul2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012A-13Jul2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt",
      'firstRun' : 190456,
      'lastRun' : 193621,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012A_22Jan2013_v1' % pd : {
      'datasetpath' : "/%s/Run2012A-22Jan2013-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
      'firstRun' : 190456,
      'lastRun' : 193621,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012B_13Jul2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012B-13Jul2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt",
      'firstRun' : 193833,
      'lastRun' : 196531,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012B_13Jul2012_v4' % pd : {
      'datasetpath' : "/%s/Run2012B-13Jul2012-v4/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt",
      'firstRun' : 193833,
      'lastRun' : 196531,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012B_22Jan2013_v1' % pd : {
      'datasetpath' : "/%s/Run2012B-22Jan2013-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
      'firstRun' : 193833,
      'lastRun' : 196531,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012C_PromptReco_v2' % pd : {
      'datasetpath' : "/%s/Run2012C-PromptReco-v2/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/JSON_ALL_2012_pixel_ecal_removed.txt",
      ## 'firstRun' : 201265,
      ## 'lastRun' : 203755,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012A_recover_06Aug2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012A-recover-06Aug2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/JSON_ALL_2012_pixel_ecal_removed.txt",
      'firstRun' : 190782, #LAG from A. David, 26 Dec 2012
      'lastRun' : 190949,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012C_PromptReco_v1' % pd : {
      'datasetpath' : "/%s/Run2012C-PromptReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/JSON_ALL_2012_pixel_ecal_removed.txt",
      'firstRun' : 197700,
      'lastRun' : 198913,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012C_24Aug2012_v1' % pd : {
      'datasetpath' : "/%s/Run2012C-24Aug2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON.txt",
      'firstRun' : 198022,
      'lastRun' : 198523,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012C_22Jan2013_v1' % pd : {
      'datasetpath' : "/%s/Run2012C-22Jan2013-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
      'firstRun' : 198022,
      'lastRun' : 203742,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012C_EcalRecover_11DEC2012_v1' % pd :{
      'datasetpath' : "/%s/Run2012C-EcalRecover_11Dec2012-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_201191-201191_8TeV_11Dec2012ReReco-recover_Collisions12_JSON.txt",
      'firstRun' : 201191,
      'lastRun' : 201191,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012D_PromptReco_v1' % pd :{
      'datasetpath' : "/%s/Run2012D-PromptReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/JSON_ALL_2012_pixel_ecal_removed.txt",
      'firstRun' : 203768,
      'lastRun' : 208686,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012D_16Jan2013_v1' % pd :{
      'datasetpath' : "/%s/Run2012D-16Jan2013-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt",
      'firstRun' : 203768,
      'lastRun' : 208686,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012D_16Jan2013_v2' % pd :{ #apparently some of these got re-re-re-recoed. Or something. v1 no longer exists for MuEG or DoubleMu IAR 19.Feb.2013
      'datasetpath' : "/%s/Run2012D-16Jan2013-v2/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt",
      'firstRun' : 203768,
      'lastRun' : 208686,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
      'data_%s_Run2012D_22Jan2013_v1' % pd :{
      'datasetpath' : "/%s/Run2012D-22Jan2013-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
      'firstRun' : 203768,
      'lastRun' : 208686,
      'analyses' : analyses,
      'calibrationTarget':'Moriond2013'
      },
    }
   sample_dict = {
      'data_%s' % pd : subsample_dict.keys()
      }
   return subsample_dict, sample_dict

# Build all the PDs we use
data_DoubleMu, list_DoubleMu = build_data_set('DoubleMu', ['VH', 'Mu','4L','HZG'])
datadefs.update(data_DoubleMu)
data_name_map.update(list_DoubleMu)

data_DoubleMuParked, list_DoubleMuParked = build_data_set('DoubleMuParked', ['VH', 'Mu','4L','HZG'])
datadefs.update(data_DoubleMuParked)
data_name_map.update(list_DoubleMuParked)

data_MuEG, list_MuEG = build_data_set('MuEG', ['VH', 'HTT', 'Mu'])
datadefs.update(data_MuEG)
data_name_map.update(list_MuEG)

data_DoubleE, list_DoubleE = build_data_set('DoubleElectron', ['VH','4L','HZG'])
datadefs.update(data_DoubleE)
data_name_map.update(list_DoubleE)

data_SingleMu, list_SingleMu = build_data_set('SingleMu', ['Tau', 'Mu', 'Wbb'])
datadefs.update(data_SingleMu)
data_name_map.update(list_SingleMu)

data_SingleElectron, list_SingleElectron = build_data_set('SingleElectron', ['Tau', 'E', 'Wjets'])
datadefs.update(data_SingleElectron)
data_name_map.update(list_SingleElectron)

data_TauPlusX, list_TauPlusX = build_data_set('TauPlusX', ['HTT', ])
datadefs.update(data_TauPlusX)
data_name_map.update(list_TauPlusX)

if __name__=="__main__":
    query_cli(datadefs)


