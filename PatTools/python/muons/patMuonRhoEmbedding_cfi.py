'''

Embed rho as a user float in pat::Muons

'''

import FWCore.ParameterSet.Config as cms

patMuonRhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho")
)
