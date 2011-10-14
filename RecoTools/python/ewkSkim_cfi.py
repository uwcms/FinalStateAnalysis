import FWCore.ParameterSet.Config as cms

'''

Basic SKIM for all EWK-type jobs

Requires at least one light lepton, and two total leptons.

A light lepton can be a:
    > Muon with |eta| < 2.1 and pt > 5
    > Electron with |eta| < 2.5 and pt > 8

A lepton can be:
    > Muon or Electron as above
    > Tau passing leading track finding with |eta| < 2.5 and pt > 10

'''

# require at least one "good quality" (global || tracker || stand-alone) muon
goodMuons = cms.EDFilter(
    "MuonSelector",
    src = cms.InputTag('muons'),
    cut = cms.string(
        "(isGlobalMuon | isStandAloneMuon | isTrackerMuon) & abs(eta) < 2.1 & pt > 25.0"),
    filter = cms.bool(False)
)

goodElectrons = cms.EDFilter(
    "GsfElectronSelector",
    src = cms.InputTag('gsfElectrons'),
    cut = cms.string(
        "abs(eta) < 2.5 & pt > 8.0"),
    filter = cms.bool(False)
)

goodTaus = cms.EDFilter(
    'PFTauSelector',
    src = cms.InputTag('hpsPFTauProducer'),
    discriminators = cms.VPSet(
        cms.PSet(
            discriminator = cms.InputTag(
                "hpsPFTauDiscriminationByDecayModeFinding"),
            selectionCut=cms.double(0.5)
        )
    ),
    cut = cms.string('et > 10. && abs(eta) < 2.5'),
    filter = cms.bool(False),
)

goodLeptons = cms.Sequence(goodMuons + goodElectrons + goodTaus)

atLeastOneDecentLightLepton = cms.EDFilter(
    "MultiCandViewCountFilter",
    srcs = cms.VInputTag(
        "goodMuons",
        "goodElectrons",
    ),
    minCount = cms.uint32(1)
)

atLeastTwoDecentLeptons = cms.EDFilter(
    "MultiCandViewCountFilter",
    srcs = cms.VInputTag(
        "goodMuons",
        "goodElectrons",
        "goodTaus",
    ),
    minCount = cms.uint32(1)
)

ewkSkimSequence = cms.Sequence(
    goodLeptons + atLeastOneDecentLightLepton + atLeastTwoDecentLeptons)

