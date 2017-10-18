'''

CandComparator makes TH2Fs which generates the correlation of kinematics
quantities between two collections.  The input collections must match 1-1.

Intended for validating/debugging.

Author: Evan K. Friis, UW Madison

'''

import FWCore.ParameterSet.Config as cms

candComparator = cms.EDAnalyzer(
    "CandComparator",
    src1 = cms.InputTag("muons1"),
    src2 = cms.InputTag("muons2"),
    comparisons = cms.PSet(
        pt = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(0),
            max = cms.double(100),
            func = cms.string("pt"),
        )
    )
)
