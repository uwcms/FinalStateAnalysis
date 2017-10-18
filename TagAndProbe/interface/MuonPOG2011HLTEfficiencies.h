/*
 * =====================================================================================
 *
 *       Filename:  MuonPOG2011HLTEfficiencies.h
 *
 *    Description:  Muon HLT efficiencies for 2011 triggers.
 *                  Interface to
 *                  https://twiki.cern.ch/twiki/pub/CMS/MuonHLT/efficiencyFunctions.C
 *                  on https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT#DoubleMu_Efficiency
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef MUONPOG2011HLTEFFICIENCIES_T6X5Z8MI
#define MUONPOG2011HLTEFFICIENCIES_T6X5Z8MI

#include "Rtypes.h"

Double_t Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATA(Double_t eta1, Double_t eta2);
Double_t Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_MC(Double_t eta1, Double_t eta2);
Double_t Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC(Double_t eta1, Double_t eta2);
Double_t Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATA(Double_t eta1, Double_t eta2);
Double_t Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_MC(Double_t eta1, Double_t eta2);
Double_t Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC(Double_t eta1, Double_t eta2);

#endif /* end of include guard: MUONPOG2011HLTEFFICIENCIES_T6X5Z8MI */
