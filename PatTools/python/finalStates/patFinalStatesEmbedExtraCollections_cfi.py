import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.finalStates.patFinalStateVertexFitter_cfi \
     import patFinalStateVertexFitter

from FinalStateAnalysis.PatTools.finalStates.patFinalStateMassResolutionEmbedder_cfi\
     import finalStateMassResolutionEmbedder

patFinalStatesEmbedTaus = cms.EDProducer(
    "PATFinalStateOverlapEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("cleanPatTaus"),
    name = cms.string("extTaus"), # external taus
    minDeltaR = cms.double(0.3),
    maxDeltaR = cms.double(1e9),
    # only keep stuff that isn't total garbage.  Here we require that the
    # pat::Jet thats matched to the tau has at least 5 GeV of Pt
    cut = cms.string('userCand("patJet").pt > 10'),
)

patFinalStatesEmbedJets = cms.EDProducer(
    "PATFinalStateOverlapEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("selectedPatJets"),
    name = cms.string("extJets"), # external taus
    minDeltaR = cms.double(0.3),
    maxDeltaR = cms.double(1e9),
    cut = cms.string('pt > 10'),
)

patFinalStatesEmbedJetschs = cms.EDProducer(
    "PATFinalStateOverlapEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("selectedPatJetsAK5chsPF"),
    name = cms.string("extJetschs"), # external taus
    minDeltaR = cms.double(0.3),
    maxDeltaR = cms.double(1e9),
    cut = cms.string('pt > 20'),
)



patFinalStatesEmbedMuons = cms.EDProducer(
    "PATFinalStateOverlapEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("cleanPatMuons"),
    name = cms.string("extMuons"), # external taus
    # Make this small, so we can pick up stuff like J/Psi
    minDeltaR = cms.double(0.05),
    maxDeltaR = cms.double(1e9),
    cut = cms.string(''),
)

patFinalStatesEmbedElectrons = cms.EDProducer(
    "PATFinalStateOverlapEmbedder",
    src = cms.InputTag("fixme"),
    toEmbedSrc = cms.InputTag("cleanPatElectrons"),
    name = cms.string("extElecs"), # external taus
    minDeltaR = cms.double(0.1),
    maxDeltaR = cms.double(1e9),
    cut = cms.string(''),
)

patFinalStatesEmbedObjects = cms.Sequence(
    patFinalStateVertexFitter#+
    #finalStateMassResolutionEmbedder
    # We do this on the fly now
    #+ patFinalStatesEmbedTaus
    #+ patFinalStatesEmbedElectrons
    #+ patFinalStatesEmbedMuons
)
