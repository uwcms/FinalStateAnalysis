/*
 * =====================================================================================
 *
 *       Filename:  SkimEfficiencyAnalyzer.cc
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

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <TH1F.h>
#include <TH2F.h>

class SkimEfficiencyAnalyzer : public edm::EDAnalyzer {
  public:
    SkimEfficiencyAnalyzer(const edm::ParameterSet& pset);
    virtual ~SkimEfficiencyAnalyzer(){}
    void analyze(const edm::Event& evt, const edm::EventSetup& es);
    void endJob();
  private:
    typedef std::vector<std::string> vstring;
    vstring paths_;
    TH1F* passedBits_;
    TH1F* exclusiveBits_;
    TH2F* correlation_;

    // matches structure of paths - don't reallocate every event.
    std::vector<bool> results_;
};

SkimEfficiencyAnalyzer::SkimEfficiencyAnalyzer(const edm::ParameterSet& pset) {

  paths_ = pset.getParameter<vstring>("paths");

  // Initialize results vector
  for (size_t i = 0; i < paths_.size(); ++i) {
    results_.push_back(false);
  }

  edm::Service<TFileService> fs;

  passedBits_ = fs->make<TH1F>(
      "passed", "Number of events in each path",
      paths_.size() + 2,  // each + total + any
      -0.5, paths_.size() + 2 - 0.5);
  // Set bin labels
  passedBits_->GetXaxis()->SetBinLabel(1, "total");
  passedBits_->GetXaxis()->SetBinLabel(2, "any");
  for (size_t i = 0; i < paths_.size(); ++i) {
    passedBits_->GetXaxis()->SetBinLabel(3+i, paths_[i].c_str());
  }
  passedBits_->SetStats(false);

  exclusiveBits_ = fs->make<TH1F>(
      "pathExlcusivePass", "Number of exclusive events in each path",
      paths_.size() + 2,  // each + total
      -0.5, paths_.size() + 2 - 0.5);
  // Set bin labels
  exclusiveBits_->GetXaxis()->SetBinLabel(1, "total");
  exclusiveBits_->GetXaxis()->SetBinLabel(2, "one path only");
  for (size_t i = 0; i < paths_.size(); ++i) {
    exclusiveBits_->GetXaxis()->SetBinLabel(3+i, paths_[i].c_str());
  }
  exclusiveBits_->SetStats(false);

  correlation_ = fs->make<TH2F>(
      "pathCorrelation", "Correlation between paths",
      paths_.size(),  -0.5, paths_.size() - 0.5,
      paths_.size(),  -0.5, paths_.size() - 0.5);
  for (size_t i = 0; i < paths_.size(); ++i) {
    correlation_->GetXaxis()->SetBinLabel(i+1, paths_[i].c_str());
    correlation_->GetYaxis()->SetBinLabel(i+1, paths_[i].c_str());
  }
  correlation_->SetDrawOption("colz");
  correlation_->SetStats(false);
}

void SkimEfficiencyAnalyzer::analyze(const edm::Event& evt, const edm::EventSetup& es) {
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

void SkimEfficiencyAnalyzer::endJob() {
  // Normalize the correlation plot by rows
  // Reading a row: each entry is what fraciton of events passing that trigger
  // passed the trigger in the column.
  for(size_t i = 0; i < paths_.size(); ++i) {
    double total_counts = correlation_->GetBinContent(i+1, i+1);
    for (size_t j = 0; j < paths_.size(); ++j) {
      double current = correlation_->GetBinContent(j+1, i+1);
      correlation_->SetBinContent(j+1, i+1, current/total_counts);
    }
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SkimEfficiencyAnalyzer);
