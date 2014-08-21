#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATSingleFinalStateT.h"

template<class FinalStateSingle>
class PATSingleFinalStateBuilderT : public edm::EDProducer {
  public:
    typedef std::vector<FinalStateSingle> FinalStateSingleCollection;

    PATSingleFinalStateBuilderT(const edm::ParameterSet& pset);
    virtual ~PATSingleFinalStateBuilderT(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag leg1Src_;
    edm::InputTag evtSrc_;
    StringCutObjectSelector<PATFinalState> cut_;
};

template<class FinalStateSingle>
PATSingleFinalStateBuilderT<FinalStateSingle>::PATSingleFinalStateBuilderT(
    const edm::ParameterSet& pset):
  cut_(pset.getParameter<std::string>("cut"), true) {
  leg1Src_ = pset.getParameter<edm::InputTag>("leg1Src");
  evtSrc_ = pset.getParameter<edm::InputTag>("evtSrc");
  produces<FinalStateSingleCollection>();
}

template<class FinalStateSingle> void
PATSingleFinalStateBuilderT<FinalStateSingle>::produce(
    edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<PATFinalStateEvent> > fsEvent;
  evt.getByLabel(evtSrc_, fsEvent);
  edm::Ptr<PATFinalStateEvent> evtPtr = fsEvent->ptrAt(0);
  assert(evtPtr.isNonnull());

  std::auto_ptr<FinalStateSingleCollection> output(new FinalStateSingleCollection);

  edm::Handle<edm::View<typename FinalStateSingle::daughter1_type> > leg1s;
  evt.getByLabel(leg1Src_, leg1s);

  for (size_t iLeg1 = 0; iLeg1 < leg1s->size(); ++iLeg1) {
    edm::Ptr<typename FinalStateSingle::daughter1_type> leg1 = leg1s->ptrAt(iLeg1);
    assert(leg1.isNonnull());
    FinalStateSingle outputCand(leg1, evtPtr);
    if (cut_(outputCand))
      output->push_back(outputCand);
    }
  evt.put(output);
}
