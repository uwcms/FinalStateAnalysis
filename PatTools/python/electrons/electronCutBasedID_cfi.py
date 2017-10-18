import FWCore.ParameterSet.Config as cms

available_wps = cms.VPSet(cms.PSet(name=cms.string("CBID_VETO"),
                                   index=cms.int32(0)),
                          cms.PSet(name=cms.string("CBID_LOOSE"),
                                   index=cms.int32(1)),
                          cms.PSet(name=cms.string("CBID_MEDIUM"),
                                   index=cms.int32(2)),
                          cms.PSet(name=cms.string("CBID_TIGHT"),
                                   index=cms.int32(3))
                          )
                          

patElectronCutBasedIdEmbedder = cms.EDProducer(
    "PATElectronCutBasedIdEmbedder",
    src            = cms.InputTag("fixme"),
    conversionsSrc = cms.InputTag("allConversions"),
    beamspotSrc    = cms.InputTag("offlineBeamSpot"),
    vtxSrc         = cms.InputTag("selectPrimaryVerticesQuality"),
    wps_to_apply   = cms.vstring("CBID_TIGHT",
                                 "CBID_MEDIUM",
                                 "CBID_LOOSE",
                                 "CBID_VETO"),                                 
    available_working_points = available_wps    
)
