
'''

Ntuple branch template sets for topological variables (MT, etc)

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

mtToMET = PSet(
    objectMtToPfMet_type1   = 'mtMET({object_idx}, "", ""     )',
    objectDPhiToPfMet_type1 = 'deltaPhiToMEt({object_idx}, "", ""     )',
    #MVA MET
    objectMtToMVAMET     = 'mtMET({object_idx}, "", "mvamet", "", 0)',
    #objectToMETDPhi = 'deltaPhi({object}.phi, met().phi())',
)

# these things break if you pass a shifted met
shiftedMtToMET = PSet(
    # Raw means no MET corrections
    objectMtToPfMet_Raw = 'mtMET({object_idx}, "", "raw")',

    #PF Type1 MET (and systematics)
    objectMtToPfMet_JetResUp          = 'mtMET({object_idx}, "", "jres+")',
    objectMtToPfMet_JetEnUp           = 'mtMET({object_idx}, "", "jes+" )',
    objectMtToPfMet_MuonEnUp          = 'mtMET({object_idx}, "", "mes+" )',
    objectMtToPfMet_ElectronEnUp      = 'mtMET({object_idx}, "", "ees+" )',
    objectMtToPfMet_TauEnUp           = 'mtMET({object_idx}, "tesUpTaus", "tes+" )',
    objectMtToPfMet_UnclusteredEnUp   = 'mtMET({object_idx}, "", "ues+" )',
    objectMtToPfMet_PhotonEnUp        = 'mtMET({object_idx}, "", "pes+" )',

    objectMtToPfMet_JetResDown        = 'mtMET({object_idx}, "", "jres-")',
    objectMtToPfMet_JetEnDown         = 'mtMET({object_idx}, "", "jes-" )',
    objectMtToPfMet_MuonEnDown        = 'mtMET({object_idx}, "", "mes-" )',
    objectMtToPfMet_ElectronEnDown    = 'mtMET({object_idx}, "", "ees-" )',
    objectMtToPfMet_TauEnDown         = 'mtMET({object_idx}, "tesDownTaus", "tes-" )',
    objectMtToPfMet_UnclusteredEnDown = 'mtMET({object_idx}, "", "ues-" )',
    objectMtToPfMet_PhotonEnDown      = 'mtMET({object_idx}, "", "pes-" )',

    objectDPhiToPfMet_JetResUp          = 'deltaPhiToMEt({object_idx}, "", "jres+")',
    objectDPhiToPfMet_JetEnUp           = 'deltaPhiToMEt({object_idx}, "", "jes+" )',
    objectDPhiToPfMet_MuonEnUp          = 'deltaPhiToMEt({object_idx}, "", "mes+" )',
    objectDPhiToPfMet_ElectronEnUp      = 'deltaPhiToMEt({object_idx}, "", "ees+" )',
    objectDPhiToPfMet_TauEnUp           = 'deltaPhiToMEt({object_idx}, "", "tes+" )',
    objectDPhiToPfMet_UnclusteredEnUp   = 'deltaPhiToMEt({object_idx}, "", "ues+" )',
    objectDPhiToPfMet_PhotonEnUp        = 'deltaPhiToMEt({object_idx}, "", "pes+" )',

    objectDPhiToPfMet_JetResDown        = 'deltaPhiToMEt({object_idx}, "", "jres-")',
    objectDPhiToPfMet_JetEnDown         = 'deltaPhiToMEt({object_idx}, "", "jes-" )',
    objectDPhiToPfMet_MuonEnDown        = 'deltaPhiToMEt({object_idx}, "", "mes-" )',
    objectDPhiToPfMet_ElectronEnDown    = 'deltaPhiToMEt({object_idx}, "", "ees-" )',
    objectDPhiToPfMet_TauEnDown         = 'deltaPhiToMEt({object_idx}, "", "tes-" )',
    objectDPhiToPfMet_UnclusteredEnDown = 'deltaPhiToMEt({object_idx}, "", "ues-" )',
    objectDPhiToPfMet_PhotonEnDown      = 'deltaPhiToMEt({object_idx}, "", "pes-" )',
)

# Variables based on pairs of objects
pairs = PSet(
    object1_object2_Mass = 'subcand({object1_idx}, {object2_idx}).get.mass',
    object1_object2_Mt = 'subcand({object1_idx}, {object2_idx}).get.mt',
    object1_object2_collinearmass = 'collinearMassMET({object1_idx}, "", {object2_idx},"","")',
    object2_object1_collinearmass = 'collinearMassMET({object2_idx}, "", {object1_idx},"","")',
   
    object1_object2_Mass_TauEnUp = 'subcand({object1_idx}, "",{object2_idx},"tesUpTaus").get.mass',
    object1_object2_Mass_TauEnDown = 'subcand({object1_idx}, "",{object2_idx},"tesDownTaus").get.mass',
    object1_object2_Mt_TauEnUp = 'subcand({object1_idx}, "",{object2_idx},"tesUpTaus").get.mt',
    object1_object2_Mt_TauEnDown = 'subcand({object1_idx}, "",{object2_idx},"tesDownTaus").get.mt',
 
    object1_object2_collinearmass_JetEnUp = 'collinearMassMET({object1_idx}, "", {object2_idx},"","jes+")',
    object2_object1_collinearmass_JetEnUp = 'collinearMassMET({object2_idx}, "", {object1_idx},"","jes+")', # for now we only need m_t_coll
    object1_object2_collinearmass_JetEnDown = 'collinearMassMET({object1_idx}, "", {object2_idx},"","jes-")',
    object2_object1_collinearmass_JetEnDown = 'collinearMassMET({object2_idx}, "", {object1_idx},"","jes-")',
    object1_object2_collinearmass_UnclusteredEnUp = 'collinearMassMET({object1_idx}, "", {object2_idx},"","ues+")',
    object2_object1_collinearmass_UnclusteredEnUp = 'collinearMassMET({object2_idx}, "", {object1_idx},"","ues+")',
    object1_object2_collinearmass_UnclusteredEnDown = 'collinearMassMET({object1_idx}, "", {object2_idx},"","ues-")',
    object2_object1_collinearmass_UnclusteredEnDown = 'collinearMassMET({object2_idx}, "", {object1_idx},"","ues-")',
    object1_object2_collinearmass_TauEnUp = 'collinearMassMET({object1_idx}, "", {object2_idx},"tesUpTaus","tes+")',
    object1_object2_collinearmass_TauEnDown = 'collinearMassMET({object1_idx}, "", {object2_idx},"tesDownTaus","tes-")',


    object1_object2_Pt = 'subcand({object1_idx}, {object2_idx}).get.pt',
    object1_object2_Eta = 'subcand({object1_idx}, {object2_idx}).get.eta',
    object1_object2_Phi = 'subcand({object1_idx}, {object2_idx}).get.phi',
    object1_object2_DR = 'dR({object1_idx}, {object2_idx})',
    object1_object2_DPhi = 'dPhi({object1_idx}, {object2_idx})',
    object1_object2_SS = 'likeSigned({object1_idx}, {object2_idx})',
    object1_object2_PZeta = 'pZeta({object1_idx}, {object2_idx})',
    object1_object2_PZetaVis = 'pZetaVis({object1_idx}, {object2_idx})',
    object1_object2_CosThetaStar = 'abs(subcand({object1_idx}, {object2_idx}).get.daughterCosThetaStar(0))',

    #Pairs + MET
    object1_object2_ToMETDPhi_Ty1 = 'twoParticleDeltaPhiToMEt({object1_idx}, {object2_idx}, "type1")',
)

svfit = PSet(
    object1_object2_SVfitMass = 'SVfit({object1_idx},{object2_idx}).at(0)',
    object1_object2_SVfitPt = 'SVfit({object1_idx},{object2_idx}).at(1)',
    object1_object2_SVfitEta = 'SVfit({object1_idx},{object2_idx}).at(2)',
    object1_object2_SVfitPhi = 'SVfit({object1_idx},{object2_idx}).at(3)',
    object1_object2_SVfitMET = 'SVfit({object1_idx},{object2_idx}).at(4)',
)

finalstate = PSet(
    LT = 'ht',
    charge = 'charge',
    Pt = 'pt',
    Eta = 'eta',
    Phi = 'phi',
    Mass = 'mass',
    Mt = 'mt',
    Ht = 'jetHt("pt>30 && abs(eta)<2.5")',
    MassError = '? hasUserFloat("cand_dM") ? userFloat("cand_dM") : -999',
    MassErrord1 = '? hasUserFloat("cand_dM_0") ? userFloat("cand_dM_0") : -999',
    MassErrord2 = '? hasUserFloat("cand_dM_1") ? userFloat("cand_dM_1") : -999',
    MassErrord3 = '? hasUserFloat("cand_dM_2") ? userFloat("cand_dM_2") : -999',
    MassErrord4 = '? hasUserFloat("cand_dM_3") ? userFloat("cand_dM_3") : -999',
)


vbf = PSet(
  # If nJets < 2, none of these other branches are valid
   vbfNJets20 = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   vbfNJets30 = 'vbfVariables("pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   vbfJetVeto30 = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30',
   vbfJetVeto20 = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20',
   vbfMVA = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mva',
   vbfMass = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass',
   vbfDeta = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta',
   vbfDphi = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi',
   vbfj1eta = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta1',
   vbfj2eta = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta2',
   vbfVispt = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).c2',
   vbfHrap = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).hrapidity',
   vbfDijetrap = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetrapidity',
   vbfDphihj = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj',
   vbfDphihjnomet = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj_nomet',
   vbfj1pt = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt1',
   vbfj2pt = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt2',
   vbfdijetpt = 'vbfVariables("pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt',

   vbfNJets20_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   vbfNJets30_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   vbfJetVeto30_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30',
   vbfJetVeto20_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20',
   vbfMVA_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mva',
   vbfMass_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass',
   vbfDeta_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta',
   vbfDphi_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi',
   vbfj1eta_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta1',
   vbfj2eta_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta2',
   vbfVispt_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).c2',
   vbfHrap_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).hrapidity',
   vbfDijetrap_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetrapidity',
   vbfDphihj_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj',
   vbfDphihjnomet_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj_nomet',
   vbfj1pt_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt1',
   vbfj2pt_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt2',
   vbfdijetpt_JetEnUp =  'vbfVariables("userCand(\'jes+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt',

   vbfNJets20_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   vbfNJets30_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   vbfJetVeto30_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30',
   vbfJetVeto20_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20',
   vbfMVA_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mva',
   vbfMass_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass',
   vbfDeta_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta',
   vbfDphi_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi',
   vbfj1eta_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta1',
   vbfj2eta_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta2',
   vbfVispt_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).c2',
   vbfHrap_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).hrapidity',
   vbfDijetrap_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetrapidity',
   vbfDphihj_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj',
   vbfDphihjnomet_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj_nomet',
   vbfj1pt_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt1',
   vbfj2pt_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt2',
   vbfdijetpt_JetEnDown =  'vbfVariables("userCand(\'jes-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt',

   #vbfNJets20_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   #vbfNJets30_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   #vbfJetVeto30_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30',
   #vbfJetVeto20_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20',
   #vbfMVA_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mva',
   #vbfMass_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass',
   #vbfDeta_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta',
   #vbfDphi_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi',
   #vbfj1eta_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta1',
   #vbfj2eta_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta2',
   #vbfVispt_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).c2',
   #vbfHrap_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).hrapidity',
   #vbfDijetrap_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetrapidity',
   #vbfDphihj_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj',
   #vbfDphihjnomet_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj_nomet',
   #vbfj1pt_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt1',
   #vbfj2pt_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt2',
   #vbfdijetpt_JetResUp =  'vbfVariables("userCand(\'jres+\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt',

   #vbfNJets20_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   #vbfNJets30_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).nJets',
   #vbfJetVeto30_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets30',
   #vbfJetVeto20_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).jets20',
   #vbfMVA_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mva',
   #vbfMass_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).mass',
   #vbfDeta_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).deta',
   #vbfDphi_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphi',
   #vbfj1eta_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta1',
   #vbfj2eta_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).eta2',
   #vbfVispt_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).c2',
   #vbfHrap_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).hrapidity',
   #vbfDijetrap_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetrapidity',
   #vbfDphihj_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj',
   #vbfDphihjnomet_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dphihj_nomet',
   #vbfj1pt_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt1',
   #vbfj2pt_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).pt2',
   #vbfdijetpt_JetResDown =  'vbfVariables("userCand(\'jres-\').pt() >30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5", 0.5).dijetpt',
  
)


extraJet = PSet(
    objectPt = '? evt.jets.size()>{object_idx} ? {object}.pt() : -999',
    objectEta = '? evt.jets.size()>{object_idx} ? {object}.eta() : -999',
    objectPhi = '? evt.jets.size()>{object_idx} ? {object}.phi() : -999',
    objectIDTight = '? evt.jets.size()>{object_idx} ? {object}.userFloat("idTight") : -999',
    objectIDTightLepVeto = '? evt.jets.size()>{object_idx} ? {object}.userFloat("idTightLepVeto") : -999',
    objectIDLoose = '? evt.jets.size()>{object_idx} ? {object}.userFloat("idLoose") : -999',
    objectPUMVA = '? evt.jets.size()>{object_idx} & {object}.pt()>20 & abs({object}.eta())<2.5 ? {object}.userFloat("pileupJetId:fullDiscriminant") : -999',
    objectBJetCISV = '? evt.jets.size()>{object_idx} & {object}.pt()>20 & abs({object}.eta())<2.5 ? {object}.bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') : -999',
)
