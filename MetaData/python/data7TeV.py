# flake8: noqa
'''

Definition of 7TeV samples and data.

NB the real data samples are built automatically at the bottom.

You can query the information in this file at the command line.

Run

python data7TeV.py --help

for more information.

Author: Evan K. Friis, UW Madison

'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, query_cli, br_z_leptons
import re

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

# Define a mapping between a "nice" name and a set of datasets.
# This is so you can make an update to the underlying data sample pythia/powheg
# etc.
data_name_map = {
    'Zjets' : ['Zjets_M50'],

    'QCDMu' : ['QCD_20toInf_MuPt15'],

    'Wjets' : ['WplusJets_madgraph'],

    'WW' : ['WWJetsTo2L2Nu'],
    'WZ' : ['WZJetsTo3LNu'],
    'WZ_pythia' : ['WZJetsTo3LNu_pythia'],
    'ZZ' : ['ZZJetsTo4L_pythia'],

    'ttjets': ['TTplusJets_madgraph'],

    'VGamma': ['VGjets'],

    'VH100' : ['VH_100'],
    'VH110' : ['VH_110'],
    'VH115' : ['VH_115'],
    'VH120' : ['VH_120'],
    'VH125' : ['VH_125'],
    'VH130' : ['VH_130'],
    'VH135' : ['VH_135'],
    'VH140' : ['VH_140'],
    'VH145' : ['VH_145'],
    'VH150' : ['VH_150'],
    'VH160' : ['VH_160'],

    'VH110WW' : ['WH_110_HWW3l'],
    'VH115WW' : ['WH_115_HWW3l'],
    'VH120WW' : ['WH_120_HWW3l'],
    'VH125WW' : ['WH_125_HWW3l'],
    'VH130WW' : ['WH_130_HWW3l'],
    'VH135WW' : ['WH_135_HWW3l'],
    'VH140WW' : ['WH_140_HWW3l'],
    'VH145WW' : ['WH_145_HWW3l'],
    'VH150WW' : ['WH_150_HWW3l'],
    'VH155WW' : ['WH_155_HWW3l'],
    'VH160WW' : ['WH_160_HWW3l'],

    'TTW' : ['TTWToLplus', 'TTWToLminus'],
    'TTZ' : ['TTZToLplus', 'TTZToLminus'],
    'WWW' : ['WWWTo2Lplus', 'WWWTo2Lminus'],

    'ggH_ZZ_4l_120' : ['ggH_ZZ_4l_120'],
    'HToZG120' : ['VBFHToZG_M-120','VHToZG_M-120','ggHToZG_M-120','ttHToZG_M-120'],
    'HToZG125' : ['VBFHToZG_M-125','VHToZG_M-125','ggHToZG_M-125','ttHToZG_M-125'],
    'HToZG130' : ['VBFHToZG_M-130','VHToZG_M-130','ggHToZG_M-130','ttHToZG_M-130'],
    'HToZG135' : ['VBFHToZG_M-135','VHToZG_M-135','ggHToZG_M-135','ttHToZG_M-135'],
    'HToZG140' : ['VBFHToZG_M-140','VHToZG_M-140','ggHToZG_M-140','ttHToZG_M-140'],
    'HToZG145' : ['VBFHToZG_M-145','VHToZG_M-145','ggHToZG_M-145','ttHToZG_M-145'],
    'HToZG150' : ['VBFHToZG_M-150','VHToZG_M-150','ggHToZG_M-150','ttHToZG_M-150'],
    'ZGToLLG_PRIVATE' : ['ZGToEEG','ZGToMuMuG']
}

datadefs = {
    ############################################################################
    #### EWK background datasets            ####################################
    ############################################################################

  'WJetsToLNu_Pt-100_7TeV-herwigpp' : {
  'datasetpath' : '/WJetsToLNu_Pt-100_7TeV-herwigpp/Fall11-PU_S6_START42_V14B-v1/AODSIM',
  'x_sec' : -999,
  'pu' : 'S6',
  'calibrationTarget' : 'Fall11',
  'analyses' : [ 'Wbb' ],
  },

    'WbbToLNu_TuneZ2_7TeV-madgraph-pythia6-tauola' : {
        'datasetpath' : '/WbbToLNu_TuneZ2_7TeV-madgraph-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999, #NNLO
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['Wbb',  'VH', 'Mu'],
    },
    'Zjets_M50' : {
        'datasetpath' : '/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : 3048*picobarns, #NNLO
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT',  'VH', 'Tau', 'Mu','HZG'],
    },
    'WplusJets_madgraph' : {
        'datasetpath' : "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 31314*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT',  'VH', 'Tau', 'Mu'],
    },
    'TTplusJets_madgraph' : {
        'datasetpath' : "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        #'x_sec' : 157.5*picobarns, # NLO cross-section from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
        'x_sec' : 164.4, # From H2Tau
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT',  'VH', 'Tau', 'Mu'],
    },
    'TTplusJets_madgraph_v2' : {
        'datasetpath' : "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        #'x_sec' : 157.5*picobarns, # NLO cross-section from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
        'x_sec' : 164.4, # From H2Tau
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT',  'VH', 'Tau', 'Mu'],
    },
    # Single top samples
    'T_tW_Powheg' : {
        'datasetpath' : "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 7.87*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'T_t_Powheg' : {
        'datasetpath' : "/T_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 41.92*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'T_s_Powheg' : {
        'datasetpath' : "/T_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 3.19*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    # Single anti-top samples
    'Tbar_tW_Powheg' : {
        'datasetpath' : "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'x_sec' : 7.87*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'Tbar_t_Powheg' : {
        'datasetpath' : "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 22.65*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'Tbar_s_Powheg' : {
        'datasetpath' : "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1.44*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'Wplus1Jets_madgraph' : {
        'datasetpath' : "/W1Jet_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : -999,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'Wplus2Jets_madgraph' : {
        'datasetpath' : "/W2Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : -999,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'Wplus3Jets_madgraph' : {
        'datasetpath' : "/W3Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'x_sec' : 304.2*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },


    ############################################################################
    #### VGamma background datasets         ####################################
    ############################################################################
    'VGjets' : {
        'datasetpath' : '/GVJets_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : 56.64*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['Mu', 'VH'],
    },

    ############################################################################
    #### Diboson datasets                   ####################################
    ############################################################################

    'ZZJetsTo4L_pythia' : {
        'datasetpath' : "/ZZTo4L_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : 0.106*picobarns, # from MCFM via Ian
        'x_sec_unc' : quad(1.5, 0.2, 0.2)*0.10096*0.10096,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'WZJetsTo3LNu' : {
        'datasetpath' : "/WZJetsTo3LNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : 26.735*picobarns*3*0.03365*(0.1075+0.1057+0.1125),
        'x_sec' : 0.857369, #H2Tau
        'x_sec_unc' : quad(2.4, 1.1, 1.0)*0.3257*0.10096,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', ],
    },
    'WZJetsTo2L2Q' : {
        'datasetpath' : "/WZJetsTo2L2Q_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : 3.85*picobarns ,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'WZJetsTo3LNu_pythia' : {
        'datasetpath' : "/WZTo3LNu_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        # This xsec comes from PREP and is only LO.  Different from the PREP
        # value for the madgraph sample, as Pythia does not include gamma*
        'x_sec' : 0.33*picobarns, # FIXME !!!!!!!!
        'x_sec_unc' : quad(2.4, 1.1, 1.0)*0.3257*0.10096,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH',  'HTT'],
    },
    'WWJetsTo2L2Nu' : {
        'datasetpath' : '/WWJetsTo2L2Nu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'pu' : 'S6',
        #'x_sec' : 3.783*picobarns, # FROM PREP
        # 55.3 +- 3.3 6.9 3.3 from EWK-11-10
        #'x_sec' : 55.3*picobarns*0.3257*0.3257, # 32.57% BR to leptons
        'x_sec' : 4.783389, # From H2Tau twiki
        'x_sec_unc' : quad(3.3, 6.9, 3.3)*0.3257*0.3257,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'WZinclusive' : {
        'datasetpath' : "/WZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : 18*picobarns,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH',  'HTT'],
    },
    'ZZinclusive' : {
        'datasetpath' : "/ZZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : -999,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH',  'HTT'],
    },
    'WWinclusive' : {
        'datasetpath' : '/WW_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'pu' : 'S6',
        'x_sec' : 47*picobarns,
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'GluGluToZZTo4L' : {
        'datasetpath' : "/GluGluToZZTo4L_7TeV-gg2zz-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.00174*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'GluGluToZZTo2L2L' : {
        'datasetpath' : "/GluGluToZZTo2L2L_7TeV-gg2zz-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.00348*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo4mu_powheg' : { #now using official samples with mll>4 IAR 11.Oct.2012
        'datasetpath' : "/ZZTo4mu_mll4_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.06609*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo4e_powheg' : { #now using official samples with mll>4 IAR 11.Oct.2012
        'datasetpath' : "/ZZTo4e_mll4_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.06609*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo4tau_powheg' : { #now using official samples with mll>4 IAR 11.Oct.2012
        'datasetpath' : "/ZZTo4tau_mll4_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.06609*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo2e2tau_powheg' : { #now using official samples with mll>4 IAR 11.Oct.2012
        'datasetpath' : "/ZZTo2e2tau_mll4_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : 0.152*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo2e2mu_powheg' : { #now using official samples with mll>4 IAR 11.Oct.2012
        'datasetpath' : "/ZZTo2e2mu_mll4_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.152*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo2mu2tau_powheg' : { #now using official samples with mll>4 IAR 11.Oct.2012
        'datasetpath' : "/ZZTo2mu2tau_mll4_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.152*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo4mu_powheg_v2' : { #v1 samples had a bug where the Z->4l peak weighting screwed the overall cross-section IAR 31.May.2012
        'datasetpath' : "/ZZTo4mu_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.03067*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo4e_powheg_v2' : { #v1 samples had a bug where the Z->4l peak weighting screwed the overall cross-section IAR 31.May.2012
        'datasetpath' : "/ZZTo4e_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.03067*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo4tau_powheg_v2' : { #v1 samples had a bug where the Z->4l peak weighting screwed the overall cross-section IAR 31.May.2012
        'datasetpath' : "/ZZTo4tau_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.03067*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo2e2tau_powheg_v2' : { #v1 samples had a bug where the Z->4l peak weighting screwed the overall cross-section IAR 31.May.2012
        'datasetpath' : "/ZZTo2e2tau_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.01386*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo2e2mu_powheg_v2' : { #v1 samples had a bug where the Z->4l peak weighting screwed the overall cross-section IAR 31.May.2012
        'datasetpath' : "/ZZTo2e2mu_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.01386*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },
    'ZZTo2mu2tau_powheg_v2' : { #v1 samples had a bug where the Z->4l peak weighting screwed the overall cross-section IAR 31.May.2012
        'datasetpath' : "/ZZTo2mu2tau_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v2/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 0.01386*picobarns, # from https://twiki.cern.ch/twiki/bin/view/CMS/HZZSamples7TeV
        'analyses' : ['VH',  '4L', 'HTT'],
    },

    ############################################################################
    #### QCD datasets                       ####################################
    ############################################################################

    'QCD_20toInf_MuPt15' : {
        'datasetpath' : '/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : 2.966E8*picobarns*2.855E-4,
        'analyses' : ['HTT', 'VH', 'Tau', 'Mu'],
    },

    ############################################################################
    #### Signal datasets                    ####################################
    ############################################################################
    'VH_100' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : (1.186 + 0.6313 + 0.1638)*picobarns*8.36e-2,
        'analyses' : ['VH', 'HTT'],
    },
    'VH_110' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-110_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : (0.8754 + 0.4721 + 0.1257)*picobarns*8.02e-2,
        'analyses' : ['VH', 'HTT'],
    },
    'VH_115' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-115_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : (0.7546 + 0.4107 + 0.1106)*picobarns*7.65e-2,
        'analyses' : ['VH', 'HTT'],
    },
    'VH_120' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'x_sec' : (0.6561 + 0.3598 + 0.09756)*picobarns*7.1e-2,
        'analyses' : ['VH', 'HTT'],
    },
    'VH_125' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-125_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.6729 + 0.3158 + 0.08634)*picobarns*6.37e-2,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'VH_130' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-130_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.5008 + 0.2778 + 0.07658)*picobarns*5.48e-2,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'VH_135' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-135_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.4390 + 0.2453 + 0.06810)*picobarns*4.52e-2,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'VH_140' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.3857 + 0.2172 + 0.06072)*picobarns*3.54e-2,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'VH_145' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-145_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.3406 + 0.1930 + 0.05435)*picobarns*2.61e-2,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'VH_150' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.3001 + 0.1713 + 0.04869)*picobarns*1.78e-2,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },
    'VH_160' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.2291 + 0.1334 + 0.03942)*picobarns*3.96E-03,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH', 'HTT'],
    },

    ############################################################################
    #### VH -> WW dataset                   ####################################
    ############################################################################
    'WH_110_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-110_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.8754*picobarns*cube(br_w_leptons)*4.82E-02,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_115_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-115_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.7546*picobarns*cube(br_w_leptons)*8.67E-02,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_120_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-120_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.6561*picobarns*cube(br_w_leptons)*1.43E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_125_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-125_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.5729*picobarns*cube(br_w_leptons)*2.16E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_130_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-130_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.5008*picobarns*cube(br_w_leptons)*3.05E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_135_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-135_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.4390*picobarns*cube(br_w_leptons)*4.03E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_140_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-140_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.3857*picobarns*cube(br_w_leptons)*5.03E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_145_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-145_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.3406*picobarns*cube(br_w_leptons)*6.02E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_150_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-150_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.3001*picobarns*cube(br_w_leptons)*6.98E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_155_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-155_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.2646*picobarns*cube(br_w_leptons)*7.95E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },
    'WH_160_HWW3l' : {
        'datasetpath' : "/WH_HToWW_3l_M-160_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 0.2291*picobarns*cube(br_w_leptons)*9.08E-01,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    ############################################################################
    #### H2Tau samples                      ####################################
    ############################################################################

    ######################### VBF H-->tau+tau ##################################
    'VBF_H2Tau_M-100' : {
        'datasetpath' : '/VBF_HToTauTau_M-100_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-105' : {
        'datasetpath' : '/VBF_HToTauTau_M-105_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-110' : {
        'datasetpath' : '/VBF_HToTauTau_M-110_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-115' : {
        'datasetpath' : '/VBF_HToTauTau_M-115_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-120' : {
        'datasetpath' : '/VBF_HToTauTau_M-120_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-125' : {
        'datasetpath' : '/VBF_HToTauTau_M-125_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-130' : {
        'datasetpath' : '/VBF_HToTauTau_M-130_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-135' : {
        'datasetpath' : '/VBF_HToTauTau_M-135_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-140' : {
        'datasetpath' : '/VBF_HToTauTau_M-140_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-145' : {
        'datasetpath' : '/VBF_HToTauTau_M-145_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'VBF_H2Tau_M-150' : {
        'datasetpath' : '/VBF_HToTauTau_M-150_7TeV-powheg-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },

    ######################### GGH SM H-->tau+tau ##################################

    'GGH_H2Tau_M-100' : {
        'datasetpath' : '/GluGluToHToTauTau_M-100_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-105' : {
        'datasetpath' : '/GluGluToHToTauTau_M-105_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-110' : {
        'datasetpath' : '/GluGluToHToTauTau_M-110_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-115' : {
        'datasetpath' : '/GluGluToHToTauTau_M-115_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-120' : {
        'datasetpath' : '/GluGluToHToTauTau_M-120_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-125' : {
        'datasetpath' : '/GluGluToHToTauTau_M-125_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-130' : {
        'datasetpath' : '/GluGluToHToTauTau_M-130_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-135' : {
        'datasetpath' : '/GluGluToHToTauTau_M-135_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-140' : {
        'datasetpath' : '/GluGluToHToTauTau_M-140_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-145' : {
        'datasetpath' : '/GluGluToHToTauTau_M-145_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGH_H2Tau_M-150' : {
        'datasetpath' : '/GluGluToHToTauTau_M-150_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },

    ######################### GGH MSSM H-->tau+tau ##################################

    'GGHMSSM_H2Tau_M-90' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-100' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-120' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-130' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-130_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-140' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-160' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-180' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-200' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-200_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-250' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-250_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-300' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-300_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-350' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-350_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-400' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-400_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-450' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-450_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-500' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-500_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-600' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-600_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6','calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-700' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-700_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-800' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-800_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-900' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-900_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'GGHMSSM_H2Tau_M-1000' : {
        'datasetpath' : '/SUSYGluGluToHToTauTau_M-1000_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },

	######################### BBH MSSM H-->tau+tau ##################################

    'BBH_H2Tau_M-90' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-100' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-120' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-130' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-130_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-140' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-160' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-180' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-200' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-200_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-250' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-250_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-300' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-300_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-350' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-350_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-400' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-400_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-450' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-450_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-500' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-500_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-600' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-600_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-700' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-700_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-800' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-800_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-900' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-900_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },
    'BBH_H2Tau_M-1000' : {
        'datasetpath' : '/SUSYBBHToTauTau_M-1000_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : -999*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['HTT'],
    },

    ############################################################################
    #### Obscure VH backgrounds             ####################################
    ############################################################################

    'TTWToLplus' : {
        'datasetpath' :"/TTWTo2Lplus2Nu_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.006841)*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    'TTZToLplus' : {
        'datasetpath' :"/TTZTo2Lplus2Nu_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.002024)*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    'WWWTo2Lplus' : {
        'datasetpath' :"/WWWTo2Lplus2Nu_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        # These have some problems with the xsec for this sample
        #'x_sec' : (0.008957)*picobarns,
        # Just basically turn it off.
        'x_sec' : (0.017)*picobarns*cube(br_w_leptons),
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    'TTWToLminus' : {
        'datasetpath' :"/TTWTo2Lminus2Nu_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.002705)*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    'TTZToLminus' : {
        'datasetpath' :"/TTZTo2Lminus2Nu_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.001946)*picobarns,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    'WWWTo2Lminus' : {
        'datasetpath' :"/WWWTo2Lminus2Nu_7TeV-madgraph/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        #'x_sec' : (0.004109)*picobarns,
        # These have some problems with the xsec for this sample
        # Just basically turn it off.
        'x_sec' : (0.017)*picobarns*cube(br_w_leptons),
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['VH'],
    },

    ############################################################################
    #### UF ZZ private production (M_ll>4)  ####################################
    ############################################################################

    'uf_zz2e2m' : {
        'datasetpath' : "/Summer11/zz2e2m_powheg_GENSIMRECO_v2/USER",
        'x_sec' : (0.1525)*picobarns,
        'pu' : 'S6', #todo: check this
        'calibrationTarget' : 'Summer11',
        'analyses' : ['4L'],
        'dbs' : "cms_dbs_ph_analysis_02",
    },
    'uf_zz2e2t' : {
        'datasetpath' : "/Summer11/zz2e2tau_powheg_GENSIMRECO_v2/USER",
        'x_sec' : (0.1523)*picobarns,
        'pu' : 'S6', #todo: check this
        'calibrationTarget' : 'Summer11',
        'analyses' : ['4L'],
        'dbs' : "cms_dbs_ph_analysis_02",
    },
    'uf_zz2m2t' : {
        'datasetpath' : "/Summer11/zz2mu2tau_powheg_GENSIMRECO_v2/USER",
        'x_sec' : (0.1517)*picobarns,
        'pu' : 'S6', #todo: check this
        'calibrationTarget' : 'Summer11',
        'analyses' : ['4L'],
        'dbs' : "cms_dbs_ph_analysis_02",
    },
    'uf_zz4e' : {
        'datasetpath' : "/Summer11/zz4e_powheg_GENSIMRECO_v2/USER",
        'x_sec' : (0.0664)*picobarns,
        'pu' : 'S6', #todo: check this
        'calibrationTarget' : 'Summer11',
        'analyses' : ['4L'],
        'dbs' : "cms_dbs_ph_analysis_02",
    },
    'uf_zz4m' : {
        'datasetpath' : "/Summer11/zz4mu_powheg_GENSIMRECO_v2/USER",
        'x_sec' : (0.0661)*picobarns,
        'pu' : 'S6', #todo: check this
        'calibrationTarget' : 'Summer11',
        'analyses' : ['4L'],
        'dbs' : "cms_dbs_ph_analysis_02",
    },
    'uf_zz4t' : {
        'datasetpath' : "/Summer11/zz4tau_powheg_GENSIMRECO_v2/USER",
        'x_sec' : (0.0659)*picobarns,
        'pu' : 'S6', #todo: check this
        'calibrationTarget' : 'Summer11',
        'analyses' : ['4L'],
        'dbs' : "cms_dbs_ph_analysis_02",

    },
    ############################################################################
    #### H->ZZ->4L signal samples           ####################################
    ############################################################################
    #todo: add lots of HZZ samples IAR 31.May.2012
    'ggH_ZZ_4l_115' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-115_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_120' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-120_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_130' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-130_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_140' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-140_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_150' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-150_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_160' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-160_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_170' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-170_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_180' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-180_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_190' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-190_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_200' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-200_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_210' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-210_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_220' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-220_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_230' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-230_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_250' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-250_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_275' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-275_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_300' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-30_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_325' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-325_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_350' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-350_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_375' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-375_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_400' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-400_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_425' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-425_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_450' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-450_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_475' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-475_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_500' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-500_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_525' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-525_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_550' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-550_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_575' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-575_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'ggH_ZZ_4l_600' : {
        'datasetpath' : "/GluGluToHToZZTo4L_M-600_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_115' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-115_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_120' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-120_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_130' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-130_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_140' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-140_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_150' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-150_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_160' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-160_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_170' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-170_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_180' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-180_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_190' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-190_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_200' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-200_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_210' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-210_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_220' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-220_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_230' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-230_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_250' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-250_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_275' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-275_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_300' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-300_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_325' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-325_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_350' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-350_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_375' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-375_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_400' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-400_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_425' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-425_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_450' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-450_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_475' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-475_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_500' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-500_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_525' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-525_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_550' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-550_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_575' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-575_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },
    'VBF_ZZ_4l_600' : {
        'datasetpath' : "/VBF_ToHToZZTo4L_M-600_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 1,
        'pu' : 'S6',
        'calibrationTarget' : 'Fall11',
        'analyses' : ['4L'],
    },

}

# H -> Z\gamma signal datasets
hzgMap = {'gg':['/GluGluToHToZG_M-','_7TeV-powheg-pythia6'],
          'VBF':['/VBF_HToZG_M-','_7TeV-powheg-pythia6'],
          'V':['/WH_ZH_HToZG_M-','_7TeV-pythia6'],
          'tt':['/TTH_HToZG_M-','_7TeV-pythia6']}
#all cross sections in picobarns
cs_hzg = {120.0:{'gg':16.65,'VBF':1.279,'V':0.6561+0.3598,'tt':0.0976},
          125.0:{'gg':15.32,'VBF':1.222,'V':0.5729+0.3158,'tt':0.0863},
          130.0:{'gg':14.16,'VBF':1.168,'V':0.5008+0.2778,'tt':0.0766},
          135.0:{'gg':13.11,'VBF':1.117,'V':0.4390+0.2453,'tt':0.0681},
          140.0:{'gg':12.18,'VBF':1.069,'V':0.3857+0.2172,'tt':0.0607},
          145.0:{'gg':11.33,'VBF':1.023,'V':0.3406+0.1930,'tt':0.0544},
          150.0:{'gg':10.58,'VBF':0.9800,'V':0.3001+0.1713,'tt':0.0487}}
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
      'datasetpath' :'%s%i%s/Fall11-PU_S6_START42_V14B-v%i/AODSIM' % (hzgMap[ch][0],
                                                                      mass,
                                                                      hzgMap[ch][1],
                                                                      ver),
      'pu' : 'S6',
      'calibrationTarget' : 'Fall11',
      'x_sec' : cs_hzg[mass][ch]*hbr_hzg[mass]*zbr_hzg[ch]*picobarns,
      'analyses' : ['HZG']
      }

#Z\gamma standard model background (private datasamples!!!)
#needs dbs = http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet
#needs 'REDIGI' process fed to the pat HLT handler
datadefs['ZGToEEG']= {
      'datasetpath':'/ZGToEEG_TuneZ2_7TeV-madgraph-upto2jets/lgray-Fall11-REDIGI-AODSIM-START42_V14B-v1_ZGToEEG-RECO-01715716b3165466edf30580d661ec8b/USER',
      'pu' : 'S6',
      'x_sec' : 12.29*picobarns,
      'analyses' : ['HZG'],
      'calibrationTarget' : 'Fall11',
      'dbs' : 'cms_dbs_ph_analysis_01',
      'hlt_process' : 'REDIGI'
      }
datadefs['ZGToMuMuG']= {
      'datasetpath':'/ZGToMuMuG_TuneZ2_7TeV-madgraph-upto2jets/lgray-Fall11-REDIGI-AODSIM-START42_V14B-v1_ZGToMuMuG-RECO-01715716b3165466edf30580d661ec8b/USER',
      'pu' : 'S6',
      'x_sec' : 12.29*picobarns,
      'analyses' : ['HZG'],
      'calibrationTarget' : 'Fall11',
      'dbs' : 'cms_dbs_ph_analysis_01',
      'hlt_process' : 'REDIGI'
      }


#VH->HWW xsec: WH + ZH; ZH --> totalxsec * BR(ZtoLL) * BR(HtoWW) * BR( WtoLL )^2
for mass in range(90, 150, 10):
      datadefs['VH_%s_HWW' % mass] = {'x_sec' : (xs(7,mass,'wh')[0]*br_w_leptons+xs(7,mass,'zh')[0]*br_z_leptons+xs(7,mass,'tth')[0]*br_w_leptons**2)*br(mass,'WW')*br_w_leptons**2}

# Add HToBB
for mass in range(100, 150, 5):
  ver=4
  if mass>135 :
    ver=1
  datadefs['WH_WToLNu_HToBB_M-%i' % mass]= {
    'datasetpath' :'/WH_WToLNu_HToBB_M-%i_7TeV-powheg-herwigpp/Fall11-PU_S6_START42_V14B-v%i/AODSIM' % (mass, ver),
    'pu' : 'S6',
    'x_sec' : -999,
    'calibrationTarget' : 'Fall11',
    'analyses' : ['VH', 'HBB'],
    }

for mass in range(90, 150, 10):
    datadefs['VHWW_lepdecay_%i' % mass] = {
        'analyses': ['VH'],
        'datasetpath': "/WH_ZH_TTH_HToWW_M-%i_lepdecay_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM" % mass,
        'pu' : 'S6',
        'x_sec' : -999,
        'calibrationTarget' : 'Fall11'
    }

# Add all the datasets
# Following https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2011Analysis
def build_data_set(pd, analyses):
  subsample_dict = {
      'data_%s_Run2011B_PromptReco_v1' % pd : {
          'datasetpath' : "/%s/Run2011B-PromptReco-v1/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
          'firstRun' : 175832,
          'lastRun' : 180296,
          'calibrationTarget' : 'Prompt',
          'analyses' : analyses,
      },
      'data_%s_Run2011A_PromptReco_v6' % pd : {
          'datasetpath' : "/%s/Run2011A-PromptReco-v6/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
          'firstRun' : 172620,
          'lastRun' : 175770,
          'calibrationTarget' : 'Prompt',
          'analyses' : analyses,
      },
      'data_%s_Run2011A_05Aug2011_v1' % pd : {
          'datasetpath' : "/%s/Run2011A-05Aug2011-v1/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt",
          'firstRun' : 170053,
          'lastRun' : 172619,
          'calibrationTarget' : 'ReReco',
          'analyses' : analyses,
      },
      'data_%s_Run2011A_PromptReco_v4' % pd : {
          'datasetpath' : "/%s/Run2011A-PromptReco-v4/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
          'firstRun' : 165071,
          'lastRun' : 168437,
          'calibrationTarget' : 'Prompt',
          'analyses' : analyses,
      },
      'data_%s_Run2011A_May10ReReco_v1' % pd : {
          'datasetpath' : "/%s/Run2011A-May10ReReco-v1/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt",
          'firstRun' : 160404,
          'lastRun' : 163869,
          'calibrationTarget' : 'Prompt',
          'analyses' : analyses,
      },
      'data_%s_Run2011A_16Jan2012_v1' % pd : {
          'datasetpath' : "/%s/Run2011A-16Jan2012-v1/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON_v2.txt",
          'firstRun' : 160431,
          'lastRun' : 180252,
          'calibrationTarget' : 'Jan16ReReco',
          'analyses' : analyses,
      },
      'data_%s_Run2011B_16Jan2012_v1' % pd : {
          'datasetpath' : "/%s/Run2011B-16Jan2012-v1/AOD" % pd,
          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON_v2.txt",
          'firstRun' : 160431,
          'lastRun' : 180252,
          'calibrationTarget' : 'Jan16ReReco',
          'analyses' : analyses,
      },
# Used for 2011 ZZ results, but now the 16JanReReco is default
#      'data_%s_Run2011A_Jul05ReReco_v1' % pd : {
#          'datasetpath' : "/%s/Run2011A-05Jul2011ReReco-ECAL-v1/AOD" % pd,
#          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Jul05JSON.txt",
#          'firstRun' : 160404,
#          'lastRun' : 167913,
#          'analyses' : analyses,
#      },
#      'data_%s_Run2011A_Oct03ReReco_v1' % pd : {
#          'datasetpath' : "/%s/Run2011A-03Oct2011-v1/AOD" % pd,
#          'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
#          'firstRun' : 172620,
#          'lastRun' : 175770,
#          'analyses' : analyses,
#      },
  }
  sample_dict = {
    'data_%s' % pd : subsample_dict.keys()
  }
  return subsample_dict, sample_dict

# We use the same name for the 53X lepdecay only samples (sigh)
#for mass in range(90, 180, 10):
#    datadefs['VH_%s_HWW' % mass] = {
#        'datasetpath' :"/WH_ZH_TTH_HToWW_M-%s_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM" % mass,
#        'x_sec' :  (xs(7,mass,'wh')[0]*br_w_leptons+xs(7,mass,'zh')[0]*br_z_leptons+xs(7,mass,'tth')[0])*br(mass,'WW')*br_w_leptons**2,
#        'pu' : 'S6',
#        'calibrationTarget' : 'Fall11',
#        'analyses' : ['VH'],
#    }

for mass in range(90, 165, 5):
      datadefs['VH_H2Tau_M-%s' % mass] = {}
      datadefs['VH_H2Tau_M-%s' % mass]['x_sec'] = xsbr(7,mass,'wh','tautau')[0] + xsbr(7,mass,'zh','tautau')[0] + xsbr(7,mass,'tth','tautau')[0]
      datadefs['VH_%s' % mass] = {}
      datadefs['VH_%s' % mass]['x_sec'] = xsbr(7,mass,'wh','tautau')[0] + xsbr(7,mass,'zh','tautau')[0] + xsbr(7,mass,'tth','tautau')[0]

      datadefs['VHtautau_lepdecay_%i' % mass] = {
            'analyses': ['VH'],
            'datasetpath': "/WH_ZH_TTH_HToTauTau_M-%i_lepdecay_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM" % mass,
            'pu' : 'S6',
            'x_sec' : xsbr(7,mass,'wh','tautau')[0]*br_w_leptons + xsbr(7,mass,'zh','tautau')[0]*br_z_leptons + xsbr(7,mass,'tth','tautau')[0]*br_w_leptons**2,
            'calibrationTarget' : 'Fall11'
      }
      
              
# Build all the PDs we use
data_DoubleMu, list_DoubleMu = build_data_set('DoubleMu', ['VH', 'Mu','HZG'])
datadefs.update(data_DoubleMu)
data_name_map.update(list_DoubleMu)

data_MuEG, list_MuEG = build_data_set('MuEG', ['VH', 'HTT', 'Mu'])
datadefs.update(data_MuEG)
data_name_map.update(list_MuEG)

data_DoubleE, list_DoubleE = build_data_set('DoubleElectron', ['VH','HZG'])
datadefs.update(data_DoubleE)
data_name_map.update(list_DoubleE)

data_SingleMu, list_SingleMu = build_data_set('SingleMu', ['Tau', 'Mu'])
datadefs.update(data_SingleMu)
data_name_map.update(list_SingleMu)

data_SingleElectron, list_SingleElectron = build_data_set('SingleElectron', ['Tau', 'E', 'Wjets'])
datadefs.update(data_SingleElectron)
data_name_map.update(list_SingleElectron)

data_TauPlusX, list_TauPlusX = build_data_set('TauPlusX', ['HTT', ])
datadefs.update(data_TauPlusX)
data_name_map.update(list_TauPlusX)

    # Add all the embedded samples
embedded_samples = [
    "/DoubleMu/StoreResults-DoubleMu_2011B_PR_v1_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011B_PR_v1_embedded_trans1_tau115_ptelec1_17had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_PR_v4_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_PR_v4_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_May10thRR_v1_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_May10thRR_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_Aug05thRR_v1_embedded_trans1_tau116_ptmu1_13had1_17_v2-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_Aug05thRR_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_03Oct2011_v1_embedded_trans1_tau116_ptmu1_13had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
    "/DoubleMu/StoreResults-DoubleMu_2011A_03Oct2011_v1_embedded_trans1_tau115_ptelec1_17had1_17_v1-f456bdbb960236e5c696adfe9b04eaae/USER",
]
_embed_matcher = re.compile('.*(?P<name>2011.*)_v\d-f4.*')
for embedded_sample in embedded_samples:
    match = _embed_matcher.match(embedded_sample)
    assert(match)
    name = match.group('name')
    datadefs[name] = {
        'datasetpath' : embedded_sample,
        'analyses' : ['HTT'],
        'x_sec' : -999,
        'pu' : 'data',
    }

if __name__=="__main__":
    query_cli(datadefs)
