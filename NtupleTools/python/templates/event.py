'''

Ntuple branch template sets for event level quantities

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
num = PSet(
    evt=cms.vstring('evt.evtId.event', 'I'),  # use int branch
    lumi=cms.vstring('evt.evtId.luminosityBlock', 'I'),  # use int branch
    run=cms.vstring('evt.evtId.run', 'I'),  # use int branch
    isdata=cms.vstring('evt.isRealData', 'I'),
)

pileup = PSet(
    rho='evt.rho',
    nvtx='evt.recoVertices.size',
    # Number of true PU events
    nTruePU='? evt.puInfo.size > 0 ? evt.puInfo[1].getTrueNumInteractions :-1',
)

pv_info = PSet(
    pvX='? evt.pv.isNonnull() ? evt.pv.x : -999',
    pvY='? evt.pv.isNonnull() ? evt.pv.y : -999',
    pvZ='? evt.pv.isNonnull() ? evt.pv.z : -999',
    pvDX='? evt.pv.isNonnull() ? evt.pv.xError : -999',
    pvDY='? evt.pv.isNonnull() ? evt.pv.yError : -999',
    pvDZ='? evt.pv.isNonnull() ? evt.pv.zError : -999',
    pvChi2='? evt.pv.isNonnull() ? evt.pv.chi2 : -999',
    pvndof='? evt.pv.isNonnull() ? evt.pv.ndof : -999',
    pvNormChi2='? evt.pv.isNonnull() ? evt.pv.normalizedChi2 : -999',
    pvIsValid=cms.vstring('? evt.pv.isNonnull() ? evt.pv.isValid : 0', 'I'),
    pvIsFake=cms.vstring('? evt.pv.isNonnull() ? evt.pv.isFake : 1', 'I'),
    pvRho = 'evt.pv.position.Rho',
)

met = PSet(
    mvaMetEt       = 'evt.met("mvamet").et',
    mvaMetPhi      = 'evt.met("mvamet").phi',
    pfMetEt        = 'evt.met4vector("pfmet","",1).Et',
    pfMetPhi       = 'evt.met4vector("pfmet","",1).Phi',
    type1_pfMetEt  = 'evt.met4vector("pfmet","type1",1).Et', #1 --> phi correction not in miniAOD
    type1_pfMetPhi = 'evt.met4vector("pfmet","type1",1).Phi',
    #systematics
    pfMet_mes_Et   = 'evt.met4vector("pfmet","mes+", 1).Et',
    pfMet_tes_Et   = 'evt.met4vector("pfmet","tes+", 1).Et',
    pfMet_jes_Et   = 'evt.met4vector("pfmet","jes+", 1).Et',
    pfMet_ues_Et   = 'evt.met4vector("pfmet","ues+", 1).Et',

    pfMet_mes_Phi  = 'evt.met4vector("pfmet","mes+", 1).Phi',
    pfMet_tes_Phi  = 'evt.met4vector("pfmet","tes+", 1).Phi',
    pfMet_jes_Phi  = 'evt.met4vector("pfmet","jes+", 1).Phi',
    pfMet_ues_Phi  = 'evt.met4vector("pfmet","ues+", 1).Phi',
    
    recoilDaught='getDaughtersRecoil().R()',
    recoilWithMet='getDaughtersRecoilWithMet().R()',
)

gen = PSet(
    # Process ID used to simulate in Pythia
    processID='evt.genEventInfo.signalProcessID',
    isZtautau='evt.findDecay(23,15)',
    isGtautau='evt.findDecay(22,15)',
    isWtaunu='evt.findDecay(24,15)',
    isWmunu='evt.findDecay(24,13)',
    NUP='evt.lesHouches.NUP',
    EmbPtWeight='evt.generatorFilter.filterEfficiency',
)

tauSpinner = PSet(
    tauSpinnerWeight = 'evt.weight("tauSpinnerWeight")'
)


