'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli

data_name_map = {}

datadefs = {}

datadefs["Zjets_M50"] = {
    'analyses': [],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Wjets"] = {
    'analyses': [],
    'datasetpath': '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["TTjets"] = {
    'analyses': [],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["ggHZZ"] = {
    'analyses': [],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["VBFHZZ"] = {
    'analyses': [],
    'datasetpath': '/VBF_HToZZTo4L_M-125_13TeV-powheg-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Bprime_M1000"] = {
    'analyses': [],
    'datasetpath': '/BprimeBprime_M_1000_Tune4C_13TeV-madgraph/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Bprime_M2000"] = {
    'analyses': [],
    'datasetpath': '/BprimeBprime_M_2000_Tune4C_13TeV-madgraph/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Bprime_M3000"] = {
    'analyses': [],
    'datasetpath': '/BprimeBprime_M_3000_Tune4C_13TeV-madgraph/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}

if __name__=="__main__":
    query_cli(datadefs)
