'''

Embed rho as a user float in pat::Electrons

'''

import FWCore.ParameterSet.Config as cms

patElectronRhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho")
)
