'''

Embed rho as a user float in pat::Muons

'''

import FWCore.ParameterSet.Config as cms

patMuonRhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho")
)


# Version which uses ZZ recipe
patMuonZZRhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsForIso", "rho"),
    # Used as userFloat label
    userLabel = cms.string("zzRho")
)

patMuonZZ2012RhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsCentralNeutral", "rho"),
    # Used as userFloat label
    userLabel = cms.string("zzRho2012")
)

patMuonHZG2011RhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsCentralHZGMu", "rho"),
    # Used as userFloat label
    userLabel = cms.string("hzgRho2011")
)

patMuonHZG2012RhoEmbedding = cms.EDProducer(
    "MuonRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsCentralNeutralHZGMu", "rho"),
    # Used as userFloat label
    userLabel = cms.string("hzgRho2012")
)
