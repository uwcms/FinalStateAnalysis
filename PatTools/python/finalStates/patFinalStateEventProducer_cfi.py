import FWCore.ParameterSet.Config as cms

patFinalStateEventProducer = cms.EDProducer(
    "PATFinalStateEventProducer",
    rhoSrc = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho"),
    pvSrc = cms.InputTag("selectedPrimaryVertex"),
    verticesSrc = cms.InputTag("selectPrimaryVerticesQuality"),
    electronSrc = cms.InputTag("fixme"),
    muonSrc = cms.InputTag("fixme"),
    tauSrc = cms.InputTag("fixme"),
    jetSrc = cms.InputTag("fixme"),
    pfSrc = cms.InputTag("particleFlow"),
    metSrc = cms.InputTag("fixme"),
    metCovSrc = cms.InputTag("pfMEtSignCovMatrix"),
    trgSrc = cms.InputTag("patTriggerEvent"),
    puInfoSrc = cms.InputTag("addPileupInfo"),
    genParticleSrc = cms.InputTag("genParticles"),
    trackSrc = cms.InputTag("generalTracks"),
    gsfTrackSrc = cms.InputTag("electronGsfTracks"),
    extraWeights = cms.PSet(
        #anyOldThing = cms.double(9999), # just an example
        #puAvg = cms.InputTag("lumiWeights", "3bx"),
        #puInTime = cms.InputTag("lumiWeights"),
    )
)
