import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.selectors.selectors as selectors

id = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_EID_${eID}"),
    description = cms.untracked.string("${nicename} Electron ID"),
    plotquantity = cms.untracked.string(selectors.electrons.id.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

reliso = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(2),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_ERelIso"),
    description = cms.untracked.string("${nicename} Electron Rel. Iso"),
    plotquantity = cms.untracked.string(
        selectors.electrons.reliso.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

all = [reliso]
