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
    pvIsFake=cms.vstring('? evt.pv.isNonnull() ? evt.pv.isFake : 1', 'I')
)

met = PSet(
    mva_metEt     = 'evt.met("mvamet").et',
    mva_metPhi    = 'evt.met("mvamet").phi',
    type1_pfMetEt  = 'evt.met("pfmet").userCand("type1").et',
    type1_pfMetPhi = 'evt.met("pfmet").userCand("type1").phi',
    #systematics
    pfMet_mes_Et   = 'evt.met("pfmet").userCand("mes+").et',
    pfMet_tes_Et   = 'evt.met("pfmet").userCand("tes+").et',
    pfMet_jes_Et   = 'evt.met("pfmet").userCand("jes+").et',
    pfMet_ues_Et   = 'evt.met("pfmet").userCand("ues+").et',

    pfMet_mes_Phi  = 'evt.met("pfmet").userCand("mes+").phi',
    pfMet_tes_Phi  = 'evt.met("pfmet").userCand("tes+").phi',
    pfMet_jes_Phi  = 'evt.met("pfmet").userCand("jes+").phi',
    pfMet_ues_Phi  = 'evt.met("pfmet").userCand("ues+").phi',
    
    #metSignificance='evt.metSignificance',
    recoilDaught='getDaughtersRecoil().R()',
    recoilWithMet='getDaughtersRecoilWithMet().R()',
    #does not seem to work, investigating...
    #recoilWMetSig ='getRecoilWithMetSignificance()',
    #mvametEt='evt.met("mvamet").et',
    #mvametPhi='evt.met("mvamet").phi',
    #mvametSignificance='evt.met("mvamet").significance',
)

gen = PSet(
    # Process ID used to simulate in Pythia
    processID='evt.genEventInfo.signalProcessID',
)
