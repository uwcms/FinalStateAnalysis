'''

Embed a link to the matched PAT jet into the tau.

Author: Evan K. Friis, UW

'''
import FWCore.ParameterSet.Config as cms

patTausEmbedJetInfo = cms.EDProducer(
    "PATTauJetInfoEmbedder",
    src=cms.InputTag("fixme"),
    embedBtags=cms.bool(False),
    suffix=cms.string(''),
    jetSrc=cms.InputTag("selectedPatJets"),
    maxDeltaR=cms.double(0.1),
)
