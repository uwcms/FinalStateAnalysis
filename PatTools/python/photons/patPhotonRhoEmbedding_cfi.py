'''

Embed rho as a user float in pat::Photons

'''

import FWCore.ParameterSet.Config as cms

patPhotonRhoEmbedder = cms.EDProducer(
    "PhotonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsHZGPho", "rho"),
    userLabel = cms.string('kt6PFJetsRho')
)
