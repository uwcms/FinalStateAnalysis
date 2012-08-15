#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"

#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalStateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"

#include "FinalStateAnalysis/DataFormats/interface/PATDiLeptonFinalStates.h"

#include "FinalStateAnalysis/DataFormats/interface/PATTriLeptonFinalStates.h"

#include "FinalStateAnalysis/DataFormats/interface/PATQuadLeptonFinalStates.h"

#include "FinalStateAnalysis/DataAlgos/interface/VBFVariables.h"

#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

namespace {
  struct FinalStateAnalysis_DataFormats_dicts {
    // General missing dictionaries
    edm::Ptr<reco::Vertex> dummyVertexPtr;
    edm::PtrVector<reco::Vertex> dummyVertexPtrVector;

    edm::RefProd<pat::ElectronCollection> dummyElectronRefProd;
    edm::RefProd<pat::MuonCollection> dummyMuonRefProd;
    edm::RefProd<pat::TauCollection> dummyTauRefProd;
    edm::RefProd<pat::JetCollection> dummyJetRefProd;

    std::map<std::string, float> dummyFloatMap;
    std::map<std::string, int> dummyIntMap;
    std::pair<std::string, float> dummyFloatPair;
    std::pair<std::string, int> dummyIntPair;

    // For the VBF variables
    VBFVariables dummyVBFVars;

    // shared pointer wrapper class
    PATFinalStateProxy proxyDummy;

    // base classes
    FWD_ABS_CLASSDECL(PATFinalState)
    FWD_CLASSDECL(PATFinalStateEvent)
    FWD_CLASSDECL(PATFinalStateLS)

    // n-cand state
    FWD_CLASSDECL(PATMultiCandFinalState)

    // pair final states
    FWD_CLASSDECL(PATElecElecFinalState)
    FWD_CLASSDECL(PATElecMuFinalState)
    FWD_CLASSDECL(PATElecTauFinalState)
    FWD_CLASSDECL(PATMuMuFinalState)
    FWD_CLASSDECL(PATMuTauFinalState)
    FWD_CLASSDECL(PATTauTauFinalState)

    // triplet final states
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

    // quad final states
    FWD_CLASSDECL(PATElecElecElecElecFinalState)
    FWD_CLASSDECL(PATElecElecElecMuFinalState)
    FWD_CLASSDECL(PATElecElecElecTauFinalState)
    FWD_CLASSDECL(PATElecElecMuMuFinalState)
    FWD_CLASSDECL(PATElecElecMuTauFinalState)
    FWD_CLASSDECL(PATElecElecTauTauFinalState)
    FWD_CLASSDECL(PATElecMuMuMuFinalState)
    FWD_CLASSDECL(PATElecMuMuTauFinalState)
    FWD_CLASSDECL(PATElecMuTauTauFinalState)
    FWD_CLASSDECL(PATElecTauTauTauFinalState)
    FWD_CLASSDECL(PATMuMuMuMuFinalState)
    FWD_CLASSDECL(PATMuMuMuTauFinalState)
    FWD_CLASSDECL(PATMuMuTauTauFinalState)
    FWD_CLASSDECL(PATMuTauTauTauFinalState)
    FWD_CLASSDECL(PATTauTauTauTauFinalState)
  };
}
