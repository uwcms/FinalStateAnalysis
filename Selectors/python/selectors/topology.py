import FWCore.ParameterSet.Config as cms

descending_pt = cms.PSet(
    name = cms.string("${name}_Unique"),
    description = cms.string("$nicename p_{T} Ordering"),
    cut = cms.string("${getter1}pt > ${getter2}pt"),
    invert = cms.bool(False),
)

# This cut is slightly nonsense, but it is unbiased way of ensuring that
# we don't double count pairs (i.e. AB and BA)
descending_phi = cms.PSet(
    name = cms.string("${name}_Unique"),
    description = cms.string("$nicename #phi Ordering"),
    cut = cms.string("${getter1}phi > ${getter2}phi"),
    invert = cms.bool(False),
)

z_veto = cms.PSet(
    name = cms.string("${name}_ZVeto"),
    description = cms.string("$nicename OS, like-flavor, 85 < M < 95 veto"),
    cut = cms.string("likeSigned(${index1}, ${index2}) || "
                     "!likeFlavor(${index1}, ${index2}) || "
                     "subcand(${index1}, ${index2}).mass() < 85 || "
                     "subcand(${index1}, ${index2}).mass() > 95"),
    invert = cms.bool(False),
)

mtMetCut = cms.PSet(
    name = cms.string("${name}_MET_M_{T}"),
    description = cms.string("$nicename-MET M_{T}"),
    cut = cms.string('mtMET(${index}) < ${threshold}'),
    plottable = cms.string('mtMET(${index})'),
    invert = cms.bool(False),
)
