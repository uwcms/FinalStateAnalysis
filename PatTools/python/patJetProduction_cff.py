import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.jets.patJetEmbedId_cfi import patJetId

customizeJetSequence = cms.Sequence()

customizeJetSequence += patJetId
