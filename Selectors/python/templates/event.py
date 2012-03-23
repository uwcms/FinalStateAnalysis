'''

Ntuple branch template sets for event level quantities

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
num = PSet(
    evt = cms.vstring('evt.evtId.event', 'I'), # use int branch
    lumi = cms.vstring('evt.evtId.luminosityBlock', 'I'), # use int branch
    run = cms.vstring('evt.evtId.run', 'I'), # use int branch
    isdata = cms.vstring('evt.isRealData', 'I'),
)

pileup = PSet(
    rho = 'evt.rho',
    nvtx = 'evt.recoVertices.size',
    # Number of true PU events
    nTruePU = '? evt.puInfo.size > 0 ? evt.puInfo[1].getTrueNumInteractions : -1',
    puWeightFall11Data2011A = 'evt.puWeight("fall11", "data2011A")',
    puWeightFall11Data2011AB = 'evt.puWeight("fall11", "data2011AB")'
    puWeightFall11Data2011B = 'evt.puWeight("fall11", "data2011B")'
)

met = PSet(
    metEt = 'evt.met.et',
    metPhi = 'evt.met.phi',
    metSignificance = 'evt.metSignificance',
)
