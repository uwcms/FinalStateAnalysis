/*
 * Wrapper about PATFinalStateSelection which handles the getting objects from
 * the event.
 */

#ifndef PATFINALSTATEANALYSIS_FRM3UCVB
#define PATFINALSTATEANALYSIS_FRM3UCVB

#include <vector>
#include <map>
#include <boost/shared_ptr.hpp>
#include <iostream>
#include <SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Provenance/interface/RunID.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateSelection.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
//#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
//#include "PhysicsTools/UtilAlgos/interface/BasicAnalyzer.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

class TH1;
class TTree;
class PATFinalStateSelection;
class TFileDirectory;
namespace edm {
  class LuminosityBlock;
  class LuminosityBlockBase;
}

class PATFinalStateAnalysis {
  public:
    PATFinalStateAnalysis(const edm::ParameterSet& pset, TFileDirectory& fs);
    PATFinalStateAnalysis(const edm::ParameterSet& pset, TFileDirectory& fs, edm::ConsumesCollector&& iC);
    virtual ~PATFinalStateAnalysis();
    void beginJob() {}
    void endJob();
    // Alias for filter with no return value
    void analyze(const edm::Event& evt);
    void analyze(const edm::EventBase& evt);
    bool filter(const edm::Event& evt);
    bool filter(const edm::EventBase& evt);
    // Do nothing at beginning
    void beginLuminosityBlock(const edm::LuminosityBlock& ls){};
    void beginLuminosityBlock(const edm::LuminosityBlockBase& ls){};
    void endLuminosityBlock(const edm::LuminosityBlock& ls);
    void endLuminosityBlock(const edm::LuminosityBlockBase& ls);

  private:
    edm::EDGetTokenT<PATFinalStateCollection> srcToken_;
    std::string name_;
    TFileDirectory& fs_;
    edm::ParameterSet analysisCfg_;
    boost::shared_ptr<PATFinalStateSelection> analysis_;

    // Tools for applying event weights
    typedef StringObjectFunction<PATFinalStateEvent> EventFunction;
    edm::EDGetTokenT<PATFinalStateEventCollection> evtSrcToken_;
    std::vector<EventFunction> evtWeights_;

    // Tool for examining individual runs
    bool splitRuns_;
    std::auto_ptr<TFileDirectory> runDir_;
    typedef std::map<edm::RunNumber_t, boost::shared_ptr<PATFinalStateSelection> > RunMap;
    RunMap runAnalysis_;

    // For counting events
    TH1* eventCounter_;
    TH1* eventCounterWeighted_;
    TH1* eventWeights_;
    // For keeping track of the skimming
    edm::EDGetTokenT<edm::MergeableCounter> skimCounterToken_;
    edm::InputTag skimCounter_;
    TH1* skimEventCounter_;
    // gen weights
    edm::EDGetTokenT<edm::MergeableCounter> summedWeightToken_;
    edm::InputTag summedWeight_;
    TH1* summedWeightHist_;
    // For counting the luminosity
    edm::EDGetTokenT<PATFinalStateLS> lumiProducerToken_;
    edm::InputTag lumiProducer_;
    TH1* integratedLumi_;

    // Keep track of the processed events in each lumi in a tree
    TTree* metaTree_;
    Int_t treeRunBranch_;
    Int_t treeLumiBranch_;
    Int_t treeEventsProcessedBranch_;
    Float_t treeSummedWeightsBranch_;
    Float_t treeIntLumi_; // The estimated integrated luminosity

    bool filter_;
};

#endif /* end of include guard: PATFINALSTATEANALYSIS_FRM3UCVB */
