'''

Ntuple branch template sets for generic candidate objects.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

kinematics = PSet(
    objectPt = '{object}.pt',
    objectPt_tes_plus = '? {object}.userCand("tes+").isNonnull() ? {object}.userCand("tes+").pt : 0',
    objectPt_tes_minus = '? {object}.userCand(\'tes-\').isNonnull() ? {object}.userCand(\'tes-\').pt: 0',
    objectPt_ees_plus = '? {object}.userCand(\'ees+\').isNonnull() ? {object}.userCand(\'ees+\').pt :0',
    objectPt_ees_minus = '? {object}.userCand(\'ees-\').isNonnull() ? {object}.userCand(\'ees-\').pt:0',
    objectEta = '{object}.eta',
    objectAbsEta = 'abs({object}.eta)',
    objectPhi = '{object}.phi',
    objectCharge = '{object}.charge',
    objectMass = '{object}.mass',
    objectRank ='{object}.userFloat("rankByPt")'
)

vertex_info = PSet(
    objectVZ = '{object}.vz',
    objectIP3D = 'getIP3D({object_idx})',
    objectIP3DErr = 'getIP3DErr({object_idx})', # uncertainty of IP3D
    objectSIP3D = 'getIP3D({object_idx}) / getIP3DErr({object_idx})',
    objectPVDZ = 'getPVDZ({object_idx})',
    objectPVDXY = 'getPVDXY({object_idx})',
    objectSIP2D = 'getIP2D({object_idx}) / getIP2DErr({object_idx})',
#    objectPVAssociation = '{object}.fromPV', # 0->used in PV fit, 1->PV is closest VTX, 2->other VTX is closest, 3->used in other VTX fit
)

# The info about the associated pat::Jet
base_jet = PSet(
    objectJetPt = '{object}.userFloat("jetPt")',
    objectJetBtag = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").bDiscriminator("") : -5',
    objectJetPFCISVBtag = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") : -5',
    objectJetEtaPhiSpread = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").constituentEtaPhiSpread() : -5',
    objectJetEtaEtaMoment = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").etaetaMoment() : -5',
    objectJetEtaPhiMoment = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").etaphiMoment() : -5',
    objectJetPhiPhiMoment = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").phiphiMoment() : -5',
    objectJetArea = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").jetArea() : -5',
    #objectJetptD  =   '? {object}.userCand("patJet").isNonnull ? '
    #'jetVariables({object_idx}, "ptD") : -100',
    #objectJetaxis1  =   '? {object}.userCand("patJet").isNonnull ? '
    #'jetVariables({object_idx},"axis1") : -100 ',
    #objectJetaxis2  =   '? {object}.userCand("patJet").isNonnull ? '
    #'jetVariables({object_idx},"axis2") : -100',
    #objectJetmult  =   '? {object}.userCand("patJet").isNonnull ? '
    #'jetVariables({object_idx},"mult") : -100',
    #objectJetmultMLPQC  =   '? {object}.userCand("patJet").isNonnull ? '
    #'jetVariables({object_idx},"mult_MLP_QC") : -100 ',
    #objectJetmultMLP    =   '? {object}.userCand("patJet").isNonnull ? '
    #'jetVariables({object_idx},"mult_MLP") : -100',
    objectJetPartonFlavour = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").partonFlavour : -100',
)

