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

patElectronZZ2012RhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJets", "rho"),
    # Used as userFloat label
    userLabel = cms.string("zzRho2012")
)

patElectronHZZ2012RhoEmbedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("double_kt6PFJets_rho", "rho"),
    # Used as userFloat label
    userLabel = cms.string("hzzRho2012")
)

patElectronHZGRho2011Embedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsCentralHZGEle", "rho"),
    # Used as userFloat label
    userLabel = cms.string("hzgRho2011")
)

patElectronHZGRho2012Embedding = cms.EDProducer(
    "ElectronRhoOverloader",
    src = cms.InputTag("fixme"),
    srcRho = cms.InputTag("kt6PFJetsHZGPho", "rho"),
    # Used as userFloat label
    userLabel = cms.string("hzgRho2012")
)
