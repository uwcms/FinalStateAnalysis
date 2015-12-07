# Filters to select events with (or without) taus coming from the hard process.
# Author: Kenneth Long, U. Wisconsin

import FWCore.ParameterSet.Config as cms

hardProcessTausP = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("prunedGenParticles"),
        cut = cms.string("pdgId == 15 && isHardProcess()")
)
hardProcessTausM = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("prunedGenParticles"),
        cut = cms.string("pdgId == -15 && isHardProcess()")
)
hardProcessTaus = cms.EDProducer("CandViewMerger",
    src = cms.VInputTag("hardProcessTausP", "hardProcessTausM")
)
tauFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("hardProcessTaus"),
    minNumber = cms.uint32(1)
)

filterForGenTaus = cms.Sequence(
    (hardProcessTausM + hardProcessTausP)*
    hardProcessTaus*
    tauFilter
)

filterAgainstGenTaus = cms.Sequence(
    (hardProcessTausM + hardProcessTausP)*
    hardProcessTaus*
    ~tauFilter
)

