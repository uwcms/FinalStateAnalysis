import FWCore.ParameterSet.Config as cms

pt = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}Pt"),
    description = cms.untracked.string("${nicename} p_{T}"),
    plotquantity = cms.untracked.string("${getter}pt"),
)

eta = cms.PSet(
    min = cms.untracked.double(-5),
    max = cms.untracked.double(5),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}Eta"),
    description = cms.untracked.string("${nicename} #eta"),
    plotquantity = cms.untracked.string("${getter}eta"),
)

abseta = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(5),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}AbsEta"),
    description = cms.untracked.string("${nicename} #eta"),
    plotquantity = cms.untracked.string("abs(${getter}eta)"),
)

phi = cms.PSet(
    min = cms.untracked.double(-3.14),
    max = cms.untracked.double(3.14),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}Phi"),
    description = cms.untracked.string("${nicename} #phi"),
    plotquantity = cms.untracked.string("${getter}phi"),
)

charge = cms.PSet(
    min = cms.untracked.double(-3.5),
    max = cms.untracked.double(3.5),
    nbins = cms.untracked.int32(7),
    name = cms.untracked.string("${name}Charge"),
    description = cms.untracked.string("${nicename} charge"),
    plotquantity = cms.untracked.string("${getter}charge"),
)

genPdgId = cms.PSet(
    min = cms.untracked.double(-1.5),
    max = cms.untracked.double(30.5),
    nbins = cms.untracked.int32(32),
    name = cms.untracked.string("${name}GenPdgId"),
    description = cms.untracked.string("${nicename} gen. PDG ID"),
    plotquantity = cms.untracked.string(
        "? ${getter}genParticleRef().isNonnull ? abs(${getter}genParticleRef().pdgId()) : -1"),
    lazyParsing = cms.untracked.bool(True),
)

dz = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(30),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}DZ"),
    description = cms.untracked.string("${nicename} #Delta_{PV}"),
    plotquantity = cms.untracked.string(
        "abs(${getter}vertex().z() - evt.pv.position.z)",
    ),
    lazyParsing = cms.untracked.bool(True),
)

# Collect the common ones
all = [
    pt, phi, eta, abseta, charge, genPdgId, dz
]
