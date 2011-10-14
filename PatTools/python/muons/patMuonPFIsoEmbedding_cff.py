import FWCore.ParameterSet.Config as cms

patMuonsLoosePFIsoEmbedded03 = cms.EDProducer("PATMuonPFIsolationEmbedder",
    src = cms.InputTag('patMuons'),
    userFloatName = cms.string('pfLooseIsoPt03'),
    pfCandidateSource = cms.InputTag('pfNoPileUp'),
    chargedHadronIso = cms.PSet(
        ptMin = cms.double(0.5),
        dRvetoCone = cms.double(-1.),
        dRisoCone = cms.double(0.3)
    ),
    neutralHadronIso = cms.PSet(
        ptMin = cms.double(1.0),
        dRvetoCone = cms.double(0.08),
        dRisoCone = cms.double(0.3)
    ),
    photonIso = cms.PSet(
        ptMin = cms.double(1.0),
        dPhiVeto = cms.double(-1.),
        dEtaVeto = cms.double(-1.),
        dRvetoCone = cms.double(0.05),
        dRisoCone = cms.double(0.3)
    )
)

patMuonsLoosePFIsoEmbedded04 = patMuonsLoosePFIsoEmbedded03.clone(
    src = cms.InputTag('patMuonsLoosePFIsoEmbedded03'),
    userFloatName = cms.string('pfLooseIsoPt04'),
    pfCandidateSource = cms.InputTag('pfNoPileUp'),
    chargedHadronIso = patMuonsLoosePFIsoEmbedded03.chargedHadronIso.clone(
        dRisoCone = cms.double(0.4)
    ),
    neutralHadronIso = patMuonsLoosePFIsoEmbedded03.neutralHadronIso.clone(
        dRisoCone = cms.double(0.4)
    ),
    photonIso = patMuonsLoosePFIsoEmbedded03.photonIso.clone(
        dRisoCone = cms.double(0.4)
    )
)

patMuonsLoosePFIsoEmbedded06 = patMuonsLoosePFIsoEmbedded03.clone(
    src = cms.InputTag('patMuonsLoosePFIsoEmbedded04'),
    userFloatName = cms.string('pfLooseIsoPt06'),
    pfCandidateSource = cms.InputTag('pfNoPileUp'),
    chargedHadronIso = patMuonsLoosePFIsoEmbedded03.chargedHadronIso.clone(
        dRisoCone = cms.double(0.6)
    ),
    neutralHadronIso = patMuonsLoosePFIsoEmbedded03.neutralHadronIso.clone(
        dRisoCone = cms.double(0.6)
    ),
    photonIso = patMuonsLoosePFIsoEmbedded03.photonIso.clone(
        dRisoCone = cms.double(0.6)
    )
)

patMuonsLoosePFIsoEmbedded = cms.Sequence(
    patMuonsLoosePFIsoEmbedded03
    *patMuonsLoosePFIsoEmbedded04
    *patMuonsLoosePFIsoEmbedded06
)
