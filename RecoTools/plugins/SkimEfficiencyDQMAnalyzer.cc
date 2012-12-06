/*
 * =====================================================================================
 *
 *       Filename:  SkimEfficiencyDQMAnalyzer.cc
 *
 *    Description:  Track the efficiencies of different skim paths.
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DQMServices/Core/interface/MonitorElement.h"
#include "DQMServices/Core/interface/DQMStore.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

class SkimEfficiencyDQMAnalyzer : public edm::EDAnalyzer {
  public:
    SkimEfficiencyDQMAnalyzer(const edm::ParameterSet& pset);
    virtual ~SkimEfficiencyDQMAnalyzer(){}
    void analyze(const edm::Event& evt, const edm::EventSetup& es);
  private:
    typedef std::vector<std::string> vstring;
    vstring paths_;
    MonitorElement* passedBits_;
    MonitorElement* exclusiveBits_;
    MonitorElement* correlation_;

    // matches structure of paths - don't reallocate every event.
    std::vector<bool> results_;
};

SkimEfficiencyDQMAnalyzer::SkimEfficiencyDQMAnalyzer(const edm::ParameterSet& pset) {

  paths_ = pset.getParameter<vstring>("paths");

  // Initialize results vector
  for (size_t i = 0; i < paths_.size(); ++i) {
    results_.push_back(false);
  }

  DQMStore* store = &*edm::Service<DQMStore>();
  passedBits_ = store->book1D(
      "passed", "Number of events in each path",
      paths_.size() + 2,  // each + total + any
      -0.5, paths_.size() + 2 - 0.5);
  // Set bin labels
  passedBits_->setBinLabel(1, "total");
  passedBits_->setBinLabel(2, "any");
  for (size_t i = 0; i < paths_.size(); ++i) {
    passedBits_->setBinLabel(3+i, paths_[i]);
  }

  exclusiveBits_ = store->book1D(
      "pathExlcusivePass", "Number of exclusive events in each path",
      paths_.size() + 2,  // each + total
      -0.5, paths_.size() + 2 - 0.5);
  // Set bin labels
  exclusiveBits_->setBinLabel(1, "total");
  exclusiveBits_->setBinLabel(2, "one path only");
  for (size_t i = 0; i < paths_.size(); ++i) {
    exclusiveBits_->setBinLabel(3+i, paths_[i]);
  }

  correlation_ = store->book2D(
      "pathCorrelation", "Correlation between paths",
      paths_.size(),  -0.5, paths_.size() - 0.5,
      paths_.size(),  -0.5, paths_.size() - 0.5);
  for (size_t i = 0; i < paths_.size(); ++i) {
    correlation_->setBinLabel(i+1, paths_[i], 1);
    correlation_->setBinLabel(i+1, paths_[i], 2);
  }
}

void SkimEfficiencyDQMAnalyzer::analyze(const edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::TriggerResults> triggerResults;
  evt.getByLabel(edm::InputTag("TriggerResults"), triggerResults);

  // put the results into our simple vector
  unsigned int numPassed = 0;

  const edm::TriggerNames& triggerNames = evt.triggerNames(*triggerResults);
  for (size_t i = 0; i < paths_.size(); ++i) {
    unsigned int pathIndex = triggerNames.triggerIndex(paths_[i]);
    bool result = triggerResults->accept(pathIndex);
    results_[i] = result;
    if (result)
      numPassed++;
  }

  // Always fill the total column
  passedBits_->Fill(0);
  exclusiveBits_->Fill(0);

  // Nothing passed, we are done.
  if (!numPassed)
    return;

  // Fill passed column
  passedBits_->Fill(1);
  // Check if this event was fired by only one trigger
  if (numPassed == 1)
    exclusiveBits_->Fill(1);

  // Fill passed info
  for (size_t i = 0; i < paths_.size(); ++i) {
    if (results_[i]) {
      passedBits_->Fill(2 + i);
      if (numPassed == 1) {
        // this bit was exclusive
        exclusiveBits_->Fill(2 + i);
      }
    }
  }

  // Fill correlation
  for (size_t i = 0; i < paths_.size(); ++i) {
    for (size_t j = 0; j < paths_.size(); ++j) {
      if (results_[i] && results_[j])
        correlation_->Fill(i, j);
    }
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SkimEfficiencyDQMAnalyzer);
