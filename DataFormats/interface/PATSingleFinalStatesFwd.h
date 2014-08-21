#ifndef FinalStateAnalysis_DataFormats_PATSingleFwd_h
#define FinalStateAnalysis_DataFormats_PATSingleFwd_h

#include "FinalStateAnalysis/DataFormats/interface/FwdIncludes.h"
#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

// Forward declarations
template<typename A> class PATSingleFinalStateT;

namespace pat {
  class Electron;
  class Muon;
  class Tau;
  class Photon;
  class Jet;
}

typedef PATSingleFinalStateT<pat::Electron> PATElecFinalState;
typedef PATSingleFinalStateT<pat::Muon> PATMuFinalState;
typedef PATSingleFinalStateT<pat::Tau> PATTauFinalState;
typedef PATSingleFinalStateT<pat::Photon> PATPhoFinalState;
typedef PATSingleFinalStateT<pat::Jet> PATJetFinalState;

FWD_TYPEDEFS(PATElecFinalState)
FWD_TYPEDEFS(PATMuFinalState)
FWD_TYPEDEFS(PATTauFinalState)
FWD_TYPEDEFS(PATPhoFinalState)
FWD_TYPEDEFS(PATJetFinalState)

#endif
