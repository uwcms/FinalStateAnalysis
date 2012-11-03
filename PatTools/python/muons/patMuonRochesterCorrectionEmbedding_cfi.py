import FWCore.ParameterSet.Config as cms

correction_versions = cms.VPSet(
    cms.PSet(name             = cms.string('RochCor2011A'),
             dataSet          = cms.string('2011A'),
             systematic_error = cms.double(0.0012)
             ),
    cms.PSet(name             = cms.string("RochCor2011B"),
             dataSet          = cms.string("2011B"),
             systematic_error = cms.double(0.0012)
             ),
    cms.PSet(name             = cms.string("RochCor2012"),
             dataSet          = cms.string("2012"),
             systematic_error = cms.double(0.0012) ##this is a fake value, not yet calculated
             )
    )

# available correction targets:
# 2012 Data : 2012
# 2012 MC   : 2012
#
# 2011 Data : 2011A, 2011B
# 2011 MC   : 2011A, 2011B


patMuonRochesterCorrectionEmbedder = cms.EDProducer(
    "PATMuonRochesterCorrectionEmbedder",
    available_corrections = correction_versions,
    applyCorrections = cms.vstring("RochCor2011A",
                                   "RochCor2011B",
                                   "RochCor2012"),
    src = cms.InputTag("fixme"),
    isMC = cms.bool(True),
    userP4Prefix = cms.string("p4_")
)
