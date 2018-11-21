'''

Ntuple branch template sets for event level quantities

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
num = PSet(
    evt=cms.vstring('evt.eventDouble', 'l'), # use unsigned long long branch
    lumi=cms.vstring('evt.evtId.luminosityBlock', 'I'),  # use int branch
    run=cms.vstring('evt.evtId.run', 'I'),  # use int branch
    isdata=cms.vstring('evt.isRealData', 'I'),
    isembed=cms.vstring('evt.isEmbeddedSample', 'I'),
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
    mvaMetCov00    = 'evt.met("mvamet").getSignificanceMatrix[0][0]',
    mvaMetCov01    = 'evt.met("mvamet").getSignificanceMatrix[0][1]',
    mvaMetCov10    = 'evt.met("mvamet").getSignificanceMatrix[1][0]',
    mvaMetCov11    = 'evt.met("mvamet").getSignificanceMatrix[1][1]',
    type1_pfMetEt  = 'evt.met("pfmet").pt', 
    type1_pfMetPhi = 'evt.met("pfmet").phi',
    puppiMetEt  = 'evt.met("puppimet").pt',
    puppiMetPhi = 'evt.met("puppimet").phi',
    
    recoilDaught='getDaughtersRecoil().R()',
    recoilWithMet='getDaughtersRecoilWithMet().R()',
)

# these things break if you pass a shifted met to fsa
shiftedMet = PSet(

    # 27s Jes Test
    #type1_pfMet_shiftedPt_JetAbsoluteFlavMapUp             = 'evt.metShift("pfmet","pt","jesAbsoluteFlavMap+")',
    #type1_pfMet_shiftedPt_JetAbsoluteFlavMapDown             = 'evt.metShift("pfmet","pt","jesAbsoluteFlavMap-")',
    #type1_pfMet_shiftedPt_JetAbsoluteMPFBiasUp             = 'evt.metShift("pfmet","pt","jesAbsoluteMPFBias+")',
    #type1_pfMet_shiftedPt_JetAbsoluteMPFBiasDown             = 'evt.metShift("pfmet","pt","jesAbsoluteMPFBias-")',
    #type1_pfMet_shiftedPt_JetAbsoluteScaleUp             = 'evt.metShift("pfmet","pt","jesAbsoluteScale+")',
    #type1_pfMet_shiftedPt_JetAbsoluteScaleDown             = 'evt.metShift("pfmet","pt","jesAbsoluteScale-")',
    #type1_pfMet_shiftedPt_JetAbsoluteStatUp             = 'evt.metShift("pfmet","pt","jesAbsoluteStat+")',
    #type1_pfMet_shiftedPt_JetAbsoluteStatDown             = 'evt.metShift("pfmet","pt","jesAbsoluteStat-")',
    #type1_pfMet_shiftedPt_JetFlavorQCDUp             = 'evt.metShift("pfmet","pt","jesFlavorQCD+")',
    #type1_pfMet_shiftedPt_JetFlavorQCDDown             = 'evt.metShift("pfmet","pt","jesFlavorQCD-")',
    #type1_pfMet_shiftedPt_JetFragmentationUp             = 'evt.metShift("pfmet","pt","jesFragmentation+")',
    #type1_pfMet_shiftedPt_JetFragmentationDown             = 'evt.metShift("pfmet","pt","jesFragmentation-")',
    #type1_pfMet_shiftedPt_JetPileUpDataMCUp             = 'evt.metShift("pfmet","pt","jesPileUpDataMC+")',
    #type1_pfMet_shiftedPt_JetPileUpDataMCDown             = 'evt.metShift("pfmet","pt","jesPileUpDataMC-")',
    #type1_pfMet_shiftedPt_JetPileUpPtBBUp             = 'evt.metShift("pfmet","pt","jesPileUpPtBB+")',
    #type1_pfMet_shiftedPt_JetPileUpPtBBDown             = 'evt.metShift("pfmet","pt","jesPileUpPtBB-")',
    #type1_pfMet_shiftedPt_JetPileUpPtEC1Up             = 'evt.metShift("pfmet","pt","jesPileUpPtEC1+")',
    #type1_pfMet_shiftedPt_JetPileUpPtEC1Down             = 'evt.metShift("pfmet","pt","jesPileUpPtEC1-")',
    #type1_pfMet_shiftedPt_JetPileUpPtEC2Up             = 'evt.metShift("pfmet","pt","jesPileUpPtEC2+")',
    #type1_pfMet_shiftedPt_JetPileUpPtEC2Down             = 'evt.metShift("pfmet","pt","jesPileUpPtEC2-")',
    #type1_pfMet_shiftedPt_JetPileUpPtHFUp             = 'evt.metShift("pfmet","pt","jesPileUpPtHF+")',
    #type1_pfMet_shiftedPt_JetPileUpPtHFDown             = 'evt.metShift("pfmet","pt","jesPileUpPtHF-")',
    #type1_pfMet_shiftedPt_JetPileUpPtRefUp             = 'evt.metShift("pfmet","pt","jesPileUpPtRef+")',
    #type1_pfMet_shiftedPt_JetPileUpPtRefDown             = 'evt.metShift("pfmet","pt","jesPileUpPtRef-")',
    type1_pfMet_shiftedPt_JetRelativeBalUp             = 'evt.metShift("pfmet","pt","jesRelativeBal+")',
    type1_pfMet_shiftedPt_JetRelativeBalDown             = 'evt.metShift("pfmet","pt","jesRelativeBal-")',
    #type1_pfMet_shiftedPt_JetRelativeFSRUp             = 'evt.metShift("pfmet","pt","jesRelativeFSR+")',
    #type1_pfMet_shiftedPt_JetRelativeFSRDown             = 'evt.metShift("pfmet","pt","jesRelativeFSR-")',
    #type1_pfMet_shiftedPt_JetRelativeJEREC1Up             = 'evt.metShift("pfmet","pt","jesRelativeJEREC1+")',
    #type1_pfMet_shiftedPt_JetRelativeJEREC1Down             = 'evt.metShift("pfmet","pt","jesRelativeJEREC1-")',
    #type1_pfMet_shiftedPt_JetRelativeJEREC2Up             = 'evt.metShift("pfmet","pt","jesRelativeJEREC2+")',
    #type1_pfMet_shiftedPt_JetRelativeJEREC2Down             = 'evt.metShift("pfmet","pt","jesRelativeJEREC2-")',
    #type1_pfMet_shiftedPt_JetRelativeJERHFUp             = 'evt.metShift("pfmet","pt","jesRelativeJERHF+")',
    #type1_pfMet_shiftedPt_JetRelativeJERHFDown             = 'evt.metShift("pfmet","pt","jesRelativeJERHF-")',
    #type1_pfMet_shiftedPt_JetRelativePtBBUp             = 'evt.metShift("pfmet","pt","jesRelativePtBB+")',
    #type1_pfMet_shiftedPt_JetRelativePtBBDown             = 'evt.metShift("pfmet","pt","jesRelativePtBB-")',
    #type1_pfMet_shiftedPt_JetRelativePtEC1Up             = 'evt.metShift("pfmet","pt","jesRelativePtEC1+")',
    #type1_pfMet_shiftedPt_JetRelativePtEC1Down             = 'evt.metShift("pfmet","pt","jesRelativePtEC1-")',
    #type1_pfMet_shiftedPt_JetRelativePtEC2Up             = 'evt.metShift("pfmet","pt","jesRelativePtEC2+")',
    #type1_pfMet_shiftedPt_JetRelativePtEC2Down             = 'evt.metShift("pfmet","pt","jesRelativePtEC2-")',
    #type1_pfMet_shiftedPt_JetRelativePtHFUp             = 'evt.metShift("pfmet","pt","jesRelativePtHF+")',
    #type1_pfMet_shiftedPt_JetRelativePtHFDown             = 'evt.metShift("pfmet","pt","jesRelativePtHF-")',
    #type1_pfMet_shiftedPt_JetRelativeStatECUp             = 'evt.metShift("pfmet","pt","jesRelativeStatEC+")',
    #type1_pfMet_shiftedPt_JetRelativeStatECDown             = 'evt.metShift("pfmet","pt","jesRelativeStatEC-")',
    #type1_pfMet_shiftedPt_JetRelativeStatFSRUp             = 'evt.metShift("pfmet","pt","jesRelativeStatFSR+")',
    #type1_pfMet_shiftedPt_JetRelativeStatFSRDown             = 'evt.metShift("pfmet","pt","jesRelativeStatFSR-")',
    #type1_pfMet_shiftedPt_JetRelativeStatHFUp             = 'evt.metShift("pfmet","pt","jesRelativeStatHF+")',
    #type1_pfMet_shiftedPt_JetRelativeStatHFDown             = 'evt.metShift("pfmet","pt","jesRelativeStatHF-")',
    #type1_pfMet_shiftedPt_JetSinglePionECALUp             = 'evt.metShift("pfmet","pt","jesSinglePionECAL+")',
    #type1_pfMet_shiftedPt_JetSinglePionECALDown             = 'evt.metShift("pfmet","pt","jesSinglePionECAL-")',
    #type1_pfMet_shiftedPt_JetSinglePionHCALUp             = 'evt.metShift("pfmet","pt","jesSinglePionHCAL+")',
    #type1_pfMet_shiftedPt_JetSinglePionHCALDown             = 'evt.metShift("pfmet","pt","jesSinglePionHCAL-")',
    #type1_pfMet_shiftedPt_JetTimePtEtaUp             = 'evt.metShift("pfmet","pt","jesTimePtEta+")',
    #type1_pfMet_shiftedPt_JetTimePtEtaDown             = 'evt.metShift("pfmet","pt","jesTimePtEta-")',
    type1_pfMet_shiftedPt_JetTotalUp             = 'evt.metShift("pfmet","pt","jesTotal+")',
    type1_pfMet_shiftedPt_JetTotalDown             = 'evt.metShift("pfmet","pt","jesTotal-")',
    type1_pfMet_shiftedPt_JetEta3to5Up             = 'evt.metShift("pfmet","pt","jesEta3to5+")',
    type1_pfMet_shiftedPt_JetEta3to5Down             = 'evt.metShift("pfmet","pt","jesEta3to5-")',
    type1_pfMet_shiftedPt_JetEta0to3Up             = 'evt.metShift("pfmet","pt","jesEta0to3+")',
    type1_pfMet_shiftedPt_JetEta0to3Down             = 'evt.metShift("pfmet","pt","jesEta0to3-")',
    type1_pfMet_shiftedPt_JetEta0to5Up             = 'evt.metShift("pfmet","pt","jesEta0to5+")',
    type1_pfMet_shiftedPt_JetEta0to5Down             = 'evt.metShift("pfmet","pt","jesEta0to5-")',
    #type1_pfMet_shiftedPt_JetCheckUESUp             = 'evt.metShift("pfmet","pt","checkUES+")',
    #type1_pfMet_shiftedPt_JetCheckUESDown             = 'evt.metShift("pfmet","pt","checkUES-")',

    #type1_pfMet_shiftedPhi_JetAbsoluteFlavMapUp             = 'evt.metShift("pfmet","phi","jesAbsoluteFlavMap+")',
    #type1_pfMet_shiftedPhi_JetAbsoluteFlavMapDown             = 'evt.metShift("pfmet","phi","jesAbsoluteFlavMap-")',
    #type1_pfMet_shiftedPhi_JetAbsoluteMPFBiasUp             = 'evt.metShift("pfmet","phi","jesAbsoluteMPFBias+")',
    #type1_pfMet_shiftedPhi_JetAbsoluteMPFBiasDown             = 'evt.metShift("pfmet","phi","jesAbsoluteMPFBias-")',
    #type1_pfMet_shiftedPhi_JetAbsoluteScaleUp             = 'evt.metShift("pfmet","phi","jesAbsoluteScale+")',
    #type1_pfMet_shiftedPhi_JetAbsoluteScaleDown             = 'evt.metShift("pfmet","phi","jesAbsoluteScale-")',
    #type1_pfMet_shiftedPhi_JetAbsoluteStatUp             = 'evt.metShift("pfmet","phi","jesAbsoluteStat+")',
    #type1_pfMet_shiftedPhi_JetAbsoluteStatDown             = 'evt.metShift("pfmet","phi","jesAbsoluteStat-")',
    #type1_pfMet_shiftedPhi_JetFlavorQCDUp             = 'evt.metShift("pfmet","phi","jesFlavorQCD+")',
    #type1_pfMet_shiftedPhi_JetFlavorQCDDown             = 'evt.metShift("pfmet","phi","jesFlavorQCD-")',
    #type1_pfMet_shiftedPhi_JetFragmentationUp             = 'evt.metShift("pfmet","phi","jesFragmentation+")',
    #type1_pfMet_shiftedPhi_JetFragmentationDown             = 'evt.metShift("pfmet","phi","jesFragmentation-")',
    #type1_pfMet_shiftedPhi_JetPileUpDataMCUp             = 'evt.metShift("pfmet","phi","jesPileUpDataMC+")',
    #type1_pfMet_shiftedPhi_JetPileUpDataMCDown             = 'evt.metShift("pfmet","phi","jesPileUpDataMC-")',
    #type1_pfMet_shiftedPhi_JetPileUpPtBBUp             = 'evt.metShift("pfmet","phi","jesPileUpPtBB+")',
    #type1_pfMet_shiftedPhi_JetPileUpPtBBDown             = 'evt.metShift("pfmet","phi","jesPileUpPtBB-")',
    #type1_pfMet_shiftedPhi_JetPileUpPtEC1Up             = 'evt.metShift("pfmet","phi","jesPileUpPtEC1+")',
    #type1_pfMet_shiftedPhi_JetPileUpPtEC1Down             = 'evt.metShift("pfmet","phi","jesPileUpPtEC1-")',
    #type1_pfMet_shiftedPhi_JetPileUpPtEC2Up             = 'evt.metShift("pfmet","phi","jesPileUpPtEC2+")',
    #type1_pfMet_shiftedPhi_JetPileUpPtEC2Down             = 'evt.metShift("pfmet","phi","jesPileUpPtEC2-")',
    #type1_pfMet_shiftedPhi_JetPileUpPtHFUp             = 'evt.metShift("pfmet","phi","jesPileUpPtHF+")',
    #type1_pfMet_shiftedPhi_JetPileUpPtHFDown             = 'evt.metShift("pfmet","phi","jesPileUpPtHF-")',
    #type1_pfMet_shiftedPhi_JetPileUpPtRefUp             = 'evt.metShift("pfmet","phi","jesPileUpPtRef+")',
    #type1_pfMet_shiftedPhi_JetPileUpPtRefDown             = 'evt.metShift("pfmet","phi","jesPileUpPtRef-")',
    type1_pfMet_shiftedPhi_JetRelativeBalUp             = 'evt.metShift("pfmet","phi","jesRelativeBal+")',
    type1_pfMet_shiftedPhi_JetRelativeBalDown             = 'evt.metShift("pfmet","phi","jesRelativeBal-")',
    #type1_pfMet_shiftedPhi_JetRelativeFSRUp             = 'evt.metShift("pfmet","phi","jesRelativeFSR+")',
    #type1_pfMet_shiftedPhi_JetRelativeFSRDown             = 'evt.metShift("pfmet","phi","jesRelativeFSR-")',
    #type1_pfMet_shiftedPhi_JetRelativeJEREC1Up             = 'evt.metShift("pfmet","phi","jesRelativeJEREC1+")',
    #type1_pfMet_shiftedPhi_JetRelativeJEREC1Down             = 'evt.metShift("pfmet","phi","jesRelativeJEREC1-")',
    #type1_pfMet_shiftedPhi_JetRelativeJEREC2Up             = 'evt.metShift("pfmet","phi","jesRelativeJEREC2+")',
    #type1_pfMet_shiftedPhi_JetRelativeJEREC2Down             = 'evt.metShift("pfmet","phi","jesRelativeJEREC2-")',
    #type1_pfMet_shiftedPhi_JetRelativeJERHFUp             = 'evt.metShift("pfmet","phi","jesRelativeJERHF+")',
    #type1_pfMet_shiftedPhi_JetRelativeJERHFDown             = 'evt.metShift("pfmet","phi","jesRelativeJERHF-")',
    #type1_pfMet_shiftedPhi_JetRelativePtBBUp             = 'evt.metShift("pfmet","phi","jesRelativePtBB+")',
    #type1_pfMet_shiftedPhi_JetRelativePtBBDown             = 'evt.metShift("pfmet","phi","jesRelativePtBB-")',
    #type1_pfMet_shiftedPhi_JetRelativePtEC1Up             = 'evt.metShift("pfmet","phi","jesRelativePtEC1+")',
    #type1_pfMet_shiftedPhi_JetRelativePtEC1Down             = 'evt.metShift("pfmet","phi","jesRelativePtEC1-")',
    #type1_pfMet_shiftedPhi_JetRelativePtEC2Up             = 'evt.metShift("pfmet","phi","jesRelativePtEC2+")',
    #type1_pfMet_shiftedPhi_JetRelativePtEC2Down             = 'evt.metShift("pfmet","phi","jesRelativePtEC2-")',
    #type1_pfMet_shiftedPhi_JetRelativePtHFUp             = 'evt.metShift("pfmet","phi","jesRelativePtHF+")',
    #type1_pfMet_shiftedPhi_JetRelativePtHFDown             = 'evt.metShift("pfmet","phi","jesRelativePtHF-")',
    #type1_pfMet_shiftedPhi_JetRelativeStatECUp             = 'evt.metShift("pfmet","phi","jesRelativeStatEC+")',
    #type1_pfMet_shiftedPhi_JetRelativeStatECDown             = 'evt.metShift("pfmet","phi","jesRelativeStatEC-")',
    #type1_pfMet_shiftedPhi_JetRelativeStatFSRUp             = 'evt.metShift("pfmet","phi","jesRelativeStatFSR+")',
    #type1_pfMet_shiftedPhi_JetRelativeStatFSRDown             = 'evt.metShift("pfmet","phi","jesRelativeStatFSR-")',
    #type1_pfMet_shiftedPhi_JetRelativeStatHFUp             = 'evt.metShift("pfmet","phi","jesRelativeStatHF+")',
    #type1_pfMet_shiftedPhi_JetRelativeStatHFDown             = 'evt.metShift("pfmet","phi","jesRelativeStatHF-")',
    #type1_pfMet_shiftedPhi_JetSinglePionECALUp             = 'evt.metShift("pfmet","phi","jesSinglePionECAL+")',
    #type1_pfMet_shiftedPhi_JetSinglePionECALDown             = 'evt.metShift("pfmet","phi","jesSinglePionECAL-")',
    #type1_pfMet_shiftedPhi_JetSinglePionHCALUp             = 'evt.metShift("pfmet","phi","jesSinglePionHCAL+")',
    #type1_pfMet_shiftedPhi_JetSinglePionHCALDown             = 'evt.metShift("pfmet","phi","jesSinglePionHCAL-")',
    #type1_pfMet_shiftedPhi_JetTimePtEtaUp             = 'evt.metShift("pfmet","phi","jesTimePtEta+")',
    #type1_pfMet_shiftedPhi_JetTimePtEtaDown             = 'evt.metShift("pfmet","phi","jesTimePtEta-")',
    type1_pfMet_shiftedPhi_JetTotalUp             = 'evt.metShift("pfmet","phi","jesTotal+")',
    type1_pfMet_shiftedPhi_JetTotalDown             = 'evt.metShift("pfmet","phi","jesTotal-")',
    type1_pfMet_shiftedPhi_JetEta3to5Up             = 'evt.metShift("pfmet","phi","jesEta3to5+")',
    type1_pfMet_shiftedPhi_JetEta3to5Down             = 'evt.metShift("pfmet","phi","jesEta3to5-")',
    type1_pfMet_shiftedPhi_JetEta0to3Up             = 'evt.metShift("pfmet","phi","jesEta0to3+")',
    type1_pfMet_shiftedPhi_JetEta0to3Down             = 'evt.metShift("pfmet","phi","jesEta0to3-")',
    type1_pfMet_shiftedPhi_JetEta0to5Up             = 'evt.metShift("pfmet","phi","jesEta0to5+")',
    type1_pfMet_shiftedPhi_JetEta0to5Down             = 'evt.metShift("pfmet","phi","jesEta0to5-")',

    #type1_pfMet_shiftedPt_RunIUESDown             = 'evt.met().userCand("metSystUesRunI-").pt',
    #type1_pfMet_shiftedPt_RunIUESUp             = 'evt.met().userCand("metSystUesRunI+").pt',
    #type1_pfMet_shiftedPhi_RunIUESDown             = 'evt.met().userCand("metSystUesRunI-").phi',
    #type1_pfMet_shiftedPhi_RunIUESUp             = 'evt.met().userCand("metSystUesRunI+").phi',

    #type1_pfMet_shiftedPt_CHARGEDUESDown             = 'evt.met().userCand("metSystUesCHARGED-").pt',
    #type1_pfMet_shiftedPt_CHARGEDUESUp             = 'evt.met().userCand("metSystUesCHARGED+").pt',
    #type1_pfMet_shiftedPhi_CHARGEDUESDown             = 'evt.met().userCand("metSystUesCHARGED-").phi',
    #type1_pfMet_shiftedPhi_CHARGEDUESUp             = 'evt.met().userCand("metSystUesCHARGED+").phi',

    #type1_pfMet_shiftedPt_ECALUESDown             = 'evt.met().userCand("metSystUesECAL-").pt',
    #type1_pfMet_shiftedPt_ECALUESUp             = 'evt.met().userCand("metSystUesECAL+").pt',
    #type1_pfMet_shiftedPhi_ECALUESDown             = 'evt.met().userCand("metSystUesECAL-").phi',
    #type1_pfMet_shiftedPhi_ECALUESUp             = 'evt.met().userCand("metSystUesECAL+").phi',

    #type1_pfMet_shiftedPt_HFUESDown             = 'evt.met().userCand("metSystUesHF-").pt',
    #type1_pfMet_shiftedPt_HFUESUp             = 'evt.met().userCand("metSystUesHF+").pt',
    #type1_pfMet_shiftedPhi_HFUESDown             = 'evt.met().userCand("metSystUesHF-").phi',
    #type1_pfMet_shiftedPhi_HFUESUp             = 'evt.met().userCand("metSystUesHF+").phi',

    #type1_pfMet_shiftedPt_HCALUESDown             = 'evt.met().userCand("metSystUesHCAL-").pt',
    #type1_pfMet_shiftedPt_HCALUESUp             = 'evt.met().userCand("metSystUesHCAL+").pt',
    #type1_pfMet_shiftedPhi_HCALUESDown             = 'evt.met().userCand("metSystUesHCAL-").phi',
    #type1_pfMet_shiftedPhi_HCALUESUp             = 'evt.met().userCand("metSystUesHCAL+").phi',

    raw_pfMetEt    = 'evt.met("pfmet").uncorPt',
    raw_pfMetPhi   = 'evt.met("pfmet").uncorPhi',

    # new systematics
    type1_pfMet_shiftedPt_JetResUp             = 'evt.metShift("pfmet","pt","jres+")',
    type1_pfMet_shiftedPt_JetResDown           = 'evt.metShift("pfmet","pt","jres-")',
    type1_pfMet_shiftedPhi_JetResUp            = 'evt.metShift("pfmet","phi","jres+")',
    type1_pfMet_shiftedPhi_JetResDown          = 'evt.metShift("pfmet","phi","jres-")',

    type1_pfMet_shiftedPt_JetEnUp              = 'evt.metShift("pfmet","pt","jes+")',
    type1_pfMet_shiftedPt_JetEnDown            = 'evt.metShift("pfmet","pt","jes-")',
    type1_pfMet_shiftedPhi_JetEnUp             = 'evt.metShift("pfmet","phi","jes+")',
    type1_pfMet_shiftedPhi_JetEnDown           = 'evt.metShift("pfmet","phi","jes-")',

    type1_pfMet_shiftedPhi_UnclusteredEnDown   = 'evt.metShift("pfmet","phi","ues-")',
    type1_pfMet_shiftedPhi_UnclusteredEnUp     = 'evt.metShift("pfmet","phi","ues+")',
    type1_pfMet_shiftedPt_UnclusteredEnDown    = 'evt.metShift("pfmet","pt","ues-")',
    type1_pfMet_shiftedPt_UnclusteredEnUp      = 'evt.metShift("pfmet","pt","ues+")',
# We do not use these 
#    type1_pfMet_shiftedPt_MuonEnUp             = 'evt.metShift("pfmet","pt","mes+")',
#    type1_pfMet_shiftedPt_ElectronEnUp         = 'evt.metShift("pfmet","pt","ees+")',
#    type1_pfMet_shiftedPt_TauEnUp              = 'evt.metShift("pfmet","pt","tes+")',

#    type1_pfMet_shiftedPt_PhotonEnUp           = 'evt.metShift("pfmet","pt","pes+")',
#    type1_pfMet_shiftedPt_MuonEnDown           = 'evt.metShift("pfmet","pt","mes-")',
#    type1_pfMet_shiftedPt_ElectronEnDown       = 'evt.metShift("pfmet","pt","ees-")',
#    type1_pfMet_shiftedPt_TauEnDown            = 'evt.metShift("pfmet","pt","tes-")',

#    type1_pfMet_shiftedPt_PhotonEnDown         = 'evt.metShift("pfmet","pt","pes-")',
#    type1_pfMet_shiftedPhi_MuonEnUp            = 'evt.metShift("pfmet","phi","mes+")',
#    type1_pfMet_shiftedPhi_ElectronEnUp        = 'evt.metShift("pfmet","phi","ees+")',
#    type1_pfMet_shiftedPhi_TauEnUp             = 'evt.metShift("pfmet","phi","tes+")',

#    type1_pfMet_shiftedPhi_PhotonEnUp          = 'evt.metShift("pfmet","phi","pes+")',
#    type1_pfMet_shiftedPhi_MuonEnDown          = 'evt.metShift("pfmet","phi","mes-")',
#    type1_pfMet_shiftedPhi_ElectronEnDown      = 'evt.metShift("pfmet","phi","ees-")',
#    type1_pfMet_shiftedPhi_TauEnDown           = 'evt.metShift("pfmet","phi","tes-")',

#    type1_pfMet_shiftedPhi_PhotonEnDown        = 'evt.metShift("pfmet","phi","pes-")',
)

gen = PSet(
    # Process ID used to simulate in Pythia
    processID='evt.genEventInfo.signalProcessID',
    isZtautau='evt.findDecay(23,15)',
    isGtautau='evt.findDecay(22,15)',
    isWtaunu='evt.findDecay(24,15)',
    isWmunu='evt.findDecay(24,13)',
    isWenu='evt.findDecay(24,11)',
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


