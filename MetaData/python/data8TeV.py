'''

Dataset definitions for 8TeV

Author: Evan K. Friis, UW Madison

'''

from datacommon import square, cube, quad, picobarns, br_w_leptons

# Figure this out later.
data_name_map = None

datadefs = {
    'WplusJets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Maria',
    },
    'Zjets_M50' : {
        'analyses': ['HTT'],
        'datasetpath': '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Josh',
    },
    'TTplusJets_madgraph' : {
        'analyses': ['HTT'],
        'datasetpath': '/TTJets_TuneZ2star_8TeV-madgraph-tauola/Summer12-PU_S7_START52_V5-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Evan',
    },
    'WZJetsTo3LNu_pythia' : {
        'analyses': ['HTT'],
        'datasetpath': '/WZTo3LNu_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Evan',
    },
    'WWJetsTo2L2Nu_TuneZ2_7TeV' : {
        'analyses': ['HTT'],
        'datasetpath': '/WWTo2L2Nu_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Josh',
    },
    'ZZJetsTo4L_pythia' : {
        'analyses': ['HTT'],
        'datasetpath': '/ZZTo4L_TuneZ2star_8TeV_pythia6_tauola/Summer12-PU_S7_START52_V9-v1/AODSIM',
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Ian',
    },
}

# Add GGH H2Tau samples
for mass in range(110, 165, 5):
    datadefs['GGH_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT'],
        'datasetpath': '/GluGluToHToTauTau_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Josh',
    }

# Add VBF H2Tau samples - not all done.
for mass in [110, 115, 120, 125, 135, 145, 155]:
    datadefs['VBF_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT'],
        'datasetpath': '/VBF_HToTauTau_M-%i_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM' % mass,
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Josh',
    }

# Add WH TauTau signal samples
for mass in [115, 120, 125, 130, 140, 145, 150, 155, 160]:
    datadefs['VH_H2Tau_M-%i' % mass] = {
        'analyses': ['HTT', 'VH'],
        'datasetpath': '/WH_ZH_TTH_HToTauTau_M-%i_8TeV-pythia6-tauola/Summer12-PU_S7_START52_V9-v2/AODSIM' % mass,
        'pu': 'S7',
        'xsec': -999,
        'responsible' : 'Evan',
    }
