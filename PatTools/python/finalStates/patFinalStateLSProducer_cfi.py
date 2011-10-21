import FWCore.ParameterSet.Config as cms

'''
Build the PATFinalStateLS wrapper data class which holds the lumi summary.
'''

finalStateLS = cms.EDProducer(
    "PATFinalStateLSProducer",
    src = cms.InputTag("lumiSummary"),
)
