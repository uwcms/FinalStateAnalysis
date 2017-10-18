/*
 * Embed float into a PAT final state.  The float is taken from a double in the
 * event.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include <string>
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class PATFinalStateFloatEmbedder : public edm::EDProducer {
  public:
    PATFinalStateFloatEmbedder(const edm::ParameterSet& pset);
    virtual ~PATFinalStateFloatEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag toEmbedSrc_;
    std::string name_;
};

PATFinalStateFloatEmbedder::PATFinalStateFloatEmbedder(
    const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  toEmbedSrc_ = pset.getParameter<edm::InputTag>("toEmbedSrc");
  name_ = pset.getParameter<std::string>("name");
  produces<PATFinalStateCollection>();
}
void PATFinalStateFloatEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesH;
  evt.getByLabel(src_, finalStatesH);

  edm::Handle<double> toEmbedH;
  evt.getByLabel(toEmbedSrc_, toEmbedH);

  for (size_t i = 0; i < finalStatesH->size(); ++i) {
    PATFinalState* embedInto = finalStatesH->ptrAt(i)->clone();
    embedInto->addUserFloat(name_, *toEmbedH);
    output->push_back(embedInto); // takes ownership
  }
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateFloatEmbedder);
