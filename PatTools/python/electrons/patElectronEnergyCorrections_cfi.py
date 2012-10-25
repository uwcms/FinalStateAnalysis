import FWCore.ParameterSet.Config as cms

regression_versions = cms.VPSet(
    cms.PSet(type    = cms.string("NoTrackVars"), #kNoTrackVars
             version = cms.int32(1),
             index   = cms.int32(0),
             weightsFile = cms.string("EGamma/EGammaAnalysisTools/data/eleEnergyRegWeights_V1.root")
             ),
    cms.PSet(type    = cms.string("WithTrackVars"), #kWithTrackVars
             version = cms.int32(2),
             index   = cms.int32(1),
             weightsFile = cms.string("EGamma/EGammaAnalysisTools/data/eleEnergyRegWeights_V2.root")
             ),
    cms.PSet(type    = cms.string("NoRegression"),
             version = cms.int32(-1),
             index   = cms.int32(-1),
             weightsFile = cms.string("")
             ),
    )

calibration_versions = cms.VPSet(
    cms.PSet(type       = cms.string('NoCorrection'),
             regression = cms.string('NoRegression'),
             applyCorrections      = cms.int32(0)
             ),
    cms.PSet(type       = cms.string("SmearedRegression"),
             regression = cms.string("NoTrackVars"),
             applyCorrections      = cms.int32(1)
             ),
    cms.PSet(type       = cms.string("RegressionOnly"),
             regression = cms.string("NoTrackVars"),
             applyCorrections      = cms.int32(10)
             ),
    cms.PSet(type       = cms.string("SmearedNoRegression"),
             regression = cms.string("NoRegression"),
             applyCorrections      = cms.int32(999)
             )
    )

patElectronEnergyCorrections = cms.EDProducer(
    "PATElectronEnergyCorrectionEmbedder",
    available_regressions  = regression_versions,
    available_calibrations = calibration_versions,
    applyCalibrations = cms.vstring("SmearedRegression",
                                    "RegressionOnly",
                                    "SmearedNoRegression"),
    recHitsEB = cms.InputTag("reducedEcalRecHitsEB"),
    recHitsEE = cms.InputTag("reducedEcalRecHitsEE"),
    dataSet = cms.string("placeholder"),
    src = cms.InputTag("fixme"),
    isAOD = cms.bool(True),
    isMC = cms.bool(True),
    vtxSrc = cms.InputTag("selectPrimaryVerticesQuality"),
    rhoSrc = cms.InputTag("kt6PFJets:rho:RECO"),
    userP4Prefix = cms.string("EGCorr_")
)
