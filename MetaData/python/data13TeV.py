'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli, picobarns

data_name_map = {}

datadefs = {}

datadefs["Zjets_M50"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 6025.2*picobarns,
}
datadefs["Wjets"] = {
    'analyses': [],
    'datasetpath': '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 20508.9*picobarns,
}
datadefs["TTjets"] = {
    'analyses': ['4L'],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 689.1*picobarns, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}
datadefs["ggHZZ"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 43.62*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["VBFHZZ"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBF_HToZZTo4L_M-125_13TeV-powheg-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 3.72*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["DYJetsToLL_M-50"] = {
    'analyses' : ['4L'],
    'datasetpath' : '/DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu' : '20bx25',
    'calibrationTarget' : 'Spring14miniaod',
    'x_sec' : 6025.2*picobarns,
}
datadefs["ZZJetsTo4L"] = {
    'analyses' : ['4L'],
    'datasetpath' : '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu' : '20bx25',
    'calibrationTarget' : 'Spring14miniaod',
    'xsec' : 15.4*picobarns,
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
