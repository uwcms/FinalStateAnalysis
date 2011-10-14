/*
 * Embed the index (i.e. how many final states are in an event) into a
 * PATFinalState.
 *
 * Embeds a userInt with: idx[_suffix]
 *
 * Author: Evan K. Friis, UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"

class PATFinalStateIdxEmbedder : public edm::EDProducer {
  public:
    PATFinalStateIdxEmbedder(const edm::ParameterSet& pset);
    virtual ~PATFinalStateIdxEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag toEmbedSrc_;
    const std::string suffix_;
};

PATFinalStateIdxEmbedder::PATFinalStateIdxEmbedder(
    const edm::ParameterSet& pset):
  suffix_(pset.getParameter<std::string>("suffix")) {
  src_ = pset.getParameter<edm::InputTag>("src");
  produces<PATFinalStateCollection>();
}

void PATFinalStateIdxEmbedder::produce(
    edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesH;
  evt.getByLabel(src_, finalStatesH);

  for (size_t i = 0; i < finalStatesH->size(); ++i) {
    PATFinalState* embedInto = finalStatesH->ptrAt(i)->clone();
    embedInto->addUserInt("idx" + suffix_, i);
    output->push_back(embedInto); // takes ownership
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateIdxEmbedder);
