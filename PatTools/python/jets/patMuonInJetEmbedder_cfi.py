import FWCore.ParameterSet.Config as cms

'''
Embed information about muons/electrons found in jets
'''

patMuonInJetEmbedder = cms.EDProducer(
    "PATMuonInJetEmbedder",
    src = cms.InputTag("fixme"),
    srcVertex = cms.InputTag("selectedPrimaryVertex"),
)
