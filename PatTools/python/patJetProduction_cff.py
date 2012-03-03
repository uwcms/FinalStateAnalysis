import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.jets.patJetEmbedId_cfi import patJetId

from FinalStateAnalysis.PatTools.jets.patJetUncorrectedEmbedder_cfi import \
        patJetUncorrectedEmbedder

from FinalStateAnalysis.PatTools.jets.patJetEmbedSystematics_cfi import \
        patJetEmbedSystematics
from FinalStateAnalysis.PatTools.jets.patJetEmbedSmear_cfi import \
        patJetEmbedSmear

customizeJetSequence = cms.Sequence()

customizeJetSequence += patJetId

# Remove low pt garbage jets.  This cut is propagated to the taus - only taus
# that have an existing jet are kept.  This cut is important, so we require
# it is explicitly defined elsewhere.
patJetGarbageRemoval = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag("fixme"),
    cut = cms.string("fixme"),
    filter = cms.bool(False),
)
customizeJetSequence += patJetGarbageRemoval

# We have to embed the uncorrected P4 of the jet before we start any monkey
# business with smearing so that we can apply type 1 corrections to MET later
customizeJetSequence += patJetUncorrectedEmbedder
# NB that it is critical that these are applied AFTER the corrections
customizeJetSequence += patJetEmbedSmear
# This has to go second, so the MC smeared value is used as the central value.
customizeJetSequence += patJetEmbedSystematics
