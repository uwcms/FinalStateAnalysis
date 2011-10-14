import FWCore.ParameterSet.Config as cms

pt = cms.PSet(
    name = cms.string("${name}_Pt"),
    description = cms.string("$nicename p_{T} Cut"),
    cut = cms.string("${getter}pt > ${threshold}"),
    invert = cms.bool(False),
)

# A rectangular pt cut
rect_pt = cms.PSet(
    name = cms.string("${name}_Pt"),
    description = cms.string(
        "$nicename Rect. p_{T} (${threshold1},${threshold2}) Cut"),
    cut = cms.string(
        "(${getter1}pt > ${threshold1} && ${getter2}pt > ${threshold2})"
        "|| (${getter2}pt > ${threshold1} && ${getter1}pt > ${threshold2})"
    ),
    invert = cms.bool(False),
)

eta = cms.PSet(
    name = cms.string("${name}_AbsEta"),
    description = cms.string("$nicename |#eta| Cut"),
    cut = cms.string("abs(${getter}eta) < ${threshold}"),
    invert = cms.bool(False),
)

charge = cms.PSet(
    name = cms.string("${name}_AbsCharge"),
    description = cms.string("$nicename |q| = ${charge}"),
    cut = cms.string("abs(${getter}charge) == ${charge}"),
    invert = cms.bool(False),
)

usrFloat = cms.PSet(
    name = cms.string("${name}"),
    description = cms.string("$nicename |#eta| Cut"),
    cut = cms.string("${getter}userFloat('${item}') > ${threshold}"),
    invert = cms.bool(False),
)

dz = cms.PSet(
    name = cms.string("${name}_DZ"),
    description = cms.string("$nicename #DeltaZ_{PV} < ${threshold}"),
    cut = cms.string(
        "abs(${getter}vertex().z() - evt.pv.position.z) < ${threshold}"),
    plottable = cms.string(
        "abs(${getter}vertex().z() - evt.pv.position.z)"),
    invert = cms.bool(False),
)
