
'''

Ntuple branch template sets for topological variables (MT, etc)

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

mtToMET = PSet(
    # Raw means no MET corrections
    objectMtToMET = 'mtMET({object_idx}, "raw")',

    #PF Type1 MET (and systematics)
    objectMtToPFMET      = 'mtMET({object_idx}, "", "pfmet", ""     , 1)',
    objectMtToPfMet_Ty1  = 'mtMET({object_idx}, "", "pfmet", "type1", 1)',
    objectMtToPfMet_mes  = 'mtMET({object_idx}, "", "pfmet", "mes+" , 1)',
    objectMtToPfMet_tes  = 'mtMET({object_idx}, "", "pfmet", "tes+" , 1)',
    objectMtToPfMet_jes  = 'mtMET({object_idx}, "", "pfmet", "jes+" , 1)',
    objectMtToPfMet_ues  = 'mtMET({object_idx}, "", "pfmet", "ues+" , 1)',

    #MVA MET
    objectMtToMVAMET     = 'mtMET({object_idx}, "", "mvamet", "", 0)',

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
    object1_object2_CosThetaStar = 'abs(subcand({object1_idx}, {object2_idx}).get.daughterCosThetaStar(0))',

    #Pairs + MET
    object1_object2_ToMETDPhi_Ty1 = 'deltaPhi(subcand({object1_idx}, {object2_idx}).get.phi, evt.met("pfmet").userCand("type1").phi)',
)

svfit = PSet(
    object1_object2_SVfitMass = 'SVfit({object1_idx},{object2_idx})',
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
   vbfNJets = 'vbfVariables("pt >30& userInt(\'fullIdTight\') & userFloat(\'idLoose\')").nJets',
   vbfJetVeto30 = 'vbfVariables("pt >30& userInt(\'fullIdLoose\') & userFloat(\'idLoose\')").jets30',
   vbfJetVeto20 = 'vbfVariables("pt >30& userInt(\'fullIdLoose\')  & userFloat(\'idLoose\')").jets20',
   vbfJetVetoTight30 = 'vbfVariables("pt >30& userInt(\'fullIdTight\') & userFloat(\'idLoose\')").jets30',
   vbfJetVetoTight20 = 'vbfVariables("pt >30& userInt(\'fullIdTight\')  & userFloat(\'idLoose\')").jets20',
   vbfMVA = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\') ").mva',
   vbfMass = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").mass',
   vbfDeta = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").deta',
   vbfDphi = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dphi',
   vbfj1eta = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").eta1',
   vbfj2eta = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").eta2',
   vbfVispt = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").c2',
   vbfHrap = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").hrapidity',
   vbfDijetrap = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dijetrapidity',
   vbfDphihj = 'vbfVariables("pt >30& userInt(\'fullIdTight\')  & userFloat(\'idLoose\')").dphihj',
   vbfDphihjnomet = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dphihj_nomet',
   vbfj1pt = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").pt1',
   vbfj2pt = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").pt2',
   vbfdijetpt = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dijetpt',
   vbfditaupt = 'vbfVariables("pt >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").ditaupt',
   #vbfj1IdTight = 'vbfVariables("pt >30& userInt(\'fullIdLoose\') &  userFloat(\'idLoose\')").leadJet.userInt(\'fullIdTight\')', # crashes!!
   #vbfj2IdTight = 'vbfVariables("pt >30& userInt(\'fullIdLoose\') &  userFloat(\'idLoose\')").subleadJet.userInt(\'fullIdTight\')', # not protected in the code


)




