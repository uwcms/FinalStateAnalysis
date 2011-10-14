import FWCore.ParameterSet.Config as cms

# Import both so provenance tracks it
from FinalStateAnalysis.PatTools.met.metSystematics_cfi import metTypeCategorization, \
        systematicsMET

customizeMETSequence = cms.Sequence(systematicsMET)
