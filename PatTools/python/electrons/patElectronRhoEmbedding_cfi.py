'''

Embed rho as a user float in pat::Electrons

'''

import FWCore.ParameterSet.Config as cms

patElectronRhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho")
)

# Version which uses ZZ recipe
patElectronZZRhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsForIso", "rho"),
    # Used as userFloat label
    userLabel = cms.string("zzRho")
)
