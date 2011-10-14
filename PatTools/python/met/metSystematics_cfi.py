import FWCore.ParameterSet.Config as cms

metTypeCategorization = cms.PSet(
    tauCut = cms.string(
        'pt > 10 && (tauID("decayModeFinding") && tauID("byLooseIsolation"))'
    ),
    jetCut = cms.string(
        '!(tauID("decayModeFinding") && tauID("byLooseIsolation")) && pt > 10'
    ),
    unclusteredCut = cms.string(
        'pt <= 10'
    ),
)

systematicsMET = cms.EDProducer(
    "PATMETSystematicsEmbedder",
    src = cms.InputTag("patMETsPF"),
    tauSrc = cms.InputTag("fixme"),
    muonSrc = cms.InputTag("fixme"),
    electronSrc = cms.InputTag("fixme"),
    tauCut = metTypeCategorization.tauCut,
    jetCut = metTypeCategorization.jetCut,
    unclusteredCut = metTypeCategorization.unclusteredCut,
)
