import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs

metTypeCategorization = cms.PSet(
    tauCut = cms.string(
        'pt > 10 && (tauID("decayModeFinding") && tauID("byLooseIsolation"))'
    ),
    jetCut = cms.string(
        '!(tauID("decayModeFinding") && tauID("byLooseIsolation")) && userCand("patJet").pt > 10'
    ),
    # The part about passing the tauID is to catch the low pt taus
    unclusteredCut = cms.string(
        'userCand("patJet").pt < 10 | (pt < 10 && tauID("decayModeFinding") && tauID("byLooseIsolation"))'
    ),
)

systematicsMET = cms.EDProducer(
    "PATMETSystematicsEmbedder",
    src = cms.InputTag("patPfMet"),
    metT1Src = cms.InputTag("patPfMetT1"),
    metT0pcT1TxySrc = cms.InputTag("patPfMetT0pcT1Txy"), 
    metT0rtT1TxySrc = cms.InputTag("patPfMetT0rtT1Txy"), 
    tauSrc = cms.InputTag("fixme"),
    muonSrc = cms.InputTag("fixme"),
    electronSrc = cms.InputTag("fixme"),
    tauCut = metTypeCategorization.tauCut,
    jetCut = metTypeCategorization.jetCut,
    unclusteredCut = metTypeCategorization.unclusteredCut,
    applyType1ForTaus = cms.bool(False),
    applyType1ForMuons = cms.bool(False),
    applyType1ForElectrons = cms.bool(False),
    applyType1ForJets = cms.bool(True),
    applyType2ForJets = cms.bool(False),
)
