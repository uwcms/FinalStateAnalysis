/*
 * Produce the PATFinalStateLS objects that wrap the LumiSummary
 *
 * Author: Evan K. Friis UW Madison
 *
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

class PATFinalStateLSProducer : public edm::EDProducer {
  public:
    PATFinalStateLSProducer(const edm::ParameterSet& pset);
    virtual ~PATFinalStateLSProducer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
    void endLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup& es);
  private:
    const edm::InputTag trigSrc_;
    // For MC
    // The process xsec
    const double xSec_;
    unsigned int eventCount_;

    // The LumiSummary source for data
    const edm::InputTag src_;

    // Store a copy of the trigger event from one of the events
    bool needTriggerEvent_;
    std::vector<LumiSummary::HLT> hltInfos_;
    std::vector<LumiSummary::L1> l1Infos_;
};

PATFinalStateLSProducer::PATFinalStateLSProducer(
    const edm::ParameterSet& pset):
  trigSrc_(pset.getParameter<edm::InputTag>("trigSrc")),
  xSec_(pset.getParameter<double>("xSec")),
  eventCount_(0),
  src_(pset.getParameter<edm::InputTag>("lumiSrc")) {
    produces<PATFinalStateLS, edm::InLumi>();
}

void
PATFinalStateLSProducer::produce(edm::Event& evt, const edm::EventSetup& es) {
  eventCount_ += 1;
  if (needTriggerEvent_) {
    edm::Handle<pat::TriggerEvent> trigEv;
    evt.getByLabel(trigSrc_,trigEv);
    const pat::TriggerPathCollection * paths = trigEv->paths();
    hltInfos_.clear();
    assert(paths);
    for (size_t i = 0; i < paths->size(); ++i) {
      const std::string& pathName = paths->at(i).name();
      int prescale = paths->at(i).prescale();
      int ratecount = -1;
      int inputcount = -1;
      LumiSummary::HLT hltInfo;
      hltInfo.pathname = pathName;
      hltInfo.prescale = prescale;
      hltInfo.ratecount = ratecount;
      hltInfo.inputcount = inputcount;
      hltInfos_.push_back(hltInfo);
    }

    const pat::TriggerAlgorithmCollection* triggers = trigEv->algorithms();
    l1Infos_.clear();
    assert(triggers);
    for (size_t i = 0; i < triggers->size(); ++i) {
      const std::string& triggerName = triggers->at(i).name();
      int prescale = triggers->at(i).prescale();
      int ratecount = 999;
      LumiSummary::L1 l1Info;
      l1Info.triggername = triggerName;
      l1Info.prescale = prescale;
      l1Info.ratecount = ratecount;
      l1Infos_.push_back(l1Info);
    }
    needTriggerEvent_ = false;
  }
}

void PATFinalStateLSProducer::endLuminosityBlock(
    edm::LuminosityBlock& ls, const edm::EventSetup& es) {

  double intgRecLumi = -999;
  double instLumi = -999;

  edm::Handle<LumiSummary> summary;
  ls.getByLabel(src_, summary);

  if (summary.isValid()) { // Data
    // Factor of ten comes from bug in LumiSummary.cc
    // (see https://hypernews.cern.ch/HyperNews/CMS/get/swDevelopment/2617/2/1/1/1/1.html)
    intgRecLumi = summary->intgRecLumi()/10.0;
    instLumi = summary->avgInsDelLumi();
  } else {
    // Compute the effective luminosity
    double intgRecLumi = eventCount_ / xSec_;
    // Convert to inverse microbarns
    intgRecLumi *= 1e6;
  }

  std::auto_ptr<PATFinalStateLS> output(new PATFinalStateLS(
        ls.id(), intgRecLumi, instLumi, hltInfos_, l1Infos_));

  ls.put(output);

  eventCount_ = 0;
  // We need to update the trigger information after each LS
  needTriggerEvent_ = true;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateLSProducer);
