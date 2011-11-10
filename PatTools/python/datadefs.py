import math

# Conversions to pico barns
_millibarns = 1.0e+9
_microbarns = 1.0e+6
_nanobarns  = 1.0e+3
_picobarns =  1.0
_femtobarns = 1.0e-3

def quad(*xs):
    # Add stuff in quadrature
    return math.sqrt(sum(x*x for x in xs))

# NB the data samples are built automatically at the bottom

data_name_map = {
    # Fixme there is some double counting here!
    #'Zjets' : ['Zjets_M50', 'Zbb_M50', 'Zcc_M40'],
    'Zjets' : ['Zjets_M50',],

    'QCDMu' : ['QCD_20toInf_MuPt15'],

    'QCDE' : ['QCD_20to30_EM', 'QCD_30to80_EM', 'QCD_80to170_EM'],

    'Wjets' : ['WplusJets_madgraph'],

    'WW' : ['WWJetsTo2L2Nu'],
    'WZ' : ['WZJetsTo3LNu'],
    'ZZ' : ['ZZJetsTo4L'],

    'ttjets': ['TTplusJets_madgraph'],

    'VH110' : ['VH_110'],
    'VH115' : ['VH_115'],
    'VH120' : ['VH_120'],
    'VH125' : ['VH_125'],
    #'VH130' : ['VH_130'],
    #'VH135' : ['VH_135'],
    #'VH140' : ['VH_140'],
    #'VH145' : ['VH_145'],
    #'VH150' : ['VH_150'],
}


datadefs = {
    ############################################################################
    #### EWK background datasets            ####################################
    ############################################################################

    'Zjets_M50' : {
        'datasetpath' : '/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM',
        'x_sec' : 3048*_picobarns, #NNLO
        'pu' : 'S6',
        'analyses' : ['HTT', 'SSDL', 'VH', 'Tau', 'Mu'],
    },
    'WplusJets_madgraph' : {
        'datasetpath' : "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 31314*_picobarns,
        'pu' : 'S6',
        'analyses' : ['HTT', 'SSDL', 'VH', 'Tau', 'Mu'],
    },
    'TTplusJets_madgraph' : {
        'datasetpath' : "/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 157.5*_picobarns, # NLO cross-section from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
        'pu' : 'S6',
        'analyses' : ['HTT', 'SSDL', 'VH', 'Tau', 'Mu'],
    },
    #'Zbb_M50' : {
        #'datasetpath' : '/ZbbToLL_M-40_PtB1-15_TuneZ2_7TeV-madgraph-pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM',
        #'x_sec' : 13.75*_picobarns,
        #'pu' : 'S4',
        #'analyses' : ['HTT', 'VH'],
    #},
    #'Zcc_M40' : {
        #'datasetpath': '/ZccToLL_M-40_PtB1-15_TuneZ2_7TeV-madgraph-pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM',
        #'x_sec' : 18.74*_picobarns,
        #'pu' : 'S4',
        #'analyses' : ['HTT', 'VH'],
    #},

    ############################################################################
    #### VGamma background datasets         ####################################
    ############################################################################
    #'VGjets' : {
        #'datasetpath' : '/GVJets_7TeV-madgraph/Summer11-PU_S4_START42_V11-v1/AODSIM',
        #'x_sec' : 56.64*_picobarns,
        #'pu' : 'S4',
        #'analyses' : ['HTT', 'VH'],
    #},

    ############################################################################
    #### Diboson datasets                   ####################################
    ############################################################################

    'ZZJetsTo4L' : {
        'datasetpath' : "/ZZJetsTo4L_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        #'x_sec' : 0.03906*_picobarns,
        # 3.8 +- 1.5 0.2 0.2 from EWK-11-10
        'x_sec' : 3.8*_picobarns*0.1096*0.1096,
        'x_sec_unc' : quad(1.5, 0.2, 0.2)*0.1096*0.1096,
        'analyses' : ['VH', 'SSDL'],
    },
    'WZJetsTo3LNu' : {
        'datasetpath' : "/WZJetsTo3LNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6-START44_V5-v1/AODSIM",
        'pu' : 'S6',
        #'x_sec' : 0.7192*_picobarns, # FROM PREP
        # 17 +- 2.4 1.1 1.0 from EWK-11-10
        'x_sec' : 17.0*_picobarns*0.3257*0.1096,
        'x_sec_unc' : quad(2.4, 1.1, 1.0)*0.3257*0.1096,
        'analyses' : ['VH', 'SSDL'],
    },
    'WWJetsTo2L2Nu' : {
        'datasetpath' : '/WWJetsTo2L2Nu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM',
        'pu' : 'S4',
        #'x_sec' : 3.783*_picobarns, # FROM PREP
        # 55.3 +- 3.3 6.9 3.3 from EWK-11-10
        'x_sec' : 55.3*_picobarns*0.3257*0.3257, # 32.57% BR to leptons
        'x_sec_unc' : quad(3.3, 6.9, 3.3)*0.3257*0.3257,
        'analyses' : ['VH', 'SSDL'],
    },

    ############################################################################
    #### QCD datasets                       ####################################
    ############################################################################

    'QCD_20toInf_MuPt15' : {
        'datasetpath' : '/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM',
        'pu' : 'S4',
        'x_sec' : 2.966E8*_picobarns*2.855E-4,
        'analyses' : ['HTT', 'VH', 'Tau', 'Mu'],
    },
    # Electron enriched
    #'QCD_20to30_EM' : {
        #'datasetpath' : "/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        #'pu' : 'S6',
        #'x_sec' : 2.361E8*_picobarns*0.0106,
        #'analyses' : ['HTT', 'VH'],
    #},
    'QCD_30to80_EM' : {
        'datasetpath' : "/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6/Fall11-PU_S6-START44_V5-v1/AODSIM",
        'pu' : 'S6',
        # FIXME
        'x_sec' : 5.944E7*_picobarns*0.061,
        'analyses' : ['HTT', 'VH'],
    },
    'QCD_80to170_EM' : {
        'datasetpath' : "/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia/Fall11-PU_S6-START44_V5-v1/AODSIM",
        'pu' : 'S6',
        # FIXME
        'x_sec' : 898200.0*_picobarns*0.159,
        'analyses' : ['HTT', 'VH'],
    },
    'VH_100' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : (1.186 + 0.6313 + 0.1638)*_picobarns*8.36e-2,
        'skim' : 1.0,
        'analyses' : ['VH'],
    },
    'VH_110' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-110_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : (0.8754 + 0.4721 + 0.1257)*_picobarns*8.02e-2,
        'skim' : 1.0,
        'analyses' : ['VH'],
    },
    'VH_115' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-115_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : (0.7546 + 0.4107 + 0.1106)*_picobarns*7.65e-2,
        'skim' : 1.0,
        'analyses' : ['VH'],
    },
    'VH_120' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'pu' : 'S6',
        'x_sec' : (0.6561 + 0.3598 + 0.09756)*_picobarns*7.1e-2,
        'skim' : 1.0,
        'analyses' : ['VH'],
    },
    'VH_125' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-125_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.6729 + 0.3158 + 0.08634)*_picobarns*6.37e-2,
        'pu' : 'S6',
        'analyses' : ['VH'],
    },
    #'VH_130' : {
        #'datasetpath' :"",
        #'x_sec' : (0.5008 + 0.2778 + 0.07658)*_picobarns*5.48-2,
        #'pu' : 'S6',
        #'analyses' : ['VH'],
    #},
    'VH_135' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-135_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.4390 + 0.2453 + 0.06810)*_picobarns*4.52e-2,
        'pu' : 'S6',
        'analyses' : ['VH'],
    },
    'VH_140' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.3857 + 0.2172 + 0.06072)*_picobarns*3.54e-2,
        'pu' : 'S6',
        'analyses' : ['VH'],
    },
    'VH_145' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-145_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : (0.3406 + 0.1930 + 0.05435)*_picobarns*2.61e-2,
        'pu' : 'S6',
        'analyses' : ['VH'],
    },
    #'VH_150' : {
        #'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-150_7TeV-pythia6-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
        #'x_sec' : (0.3011 + 0.1713 + 0.04869)*_picobarns*1.78e-2,
        #'pu' : 'S6',
        #'analyses' : ['VH'],
    #},
    'VH_160' : {
        'datasetpath' :"/WH_ZH_TTH_HToTauTau_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM",
        'x_sec' : 10000,
        'pu' : 'S6',
        'analyses' : ['VH'],
    },
    }

# Add all the datasets
def build_data_set(pd, analyses):
  subsample_dict = {
    'data_%s_Run2011B_PromptReco_v1_d' % pd : {
      'datasetpath' : "/%s/Run2011B-PromptReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
      'firstRun' : 178678,
      'lastRun' : 180252,
      'analyses' : analyses,
    },
    'data_%s_Run2011B_PromptReco_v1_c' % pd : {
      'datasetpath' : "/%s/Run2011B-PromptReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-178677_7TeV_PromptReco_Collisions11_JSON.txt",
      'firstRun' : 177516,
      'lastRun' : 178677,
      'analyses' : analyses,
    },
    'data_%s_Run2011B_PromptReco_v1_b' % pd : {
      'datasetpath' : "/%s/Run2011B-PromptReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-178677_7TeV_PromptReco_Collisions11_JSON.txt",
      'firstRun' : 177074,
      'lastRun' : 177515,
      'analyses' : analyses,
    },
    'data_%s_Run2011B_PromptReco_v1_a' % pd : {
      'datasetpath' : "/%s/Run2011B-PromptReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-178677_7TeV_PromptReco_Collisions11_JSON.txt",
      'firstRun' : 175832,
      'lastRun' : 177053,
      'analyses' : analyses,
    },
    'data_%s_Run2011A_PromptReco_v6_1409' % pd : {
      'datasetpath' : "/%s/Run2011A-PromptReco-v6/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-178677_7TeV_PromptReco_Collisions11_JSON.txt",
      'firstRun' : 172620,
      'lastRun' : 175831,
      'analyses' : analyses,
    },
    'data_%s_Run2011A_05Aug2011_v1' % pd : {
      'datasetpath' : "/%s/Run2011A-05Aug2011-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt",
      'firstRun' : 170249,
      'lastRun' : 172619,
      'analyses' : analyses,
    },
    'data_%s_Run2011A_PromptReco_v4' % pd : {
      'datasetpath' : "/%s/Run2011A-PromptReco-v4/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-178677_7TeV_PromptReco_Collisions11_JSON.txt",
      'firstRun' : 163870,
      'lastRun' : 170248,
      'analyses' : analyses,
    },
    'data_%s_Run2011A_May10ReReco_v1' % pd : {
      'datasetpath' : "/%s/Run2011A-May10ReReco-v1/AOD" % pd,
      'lumi_mask' : "FinalStateAnalysis/RecoTools/data/masks/Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt",
      'firstRun' : 160404,
      'lastRun' : 163869,
      'analyses' : analyses,
    },
  }
  sample_dict = {
    'data_%s' % pd : subsample_dict.keys()
  }
  return subsample_dict, sample_dict

# Build all the PDs we use
data_DoubleMu, list_DoubleMu = build_data_set('DoubleMu', ['VH'])
datadefs.update(data_DoubleMu)
data_name_map.update(list_DoubleMu)

data_MuEG, list_MuEG = build_data_set('MuEG', ['VH', 'HTT'])
datadefs.update(data_MuEG)
data_name_map.update(list_MuEG)

data_DoubleE, list_DoubleE = build_data_set('DoubleElectron', ['VH',])
datadefs.update(data_DoubleE)
data_name_map.update(list_DoubleE)

data_SingleMu, list_SingleMu = build_data_set('SingleMu', ['Tau', 'Mu'])
datadefs.update(data_SingleMu)
data_name_map.update(list_SingleMu)

data_TauPlusX, list_TauPlusX = build_data_set('TauPlusX', ['HTT', 'SSDL'])
datadefs.update(data_TauPlusX)
data_name_map.update(list_TauPlusX)

data_MuHad, list_MuHad = build_data_set('MuHad', ['SSDL'])
datadefs.update(data_MuHad)
data_name_map.update(list_MuHad)

if __name__ == "__main__":
    # Print a latex table of the samples
    samples = []
    for sample, sample_info in datadefs.iteritems():
        if 'data' not in sample:
            #samples.append(sample_info['datasetpath'].split('/')[1])
            samples.append(sample_info['datasetpath'])

    for sample in sorted(samples):
        print sample.replace('_', '\_') + ' \\\\'
