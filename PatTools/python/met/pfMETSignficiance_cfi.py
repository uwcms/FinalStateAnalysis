'''

Define sequence to compute the MET significance in the event

'''

import FWCore.ParameterSet.Config as cms

metSignficanceSequence = cms.Sequence()

# Select decent muons
metSigDecentMuons = cms.EDFilter(
    "PATMuonRefSelector",
    src = cms.InputTag("cleanPatMuons"),
    cut = cms.string("userInt('VBTF') & pt > 5 & chargedHadronIso()/pt < 0.3"),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigDecentMuons

metSigDecentElectrons = cms.EDFilter(
    "PATElectronRefSelector",
    src = cms.InputTag("cleanPatElectrons"),
    cut = cms.string("!hasOverlaps('muons') & userFloat('wp95') > 0.5 & pt > 8 & dr03TkSumPt()/pt < 0.3"),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigDecentElectrons

metSigDecentTausUnclean = cms.EDFilter(
    "PATTauRefSelector",
    src = cms.InputTag("cleanPatTaus"),
    cut = cms.string('!hasOverlaps("muons") & pt > 18 & tauID("decayModeFinding") & tauID("byLooseCombinedIsolationDeltaBetaCorr")'),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigDecentTausUnclean

# Make sure we don't have any overlaps with our taus from electrons
metSigDecentTaus = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("metSigDecentTausUnclean"),
    subtractSrc = cms.InputTag("metSigDecentElectrons"),
    minDeltaR = cms.double(0.3),
    filter = cms.bool(False),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigDecentTaus

# Now clean the pat::Jets.  This is sort of a pain
metSigJetsDirty = cms.EDFilter(
    "CandViewRefSelector",
    src = cms.InputTag("patJets"),
    cut = cms.string("pt > 20"),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigJetsDirty

# Remove muons
metSigJetsNoMuons = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("metSigJetsDirty"),
    subtractSrc = cms.InputTag("metSigDecentMuons"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigJetsNoMuons

metSigJetsNoElectrons = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("metSigJetsNoMuons"),
    subtractSrc = cms.InputTag("metSigDecentElectrons"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
)
metSignficanceSequence += metSigJetsNoElectrons

metSigJetsClean = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("metSigJetsNoElectrons"),
    subtractSrc = cms.InputTag("metSigDecentTaus"),
    minDeltaR = cms.double(0.4),
    filter = cms.bool(False),
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
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
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
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
pfMEtSignCovMatrix = cms.EDProducer(
    "PFMETSignificanceProducer",
    METSignificance_params,
    noSeqChain = cms.bool(True), # Don't "chain" these sequence and update [src]
    src = cms.VInputTag(
        'metSigDecentMuons',
        'metSigDecentElectrons',
        'metSigDecentTaus',
        'metSigGetPFJets',
        'pfCandsNotInSelectedJets'
    )
)
metSignficanceSequence += pfMEtSignCovMatrix
