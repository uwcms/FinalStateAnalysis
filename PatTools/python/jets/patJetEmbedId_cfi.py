import FWCore.ParameterSet.Config as cms

# Embed loose medium and tight official PFJet IDs into pat::Jets
# (see https://twiki.cern.ch/twiki/bin/view/CMS/JetID)
patJetId = cms.EDProducer(
    "PATJetIdEmbedder",
    src = cms.InputTag('fixme')
)
