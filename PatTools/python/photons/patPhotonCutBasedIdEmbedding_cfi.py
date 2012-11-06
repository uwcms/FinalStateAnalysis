import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.PatTools.photons.photonCutBasedIdConfiguration_cfi \
        import cbid_LOOSE, cbid_MEDIUM, cbid_TIGHT

from copy import deepcopy

patPhotonCutBasedIdEmbedder = cms.EDProducer(
    "PATPhotonCutBasedIDEmbedder",
    LOOSE  = deepcopy(cbid_LOOSE),
    MEDIUM = deepcopy(cbid_MEDIUM),
    TIGHT  = deepcopy(cbid_TIGHT),
    idsToApply     = cms.vstring("LOOSE","MEDIUM","TIGHT"),
    src            = cms.InputTag("fixme"),
    # conversion safe electron veto config
    beamSpotSrc    = cms.InputTag("offlineBeamSpot"),
    conversionSrc  = cms.InputTag("allConversions"),
    electronSrc    = cms.InputTag("gsfElectrons"),
    # single tower H/E config
    hOverEConeSize = cms.double(0.15),
    hOverETowerSrc = cms.InputTag("towerMaker"),
    hOverEPtMin    = cms.double(0.0)   
)
