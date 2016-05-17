import FWCore.ParameterSet.Config as cms

patFinalStateEventProducer = cms.EDProducer(
    "PATFinalStateEventProducer",
    #rhoSrc = cms.InputTag("fixedGridRhoFastjetAll"), #cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho"),
    rhoSrc = cms.InputTag('kt6PFJets', "rho"), #cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho"),
    pvSrc = cms.InputTag("selectedPrimaryVertex"),
    pvSrcBackup = cms.InputTag("selectedPrimaryVertexUnclean"),
    verticesSrc = cms.InputTag("selectPrimaryVerticesQuality"),
    electronSrc = cms.InputTag("fixme"),
    muonSrc = cms.InputTag("fixme"),
    tauSrc = cms.InputTag("fixme"),
    jetSrc = cms.InputTag("fixme"),
    pfSrc = cms.InputTag("particleFlow"),
    metSrc = cms.InputTag("fixme"),
    metCovSrc = cms.InputTag("pfMEtSignCovMatrix"),
    MVAMETSrc = cms.InputTag("MVAMET","MVAMET","Ntuples"),
    trgSrc = cms.InputTag("patTriggerEvent"),
    puInfoSrc = cms.InputTag("slimmedAddPileupInfo"),
    genParticleSrc = cms.InputTag("genParticles"),
    trackSrc = cms.InputTag("generalTracks"),
    gsfTrackSrc = cms.InputTag("electronGsfTracks"),
    mets = cms.PSet(
        pfmet = cms.InputTag("slimmedMETs"),
        mvamet = cms.InputTag("fixme"),
        puppimet = cms.InputTag("slimmedMETsPuppi"),
    ),
    extraWeights = cms.PSet(
        #anyOldThing = cms.double(9999), # just an example
        #puAvg = cms.InputTag("lumiWeights", "3bx"),
        #puInTime = cms.InputTag("lumiWeights"),
    ),
    # now some miniAOD specific stuff
    trgPrescaleSrc = cms.InputTag("patTrigger"),
    trgResultsSrc = cms.InputTag("TriggerResults","","HLT"),
    l1extraIsoTauSrc = cms.InputTag("l1extraParticles","IsoTau","RECO"),
    packedGenSrc = cms.InputTag("packedGenParticles"),
    packedPFSrc = cms.InputTag("packedPFCandidates"),
    jetAK8Src = cms.InputTag("slimmedJetsAK8"),
    photonCoreSrc = cms.InputTag("reducedEgamma","reducedGedPhotonCores"),
    gsfCoreSrc = cms.InputTag("reducedEgamma","reducedGedGsfElectronCores")
)
