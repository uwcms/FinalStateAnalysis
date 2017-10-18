import FWCore.ParameterSet.Config as cms

patElectronConversionMatch = cms.EDProducer(
    'PATElectronConversionEmbedder',
    src             = cms.InputTag("fixme"),
    conversionSrc   = cms.InputTag("allConversions"),
    beamSpotSrc     = cms.InputTag("offlineBeamSpot")    
)
