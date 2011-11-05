import FWCore.ParameterSet.Config as cms

'''
Build the PATFinalStateLS wrapper data class which holds the lumi summary.
'''

finalStateLS = cms.EDProducer(
    "PATFinalStateLSProducer",
    lumiSrc = cms.InputTag("lumiProducer"),
    trigSrc = cms.InputTag("patTriggerEvent"),
    xSec = cms.double(-1),
)
