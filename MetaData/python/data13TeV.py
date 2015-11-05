'''
Data definitions for 13 TeV samples.
'''

from datacommon import square, cube, quad, picobarns, br_w_leptons, br_z_leptons, query_cli
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


data_name_map = {}

datadefs = {}
datadefs["GluGlu_LFV_HToETau_M120_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToETau_M120_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,120,'ggf')[0], 
}
datadefs["VBF_LFV_HToETau_M120_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToETau_M120_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,120,'vbf')[0],
}
datadefs["GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,125,'ggf')[0],
}
datadefs["VBF_LFV_HToETau_M125_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToETau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,125,'vbf')[0],
}
datadefs["GluGlu_LFV_HToETau_M130_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToETau_M130_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,130,'ggf')[0],
}
datadefs["VBF_LFV_HToETau_M130_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToETau_M130_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,130,'vbf')[0],
}
datadefs["GluGlu_LFV_HToETau_M200_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToETau_M200_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,200,'ggf')[0],
}
datadefs["VBF_LFV_HToETau_M200_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToETau_M200_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,200,'vbf')[0],
}

datadefs["GluGlu_LFV_HToMuTau_M120_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToMuTau_M120_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,120,'ggf')[0], 
}
datadefs["VBF_LFV_HToMuTau_M120_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToMuTau_M120_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,120,'vbf')[0],
}
datadefs["GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToMuTau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,125,'ggf')[0],
}
datadefs["VBF_LFV_HToMuTau_M125_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToMuTau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,125,'vbf')[0],
}
datadefs["GluGlu_LFV_HToMuTau_M130_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToMuTau_M130_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,130,'ggf')[0],
}
datadefs["VBF_LFV_HToMuTau_M130_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToMuTau_M130_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,130,'vbf')[0],
}
datadefs["GluGlu_LFV_HToMuTau_M200_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/GluGlu_LFV_HToMuTau_M200_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR7',
    'x_sec': xs(14,200,'ggf')[0],
}
datadefs["VBF_LFV_HToMuTau_M200_13TeV_powheg_pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/VBF_LFV_HToMuTau_M200_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
    'pu': 'Asympt25ns',
    'calibrationTarget': 'RunIISpring15DR74',
    'x_sec': xs(14,200,'vbf')[0],
}

datadefs["DYJetsToLL_M-50_13TeV-madgraph-pythia8"]={
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 6025.2,
}

datadefs["DYJets_M50-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 6025.2*picobarns,
}
datadefs["TTJets-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 689.1*picobarns, # might be 809.1, I'm not sure. See https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
}
datadefs["ggHZZ-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 43.62*picobarns*0.00133, # xsec * br. ratio. BR for L=e,mu, might need to use BR with tau? (=0.000294)
}
datadefs["ZZTo4L-PU20bx25"] = {
    'analyses': ['4L'],
    'datasetpath': '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': 15.4*picobarns,
}
datadefs["WZTo3LNu-PU20bx25"] = {
    'analyses': [],
    'datasetpath': '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM',
    'pu': '20bx25',
    'calibrationTarget': 'Phys14DR',
    'x_sec': -999,
}


if __name__=="__main__":
    query_cli(datadefs)
