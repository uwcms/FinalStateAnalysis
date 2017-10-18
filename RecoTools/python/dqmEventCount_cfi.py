'''

Embed the event count as a DQM float

'''

import FWCore.ParameterSet.Config as cms

dqmEventCount = cms.EDProducer(
    "DQMEventCounter",
    name = cms.string("processedEvents")
)
