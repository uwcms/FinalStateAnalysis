'''

Dataset definitions for 8TeV

You can query the information in this file at the command line.

Run

python data8TeV.py --help

for more information.

Author: Evan K. Friis, UW Madison

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

# Figure this out later.
data_name_map = {}

datadefs = {
   'WJetsToLNu_PtW-100_TuneZ2star_8TeV-madgraph' : {
        'analyses': ['Wbb'],
        'datasetpath': '/WJetsToLNu_PtW-100_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM',
        'pu': 'S10',
        'calibrationTarget': 'Summer12_DR53X_HCP2012',
        'x_sec': -999,
    },
    'WplusJets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 36257.2,
    },
    'WplusJets_madgraph_Extension' : {
        'analyses': ['HTT'],
        'datasetpath': '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9_extension-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 36257.2,
    },

     'Zjets_M50' : {
         'analyses': ['HTT','HZG'],
         'datasetpath': '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',
         'pu': 'S7',
         'calibrationTarget': 'Summer12',
         # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
         'x_sec': 3503.71,
     },
    'Z2jets_M50' : {
        'analyses': ['HTT'],
        'datasetpath': '/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'xsec': -999,
        'responsible' : 'Austin',
    },
    'TBartW_powheg' : {
   'analyses': ['HTT'],
   'datasetpath': '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
   'pu': 'S7',
   'calibrationTarget': 'Summer12',
   'xsec': -999,
       },
    'TtW_powheg' : {
   'analyses': ['HTT'],
   'datasetpath': '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
   'pu': 'S7',
   'calibrationTarget': 'Summer12',
   'xsec': -999,
       },
    'WZJetsTo2L2Q_madgraph' : {
   'analyses': ['HTT'],
   'datasetpath': '/WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
   'pu': 'S7',
   'calibrationTarget': 'Summer12',
   'xsec': -999,
       },
    'ZZJetsTo2L2Nu_TuneZ2' : {
   'analyses': ['HTT'],
   'datasetpath': '/ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v3/AODSIM',
   'pu': 'S7',
   'calibrationTarget': 'Summer12',
   'xsec': -999,
       },
    'ZZJetsTo2L2Q_TuneZ2' : {
   'analyses': ['HTT'],
   'datasetpath': '/ZZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v3/AODSIM',
   'pu': 'S7',
   'calibrationTarget': 'Summer12',
   'xsec': -999,
       },
    'TTplusJets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/TTJets_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V5-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 225.197,
        #'x_sec': 136.3, # prep
    },
    'WZJetsTo3LNu_pythia' : {
        'analyses': ['HTT'],
        'datasetpath': '/WZTo3LNu_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 32.3161*3*0.03365*(0.1075+0.1057+0.1125) ,
    },
    'WWJetsTo2L2Nu_TuneZ2_8TeV' : {
        'analyses': ['HTT'],
        'datasetpath': '/WWTo2L2Nu_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        # seems too high..
        'x_sec': 54.838*(0.1075+0.1057+0.1125)*(0.1075+0.1057+0.1125),
        #'x_sec': 3.53, # prep
    },
    'ZZJetsTo4L_pythia' : {
        'analyses': ['HTT'],
        'datasetpath': '/ZZTo4L_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': 0.130,#17.890*0.10096*0.10096,
    },
    'ZZ4LJetsTo4L_madgraph' : {
        'analyses': ['4L'],
        'datasetpath': '/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V9-v3/AODSIM',
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': -999,
    },
	'ZZ4M_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo4mu_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
                'calibrationTarget': 'Summer12',
		'x_sec': 0.07691,
	},
	'ZZ4E_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo4e_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
                'calibrationTarget': 'Summer12',
		'x_sec': 0.07691,
	},
	'ZZ2E2M_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo2e2mu_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
                'calibrationTarget': 'Summer12',
		'x_sec': 0.1767,
	},
	'ZZ4T_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo4tau_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
                'calibrationTarget': 'Summer12',
		'x_sec': 0.07691,
	},
	'ZZ2M2T_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo2mu2tau_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
                'calibrationTarget': 'Summer12',
		'x_sec': 0.1767,
	},
	'ZZ2E2T_powheg' : {
		'analyses': ['4L'],
		'datasetpath': '/ZZTo2e2tau_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
		'pu': 'S7',
                'calibrationTarget': 'Summer12',
		'x_sec': 0.1767,
	},
    'ggZZ4L' : {
        'analyses': ['4L'],
        'datasetpath': '/GluGluToZZTo4L_8TeV-gg2zz-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'calibrationTarget': 'Summer12',
        'responsible' : 'Ian',
    },   
    'ggZZ2L2L' : {
        'analyses': ['4L'],
        'datasetpath': '/GluGluToZZTo2L2L_TuneZ2star_8TeV-gg2zz-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'calibrationTarget': 'Summer12',
        'responsible' : 'Ian',
    },   
    'WW_pythi6_tauola' :{
   'analyses': [''],
   'datasetpath': '/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S8_START52_V9-v1/AODSIM',
   'pu':'S7',
   'calibrationTarget': 'Summer12',
   'x_sec':-999,
   },
    'T_t_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v3/GEN',
   'pu':'S7',
   'calibrationTarget': 'Summer12',
   'x_sec':-999,
   },
    'T_s_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v4/GEN',
   'pu':'S7',
   'calibrationTarget': 'Summer12',
   'x_sec':-999,
   },
    'Tbar_t_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v1/GEN',
   'pu':'S7',
   'calibrationTarget': 'Summer12',
   'x_sec':-999,
   },
    'Tbar_s_powheg_tauola' :{
   'analyses': [''],
   'datasetpath': '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12-START50_V13-v4/GEN',
   'pu':'S7',
   'calibrationTarget': 'Summer12',
   'x_sec':-999,
   },
    'embedded_2012A_mutau' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012A_PromptReco_v1_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
        'x_sec' : -999,
        'calibrationTarget': 'ICHEP2012',
        'pu' : 'data',
    },
    'embedded_2012A_etau' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012A_PromptReco_v1_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
        'x_sec' : -999,
        'calibrationTarget': 'ICHEP2012',
        'pu' : 'data',
    },
    'embedded_2012B_mutau_193752_195135' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run193752to195135_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'calibrationTarget': 'ICHEP2012',
        'pu' : 'data',
    },
    'embedded_2012B_etau_193752_195135' : {
        'analyses': ['HTT'],
        'datasetpath': '/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run193752to195135_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER',
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'calibrationTarget': 'ICHEP2012',
        'pu' : 'data',
    },
    'embedded_2012B_etau_195147_196070' : {
        'analyses': ['HTT'],
        'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run195147to196070_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'calibrationTarget': 'ICHEP2012',
        'pu' : 'data',
    },
    'embedded_2012B_mutau_195147_196070' : {
        'analyses': ['HTT'],
        'datasetpath' : "/DoubleMu/StoreResults-DoubleMu_2012B_PromptReco_v1_Run195147to196070_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
        'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
        'xsec' : -999,
        'calibrationTarget': 'ICHEP2012',
        'pu' : 'data',
        },
}

############################################################################
#### Signal datasets                    ####################################
############################################################################
# Add LFV

datadefs['LFV_VBF_H2Tau_M-126'] = { 'analyses': ['HTT'], 'x_sec' : 0.157, 'pu' : 'S10',
      'calibrationTarget': 'Summer12_DR53X_HCP2012', 'datasetpath':'something'}

datadefs['LFV_GluGlu_H2Tau_M-126'] = { 'analyses': ['HTT'], 'x_sec' :1.922, 'pu' : 'S10',
      'calibrationTarget': 'Summer12_DR53X_HCP2012', 'datasetpath':'something'}


# Add HToBB
for mass in range(110, 140, 5):
   ver=1
   if mass==120 :
      ver=2
   datadefs['WH_WToLNu_HToBB_M-%i' % mass]= {
      'datasetpath' :'/WH_WToLNu_HToBB_M-%i_8TeV-powheg-herwigpp/Summer12-PU_S7_START52_V9-v%i/AODSIM' % (mass, ver),
      'pu' : 'S7',
      'calibrationTarget': 'Summer12',
      'x_sec' : -999,
      'analyses' : ['VH', 'HBB'],
   }

# Add GGH H2Tau samples
for mass in range(110, 165, 5):
   datadefs['GGH_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT'],
        'datasetpath': '/GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': -999,
    }

# Add VBF H2Tau samples - not all done.
for mass in [110, 115, 120, 125, 135, 145, 155]:
    datadefs['VBF_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT'],
        'datasetpath': '/VBF_HToTauTau_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': -999,
    }

# Add ggHZZ4L samples
# https://cmsweb.cern.ch/das/request?view=list&limit=10&instance=cms_dbs_prod_global&input=dataset+dataset%3D%2FGluGluToHToZZTo4L_M-*_8TeV-powheg-pythia6%2FSummer12-PU_S7_START52_V9-v1%2FAODSIM+%7C+sort+dataset.name
# only 33 exist IAR 30.May.2012
for mass in[115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 135, 140, 145, 150, 160, 170, 180, 190, 200, 210, 220, 230, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 650, 700, 750, 800, 850, 900, 950, 1000]:
	datadefs['GGH_HZZ4L_M-%i' % mass] = {
        'analyses': ['4L'],
        'datasetpath': '/GluGluToHToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': -999,
        }

# Add VBF HZZ4L samples
# https://cmsweb.cern.ch/das/request?view=list&limit=10&instance=cms_dbs_prod_global&input=dataset+dataset%3D%2FVBF_HToZZTo4L_M-*_8TeV-powheg-pythia6%2FSummer12-PU_S7_START52_V9-v1%2FAODSIM+%7C+sort+dataset.name
# only 33 exist IAR 30.May.2012
for mass in[115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 135, 140, 145, 150, 160, 170, 180, 190, 200, 210, 220, 230, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 650, 700, 750, 800, 850, 900, 950, 1000]:
	datadefs['VBF_HZZ4L_M-%i' % mass] = {
        'analyses': ['4L'],
        'datasetpath': '/VBF_HToZZTo4L_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'calibrationTarget': 'Summer12',
        'x_sec': -999,
        }

# Add WH TauTau signal samples
for mass in range(90, 165, 5):
      datadefs['VHtautau_lepdecay_%i' % mass] = {
            'analyses': ['VH'],
            'datasetpath': "/WH_ZH_TTH_HToTauTau_M-%i_lepdecay_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
            'pu' : 'S10',
            'calibrationTarget':'Summer12_DR53X_HCP2012',
            'x_sec' : xsbr(8,mass,'wh','tautau')[0]*br_w_leptons + xsbr(8,mass,'zh','tautau')[0]*br_z_leptons + xsbr(8,mass,'tth','tautau')[0]*br_w_leptons**2,
      }

      datadefs['VH_H2Tau_M-%i' % mass] = {
            'analyses': ['HTT', 'VH'],
            'datasetpath': '/WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola/Summer12-PU_S7_START52_V9-v2/AODSIM' % mass,
            'pu': 'S7',
            'calibrationTarget': 'Summer12',
            'x_sec': xsbr(8,mass,'wh','tautau')[0] + xsbr(8,mass,'zh','tautau')[0] + xsbr(8,mass,'tth','tautau')[0],
      }
      if mass == 110:
            # Special case use v3 instead of v2, which doesn't exist
            datadefs['VH_H2Tau_M-110']['datasetpath'] = datadefs['VH_H2Tau_M-110']['datasetpath'].replace(
                  'V9-v2', 'V9-v3')
      

## datadefs['VH_H2Tau_M-110']['x_sec'] = (1.060*br_w_leptons + 0.5869*br_z_leptons + 0.1887*square(br_w_leptons))*7.95E-02
## datadefs['VH_H2Tau_M-120']['x_sec'] = (0.7966*br_w_leptons + 0.4483*br_z_leptons + 0.1470*square(br_w_leptons))*7.04E-02
## datadefs['VH_H2Tau_M-130']['x_sec'] = (0.6095*br_w_leptons + 0.3473*br_z_leptons + 0.1157*square(br_w_leptons))*5.48E-02
## datadefs['VH_H2Tau_M-140']['x_sec'] = (0.4713*br_w_leptons + 0.2728*br_z_leptons + 0.09207*square(br_w_leptons))*3.54E-02

# fix me
for mass in range(90, 150, 10):
   datadefs['VHWW_lepdecay_%i' % mass] = {
      'analyses': ['VH'],
      'datasetpath': "/WH_ZH_TTH_HToWW_M-%i_lepdecay_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM" % mass,
      'pu' : 'S10',
      'calibrationTarget': 'Summer12_DR53X_HCP2012',
      'x_sec' : -999,
      }

# Add the only one we are currently interested int
#datadefs['VH_H2Tau_M-110']['x_sec'] = (1.060 + 0.5869 + 0.1887)*7.95E-02
#datadefs['VH_H2Tau_M-120']['x_sec'] = (0.7966 + 0.4483 + 0.1470)*7.04E-02
#datadefs['VH_H2Tau_M-130']['x_sec'] = (0.6095 + 0.3473 + 0.1157)*5.48E-02
#datadefs['VH_H2Tau_M-140']['x_sec'] = (0.4713 + 0.2728 + 0.09207)*3.54E-02

# Add the cross sections for WH->HWW samples.  We use the 7TeV ones here,
# and then just change the xsec.
datadefs['WH_110_HWW3l'] = { 'x_sec' : 1.060*cube(br_w_leptons)* 4.82E-02 }
datadefs['WH_120_HWW3l'] = { 'x_sec' : 0.7966*cube(br_w_leptons)*1.43E-01 }
datadefs['WH_130_HWW3l'] = { 'x_sec' : 0.6095*cube(br_w_leptons)*3.05E-01 }
datadefs['WH_140_HWW3l'] = { 'x_sec' : 0.4713*cube(br_w_leptons)*5.03E-01 }

#VH->HWW xsec: WH + ZH; ZH --> totalxsec * BR(ZtoLL) * BR(HtoWW) * BR( WtoLL )^2
for mass in range(90, 150, 10):
      datadefs['VH_%s_HWW' % mass] = {'x_sec' : (xs(8,mass,'wh')[0]*br_w_leptons+xs(8,mass,'zh')[0]*br_z_leptons+xs(8,mass,'tth')[0]*br_w_leptons**2)*br(mass,'WW')*br_w_leptons**2}


# Add data files
def build_data_set(pd, analyses):
    subsample_dict = {
        'data_%s_Run2012A_PromptReco_v1' % pd : {
            'datasetpath' : "/%s/Run2012A-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 190450,
            'lastRun' : 193686,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012B_PromptReco_v1_a' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-194479_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 193752,
            'lastRun' : 194479,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012B_PromptReco_v1_b' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195396_8TeV_PromptReco_Collisions12_JSON_v2.txt",
            'firstRun' : 194478,
            'lastRun' : 195396,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012B_PromptReco_v1_c' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-195947_8TeV_PromptReco_Collisions12_JSON_v2.txt",
            'firstRun' : 195397,
            'lastRun' : 195947,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012B_PromptReco_v1_d' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196509_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 195948,
            'lastRun' : 196509,
            'analyses' : analyses,
            'calibrationTarget':'Prompt'
        },
        'data_%s_Run2012B_PromptReco_v1_e' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 196510,
            'lastRun' : 196531,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012A_PromptReco_v1_Run190456_193683' % pd : {
            'datasetpath' : "/%s/Run2012A-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 190456,
            'lastRun' : 193683,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012B_PromptReco_v1_Run193752_196531' % pd : {
            'datasetpath' : "/%s/Run2012B-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt",
            'firstRun' : 193752,
            'lastRun' : 196531,
            'analyses' : analyses,
        },
        'data_%s_Run2012B_13Jul2012_v1' % pd : {
            'datasetpath' : "/%s/Run2012B-13Jul2012-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON.txt",
            'firstRun' : 193752,
            'lastRun' : 196531,
            'analyses' : analyses,
            'calibrationTarget':'2012Jul13ReReco'
        },
        'data_%s_Run2012C_PromptReco_v1_Run198934_201264' % pd : {
            'datasetpath' : "/%s/Run2012C-PromptReco-v1/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
            'firstRun' : 198934,
            'lastRun' : 201264,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
        'data_%s_Run2012C_PromptReco_v2_Run198934_201264' % pd : {
            'datasetpath' : "/%s/Run2012C-PromptReco-v2/AOD" % pd,
            'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/json_DCSONLY.txt",
            'firstRun' : 198934,
            'lastRun' : 201264,
            'analyses' : analyses,
            'calibrationTarget':'ICHEP2012'
        },
    }
    sample_dict = {
        'data_%s' % pd : subsample_dict.keys()
    }
    return subsample_dict, sample_dict

# Build all the PDs we use
data_DoubleMu, list_DoubleMu = build_data_set('DoubleMu', ['VH', 'Mu','4L'])
datadefs.update(data_DoubleMu)
data_name_map.update(list_DoubleMu)

data_MuEG, list_MuEG = build_data_set('MuEG', ['VH', 'HTT', 'Mu'])
datadefs.update(data_MuEG)
data_name_map.update(list_MuEG)

data_DoubleE, list_DoubleE = build_data_set('DoubleElectron', ['VH','4L'])
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

