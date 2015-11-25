
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
    objectMtToPfMet_TauEnUp           = 'mtMET({object_idx}, "", "tes+" )',
    objectMtToPfMet_UnclusteredEnUp   = 'mtMET({object_idx}, "", "ues+" )',
    objectMtToPfMet_PhotonEnUp        = 'mtMET({object_idx}, "", "pes+" )',

    objectMtToPfMet_JetResDown        = 'mtMET({object_idx}, "", "jres-")',
    objectMtToPfMet_JetEnDown         = 'mtMET({object_idx}, "", "jes-" )',
    objectMtToPfMet_MuonEnDown        = 'mtMET({object_idx}, "", "mes-" )',
    objectMtToPfMet_ElectronEnDown    = 'mtMET({object_idx}, "", "ees-" )',
    objectMtToPfMet_TauEnDown         = 'mtMET({object_idx}, "", "tes-" )',
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
    object1_object2_SVfitMass = 'SVfit({object1_idx},{object2_idx})',
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
    MassError = 'userFloat("cand_dM")',
    MassErrord1 = 'userFloat("cand_dM_0")',
    MassErrord2 = 'userFloat("cand_dM_1")',
    MassErrord3 = 'userFloat("cand_dM_2")',
    MassErrord4 = 'userFloat("cand_dM_3")'
)


vbf = PSet(
  # If nJets < 2, none of these other branches are valid
   vbfNJets = 'vbfVariables("pt >30").nJets',
   vbfJetVeto30 = 'vbfVariables("pt >30").jets30',
   vbfJetVeto20 = 'vbfVariables("pt >30").jets20',
   vbfJetVetoTight30 = 'vbfVariables("pt >30").jets30',
   vbfJetVetoTight20 = 'vbfVariables("pt >30").jets20',
   vbfMVA = 'vbfVariables("pt >30").mva',
   vbfMass = 'vbfVariables("pt >30").mass',
   vbfDeta = 'vbfVariables("pt >30").deta',
   vbfDphi = 'vbfVariables("pt >30").dphi',
   vbfj1eta = 'vbfVariables("pt >30").eta1',
   vbfj2eta = 'vbfVariables("pt >30").eta2',
   vbfVispt = 'vbfVariables("pt >30").c2',
   vbfHrap = 'vbfVariables("pt >30").hrapidity',
   vbfDijetrap = 'vbfVariables("pt >30").dijetrapidity',
   vbfDphihj = 'vbfVariables("pt >30").dphihj',
   vbfDphihjnomet = 'vbfVariables("pt >30").dphihj_nomet',
   vbfj1pt = 'vbfVariables("pt >30").pt1',
   vbfj2pt = 'vbfVariables("pt >30").pt2',
   vbfdijetpt = 'vbfVariables("pt >30").dijetpt',
   vbfditaupt = 'vbfVariables("pt >30").ditaupt',
)


extraJet = PSet(
    objectPt = '? evt.jets.size()>{object_idx} ? {object}.pt() : -999',
    objectEta = '? evt.jets.size()>{object_idx} ? {object}.eta() : -999',
    objectPhi = '? evt.jets.size()>{object_idx} ? {object}.phi() : -999',

    objectIDTight = '? evt.jets.size()>{object_idx} ? {object}.userFloat("idTight") : -999',
    objectIDTightLepVeto = '? evt.jets.size()>{object_idx} ? {object}.userFloat("idTightLepVeto") : -999',
    objectIDLoose = '? evt.jets.size()>{object_idx} ? {object}.userFloat("idLoose") : -999',
    objectPUMVA = '? evt.jets.size()>{object_idx} ? {object}.userFloat("pileupJetId:fullDiscriminant") : -999',
    objectBJetCISV = '? evt.jets.size()>{object_idx} ? {object}.bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') : -999',
)
