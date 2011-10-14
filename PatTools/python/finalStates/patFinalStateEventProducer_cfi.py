import FWCore.ParameterSet.Config as cms

patFinalStateEventProducer = cms.EDProducer(
    "PATFinalStateEventProducer",
    rhoSrc = cms.InputTag("kt6PFJets", "rho"),
    pvSrc = cms.InputTag("selectedPrimaryVertex"),
    verticesSrc = cms.InputTag("selectPrimaryVerticesQuality"),
    metSrc = cms.InputTag("fixme"),
    trgSrc = cms.InputTag("patTriggerEvent"),
    puInfoSrc = cms.InputTag("addPileupInfo"),
    extraWeights = cms.PSet(
        #anyOldThing = cms.double(9999), # just an example
        puAvg = cms.InputTag("lumiWeights", "3bx"),
        puInTime = cms.InputTag("lumiWeights"),
        puOOT = cms.InputTag("lumiWeights", "oot"),
    )
)
