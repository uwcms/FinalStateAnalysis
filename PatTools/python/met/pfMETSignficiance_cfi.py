'''

Define sequence to compute the MET significance in the event

'''

import FWCore.ParameterSet.Config as cms

metSignficanceSequence = cms.Sequence()

# Select decent muons
metSigDecentMuons = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("cleanPatMuons"),
    cut = cms.string("userInt('VBTF') & pt > 5 & chargedHadronIso()/pt < 0.3")
)
metSignficanceSequence += metSigDecentMuons

metSigDecentElectrons = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("cleanPatElectrons"),
    cut = cms.string("!hasOverlaps('muons') & userFloat('wp95') > 0.5 & pt > 8 & dr03TkSumPt()/pt < 0.3")
)
metSignficanceSequence += metSigDecentElectrons

metSigDecentTausUnclean = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("cleanPatTaus"),
    cut = cms.string('!hasOverlaps("muons") & pt > 18 & tauID("decayModeFinding") & tauID("byLooseCombinedIsolationDeltaBetaCorr")')
)
metSignficanceSequence += metSigDecentTausUnclean

# Make sure we don't have any overlaps with our taus from electrons
metSigDecentTaus = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("metSigDecentTausUnclean"),
    subtractSrc = cms.InputTag("metSigDecentElectrons"),
    minDeltaR = cms.double(0.3),
    filter = cms.bool(False),
)
metSignficanceSequence += metSigDecentTaus

# Now clean the pat::Jets.  This is sort of a pain
metSigJetsDirty = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("patJets"),
    cut = cms.string("pt > 20"),
)
metSignficanceSequence += metSigJetsDirty

# Remove muons
metSigJetsNoMuons = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("metSigJetsDirty"),
    subtractSrc = cms.InputTag("metSigDecentMuons"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False)
)
metSignficanceSequence += metSigJetsNoMuons

metSigJetsNoElectrons = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("metSigJetsNoMuons"),
    subtractSrc = cms.InputTag("metSigDecentElectrons"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False)
)
metSignficanceSequence += metSigJetsNoElectrons

metSigJetsClean = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("metSigJetsNoElectrons"),
    subtractSrc = cms.InputTag("metSigDecentTaus"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False)
)
metSignficanceSequence += metSigJetsClean

# OK, now convert these back to PFJets, so we can figure out which PFCandidates
# aren't part of any jets
metSigGetPFJets = cms.EDFilter(
    "PFJetViewOverlapSubtraction",
    src = cms.InputTag("ak5PFJets"),
    subtractSrc = cms.InputTag("metSigJetsClean"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False),
    invert = cms.bool(True),  # select AK5 PF jets that DO overlap
)
metSignficanceSequence += metSigGetPFJets

# Get the PFCandidates that aren't in these jets
from CommonTools.ParticleFlow.TopProjectors.pfNoJet_cfi import pfNoJet
pfCandsNotInSelectedJets = pfNoJet.clone(
    topCollection = cms.InputTag('metSigGetPFJets'),
    bottomCollection = cms.InputTag('particleFlow')
)
metSignficanceSequence += pfCandsNotInSelectedJets

# produce PFMET significance cov. matrix
from RecoMET.METProducers.METSigParams_cfi import METSignificance_params
pfMEtSignCovMatrix = cms.EDProducer("PFMEtSignCovMatrixProducer",
    METSignificance_params,
    src = cms.VInputTag(
        'metSigDecentMuons',
        'metSigDecentElectrons',
        'metSigDecentTaus',
        'metSigGetPFJets',
        'pfCandsNotInSelectedJets'
    )
)
metSignficanceSequence += pfMEtSignCovMatrix
