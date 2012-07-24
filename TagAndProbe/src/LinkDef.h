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

#endif

