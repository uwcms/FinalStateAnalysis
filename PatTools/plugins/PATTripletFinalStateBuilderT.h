#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATTripletFinalStateT.h"

template<class FinalState>
class PATTripletFinalStateBuilderT : public edm::stream::EDProducer<> {
  public:
    typedef std::vector<FinalState> FinalStateCollection;

    PATTripletFinalStateBuilderT(const edm::ParameterSet& pset);
    virtual ~PATTripletFinalStateBuilderT(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    const StringCutObjectSelector<PATFinalState> cut_;
    const edm::EDGetTokenT<edm::View<typename FinalState::daughter1_type> > leg1Src_;
    const edm::EDGetTokenT<edm::View<typename FinalState::daughter2_type> > leg2Src_;
    const edm::EDGetTokenT<edm::View<typename FinalState::daughter3_type> > leg3Src_;
    const edm::EDGetTokenT<edm::View<PATFinalStateEvent> > evtSrc_;
};

template<class FinalState>
PATTripletFinalStateBuilderT<FinalState>::PATTripletFinalStateBuilderT(
    const edm::ParameterSet& pset):
  cut_(pset.getParameter<std::string>("cut"), true),
  leg1Src_(consumes<edm::View<typename FinalState::daughter1_type> >(pset.getParameter<edm::InputTag>("leg1Src"))),
  leg2Src_(consumes<edm::View<typename FinalState::daughter2_type> >(pset.getParameter<edm::InputTag>("leg2Src"))),
  leg3Src_(consumes<edm::View<typename FinalState::daughter3_type> >(pset.getParameter<edm::InputTag>("leg3Src"))),
  evtSrc_(consumes<edm::View<PATFinalStateEvent> >(pset.getParameter<edm::InputTag>("evtSrc")))
{
  produces<FinalStateCollection>();
}

template<class FinalState> void
PATTripletFinalStateBuilderT<FinalState>::produce(
    edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<PATFinalStateEvent> > fsEvent;
  evt.getByToken(evtSrc_, fsEvent);
  edm::Ptr<PATFinalStateEvent> evtPtr = fsEvent->ptrAt(0);
  assert(evtPtr.isNonnull());

  std::auto_ptr<FinalStateCollection> output(new FinalStateCollection);

  edm::Handle<edm::View<typename FinalState::daughter1_type> > leg1s;
  evt.getByToken(leg1Src_, leg1s);

  edm::Handle<edm::View<typename FinalState::daughter2_type> > leg2s;
  evt.getByToken(leg2Src_, leg2s);

  edm::Handle<edm::View<typename FinalState::daughter3_type> > leg3s;
  evt.getByToken(leg3Src_, leg3s);

  for (size_t iLeg1 = 0; iLeg1 < leg1s->size(); ++iLeg1) {
    edm::Ptr<typename FinalState::daughter1_type> leg1 = leg1s->ptrAt(iLeg1);
    assert(leg1.isNonnull());

    for (size_t iLeg2 = 0; iLeg2 < leg2s->size(); ++iLeg2) {
      edm::Ptr<typename FinalState::daughter2_type> leg2 = leg2s->ptrAt(iLeg2);
      assert(leg2.isNonnull());

      // Skip if the two objects are the same thing.
      if (reco::CandidatePtr(leg1) == reco::CandidatePtr(leg2))
        continue;

      for (size_t iLeg3 = 0; iLeg3 < leg3s->size(); ++iLeg3) {
        edm::Ptr<typename FinalState::daughter3_type> leg3 = leg3s->ptrAt(iLeg3);
        assert(leg3.isNonnull());

        // Skip if the two objects are the same thing.
        if (reco::CandidatePtr(leg1) == reco::CandidatePtr(leg3))
          continue;
        if (reco::CandidatePtr(leg2) == reco::CandidatePtr(leg3))
          continue;

        FinalState outputCand(leg1, leg2, leg3, evtPtr);
        if (cut_(outputCand))
          output->push_back(outputCand);
      }
    }
  }
  evt.put(output);
}
