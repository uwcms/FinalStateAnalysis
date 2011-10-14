#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"

template<typename T1, typename T2>
class PATDiCandidateSystematicsProducer : public edm::EDProducer {
public:
  typedef PATDiCandidateSystematics<T1, T2> DiCand;
  typedef std::vector<DiCand> DiCandCollection;

  PATDiCandidateSystematicsProducer (const edm::ParameterSet& pset);
  virtual ~PATDiCandidateSystematicsProducer(){};
  void produce(edm::Event& evt, const edm::EventSetup& es);
private:
    edm::InputTag srcLeg1_;
    edm::InputTag srcLeg2_;
    edm::InputTag srcMET_;
    edm::InputTag srcVtx_;
};

template<typename T1, typename T2>
PATDiCandidateSystematicsProducer<T1,T2>::PATDiCandidateSystematicsProducer(
    const edm::ParameterSet& pset) {
  srcLeg1_ = pset.getParameter<edm::InputTag>("srcLeg1");
  srcLeg2_ = pset.getParameter<edm::InputTag>("srcLeg2");
  srcVtx_ = pset.getParameter<edm::InputTag>("srcVtx");
  srcMET_ = pset.getParameter<edm::InputTag>("srcMET");
  produces<DiCandCollection>();
}

template<typename T1, typename T2>
void PATDiCandidateSystematicsProducer<T1,T2>::produce(edm::Event& evt,
    const edm::EventSetup& es) {

  edm::Handle<edm::View<T1> > leg1s;
  evt.getByLabel(srcLeg1_, leg1s);

  edm::Handle<edm::View<T2> > leg2s;
  evt.getByLabel(srcLeg2_, leg2s);

  edm::Handle<edm::View<pat::MET> > mets;
  evt.getByLabel(srcMET_, mets);
  edm::Ptr<pat::MET> met = mets->ptrAt(0);
  assert(met.isNonnull());

  edm::Handle<edm::View<reco::Vertex> > vertices;
  evt.getByLabel(srcVtx_, vertices);
  edm::Ptr<reco::Vertex> vtx = vertices->ptrAt(0);
  assert(vtx.isNonnull());
  // fixme

  std::auto_ptr<DiCandCollection> output(new DiCandCollection);
  output->reserve(leg1s->size()*leg2s->size());

  for (size_t iLeg1 = 0; iLeg1 < leg1s->size(); ++iLeg1) {
    edm::Ptr<T1> leg1 = leg1s->ptrAt(iLeg1);
    assert(leg1.isNonnull());
    for (size_t iLeg2 = 0; iLeg2 < leg2s->size(); ++iLeg2) {
      edm::Ptr<T2> leg2 = leg2s->ptrAt(iLeg2);
      assert(leg2.isNonnull());
      DiCand outputCand(leg1, leg2, met, vtx);
      output->push_back(outputCand);
    }
  }

  evt.put(output);
}

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
typedef PATDiCandidateSystematicsProducer<pat::Muon, pat::Tau> PATMuTauSystematicsProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuTauSystematicsProducer);
