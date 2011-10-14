# Conversions to pico barns
_millibarns = 1.0e+9
_microbarns = 1.0e+6
_nanobarns  = 1.0e+3
_picobarns =  1.0
_femtobarns = 1.0e-3

data_name_map = {
    #'ztt' : 'Ztautau_pythia',
    'zjets' : 'Zjets_M50',
    'qcd' : 'PPmuXptGt20Mu15',
    'wjets' : 'WplusJets_madgraph',
    #'zll' : 'Zmumu_M20_pythia',
    'ttbar': 'TTplusJets_madgraph',
    'data': ['data_SingleMu_Run2011A_May10ReReco_v1',
             'data_SingleMu_Run2011A_PromptReco_v4',
             'data_SingleMu_Run2011A_05Aug2011_v1'],
}

stack_order = [
    #'zll',
    'ttbar',
    'qcd',
    #'ztt',
    'zjets',
    'wjets',
]

datadefs = {
    #'all_data' : {
        #'fake' : 1.0
    #},
    'data_SingleMu_Run2011A_PromptReco_v4' : {
        # Obsolete
        'datasetpath' : "/SingleMu/Run2011A-PromptReco-v4/AOD",
        'lumi_mask' : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Prompt/Cert_160404-170307_7TeV_PromptReco_Collisions11_JSON.txt",
        'firstRun' : 165071,
        'lastRun' : 170248,
        'conditions' : 'GR_R_42_V14::All',
        'size' : 2559.86,
        'skim' : 0.240326,
    },
    'data_SingleMu_Run2011A_05Aug2011_v1' : {
        'datasetpath' : "/SingleMu/Run2011A-05Aug2011-v1/AOD",
        'lumi_mask' : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Reprocessing/Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.txt",
        'firstRun' : 170249,
        'lastRun' : 172619,
        'conditions' : 'GR_R_42_V14::All',
        'size' : 3225.78,
        'skim' : 0.185,
    },
    'data_SingleMu_Run2011A_May10ReReco_v1' : {
        'datasetpath' : '/SingleMu/Run2011A-May10ReReco-v1/AOD',
        'lumi_mask' : "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Reprocessing/Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v2.txt",
        'firstRun' : 150329,
        'lastRun' : 163869,
        'conditions' : 'GR_R_42_V14::All',
        'size' : 867.464,
        'skim' : 0.112022
    },
    'Zjets_M50' : {
        'datasetpath' : '/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM',
        'x_sec' : 3048*_picobarns, # FIX ME
        'size' : 3768,
        'skim' : 0.149
    },
    'Ztautau_pythia' : {
        'datasetpath' : "/DYToTauTau_M-20_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
        'x_sec' : 1666*_picobarns,
        'skim' : 0.029136,
        'size' : 651,
    },
    'Ztautau_M10_pythia' : {
        'datasetpath' : "/DYToTauTau_M-10To20_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
        'x_sec' : 1666*_picobarns,
        'skim' : 0.00017,
        'size' : 2425,
    },
    'Zmumu_M20_pythia' : {
        'datasetpath' : "/DYToMuMu_M-20_TuneZ2_7TeV-pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
        'x_sec' : 1666*_picobarns,
        'skim' : 0.2642,
        'size' : 703,
    },
    'Zmumu_M10_20_pythia' : {
        'datasetpath' : "/DYToMuMu_M-10To20_TuneZ2_7TeV-pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
        'x_sec' : 1666*_picobarns,
        'skim' : 0.0087,
        'size' : 740,
    },
    'PPmuXptGt20Mu15' : {
        'datasetpath' : "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM",
        'x_sec' : 0.2966*_millibarns*2.855e-4, # x-sec * gen filter efficiency
        'x_sec' : 84679*_picobarns,
        'skim' : 0.0466,
        'size' : 3631,
    },
    'WplusJets_madgraph' : {
        'datasetpath' : "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
        'x_sec' : 31314*_picobarns,
        'skim' :  0.096,
        'size' : 3639,
    },
    'TTplusJets_madgraph' : {
        'datasetpath' : "/TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM",
        'x_sec' : 157.5*_picobarns, # NLO cross-section from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
        'skim' : 0.1489,
        'size' : 3238,
    },
}
