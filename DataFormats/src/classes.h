#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"

#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalStateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"

#include "FinalStateAnalysis/DataFormats/interface/PATSingleFinalStates.h"

#include "FinalStateAnalysis/DataFormats/interface/PATDiLeptonFinalStates.h"

#include "FinalStateAnalysis/DataFormats/interface/PATTriLeptonFinalStates.h"

#include "FinalStateAnalysis/DataFormats/interface/PATQuadLeptonFinalStates.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFiveLeptonFinalStates.h"

#include "FinalStateAnalysis/DataAlgos/interface/VBFVariables.h"

#include "FinalStateAnalysis/DataFormats/interface/Macros.h"

namespace {
  struct FinalStateAnalysis_DataFormats_dicts {
    // General missing dictionaries
    edm::Ptr<reco::Vertex> dummyVertexPtr;
    edm::PtrVector<reco::Vertex> dummyVertexPtrVector;

    edm::Ptr<pat::Photon> dummyPhotonPtr;

    edm::RefProd<pat::ElectronCollection> dummyElectronRefProd;
    edm::RefProd<pat::MuonCollection> dummyMuonRefProd;
    edm::RefProd<pat::TauCollection> dummyTauRefProd;
    edm::RefProd<pat::PhotonCollection> dummyPhotonRefProd;
    edm::RefProd<pat::JetCollection> dummyJetRefProd;

    std::map<std::string, float> dummyFloatMap;
    std::map<std::string, int> dummyIntMap;
    //std::pair<std::string, float> dummyFloatPair;
    //std::pair<std::string, int> dummyIntPair;
    std::map<std::string, edm::Ptr<pat::MET> > dummyMETMap;

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

    // single final states
    FWD_MIN_CLASSDECL(PATElecFinalState)
    FWD_MIN_CLASSDECL(PATMuFinalState)
    FWD_MIN_CLASSDECL(PATTauFinalState)
    FWD_MIN_CLASSDECL(PATPhoFinalState)
    FWD_MIN_CLASSDECL(PATJetFinalState)

    // pair final states
    FWD_MIN_CLASSDECL(PATElecElecFinalState)
    FWD_MIN_CLASSDECL(PATElecMuFinalState)
    FWD_MIN_CLASSDECL(PATElecTauFinalState)
    FWD_MIN_CLASSDECL(PATElecPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuMuFinalState)
    FWD_MIN_CLASSDECL(PATMuTauFinalState)
    FWD_MIN_CLASSDECL(PATMuPhoFinalState)
    FWD_MIN_CLASSDECL(PATTauTauFinalState)
    FWD_MIN_CLASSDECL(PATTauPhoFinalState)
    FWD_MIN_CLASSDECL(PATPhoPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuJetFinalState)
    FWD_MIN_CLASSDECL(PATElecJetFinalState)

    // triplet final states
    FWD_MIN_CLASSDECL(PATElecElecElecFinalState)
    FWD_MIN_CLASSDECL(PATElecElecMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecTauFinalState)
    FWD_MIN_CLASSDECL(PATElecElecPhoFinalState)
    FWD_MIN_CLASSDECL(PATElecMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecMuTauFinalState)
    FWD_MIN_CLASSDECL(PATElecMuPhoFinalState)
    FWD_MIN_CLASSDECL(PATElecTauTauFinalState)
    FWD_MIN_CLASSDECL(PATElecPhoPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuMuMuFinalState)
    FWD_MIN_CLASSDECL(PATMuMuTauFinalState)
    FWD_MIN_CLASSDECL(PATMuMuPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuTauTauFinalState)
    FWD_MIN_CLASSDECL(PATMuPhoPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuJetJetFinalState)
    FWD_MIN_CLASSDECL(PATTauTauTauFinalState)

    // quad final states
    FWD_MIN_CLASSDECL(PATElecElecElecElecFinalState)
    FWD_MIN_CLASSDECL(PATElecElecElecMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecElecTauFinalState)
    FWD_MIN_CLASSDECL(PATElecElecElecPhoFinalState)
    FWD_MIN_CLASSDECL(PATElecElecMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecMuTauFinalState)
    FWD_MIN_CLASSDECL(PATElecElecMuPhoFinalState)
    FWD_MIN_CLASSDECL(PATElecElecTauTauFinalState)
    FWD_MIN_CLASSDECL(PATElecElecPhoPhoFinalState)
    FWD_MIN_CLASSDECL(PATElecMuMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecMuMuTauFinalState)
    FWD_MIN_CLASSDECL(PATElecMuMuPhoFinalState)
    FWD_MIN_CLASSDECL(PATElecMuTauTauFinalState)
    FWD_MIN_CLASSDECL(PATElecTauTauTauFinalState)
    FWD_MIN_CLASSDECL(PATElecMuPhoPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuMuMuMuFinalState)
    FWD_MIN_CLASSDECL(PATMuMuMuTauFinalState)
    FWD_MIN_CLASSDECL(PATMuMuMuPhoFinalState)
    FWD_MIN_CLASSDECL(PATMuMuTauTauFinalState)
    FWD_MIN_CLASSDECL(PATMuTauTauTauFinalState)
    FWD_MIN_CLASSDECL(PATTauTauTauTauFinalState)
    FWD_MIN_CLASSDECL(PATMuMuPhoPhoFinalState)

    FWD_MIN_CLASSDECL(PATMuMuMuMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecMuMuMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecMuMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecElecMuMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecElecElecMuFinalState)
    FWD_MIN_CLASSDECL(PATElecElecElecElecElecFinalState)

  };
}
