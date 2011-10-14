import FWCore.ParameterSet.Config as cms

id = cms.PSet(
    name = cms.string("${name}_TauID_${tauID}"),
    description = cms.string("$nicename Tau ID [${tauID}]"),
    cut = cms.string("${getter}tauID('${tauID}') > 0.5"),
    plottable = cms.string("${getter}tauID('${tauID}')"),
    invert = cms.bool(False),
)

nobtag = cms.PSet(
    name = cms.string("${name}_NoBTag_${bID}"),
    description = cms.string("$nicename No Assoc. b-Tag [${bID}]"),
    cut = cms.string("${getter}userCand('patJet').bDiscriminator('${bID}') < ${threshold}"),
    plottable = cms.string("${getter}userCand('patJet').bDiscriminator('${bID}')"),
    invert = cms.bool(False),
)

jetpt = cms.PSet(
    name = cms.string("${name}_TauJetPt"),
    description = cms.string("${nicename} seed jet p_{T}"),
    cut = cms.string(
        "daughterUserCand(${index}, 'patJet').pt > ${threshold}"),
    plottable = cms.untracked.string("daughterUserCand(${index}, 'patJet').pt"),
    invert = cms.bool(False),
)

isTrueTau = cms.PSet(
    name = cms.string("${name}_GenTauMatch"),
    description = cms.string("${nicename} matched to gen tau"),
    cut = cms.string(
        "? ${getter}genParticleRef().isNonnull ? abs(${getter}genParticleRef().pdgId()) : -1 == 15"),
    plottable = cms.untracked.string(
        "? ${getter}genParticleRef().isNonnull ? abs(${getter}genParticleRef().pdgId()) : -1"),
    invert = cms.bool(False),
)
