#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATPairFinalStateT.h"

template<class FinalStatePair>
class PATPairFinalStateBuilderT : public edm::EDProducer {
  public:
    typedef std::vector<FinalStatePair> FinalStatePairCollection;

    PATPairFinalStateBuilderT(const edm::ParameterSet& pset);
    virtual ~PATPairFinalStateBuilderT(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<typename FinalStatePair::daughter1_type> > leg1SrcToken_;
    edm::EDGetTokenT<edm::View<typename FinalStatePair::daughter2_type> > leg2SrcToken_;
    edm::EDGetTokenT<edm::View<PATFinalStateEvent> > evtSrcToken_;
    StringCutObjectSelector<PATFinalState> cut_;
};

template<class FinalStatePair>
PATPairFinalStateBuilderT<FinalStatePair>::PATPairFinalStateBuilderT(
    const edm::ParameterSet& pset):
  cut_(pset.getParameter<std::string>("cut"), true) {
  leg1SrcToken_ = consumes<edm::View<typename FinalStatePair::daughter1_type> >(pset.getParameter<edm::InputTag>("leg1Src"));
  leg2SrcToken_ = consumes<edm::View<typename FinalStatePair::daughter2_type> >(pset.getParameter<edm::InputTag>("leg2Src"));
  evtSrcToken_  = consumes<edm::View<PATFinalStateEvent> >(pset.getParameter<edm::InputTag>("evtSrc"));
  produces<FinalStatePairCollection>();
}

template<class FinalStatePair> void
PATPairFinalStateBuilderT<FinalStatePair>::produce(
    edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<PATFinalStateEvent> > fsEvent;
  evt.getByToken(evtSrcToken_, fsEvent);
  edm::Ptr<PATFinalStateEvent> evtPtr = fsEvent->ptrAt(0);
  assert(evtPtr.isNonnull());

  std::auto_ptr<FinalStatePairCollection> output(new FinalStatePairCollection);

  edm::Handle<edm::View<typename FinalStatePair::daughter1_type> > leg1s;
  evt.getByToken(leg1SrcToken_, leg1s);

  edm::Handle<edm::View<typename FinalStatePair::daughter2_type> > leg2s;
  evt.getByToken(leg2SrcToken_, leg2s);

  for (size_t iLeg1 = 0; iLeg1 < leg1s->size(); ++iLeg1) {
    edm::Ptr<typename FinalStatePair::daughter1_type> leg1 = leg1s->ptrAt(iLeg1);
    assert(leg1.isNonnull());
    for (size_t iLeg2 = 0; iLeg2 < leg2s->size(); ++iLeg2) {
      edm::Ptr<typename FinalStatePair::daughter2_type> leg2 = leg2s->ptrAt(iLeg2);
      assert(leg2.isNonnull());

      // Skip if the two objects are the same thing.
      if (reco::CandidatePtr(leg1) == reco::CandidatePtr(leg2))
        continue;

      FinalStatePair outputCand(leg1, leg2, evtPtr);
      if (cut_(outputCand))
        output->push_back(outputCand);
    }
  }
  evt.put(output);
}
