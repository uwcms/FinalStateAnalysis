/*
 * =====================================================================================
 *
 *       Filename:  LinkDef.h
 *
 *    Description:  Make C++ correction functions visible to ROOT
 *
 *         Author:  Evan Friis (), evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FinalStateAnalysis/TagAndProbe/interface/MuonPOG2011HLTEfficiencies.h"
#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsMuEG201253X.h"
#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsDoubleE.h"
#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsDoubleMu.h"

#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ function Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATA;
#pragma link C++ function Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_MC;
#pragma link C++ function Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC;
#pragma link C++ function Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATA;
#pragma link C++ function Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_MC;
#pragma link C++ function Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC;

#pragma link C++ function muTrigScale_MuEG_2012_53X;
#pragma link C++ function eleTrigScale_MuEG_2012_53X;
#pragma link C++ function muTrigEff_MuEG_2012_53X;
#pragma link C++ function eleTrigEff_MuEG_2012_53X;
#pragma link C++ function muIDscale_MuEG_2012_53X;
#pragma link C++ function eleIDscale_MuEG_2012_53X;
#pragma link C++ function Trg_DoubleEle_2011;
#pragma link C++ function Trg_DoubleEle_2012;
#pragma link C++ function Trg_DoubleMu_2012;

#endif
