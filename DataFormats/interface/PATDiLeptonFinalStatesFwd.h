#ifndef FinalStateAnalysis_DataFormats_PATLeptonPairsFwd_h
#define FinalStateAnalysis_DataFormats_PATLeptonPairsFwd_h

#include "FinalStateAnalysis/DataFormats/interface/FwdIncludes.h"
#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

// Forward declarations
template<typename A, typename B> class PATPairFinalStateT;

namespace pat {
  class Electron;
  class Muon;
  class Tau;
}

typedef PATPairFinalStateT<pat::Electron, pat::Electron> PATElecElecFinalState;
typedef PATPairFinalStateT<pat::Electron, pat::Muon> PATElecMuFinalState;
typedef PATPairFinalStateT<pat::Electron, pat::Tau> PATElecTauFinalState;
typedef PATPairFinalStateT<pat::Muon, pat::Muon> PATMuMuFinalState;
typedef PATPairFinalStateT<pat::Muon, pat::Tau> PATMuTauFinalState;
typedef PATPairFinalStateT<pat::Tau, pat::Tau> PATTauTauFinalState;

FWD_TYPEDEFS(PATElecElecFinalState)
FWD_TYPEDEFS(PATElecMuFinalState)
FWD_TYPEDEFS(PATElecTauFinalState)
FWD_TYPEDEFS(PATMuMuFinalState)
FWD_TYPEDEFS(PATMuTauFinalState)
FWD_TYPEDEFS(PATTauTauFinalState)

#endif
