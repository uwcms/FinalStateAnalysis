'''

Embed tight ID working point cuts into

See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon

'''

import FWCore.ParameterSet.Config as cms

patMuonTightIDEmbedding = cms.EDProducer(
    "PATMuonWorkingPointEmbedder",
    src = cms.InputTag('fixme'),
    userIntLabel = cms.string('tightID'),
    categories = cms.VPSet(
        cms.PSet(
            category = cms.string('pt > 0'),
            cut = cms.vstring(
                'isGlobalMuon',
                'pfCandidateRef.isNonnull',
                'globalTrack.hitPattern.numberOfValidMuonHits > 0',
                'globalTrack.normalizedChi2 < 10.',
                'numberOfMatchedStations > 1',
                'dB < 0.2',
                'abs(userFloat("dz")) < 0.5',
                'innerTrack.hitPattern.numberOfValidPixelHits > 0',
                'track().hitPattern().trackerLayersWithMeasurement() > 5'
            )
        ),
    )
)
