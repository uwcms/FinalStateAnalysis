import FWCore.ParameterSet.Config as cms

hlt = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_HLT"),
    description = cms.untracked.string("$nicename HLT requirement [${hlt_path}]"),
    plotquantity = cms.untracked.string('evt.hltResult("${hlt_path}")'),
    lazyParsing = cms.untracked.bool(False),
)

hltGroup = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(5.5),
    nbins = cms.untracked.int32(6),
    name = cms.untracked.string("${name}_HLTGroup"),
    description = cms.untracked.string("$nicename HLT Group [${hlt_path}]"),
    plotquantity = cms.untracked.string('evt.hltGroup("${hlt_path}")'),
    lazyParsing = cms.untracked.bool(False),
)

hltPrescale = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(199.5),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_HLTPrescale"),
    description = cms.untracked.string("$nicename HLT Prescale [${hlt_path}]"),
    plotquantity = cms.untracked.string('evt.hltPrescale("${hlt_path}")'),
    lazyParsing = cms.untracked.bool(False),
)
