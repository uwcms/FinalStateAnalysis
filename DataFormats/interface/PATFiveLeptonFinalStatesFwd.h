#ifndef FinalStateAnalysis_DataFormats_PATLeptonFivesFwd_h
#define FinalStateAnalysis_DataFormats_PATLeptonFivesFwd_h

// Forward declarations
template<typename A, typename B, typename C, typename D, typename E> class PATFiveFinalStateT;

namespace pat {
  class Electron;
  class Muon;
  class Tau;
  class Photon;
}

#include "FinalStateAnalysis/DataFormats/interface/FwdIncludes.h"
#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

/*

   Use PATFiveLeptonFinalStatesFwd_gen.py to generate statements.

*/

typedef PATFiveFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Electron, pat::Electron> PATElecElecElecElecElecFinalState;
FWD_TYPEDEFS(PATElecElecElecElecElecFinalState)
typedef PATFiveFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Electron, pat::Muon> PATElecElecElecElecMuFinalState;
FWD_TYPEDEFS(PATElecElecElecElecMuFinalState)
typedef PATFiveFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Muon, pat::Muon> PATElecElecElecMuMuFinalState;
FWD_TYPEDEFS(PATElecElecElecMuMuFinalState)
typedef PATFiveFinalStateT<pat::Electron, pat::Electron, pat::Muon, pat::Muon, pat::Muon> PATElecElecMuMuMuFinalState;
FWD_TYPEDEFS(PATElecElecMuMuMuFinalState)
typedef PATFiveFinalStateT<pat::Electron, pat::Muon, pat::Muon, pat::Muon, pat::Muon> PATElecMuMuMuMuFinalState;
FWD_TYPEDEFS(PATElecMuMuMuMuFinalState)
typedef PATFiveFinalStateT<pat::Muon, pat::Muon, pat::Muon, pat::Muon, pat::Muon> PATMuMuMuMuMuFinalState;
FWD_TYPEDEFS(PATMuMuMuMuMuFinalState)

#endif
