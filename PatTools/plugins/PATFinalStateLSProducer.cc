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

class PATFinalStateLSProducer : public edm::EDProducer {
  public:
    PATFinalStateLSProducer(const edm::ParameterSet& pset);
    virtual ~PATFinalStateLSProducer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
    void endLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
};

PATFinalStateLSProducer::PATFinalStateLSProducer(
    const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  produces<PATFinalStateLS, edm::InLumi>();
}

// Nothing to do.
void
PATFinalStateLSProducer::produce(edm::Event& evt, const edm::EventSetup& es) { }

void PATFinalStateLSProducer::endLuminosityBlock(
    edm::LuminosityBlock& ls, const edm::EventSetup& es) {
  edm::Handle<LumiSummary> summary;
  ls.getByLabel(src_, summary);

  std::auto_ptr<PATFinalStateLS> output(
      new PATFinalStateLS(ls.id(), *summary));
  ls.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateLSProducer);
