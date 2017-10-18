/*
 * A workaround that just copies PaTFinalStates into a new collection.
 *
 * For process naming purposes.
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

class PATFinalStateCopier : public edm::EDProducer {
  public:
    PATFinalStateCopier(const edm::ParameterSet& pset);
    virtual ~PATFinalStateCopier(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<PATFinalState> > srcToken_;
    std::string name_;
};

PATFinalStateCopier::PATFinalStateCopier(
    const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<PATFinalState> >(pset.getParameter<edm::InputTag>("src"));
  produces<PATFinalStateCollection>();
}
void PATFinalStateCopier::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesH;
  evt.getByToken(srcToken_, finalStatesH);

  for (size_t i = 0; i < finalStatesH->size(); ++i) {
    PATFinalState* embedInto = finalStatesH->ptrAt(i)->clone();
    output->push_back(embedInto); // takes ownership
  }
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateCopier);
