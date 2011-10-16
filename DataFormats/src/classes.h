#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematicsFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalStateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATDiLeptonFinalStates.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiLeptonFinalStatesFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATTriLeptonFinalStates.h"
#include "FinalStateAnalysis/DataFormats/interface/PATTriLeptonFinalStatesFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

namespace {
  struct FinalStateAnalysis_DataFormats_dicts {
    // Needed by dicandidate systematics object
    edm::Ptr<reco::Vertex> dummyVertexPtr;
    edm::PtrVector<reco::Vertex> dummyVertexPtrVector;

    std::map<std::string, float> dummyFloatMap;
    std::map<std::string, int> dummyIntMap;
    std::pair<std::string, float> dummyFloatPair;
    std::pair<std::string, int> dummyIntPair;

    PATMuTauSystematics dummyMuTauSys;
    edm::Wrapper<PATMuTauSystematics> dummyMuTauSysW;
    PATMuTauSystematicsCollection dummyMuTauSysColl;
    edm::Wrapper<PATMuTauSystematicsCollection> dummyMuTauSysCollW;
    PATMuTauSystematicsRef dummyMuTauSysRef;
    PATMuTauSystematicsRefProd dummyMuTauSysRefProd;
    PATMuTauSystematicsRefVector dummyMuTauSysRefVector;
    PATMuTauSystematicsPtr dummyMuTauSysPtr;

    FWD_ABS_CLASSDECL(PATFinalState)
    FWD_CLASSDECL(PATFinalStateEvent)

    FWD_CLASSDECL(PATMultiCandFinalState)

    FWD_CLASSDECL(PATElecElecFinalState)
    FWD_CLASSDECL(PATElecMuFinalState)
    FWD_CLASSDECL(PATElecTauFinalState)
    FWD_CLASSDECL(PATMuMuFinalState)
    FWD_CLASSDECL(PATMuTauFinalState)
    FWD_CLASSDECL(PATTauTauFinalState)

    FWD_CLASSDECL(PATElecElecElecFinalState)
    FWD_CLASSDECL(PATElecElecMuFinalState)
    FWD_CLASSDECL(PATElecElecTauFinalState)
    FWD_CLASSDECL(PATElecMuMuFinalState)
    FWD_CLASSDECL(PATElecMuTauFinalState)
    FWD_CLASSDECL(PATElecTauTauFinalState)
    FWD_CLASSDECL(PATMuMuMuFinalState)
    FWD_CLASSDECL(PATMuMuTauFinalState)
    FWD_CLASSDECL(PATMuTauTauFinalState)
    FWD_CLASSDECL(PATTauTauTauFinalState)
  };
}
