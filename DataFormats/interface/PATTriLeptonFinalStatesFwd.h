#ifndef FinalStateAnalysis_DataFormats_PATLeptonTripletsFwd_h
#define FinalStateAnalysis_DataFormats_PATLeptonTripletsFwd_h

// Forward declarations
template<typename A, typename B, typename C> class PATTripletFinalStateT;

namespace pat {
  class Electron;
  class Muon;
  class Tau;
}

typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Electron> PATElecElecElecFinalState;
typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Muon> PATElecElecMuFinalState;
typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Tau> PATElecElecTauFinalState;
typedef PATTripletFinalStateT<pat::Electron, pat::Muon, pat::Muon> PATElecMuMuFinalState;
typedef PATTripletFinalStateT<pat::Electron, pat::Muon, pat::Tau> PATElecMuTauFinalState;
typedef PATTripletFinalStateT<pat::Electron, pat::Tau, pat::Tau> PATElecTauTauFinalState;
typedef PATTripletFinalStateT<pat::Muon, pat::Muon, pat::Muon> PATMuMuMuFinalState;
typedef PATTripletFinalStateT<pat::Muon, pat::Muon, pat::Tau> PATMuMuTauFinalState;
typedef PATTripletFinalStateT<pat::Muon, pat::Tau, pat::Tau> PATMuTauTauFinalState;
// for completeness
typedef PATTripletFinalStateT<pat::Tau, pat::Tau, pat::Tau> PATTauTauTauFinalState;

#include "FinalStateAnalysis/DataFormats/interface/FwdIncludes.h"
#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

FWD_TYPEDEFS(PATElecElecElecFinalState)
FWD_TYPEDEFS(PATElecElecMuFinalState)
FWD_TYPEDEFS(PATElecElecTauFinalState)
FWD_TYPEDEFS(PATElecMuMuFinalState)
FWD_TYPEDEFS(PATElecMuTauFinalState)
FWD_TYPEDEFS(PATElecTauTauFinalState)
FWD_TYPEDEFS(PATMuMuMuFinalState)
FWD_TYPEDEFS(PATMuMuTauFinalState)
FWD_TYPEDEFS(PATMuTauTauFinalState)
FWD_TYPEDEFS(PATTauTauTauFinalState)

#endif
