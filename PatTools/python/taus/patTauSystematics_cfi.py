import FWCore.ParameterSet.Config as cms

# Embed the systematics in the taus
systematicsTaus = cms.EDProducer(
    "PATTauSystematicsEmbedder",
    src = cms.InputTag("patTaus"),
    unclusteredEnergyScale = cms.double(0.1),
    tauEnergyScale = cms.PSet(
        applyCorrection = cms.bool(False),
        uncLabelUp = cms.string("AK5PF"),
        uncLabelDown = cms.string("AK5PF"),
        uncTag = cms.string("Uncertainty"),
        flavorUncertainty = cms.double(0),
    ),
    jetEnergyScale = cms.PSet(
        applyCorrection = cms.bool(True),
        corrLabel = cms.string('ak5PFL1L2L3Residual'),
        uncLabelUp = cms.string("AK5PF"),
        uncLabelDown = cms.string("AK5PF"),
        uncTag = cms.string("Uncertainty"),
        flavorUncertainty = cms.double(0),
    ),
)

print "WARNING: in MC fix jet correciton type for taus"
