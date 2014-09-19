'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli

data_name_map = {}

datadefs = {}

datadefs["Zjets_M50-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 6025.2*picobarns,
}
datadefs["Wjets-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 20508.9*picobarns,
}
datadefs["TTjets-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 689.1*picobarns, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}
datadefs["ggHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 43.62*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["VBFHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/VBF_HToZZTo4L_M-125_13TeV-powheg-pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 3.72*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["ZZTo4L-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': 15.4*picobarns,
}
datadefs["T_tW-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Tbar_tW-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["T_s-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Tbar_s-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["T_t-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/TToLeptons_t-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["Tbar_t-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_15to3000-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_1000to1400-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-1000to1400_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_10to15-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-10to15_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_120to170-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-120to170_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_1400to1800-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_15to30-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-15to30_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_170to300-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-170to300_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_1800-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-1800_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_1800to2400-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-1800to2400_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_2400to3200-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-2400to3200_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_300to470-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-300to470_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_30to50-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-30to50_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_3200-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-3200_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_470to600-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-470to600_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_50to80-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-50to80_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_5to10-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-5to10_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_600to800-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-600to800_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_800to1000-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-800to1000_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}
datadefs["QCD_80to120-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/QCD_Pt-80to120_Tune4C_13TeV_pythia8/Spring14miniaod-castor_PU20bx25_POSTLS170_V5-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Spring14miniaod',
    'x_sec': -999,
}

if __name__=="__main__":
    query_cli(datadefs)
