import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

pt_selector = cms.PSet(
    name = cms.string("$name_Pt"),
    description = cms.string("$nicename p_{T} Cut"),
    cut = cms.string("${getter}.pt > ${threshold}"),
    invert = cms.bool(False),
)

eta_selector = cms.PSet(
    name = cms.string("$name_AbsEta"),
    description = cms.string("$nicename |#eta| Cut"),
    cut = cms.string("abs(${getter}.eta) < ${threshold}"),
    invert = cms.bool(False),
)

eta_selector = cms.PSet(
    name = cms.string("$name_AbsEta"),
    description = cms.string("$nicename |#eta| Cut"),
    cut = cms.string("abs(${getter}.eta) < ${threshold}"),
    invert = cms.bool(False),
)
