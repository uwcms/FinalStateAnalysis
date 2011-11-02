import FWCore.ParameterSet.Config as cms

# A simple module which embeds a userCand with the uncorrected P4 of the jet.
# Must be run before any systematics or smearing is applied!

patJetUncorrectedEmbedder = cms.EDProducer(
    "PATJetUncorrectedEmbedder",
    src = cms.InputTag("fixme")
)
