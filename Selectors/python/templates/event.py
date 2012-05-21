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
    puWeightData2011A = 'evt.puWeight("data2011A")',
    puWeightData2011AB = 'evt.puWeight("data2011AB")',
    puWeightData2011B = 'evt.puWeight("data2011B")',
)

met = PSet(
    metEt = 'evt.met.et',
    metPhi = 'evt.met.phi',
    metSignificance = 'evt.metSignificance',
)

gen = PSet(
    # Process ID used to simulate in Pythia
    processID = 'evt.genEventInfo.signalProcessID',
)
