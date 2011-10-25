#include "FinalStateAnalysis/Selectors/interface/PATFinalStateAnalysis.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/Selectors/interface/PATFinalStateSelection.h"
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"

#include "FWCore/Common/interface/LuminosityBlockBase.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"
#include "TH1F.h"

#include <sstream>

PATFinalStateAnalysis::PATFinalStateAnalysis(
    const edm::ParameterSet& pset, TFileDirectory& fs):
  BasicAnalyzer(pset, fs),fs_(fs) {
  src_ = pset.getParameter<edm::InputTag>("src");
  name_ = pset.getParameter<std::string>("@module_label");

  // Setup the code to apply event level weights
  std::vector<std::string> weights =
    pset.getParameter<std::vector<std::string> >("weights");
  for (size_t i = 0; i < weights.size(); ++i) {
    evtWeights_.push_back(EventFunction(weights[i]));
  }
  evtSrc_ = pset.getParameter<edm::InputTag>("evtSrc");

  analysisCfg_ = pset.getParameterSet("analysis");
  filter_ = pset.exists("filter") ? pset.getParameter<bool>("filter") : false;
  // Build the analyzer
  analysis_.reset(new PATFinalStateSelection(analysisCfg_, fs_));
  // Check if we want to make a sub analyzer for each run (use w/ caution!)
  splitRuns_ = pset.exists("splitRuns") ?
    pset.getParameter<bool>("splitRuns") : false;
  if (splitRuns_)
    runDir_.reset(new TFileDirectory(fs.mkdir("runs")));

  skimCounter_ = pset.getParameter<edm::InputTag>("skimCounter");
  lumiProducer_ = pset.exists("lumiProducer") ?
    pset.getParameter<edm::InputTag>("lumiProducer") :
    edm::InputTag("lumiProducer");
  // Build the event counter histos.
  eventCounter_ = fs_.make<TH1F>("eventCount", "Events Processed", 1, -0.5, 0.5);
  eventCounterWeighted_ = fs_.make<TH1F>(
      "eventCountWeighted", "Events Processed (weighted)", 1, -0.5, 0.5);
  eventWeights_ = fs_.make<TH1F>(
      "eventWeights", "Events Weights", 100, 0, 5);
  skimEventCounter_ = fs_.make<TH1F>(
      "skimCounter", "Original Events Processed", 1, -0.5, 0.5);
  integratedLumi_ = fs_.make<TH1F>(
      "intLumi", "Integrated Lumi", 1, -0.5, 0.5);
}

PATFinalStateAnalysis::~PATFinalStateAnalysis() { }

void PATFinalStateAnalysis::beginLuminosityBlock(
    const edm::LuminosityBlockBase& ls) {

  edm::Handle<edm::MergeableCounter> skimmedEvents;
  ls.getByLabel(skimCounter_, skimmedEvents);
  skimEventCounter_->Fill(0.0, skimmedEvents->value);

  // Get int. lumi
  edm::Handle<LumiSummary> lumiSummary;
  ls.getByLabel(lumiProducer_, lumiSummary);
  if (lumiSummary.isValid()) {
    integratedLumi_->Fill(0.0, lumiSummary->intgRecLumi());
  }
}

bool PATFinalStateAnalysis::filter(const edm::EventBase& evt) {
  // Get the event weight
  double eventWeight = 1.0;

  if (evtWeights_.size()) {
    edm::Handle<PATFinalStateEventCollection> event;
    evt.getByLabel(evtSrc_, event);
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
  evt.getByLabel(src_, finalStates);

  std::vector<const PATFinalState*> finalStatePtrs;
  finalStatePtrs.reserve(finalStates->size());

  //Normal running
  bool mustCleanupFinalStates = false;
  for (size_t i = 0; i < finalStates->size(); ++i) {
    finalStatePtrs.push_back( &( (*finalStates)[i] ) );
  }

  // Hack workarounds into ntuple
//  bool mustCleanupFinalStates = true;
//  for (size_t i = 0; i < finalStates->size(); ++i) {
//    PATFinalState * clone = (*finalStates)[i].clone();
//    clone->addUserInt("evt", evt.id().event());
//    clone->addUserInt("run", evt.id().run());
//    clone->addUserInt("idx", i);
//    finalStatePtrs.push_back(clone);
//  }

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

void PATFinalStateAnalysis::endJob() {
  std::cout << "Cut flow for analyzer: " << name_ << std::endl;
  analysis_->cutFlow()->print(std::cout);
  std::cout << std::endl;
}
