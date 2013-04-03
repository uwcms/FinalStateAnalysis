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

# available calibration targets:
# 2012 Data : 2012Jul13ReReco,
#              ICHEP2012
# 2012 MC   : Summer12, Summer12_DR53X_HCP2012
#
# 2011 Data : Jan16ReReco,Prompt, ReReco
# 2011 MC   : Summer11, Fall11,


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
    smearRatio = cms.double(0.607), #fraction of data added on top of HCP -- (19.6-12.2)/12.2 = 0.607 for full 2012
    isSync = cms.bool(False), #if True-->use deterministic smearing
    vtxSrc = cms.InputTag("selectPrimaryVerticesQuality"),
    rhoSrc = cms.InputTag("kt6PFJets","rho"),
    userP4Prefix = cms.string("EGCorr_")
)
