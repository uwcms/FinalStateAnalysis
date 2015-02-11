#ifndef FinalStateAnalysis_DataFormats_PATLeptonTripletsFwd_h
#define FinalStateAnalysis_DataFormats_PATLeptonTripletsFwd_h

// Forward declarations
template<typename A, typename B, typename C> class PATTripletFinalStateT;

namespace pat {
  class Electron;
  class Muon;
  class Tau;
  class Photon;
}

#include "FinalStateAnalysis/DataFormats/interface/FwdIncludes.h"
#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Electron> PATElecElecElecFinalState;
FWD_TYPEDEFS(PATElecElecElecFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Muon> PATElecElecMuFinalState;
FWD_TYPEDEFS(PATElecElecMuFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Tau> PATElecElecTauFinalState;
FWD_TYPEDEFS(PATElecElecTauFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Electron, pat::Photon> PATElecElecPhoFinalState;
FWD_TYPEDEFS(PATElecElecPhoFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Muon, pat::Muon> PATElecMuMuFinalState;
FWD_TYPEDEFS(PATElecMuMuFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Muon, pat::Tau> PATElecMuTauFinalState;
FWD_TYPEDEFS(PATElecMuTauFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Muon, pat::Photon> PATElecMuPhoFinalState;
FWD_TYPEDEFS(PATElecMuPhoFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Tau, pat::Tau> PATElecTauTauFinalState;
FWD_TYPEDEFS(PATElecTauTauFinalState)
typedef PATTripletFinalStateT<pat::Electron, pat::Photon, pat::Photon> PATElecPhoPhoFinalState;
FWD_TYPEDEFS(PATElecPhoPhoFinalState)
typedef PATTripletFinalStateT<pat::Muon, pat::Muon, pat::Muon> PATMuMuMuFinalState;
FWD_TYPEDEFS(PATMuMuMuFinalState)
typedef PATTripletFinalStateT<pat::Muon, pat::Muon, pat::Tau> PATMuMuTauFinalState;
FWD_TYPEDEFS(PATMuMuTauFinalState)
typedef PATTripletFinalStateT<pat::Muon, pat::Muon, pat::Photon> PATMuMuPhoFinalState;
FWD_TYPEDEFS(PATMuMuPhoFinalState)
typedef PATTripletFinalStateT<pat::Muon, pat::Tau, pat::Tau> PATMuTauTauFinalState;
FWD_TYPEDEFS(PATMuTauTauFinalState)
typedef PATTripletFinalStateT<pat::Muon, pat::Photon, pat::Photon> PATMuPhoPhoFinalState;
FWD_TYPEDEFS(PATMuPhoPhoFinalState)
typedef PATTripletFinalStateT<pat::Muon, pat::Jet, pat::Jet> PATMuJetJetFinalState;
FWD_TYPEDEFS(PATMuJetJetFinalState)
typedef PATTripletFinalStateT<pat::Tau, pat::Tau, pat::Tau> PATTauTauTauFinalState;
FWD_TYPEDEFS(PATTauTauTauFinalState)
#endif
