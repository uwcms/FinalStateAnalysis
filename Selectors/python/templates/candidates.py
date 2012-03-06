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
    objectIP3DS = '{object}.userFloat("ip3DS")',
)

# The info about the associated pat::Jet
base_jet = PSet(
    objectJetPt = '{object}.userFloat("jetPt")',
    objectJetBtag = '? {object}.userCand("patJet").isNonnull ? '
        '{object}.userCand("patJet").bDiscriminator("") : -5',
)
