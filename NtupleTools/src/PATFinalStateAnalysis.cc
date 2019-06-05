#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateAnalysis.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateSelection.h"
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Common/interface/LuminosityBlockBase.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TTree.h"

#include <sstream>


PATFinalStateAnalysis::PATFinalStateAnalysis(
    const edm::ParameterSet& pset, TFileDirectory& fs, edm::ConsumesCollector&& iC):
    //const edm::ParameterSet& pset, TFileDirectory& fs):
  fs_(fs) {
  srcToken_ = iC.consumes<PATFinalStateCollection>(pset.getParameter<edm::InputTag>("src"));
  name_ = pset.getParameter<std::string>("@module_label");

  // Setup the code to apply event level weights
  std::vector<std::string> weights =
    pset.getParameter<std::vector<std::string> >("weights");
  for (size_t i = 0; i < weights.size(); ++i) {
    evtWeights_.push_back(EventFunction(weights[i]));
  }
  evtSrcToken_ = iC.consumes<PATFinalStateEventCollection>(pset.getParameter<edm::InputTag>("evtSrc"));

  analysisCfg_ = pset.getParameterSet("analysis");
  filter_ = pset.exists("filter") ? pset.getParameter<bool>("filter") : false;
  // Build the analyzer
  analysis_.reset(new PATFinalStateSelection(analysisCfg_, fs_));
  // Check if we want to make a sub analyzer for each run (use w/ caution!)
  splitRuns_ = pset.exists("splitRuns") ?
    pset.getParameter<bool>("splitRuns") : false;
  if (splitRuns_)
    runDir_.reset(new TFileDirectory(fs.mkdir("runs")));

  miniAODName_ = pset.getParameter<std::string>("miniAODName");

  skimCounter_  = pset.getParameter<edm::InputTag>("skimCounter");
  skimCounterToken_  = iC.consumes<edm::MergeableCounter,edm::InLumi>(skimCounter_);
  summedWeight_ = pset.getParameter<edm::InputTag>("summedWeight");
  summedWeightToken_ = iC.consumes<edm::MergeableCounter,edm::InLumi>(summedWeight_);
  lumiProducer_ = pset.exists("lumiProducer") ?
                  pset.getParameter<edm::InputTag>("lumiProducer") :
                  edm::InputTag("finalStateLS");
  lumiProducerToken_ = iC.consumes<PATFinalStateLS,edm::InLumi>(lumiProducer_);
  // Build the event counter histos.
  eventCounter_ = fs_.make<TH1F>("eventCount", "Events Processed", 1, -0.5, 0.5);
  eventCounterWeighted_ = fs_.make<TH1F>(
      "eventCountWeighted", "Events Processed (weighted)", 1, -0.5, 0.5);
  eventWeights_ = fs_.make<TH1F>(
      "eventWeights", "Events Weights", 100, 0, 5);
  skimEventCounter_ = fs_.make<TH1F>(
      "skimCounter", "Original Events Processed", 1, -0.5, 0.5);
  summedWeightHist_ = fs_.make<TH1D>(
      "summedWeights", "Sum of weights for processed events", 1, -0.5, 0.5);
  integratedLumi_ = fs_.make<TH1F>(
      "intLumi", "Integrated Lumi", 1, -0.5, 0.5);
  miniAODParent_ = fs_.make<TH1F>(miniAODName_.c_str(), "miniAODName", 1, -0.5, 0.5);
  metaTree_ = fs_.make<TTree>(
      "metaInfo", "Information about processed runs and lumis");
  metaTree_->Branch("run", &treeRunBranch_, "run/I");
  metaTree_->Branch("lumi", &treeLumiBranch_, "lumi/I");
  metaTree_->Branch("nevents", &treeEventsProcessedBranch_, "nevents/I");
  metaTree_->Branch("summedWeights", &treeSummedWeightsBranch_, "summedWeights/F");

}

PATFinalStateAnalysis::~PATFinalStateAnalysis() { }

void PATFinalStateAnalysis::endLuminosityBlock(
    const edm::LuminosityBlockBase& ls) {
  //std::cout << "Analyzing lumisec: " << ls.id() << std::endl;

  edm::Handle<edm::MergeableCounter> skimmedEvents;
  ls.getByLabel(skimCounter_, skimmedEvents);
  skimEventCounter_->Fill(0.0, skimmedEvents->value);

  edm::Handle<edm::MergeableCounter> summedWeights;
  ls.getByLabel(summedWeight_, summedWeights);
  summedWeightHist_->Fill(0.0, summedWeights->value);

  edm::Handle<PATFinalStateLS> lumiSummary;
  ls.getByLabel(lumiProducer_, lumiSummary);
  integratedLumi_->Fill(0.0, lumiSummary->intLumi());
  treeIntLumi_ = lumiSummary->intLumi();

  // Fill the meta info tree
  treeRunBranch_ = ls.run();
  treeLumiBranch_ = ls.luminosityBlock();
  treeEventsProcessedBranch_ = skimmedEvents->value;
  treeSummedWeightsBranch_ = summedWeights->value;
  metaTree_->Fill();
}


void PATFinalStateAnalysis::endLuminosityBlock(
    const edm::LuminosityBlock& ls) {
  //std::cout << "Analyzing lumisec: " << ls.id() << std::endl;

  edm::Handle<edm::MergeableCounter> skimmedEvents;
  ls.getByToken(skimCounterToken_, skimmedEvents);
  skimEventCounter_->Fill(0.0, skimmedEvents->value);

  edm::Handle<edm::MergeableCounter> summedWeights;
  ls.getByToken(summedWeightToken_, summedWeights);
  summedWeightHist_->Fill(0.0, summedWeights->value);

  edm::Handle<PATFinalStateLS> lumiSummary;
  ls.getByToken(lumiProducerToken_, lumiSummary);
  integratedLumi_->Fill(0.0, lumiSummary->intLumi());
  treeIntLumi_ = lumiSummary->intLumi();

  // Fill the meta info tree
  treeRunBranch_ = ls.run();
  treeLumiBranch_ = ls.luminosityBlock();
  treeEventsProcessedBranch_ = skimmedEvents->value;
  treeSummedWeightsBranch_ = summedWeights->value;
  metaTree_->Fill();
}

bool PATFinalStateAnalysis::filter(const edm::EventBase& evt) {
  std::cout << "TODO: add filter for PATFinalStateAnalysis" << std::endl;
  return false;
}

bool PATFinalStateAnalysis::filter(const edm::Event& evt) {
  // Get the event weight
  double eventWeight = 1.0;

  if (evtWeights_.size()) {
    edm::Handle<PATFinalStateEventCollection> event;
    evt.getByToken(evtSrcToken_, event);
    for (size_t i = 0; i < evtWeights_.size(); ++i) {
      eventWeight *= evtWeights_[i]( (*event)[0] );
    }
  }
  // Count this event
  eventCounter_->Fill(0.0);
  eventCounterWeighted_->Fill(0.0, eventWeight);
  eventWeights_->Fill(eventWeight);

  // Get the final states to analyze
  edm::Handle<PATFinalStateCollection> finalStates;
  evt.getByToken(srcToken_, finalStates);

  std::vector<const PATFinalState*> finalStatePtrs;
  finalStatePtrs.reserve(finalStates->size());

  //Normal running
  bool mustCleanupFinalStates = false;
  for (size_t i = 0; i < finalStates->size(); ++i) {
    finalStatePtrs.push_back( &( (*finalStates)[i] ) );
  }

  // Hack workarounds into ntuple here
  //  bool mustCleanupFinalStates = true;
  //  do something

  // Check if we want to split by runs
  if (splitRuns_) {
    edm::RunNumber_t run = evt.id().run();
    // make a new folder for this run if necessary
    if (!runAnalysis_.count(run)) {
      std::stringstream ss; ss << run;
      TFileDirectory subdir = runDir_->mkdir(ss.str());
      boost::shared_ptr<PATFinalStateSelection> runSelection(
          new PATFinalStateSelection(analysisCfg_, subdir));
      runAnalysis_.insert(std::make_pair(run, runSelection));
    }
    // Analyze this event using the current run folder
    RunMap::iterator theSelectionIter = runAnalysis_.find(run);
    assert(theSelectionIter != runAnalysis_.end());
    PATFinalStateSelection* selection = theSelectionIter->second.get();
    assert(selection);
    (*selection)(finalStatePtrs, eventWeight);
  }

  bool result = (*analysis_)(finalStatePtrs, eventWeight);

  if (mustCleanupFinalStates) {
    for (size_t i = 0; i < finalStatePtrs.size(); ++i) {
      delete finalStatePtrs[i];
    }
  }

  return result;
}

void PATFinalStateAnalysis::analyze(const edm::EventBase& evt) {
  filter(evt);
}

void PATFinalStateAnalysis::analyze(const edm::Event& evt) {
  filter(evt);
}

void PATFinalStateAnalysis::endJob() {
  std::cout << "Cut flow for analyzer: " << name_ << std::endl;
  analysis_->cutFlow()->print(std::cout);
  std::cout << std::endl;
}
