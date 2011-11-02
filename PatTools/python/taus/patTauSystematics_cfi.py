import FWCore.ParameterSet.Config as cms

# Embed the systematics in the taus
systematicsTaus = cms.EDProducer(
    "PATTauSystematicsEmbedder",
    src = cms.InputTag("patTaus"),
    tauEnergyScale = cms.PSet(
        applyCorrection = cms.bool(False),
        uncLabelUp = cms.string("AK5PF"),
        uncLabelDown = cms.string("AK5PF"),
        uncTag = cms.string("Uncertainty"),
        flavorUncertainty = cms.double(0),
    ),
)

