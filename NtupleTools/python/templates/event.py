'''

Ntuple branch template sets for event level quantities

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
num = PSet(
    #evt=cms.vstring('evt.evtId.event', 'I'),  # use int branch
    evt=cms.vstring('evt.event', 'I'),  # use int branch
    lumi=cms.vstring('evt.evtId.luminosityBlock', 'I'),  # use int branch
    run=cms.vstring('evt.evtId.run', 'I'),  # use int branch
    isdata=cms.vstring('evt.isRealData', 'I'),
)

pileup = PSet(
    rho='evt.rho',
    #nvtx='evt.recoVertices.size',
    nvtx='evt.numberVertices',
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
    raw_pfMetEt    = 'evt.met("pfmet").uncorPt',
    raw_pfMetPhi   = 'evt.met("pfmet").uncorPhi',
    type1_pfMetEt  = 'evt.met("pfmet").pt', 
    type1_pfMetPhi = 'evt.met("pfmet").phi',


    # new systematics
    type1_pfMet_shiftedPt_JetResUp             = 'evt.metShift("pfmet","pt","jres+")',
    type1_pfMet_shiftedPt_JetEnUp              = 'evt.metShift("pfmet","pt","jes+")',
    type1_pfMet_shiftedPt_MuonEnUp             = 'evt.metShift("pfmet","pt","mes+")',
    type1_pfMet_shiftedPt_ElectronEnUp         = 'evt.metShift("pfmet","pt","ees+")',
    type1_pfMet_shiftedPt_TauEnUp              = 'evt.metShift("pfmet","pt","tes+")',
    type1_pfMet_shiftedPt_UnclusteredEnUp      = 'evt.metShift("pfmet","pt","ues+")',
    type1_pfMet_shiftedPt_PhotonEnUp           = 'evt.metShift("pfmet","pt","pes+")',
    
    type1_pfMet_shiftedPt_JetResDown           = 'evt.metShift("pfmet","pt","jres-")',
    type1_pfMet_shiftedPt_JetEnDown            = 'evt.metShift("pfmet","pt","jes-")',
    type1_pfMet_shiftedPt_MuonEnDown           = 'evt.metShift("pfmet","pt","mes-")',
    type1_pfMet_shiftedPt_ElectronEnDown       = 'evt.metShift("pfmet","pt","ees-")',
    type1_pfMet_shiftedPt_TauEnDown            = 'evt.metShift("pfmet","pt","tes-")',
    type1_pfMet_shiftedPt_UnclusteredEnDown    = 'evt.metShift("pfmet","pt","ues-")',
    type1_pfMet_shiftedPt_PhotonEnDown         = 'evt.metShift("pfmet","pt","pes-")',
    
    type1_pfMet_shiftedPhi_JetResUp            = 'evt.metShift("pfmet","phi","jres+")',
    type1_pfMet_shiftedPhi_JetEnUp             = 'evt.metShift("pfmet","phi","jes+")',
    type1_pfMet_shiftedPhi_MuonEnUp            = 'evt.metShift("pfmet","phi","mes+")',
    type1_pfMet_shiftedPhi_ElectronEnUp        = 'evt.metShift("pfmet","phi","ees+")',
    type1_pfMet_shiftedPhi_TauEnUp             = 'evt.metShift("pfmet","phi","tes+")',
    type1_pfMet_shiftedPhi_UnclusteredEnUp     = 'evt.metShift("pfmet","phi","ues+")',
    type1_pfMet_shiftedPhi_PhotonEnUp          = 'evt.metShift("pfmet","phi","pes+")',
    
    type1_pfMet_shiftedPhi_JetResDown          = 'evt.metShift("pfmet","phi","jres-")',
    type1_pfMet_shiftedPhi_JetEnDown           = 'evt.metShift("pfmet","phi","jes-")',
    type1_pfMet_shiftedPhi_MuonEnDown          = 'evt.metShift("pfmet","phi","mes-")',
    type1_pfMet_shiftedPhi_ElectronEnDown      = 'evt.metShift("pfmet","phi","ees-")',
    type1_pfMet_shiftedPhi_TauEnDown           = 'evt.metShift("pfmet","phi","tes-")',
    type1_pfMet_shiftedPhi_UnclusteredEnDown   = 'evt.metShift("pfmet","phi","ues-")',
    type1_pfMet_shiftedPhi_PhotonEnDown        = 'evt.metShift("pfmet","phi","pes-")',
    
    type1_pfMet_Et_ues_plus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ues+", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ues+", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ues+", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ues+", 1).Py-evt.met4vector("pfmet","",1).Py))',
    type1_pfMet_Et_ues_minus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ues-", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ues-", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ues-", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ues-", 1).Py-evt.met4vector("pfmet","",1).Py))',

    type1_pfMet_Et_ees_plus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ees+", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ees+", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ees+", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ees+", 1).Py-evt.met4vector("pfmet","",1).Py))',
    type1_pfMet_Et_ees_minus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ees-", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","ees-", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ees-", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","ees-", 1).Py-evt.met4vector("pfmet","",1).Py))',

    type1_pfMet_Et_mes_plus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","mes+", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","mes+", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","mes+", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","mes+", 1).Py-evt.met4vector("pfmet","",1).Py))',
    type1_pfMet_Et_mes_minus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","mes-", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","mes-", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","mes-", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","mes-", 1).Py-evt.met4vector("pfmet","",1).Py))',

    type1_pfMet_Et_tes_plus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","tes+", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","tes+", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","tes+", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","tes+", 1).Py-evt.met4vector("pfmet","",1).Py))',
    type1_pfMet_Et_tes_minus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","tes-", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","tes-", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","tes-", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","tes-", 1).Py-evt.met4vector("pfmet","",1).Py))',

    type1_pfMet_Et_jes_plus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","jes+", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","jes+", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","jes+", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","jes+", 1).Py-evt.met4vector("pfmet","",1).Py))',
    type1_pfMet_Et_jes_minus = 'sqrt((evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","jes-", 1).Px-evt.met4vector("pfmet","",1).Px)*(evt.met4vector("pfmet","type1",1).Px + evt.met4vector("pfmet","jes-", 1).Px-evt.met4vector("pfmet","",1).Px)+(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","jes-", 1).Py-evt.met4vector("pfmet","",1).Py)*(evt.met4vector("pfmet","type1",1).Py + evt.met4vector("pfmet","jes-", 1).Py-evt.met4vector("pfmet","",1).Py))',

    pfMet_Phi_ees_plus  = 'evt.met4vector("pfmet","ees+", 1).phi',
    pfMet_Phi_mes_plus  = 'evt.met4vector("pfmet","mes+", 1).phi',
    pfMet_Phi_tes_plus  = 'evt.met4vector("pfmet","tes+", 1).phi',
    pfMet_Phi_ues_plus  = 'evt.met4vector("pfmet","ues+", 1).phi',
    pfMet_Phi_jes_plus  = 'evt.met4vector("pfmet","jes+", 1).phi',

    pfMet_Phi_ees_minus  = 'evt.met4vector("pfmet","ees-", 1).phi',
    pfMet_Phi_mes_minus  = 'evt.met4vector("pfmet","mes-", 1).phi',
    pfMet_Phi_tes_minus  = 'evt.met4vector("pfmet","tes-", 1).phi',
    pfMet_Phi_ues_minus  = 'evt.met4vector("pfmet","ues-", 1).phi',
    pfMet_Phi_jes_minus  = 'evt.met4vector("pfmet","jes-", 1).phi',
    pfMet_ues_AtanToPhi = 'atan(evt.met4vector("pfmet","ues+", 1).Py/evt.met4vector("pfmet","ues+", 1).Px)',

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
    isZmumu='evt.findDecay(23,13)',
    isZee='evt.findDecay(23,11)',

    genHTT='evt.genHTT',
    NUP='evt.lesHouches.NUP',
    EmbPtWeight='evt.generatorFilter.filterEfficiency',
    GenWeight='? evt.genEventInfo.weights().size>0 ? evt.genEventInfo.weights()[0] : 0',
)

tauSpinner = PSet(
    tauSpinnerWeight = 'evt.weight("tauSpinnerWeight")'
)


