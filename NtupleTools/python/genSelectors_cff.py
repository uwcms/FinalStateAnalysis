import FWCore.ParameterSet.Config as cms

from PhysicsTools.JetMCAlgos.TauGenJets_cfi import tauGenJets

zBosons = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        'drop *',
        'keep++ pdgId = {Z0}',
        'drop pdgId = {Z0} & status = 2',
    )
)

wBosons = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        'drop *',
        'keep++ abs(pdgId) = {24}',
        'drop abs(pdgId) = {24} & status = 2',
    )
)

higgsBosons = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        'drop *',
        'keep++ pdgId = 25',
        'drop pdgId = 25 & status = 2',
    )
)

genTausFromZs = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("zBosons"),
    select = cms.vstring(
        'drop *',
        'keep++ pdgId = 15',
    )
)

genTausFromHiggs = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("higgsBosons"),
    select = cms.vstring(
        'drop *',
        'keep++ pdgId = 15',
    )
)

tauGenJetsFromZs = tauGenJets.clone(
    GenParticles = cms.InputTag('genTausFromZs')
)

tauGenJetsFromHiggs = tauGenJets.clone(
    GenParticles = cms.InputTag('genTausFromHiggs')
)

genEwkTauSelectors = cms.Sequence(
    zBosons
    +wBosons
    +higgsBosons
    +genTausFromZs
    +genTausFromHiggs
    +tauGenJetsFromZs
    +tauGenJetsFromHiggs
)
