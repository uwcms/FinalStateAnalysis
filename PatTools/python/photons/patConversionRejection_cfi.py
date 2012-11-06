import FWCore.ParameterSet.Config as cms

electronsWWID = cms.EDProducer(
    'PATElectronWWEmbedder',
    src             = cms.InputTag("fixme"),
    srcVertices     = cms.InputTag("selectedPrimaryVertex"),
    sigmaEtaEta     = cms.vdouble(0.01,0.03,0.01,0.03),
    deltaEta        = cms.vdouble(0.004,0.005,0.004,0.007),
    deltaPhi        = cms.vdouble(0.03,0.02,0.06,0.03),
    hoE             = cms.vdouble(0.025,0.025,0.04,0.025),
    convDist        = cms.vdouble(0.02,0.02,0.02,0.02),
    convDCot        = cms.vdouble(0.02,0.02,0.02,0.02),
    id              = cms.string("WWID"),
    fbrem           = cms.double(0.15),
    EOP             = cms.double(0.95),
    d0              = cms.double(0.045),
    dz              = cms.double(0.2),
)
