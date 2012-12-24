
'''

Ntuple branch template sets for topological variables (MT, etc)

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

mtToMET = PSet(
    # Raw means no MET corrections
    objectMtToMET = 'mtMET({object_idx}, "raw")',
    objectToMETDPhi = 'deltaPhi({object}.phi, met().phi())',
)

# Variables based on pairs of objects
pairs = PSet(
    object1_object2_Mass = 'subcand({object1_idx}, {object2_idx}).get.mass',
    object1_object2_Pt = 'subcand({object1_idx}, {object2_idx}).get.pt',
    object1_object2_DR = 'dR({object1_idx}, {object2_idx})',
    object1_object2_DPhi = 'dPhi({object1_idx}, {object2_idx})',
    object1_object2_SS = 'likeSigned({object1_idx}, {object2_idx})',
    object1_object2_PZeta = 'pZeta({object1_idx}, {object2_idx})',
    object1_object2_PZetaVis = 'pZetaVis({object1_idx}, {object2_idx})',
    
)

finalstate = PSet(
    LT = 'ht',
    charge = 'charge',
    Pt = 'pt',
    Mass = 'mass',
    MassError = 'userFloat("cand_dM")',
    MassErrord1 = 'userFloat("cand_dM_0")',
    MassErrord2 = 'userFloat("cand_dM_1")',
    MassErrord3 = 'userFloat("cand_dM_2")',
    MassErrord4 = 'userFloat("cand_dM_3")'    
)

# Branches for identifying Z bosons using a pair of objects
zboson = PSet(
    # Absolute distance to Z mass.  If SS, returns 1000.  The smaller the more
    # "Z like"
    object1_object2_Zcompat = 'zCompatibility({object1_idx}, {object2_idx})'
)

vbf = PSet(
    # If nJets < 2, none of these other branches are valid
    vbfNJets = 'vbfVariables("pt > 30 & userInt(\'fullIdLoose\')").jets20',
    vbfJetVeto30 = 'vbfVariables("pt > 30 & userInt(\'fullIdLoose\')").jets30',
    vbfJetVeto20 = 'vbfVariables("pt > 30 & userInt(\'fullIdLoose\')").jets20',
    vbfMVA = 'vbfVariables("pt > 30 & userInt(\'fullIdLoose\')").mva',
    vbfMass = 'vbfVariables("pt > 30 & userInt(\'fullIdLoose\')").mass',
    vbfDeta = 'vbfVariables("pt > 30 & userInt(\'fullIdLoose\')").deta',
)
