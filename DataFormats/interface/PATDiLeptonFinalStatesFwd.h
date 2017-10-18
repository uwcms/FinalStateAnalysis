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
  class Photon;
  class Jet;
}

typedef PATPairFinalStateT<pat::Electron, pat::Electron> PATElecElecFinalState;
typedef PATPairFinalStateT<pat::Electron, pat::Muon> PATElecMuFinalState;
typedef PATPairFinalStateT<pat::Electron, pat::Tau> PATElecTauFinalState;
typedef PATPairFinalStateT<pat::Electron, pat::Photon> PATElecPhoFinalState;
typedef PATPairFinalStateT<pat::Muon, pat::Muon> PATMuMuFinalState;
typedef PATPairFinalStateT<pat::Muon, pat::Tau> PATMuTauFinalState;
typedef PATPairFinalStateT<pat::Muon, pat::Photon> PATMuPhoFinalState;
typedef PATPairFinalStateT<pat::Tau, pat::Tau> PATTauTauFinalState;
typedef PATPairFinalStateT<pat::Tau, pat::Photon> PATTauPhoFinalState;
typedef PATPairFinalStateT<pat::Photon, pat::Photon> PATPhoPhoFinalState;
typedef PATPairFinalStateT<pat::Muon, pat::Jet> PATMuJetFinalState;
typedef PATPairFinalStateT<pat::Electron, pat::Jet> PATElecJetFinalState;

FWD_TYPEDEFS(PATElecElecFinalState)
FWD_TYPEDEFS(PATElecMuFinalState)
FWD_TYPEDEFS(PATElecTauFinalState)
FWD_TYPEDEFS(PATElecPhoFinalState)
FWD_TYPEDEFS(PATMuMuFinalState)
FWD_TYPEDEFS(PATMuTauFinalState)
FWD_TYPEDEFS(PATMuPhoFinalState)
FWD_TYPEDEFS(PATTauTauFinalState)
FWD_TYPEDEFS(PATTauPhoFinalState)
FWD_TYPEDEFS(PATPhoPhoFinalState)
FWD_TYPEDEFS(PATMuJetFinalState)
FWD_TYPEDEFS(PATElecJetFinalState)

#endif
