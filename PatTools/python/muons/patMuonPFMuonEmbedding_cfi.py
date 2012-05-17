'''

Embed a reference to the PF Muon into the pat::Muon, if it exists.

(the pat::Muon is seeded by default using reco::Muons)

Author: Evan K. Friis, UW


'''

import FWCore.ParameterSet.Config as cms

patMuonPFMuonEmbedding = cms.EDProducer(
    "PATMuonPFMuonEmbedder",
    src = cms.InputTag("fixme"),
    pfSrc = cms.InputTag("particleFlow"),
)
