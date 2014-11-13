
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
    objectMtToPFMET      = 'mtMET({object_idx}, "", "pfmet", ""     , 1)',#1, apply phi correction
    objectMtToPfMet_Ty1  = 'mtMET({object_idx}, "", "pfmet", "type1", 1)',
    objectMtToPfMet_mes  = 'mtMET({object_idx}, "", "pfmet", "mes+" , 1)',
    objectMtToPfMet_tes  = 'mtMET({object_idx}, "", "pfmet", "tes+" , 1)',
    #objectMtToPfMet_jes  = 'mtMET({object_idx}, "", "pfmet", "jes+" , 1)',
    objectMtToPfMet_ues  = 'mtMET({object_idx}, "", "pfmet", "ues+" , 1)',
    objectMtToPfMet_Ty1_ues_plus = 'mtMET({object_idx}, "", "pfmet", "type1", "ues+", 1)',
    objectMtToPfMet_Ty1_ues_minus = 'mtMET({object_idx}, "", "pfmet", "type1", "ues-", 1)',
    objectMtToPfMet_mes_plus  = 'mtMET({object_idx}, "", "pfmet", "mes+" , 1)',
    objectMtToPfMet_tes_plus  = 'mtMET({object_idx}, "", "pfmet", "tes+" , 1)',
    #objectMtToPfMet_jes_plus  = 'mtMET({object_idx}, "", "pfmet", "jes+" , 1)',
    objectMtToPfMet_ues_plus  = 'mtMET({object_idx}, "", "pfmet", "ues+" , 1)',
    objectMtToPfMet_mes_minus  = 'mtMET({object_idx}, "", "pfmet", "mes-" , 1)',
    objectMtToPfMet_tes_minus  = 'mtMET({object_idx}, "", "pfmet", "tes-" , 1)',
    #objectMtToPfMet_jes_minus  = 'mtMET({object_idx}, "", "pfmet", "jes-" , 1)',
    objectMtToPfMet_ues_minus  = 'mtMET({object_idx}, "", "pfmet", "ues-" , 1)',

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
    #object1_object2_ToMETDPhi_jes_plus = 'deltaPhi(subcand({object1_idx}, {object2_idx}).get.phi, evt.met("pfmet").userCand("jes+").phi)',
    #object1_object2_ToMETDPhi_jes_minus = 'deltaPhi(subcand({object1_idx}, {object2_idx}).get.phi, evt.met("pfmet").userCand("jes-").phi)', 
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
    object1_object2_Zcompat = 'zCompatibility({object1_idx}, {object2_idx})',
    object1_object2_MassFsr = 'subcandfsr({object1_idx}, {object2_idx}).get.mass',
    object1_object2_PtFsr   = 'subcandfsr({object1_idx}, {object2_idx}).get.pt',
)

zzfsr = PSet(
    MassFsr                 = 'p4fsr().M',
    PtFsr                   = 'p4fsr().pt',
    KD                      = 'userFloat("KD")',

    # KD angles
    costheta1               = 'userFloat("costheta1")',
    costheta2               = 'userFloat("costheta2")',
    costhetastar            = 'userFloat("costhetastar")',
    Phi                     = 'userFloat("Phi")',
    Phi1                    = 'userFloat("Phi1")',

    # Gen-level KD angles
    costheta1_gen           = 'userFloat("costheta1_gen")',
    costheta2_gen           = 'userFloat("costheta2_gen")',
    costhetastar_gen        = 'userFloat("costhetastar_gen")',
    Phi_gen                 = 'userFloat("Phi_gen")',
    Phi1_gen                = 'userFloat("Phi1_gen")'
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
   #vbfNJetsjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') & userFloat(\'idLoose\')").nJets',
   #vbfJetVeto30jes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdLoose\') & userFloat(\'idLoose\')").jets30',
   #vbfJetVeto20jes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdLoose\')  & userFloat(\'idLoose\')").jets20',
   #vbfJetVetoTight30jes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') & userFloat(\'idLoose\')").jets30',
   #vbfJetVetoTight20jes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\')  & userFloat(\'idLoose\')").jets20',
   #vbfMVAjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\') ").mva',
   #vbfMassjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").mass',
   #vbfDetajes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").deta',
   #vbfDphijes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dphi',
   #vbfj1etajes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").eta1',
   #vbfj2etajes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").eta2',
   #vbfVisptjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").c2',
   #vbfHrapjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").hrapidity',
   #vbfDijetrapjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dijetrapidity',
   #vbfDphihjjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\')  & userFloat(\'idLoose\')").dphihj',
   #vbfDphihjnometjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dphihj_nomet',
   #vbfj1ptjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").pt1',
   #vbfj2ptjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").pt2',
   #vbfdijetptjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dijetpt',
   #vbfditauptjes_plus = 'vbfVariables("userCand(\'jes+\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").ditaupt',
   #vbfNJetsjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') & userFloat(\'idLoose\')").nJets',
   #vbfJetVeto30jes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdLoose\') & userFloat(\'idLoose\')").jets30',
   #vbfJetVeto20jes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdLoose\')  & userFloat(\'idLoose\')").jets20',
   #vbfJetVetoTight30jes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') & userFloat(\'idLoose\')").jets30',
   #vbfJetVetoTight20jes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\')  & userFloat(\'idLoose\')").jets20',
   #vbfMVAjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\') ").mva',
   #vbfMassjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").mass',
   #vbfDetajes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").deta',
   #vbfDphijes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dphi',
   #vbfj1etajes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").eta1',
   #vbfj2etajes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").eta2',
   #vbfVisptjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").c2',
   #vbfHrapjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").hrapidity',
   #vbfDijetrapjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dijetrapidity',
   #vbfDphihjjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\')  & userFloat(\'idLoose\')").dphihj',
   #vbfDphihjnometjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dphihj_nomet',
   #vbfj1ptjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").pt1',
   #vbfj2ptjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").pt2',
   #vbfdijetptjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").dijetpt',
   #vbfditauptjes_minus = 'vbfVariables("userCand(\'jes-\').pt() >30& userInt(\'fullIdTight\') &  userFloat(\'idLoose\')").ditaupt',
)

