import FWCore.ParameterSet.Config as cms

selectPrimaryVerticesQuality = cms.EDFilter(
    "VertexSelector",
    src=cms.InputTag('offlinePrimaryVertices'),
    cut=cms.string("isValid & ndof >= 4 && abs(z) < 24 && position.Rho < 2.0"),
    filter=cms.bool(False),
)

selectPrimaryVerticesQualityWithBS = cms.EDFilter(
    "VertexSelector",
    src=cms.InputTag('offlinePrimaryVerticesWithBS'),
    cut=cms.string("isValid & ndof >= 4 && abs(z) < 24 && position.Rho < 2.0"),
    filter=cms.bool(False),
)

selectedPrimaryVertex = cms.EDFilter(
    "PATSingleVertexSelector",
    mode=cms.string('firstVertex'),
    vertices=cms.InputTag('selectPrimaryVerticesQuality'),
    filter=cms.bool(False)
)

selectedPrimaryVertexWithBS = cms.EDFilter(
    "PATSingleVertexSelector",
    mode=cms.string('firstVertex'),
    vertices=cms.InputTag('selectPrimaryVerticesQualityWithBS'),
    filter=cms.bool(False)
)

selectedPrimaryVertexUnclean = cms.EDFilter(
    "PATSingleVertexSelector",
    mode=cms.string('firstVertex'),
    vertices=cms.InputTag('offlinePrimaryVertices'),
    filter=cms.bool(False)
)

selectedPrimaryVertexUncleanWithBS = cms.EDFilter(
    "PATSingleVertexSelector",
    mode=cms.string('firstVertex'),
    vertices=cms.InputTag('offlinePrimaryVerticesWithBS'),
    filter=cms.bool(False)
)

selectPrimaryVertices = cms.Sequence(
    selectPrimaryVerticesQuality + selectPrimaryVerticesQualityWithBS +
    selectedPrimaryVertex + selectedPrimaryVertexWithBS +
    selectedPrimaryVertexUnclean + selectedPrimaryVertexUncleanWithBS)


atLeastOneGoodVertex = cms.EDFilter(
    "VertexSelector",
    src=cms.InputTag("selectPrimaryVerticesQuality"),
    cut=cms.string(""),  # just require one
    filter=cms.bool(True)
)

# A sequence which ensure there is at least one good vertex
atLeastOneGoodVertexSequence = cms.Sequence(
    selectPrimaryVertices *
    atLeastOneGoodVertex *
    selectedPrimaryVertex
)
