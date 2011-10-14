import FWCore.ParameterSet.Config as cms
from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup

poolDBESSourceMuScleFitCentralValue = cms.ESSource("PoolDBESSource",
    CondDBSetup,
    connect = cms.string('frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS'),
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    timetype = cms.untracked.string('runnumber'),
    appendToDataLabel = cms.string("centralValue"),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('MuScleFitDBobjectRcd'),
            tag = cms.string('MuScleFit_Scale_Z_20_invNb_innerTrack')
        )
    )
)

poolDBESSourceMuScleFitShiftUp = poolDBESSourceMuScleFitCentralValue.clone(
    connect = cms.string('sqlite_fip:FinalStateAnalysis/PatTools/data/Z_20_invNb_innerTrack_plusError.db'),
    appendToDataLabel = cms.string("shiftUp"),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('MuScleFitDBobjectRcd'),
            tag = cms.string('Z_20_invNb_innerTrack')
        )
    )
)

poolDBESSourceMuScleFitShiftDown = poolDBESSourceMuScleFitCentralValue.clone(
    connect = cms.string('sqlite_fip:FinalStateAnalysis/PatTools/data/Z_20_invNb_innerTrack_minusError.db'),
    appendToDataLabel = cms.string("shiftDown"),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('MuScleFitDBobjectRcd'),
            tag = cms.string('Z_20_invNb_innerTrack')
        )
    )
)

# Embed systematics
patMuonsEmbedSystematics = cms.EDProducer(
    "PATMuonSystematicsEmbedder",
    src = cms.InputTag("patMuonsEmbedIp"),
    corrTag = poolDBESSourceMuScleFitCentralValue.appendToDataLabel,
    corrTagUp = poolDBESSourceMuScleFitShiftUp.appendToDataLabel,
    corrTagDown = poolDBESSourceMuScleFitShiftDown.appendToDataLabel,
)
