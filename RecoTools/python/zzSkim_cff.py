'''

Skim definitions for HZZ->4L analysis

'''
import FWCore.ParameterSet.Config as cms

goodVertex = cms.EDFilter(
    "VertexSelector",
    src=cms.InputTag("offlinePrimaryVertices"),
    cut=cms.string(
        '!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2'),
    filter=cms.bool(True),
)

muons4skim = cms.EDFilter(
    "MuonSelector",
    src=cms.InputTag("muons"),
    cut=cms.string(
        "pt>3 && (isTrackerMuon||isGlobalMuon) && abs(eta) < 2.4"),
)
electrons4skim = cms.EDFilter(
    "GsfElectronSelector",
    src=cms.InputTag("gsfElectrons"),
    cut=cms.string("pt>5 && abs(eta) < 2.5"),
)
leptons4skim = cms.EDProducer(
    "CandViewMerger",
    src=cms.VInputTag(cms.InputTag("muons4skim"),
                      cms.InputTag("electrons4skim"),)
)
dileptons4skim = cms.EDProducer(
    "CandViewShallowCloneCombiner",
    decay=cms.string('leptons4skim leptons4skim'),
    cut=cms.string('deltaR(daughter(0).eta,daughter(0).phi,'
                   'daughter(1).eta,daughter(1).phi)> 0.01'),
    checkCharge=cms.bool(False)
)

skim2010 = cms.EDFilter(
    "CandViewSelector",
    src=cms.InputTag("dileptons4skim"),
    cut=cms.string('min(daughter(0).pt,daughter(1).pt) > 10 && '
                   'max(daughter(0).pt,daughter(1).pt) > 20'),
    filter=cms.bool(True),
)

skim40NoOF = cms.EDFilter(
    "CandViewSelector",
    src=cms.InputTag("dileptons4skim"),
    cut=cms.string('mass > 40 && abs(daughter(0).pdgId) == '
                   'abs(daughter(1).pdgId)'),  # and SF only
    filter=cms.bool(True),
)

skimNoOS = cms.Sequence(goodVertex + muons4skim + electrons4skim +
                        leptons4skim + dileptons4skim + skim2010 + skim40NoOF)

zzSkim = cms.Path(skimNoOS)
