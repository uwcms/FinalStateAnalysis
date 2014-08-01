#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventMini.h"
#include "FinalStateAnalysis/DataFormats/interface/PATQuadFinalStateT.h"

template<class FinalState>
class PATQuadFinalStateBuilderT : public edm::EDProducer {
  public:
    typedef std::vector<FinalState> FinalStateCollection;

    PATQuadFinalStateBuilderT(const edm::ParameterSet& pset);
    virtual ~PATQuadFinalStateBuilderT(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag leg1Src_;
    edm::InputTag leg2Src_;
    edm::InputTag leg3Src_;
    edm::InputTag leg4Src_;
    edm::InputTag evtSrc_;
    StringCutObjectSelector<PATFinalState> cut_;
};

template<class FinalState>
PATQuadFinalStateBuilderT<FinalState>::PATQuadFinalStateBuilderT(
    const edm::ParameterSet& pset):
  cut_(pset.getParameter<std::string>("cut"), true) {
  leg1Src_ = pset.getParameter<edm::InputTag>("leg1Src");
  leg2Src_ = pset.getParameter<edm::InputTag>("leg2Src");
  leg3Src_ = pset.getParameter<edm::InputTag>("leg3Src");
  leg4Src_ = pset.getParameter<edm::InputTag>("leg4Src");
  evtSrc_ = pset.getParameter<edm::InputTag>("evtSrc");
  produces<FinalStateCollection>();
}

template<class FinalState> void
PATQuadFinalStateBuilderT<FinalState>::produce(
    edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<PATFinalStateEventMini> > fsEvent;
  evt.getByLabel(evtSrc_, fsEvent);
  edm::Ptr<PATFinalStateEventMini> evtPtr = fsEvent->ptrAt(0);
  assert(evtPtr.isNonnull());

  std::auto_ptr<FinalStateCollection> output(new FinalStateCollection);

  edm::Handle<edm::View<typename FinalState::daughter1_type> > leg1s;
  evt.getByLabel(leg1Src_, leg1s);

  edm::Handle<edm::View<typename FinalState::daughter2_type> > leg2s;
  evt.getByLabel(leg2Src_, leg2s);

  edm::Handle<edm::View<typename FinalState::daughter3_type> > leg3s;
  evt.getByLabel(leg3Src_, leg3s);

  edm::Handle<edm::View<typename FinalState::daughter4_type> > leg4s;
  evt.getByLabel(leg4Src_, leg4s);

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

        for (size_t iLeg4 = 0; iLeg4 < leg4s->size(); ++iLeg4) {
          edm::Ptr<typename FinalState::daughter4_type> leg4 = leg4s->ptrAt(iLeg4);
          assert(leg4.isNonnull());

          // Skip if the two objects are the same thing.
          if (reco::CandidatePtr(leg1) == reco::CandidatePtr(leg4))
            continue;
          if (reco::CandidatePtr(leg2) == reco::CandidatePtr(leg4))
            continue;
          if (reco::CandidatePtr(leg3) == reco::CandidatePtr(leg4))
            continue;

          FinalState outputCand(leg1, leg2, leg3, leg4, evtPtr);
          if (cut_(outputCand))
            output->push_back(outputCand);
        }
      }
    }
  }
  evt.put(output);
}
