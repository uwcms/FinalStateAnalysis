'''

Ntuple branch template sets for generic candidate objects.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

kinematics = PSet(
    objectPt = '{object}.pt',
    objectEta = '{object}.eta',
    objectAbsEta = 'abs({object}.eta)',
    objectPhi = '{object}.phi',
    objectCharge = '{object}.charge',
    objectMass = '{object}.mass',
)

vertex_info = PSet(
    objectDZ = '{object}.userFloat("dz")',
    objectVZ = '{object}.vz',
    objectIP3DS = '{object}.userFloat("ip3DS")',
)

# The info about the associated pat::Jet
base_jet = PSet(
    objectJetPt = '{object}.userFloat("jetPt")',
    objectJetBtag = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").bDiscriminator("") : -5',
    objectJetCSVBtag = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").bDiscriminator("combinedSecondaryVertexBJetTags") : -5',
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
)

