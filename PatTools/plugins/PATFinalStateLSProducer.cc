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
        ls.id(), intgRecLumi, instLumi));

  ls.put(output);

  eventCount_ = 0;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateLSProducer);
