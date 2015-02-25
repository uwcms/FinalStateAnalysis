#ifndef FinalStateAnalysis_DataFormats_PATLeptonQuadsFwd_h
#define FinalStateAnalysis_DataFormats_PATLeptonQuadsFwd_h

// Forward declarations
template<typename A, typename B, typename C, typename D> class PATQuadFinalStateT;

namespace pat {
  class Electron;
  class Muon;
  class Tau;
  class Photon;
}

#include "FinalStateAnalysis/DataFormats/interface/FwdIncludes.h"
#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

/*

   Use PATQuadLeptonFinalStatesFwd_gen.py to generate statements.

*/

typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Electron> PATElecElecElecElecFinalState;
FWD_TYPEDEFS(PATElecElecElecElecFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Muon> PATElecElecElecMuFinalState;
FWD_TYPEDEFS(PATElecElecElecMuFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Tau> PATElecElecElecTauFinalState;
FWD_TYPEDEFS(PATElecElecElecTauFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Electron, pat::Photon> PATElecElecElecPhoFinalState;
FWD_TYPEDEFS(PATElecElecElecPhoFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Muon, pat::Muon> PATElecElecMuMuFinalState;
FWD_TYPEDEFS(PATElecElecMuMuFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Muon, pat::Tau> PATElecElecMuTauFinalState;
FWD_TYPEDEFS(PATElecElecMuTauFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Muon, pat::Photon> PATElecElecMuPhoFinalState;
FWD_TYPEDEFS(PATElecElecMuPhoFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Tau, pat::Tau> PATElecElecTauTauFinalState;
FWD_TYPEDEFS(PATElecElecTauTauFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Electron, pat::Photon, pat::Photon> PATElecElecPhoPhoFinalState;
FWD_TYPEDEFS(PATElecElecPhoPhoFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Muon, pat::Muon, pat::Muon> PATElecMuMuMuFinalState;
FWD_TYPEDEFS(PATElecMuMuMuFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Muon, pat::Muon, pat::Tau> PATElecMuMuTauFinalState;
FWD_TYPEDEFS(PATElecMuMuTauFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Muon, pat::Muon, pat::Photon> PATElecMuMuPhoFinalState;
FWD_TYPEDEFS(PATElecMuMuPhoFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Muon, pat::Tau, pat::Tau> PATElecMuTauTauFinalState;
FWD_TYPEDEFS(PATElecMuTauTauFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Muon, pat::Photon, pat::Photon> PATElecMuPhoPhoFinalState;
FWD_TYPEDEFS(PATElecMuPhoPhoFinalState)
typedef PATQuadFinalStateT<pat::Electron, pat::Tau, pat::Tau, pat::Tau> PATElecTauTauTauFinalState;
FWD_TYPEDEFS(PATElecTauTauTauFinalState)
typedef PATQuadFinalStateT<pat::Muon, pat::Muon, pat::Muon, pat::Muon> PATMuMuMuMuFinalState;
FWD_TYPEDEFS(PATMuMuMuMuFinalState)
typedef PATQuadFinalStateT<pat::Muon, pat::Muon, pat::Muon, pat::Tau> PATMuMuMuTauFinalState;
FWD_TYPEDEFS(PATMuMuMuTauFinalState)
typedef PATQuadFinalStateT<pat::Muon, pat::Muon, pat::Muon, pat::Photon> PATMuMuMuPhoFinalState;
FWD_TYPEDEFS(PATMuMuMuPhoFinalState)
typedef PATQuadFinalStateT<pat::Muon, pat::Muon, pat::Tau, pat::Tau> PATMuMuTauTauFinalState;
FWD_TYPEDEFS(PATMuMuTauTauFinalState)
typedef PATQuadFinalStateT<pat::Muon, pat::Muon, pat::Photon, pat::Photon> PATMuMuPhoPhoFinalState;
FWD_TYPEDEFS(PATMuMuPhoPhoFinalState)
typedef PATQuadFinalStateT<pat::Muon, pat::Tau, pat::Tau, pat::Tau> PATMuTauTauTauFinalState;
FWD_TYPEDEFS(PATMuTauTauTauFinalState)
typedef PATQuadFinalStateT<pat::Tau, pat::Tau, pat::Tau, pat::Tau> PATTauTauTauTauFinalState;
FWD_TYPEDEFS(PATTauTauTauTauFinalState)

#endif
