'''

Produce track candidates from GSF electrons

'''

import FWCore.ParameterSet.Config as cms

gsfTrackCandidates = cms.EDProducer(
    "GSFTrackCandidateProducer",
    src = cms.InputTag("electronGsfTracks"),
    threshold = cms.double(8.0),
    # This is just so our internal UW code doesn't update the src
    noSeqChain = cms.bool(True),
)
