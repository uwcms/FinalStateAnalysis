import FWCore.ParameterSet.Config as cms

hlt = cms.PSet(
    name = cms.string("${name}_HLT"),
    description = cms.string("$nicename HLT requirement [${hlt_path}]"),
    cut = cms.string('evt.hltResult("${hlt_path}")'),
    plottable = cms.string('evt.hltResult("${hlt_path}")'),
    invert = cms.bool(False),
)
