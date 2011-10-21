import FWCore.ParameterSet.Config as cms

patFinalStateEventProducer = cms.EDProducer(
    "PATFinalStateEventProducer",
    rhoSrc = cms.InputTag("kt6PFJets", "rho"),
    pvSrc = cms.InputTag("selectedPrimaryVertex"),
    verticesSrc = cms.InputTag("selectPrimaryVerticesQuality"),
    metSrc = cms.InputTag("fixme"),
    trgSrc = cms.InputTag("patTriggerEvent"),
    puInfoSrc = cms.InputTag("addPileupInfo"),
    genParticleSrc = cms.InputTag("genParticles"),
    extraWeights = cms.PSet(
        #anyOldThing = cms.double(9999), # just an example
        #puAvg = cms.InputTag("lumiWeights", "3bx"),
        #puInTime = cms.InputTag("lumiWeights"),
    )
)

# Add the different possible PU weights
for weight in [ 'lumiWeightsS42011A', 'lumiWeightsS42011B178078',
               'lumiWeightsS42011AB178078' ]:
    setattr(patFinalStateEventProducer.extraWeights,
            weight.replace('lumiWeights', '3bx_'),
            cms.InputTag(weight, "3bx"))
    setattr(patFinalStateEventProducer.extraWeights,
            weight.replace('lumiWeights', 'intime_'),
            cms.InputTag(weight))
