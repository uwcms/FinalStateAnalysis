'''

Produce track candidates from muons

'''

import FWCore.ParameterSet.Config as cms

trackCandidates = cms.EDProducer(
    "TrackViewCandidateProducer",
    src = cms.InputTag("generalTracks"),
    particleType = cms.string('mu+'),
    cut = cms.string('pt > 8'),
    # This is just so our internal UW code doesn't update the src
    noSeqChain = cms.bool(True),
)

