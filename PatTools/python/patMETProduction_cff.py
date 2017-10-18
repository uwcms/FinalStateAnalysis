import FWCore.ParameterSet.Config as cms

# Import both so provenance tracks it
from FinalStateAnalysis.PatTools.met.metSystematics_cfi import metTypeCategorization, \
        systematicsMET

# Have to import all this stuff so it appears in namespace
from FinalStateAnalysis.PatTools.met.pfMETSignficiance_cfi import \
        metSignficanceSequence, \
        metSigDecentMuons, \
        metSigDecentElectrons, \
        metSigDecentTausUnclean, \
        metSigDecentTaus, \
        metSigJetsDirty, \
        metSigJetsNoMuons, \
        metSigJetsNoElectrons, \
        metSigJetsClean, \
        metSigGetPFJets, \
        pfCandsNotInSelectedJets, \
        pfMEtSignCovMatrix

customizeMETSequence = cms.Sequence(systematicsMET + metSignficanceSequence)
