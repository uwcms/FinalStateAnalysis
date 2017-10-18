#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"


namespace {
  reco::TransientTrack getTracks(
      const reco::Candidate* cand, const TransientTrackBuilder* builder) {
    const pat::Muon* muon = dynamic_cast<const pat::Muon*>(cand);
    const pat::Electron* electron = dynamic_cast<const pat::Electron*>(cand);
    const pat::Tau* tau = dynamic_cast<const pat::Tau*>(cand);
    if (muon) {
      if (muon->innerTrack().isNonnull())
        return (builder->build(muon->innerTrack()));
    } else if (electron) {
      if (electron->gsfTrack().isNonnull())
        return (builder->build(electron->gsfTrack()));
    } else if (tau && tau->signalPFChargedHadrCands().size()) {
      if (tau->signalPFChargedHadrCands()[0]->trackRef().isNonnull())
        return (builder->build(
              tau->signalPFChargedHadrCands()[0]->trackRef()));
      else
        if (tau->signalPFChargedHadrCands()[0]->gsfTrackRef().isNonnull())
          return (builder->build(
                tau->signalPFChargedHadrCands()[0]->gsfTrackRef()));
    }
    return reco::TransientTrack();
  }
}

class PATFinalStateVertexFitter : public edm::EDProducer {
  public:
    PATFinalStateVertexFitter(const edm::ParameterSet& pset);
    virtual ~PATFinalStateVertexFitter(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<PATFinalState> > srcToken_;
    bool enable_;
};

PATFinalStateVertexFitter::PATFinalStateVertexFitter(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<PATFinalState> >(pset.getParameter<edm::InputTag>("src"));
  enable_ = pset.getParameter<bool>("enable");
  produces<PATFinalStateCollection>();
}
void PATFinalStateVertexFitter::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStates;
  evt.getByToken(srcToken_, finalStates);

  edm::ESHandle<TransientTrackBuilder> trackBuilderHandle;
  if (enable_) {
    es.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilderHandle);
  }

  for (size_t i = 0; i < finalStates->size(); ++i) {
    PATFinalState * clone = finalStates->at(i).clone();
    assert(clone);
    if (enable_) {
      std::vector<reco::TransientTrack> tracks;
      for (size_t d = 0; d < clone->numberOfDaughters(); ++d) {
	reco::TransientTrack transtrack = getTracks(clone->daughter(d),
	      trackBuilderHandle.product());
	if (transtrack.isValid())
	  tracks.push_back(transtrack);
      }
      double vtxChi2 = -1;
      double vtxNDOF = -1;
      // Make sure all legs have a track
      if (tracks.size() >= clone->numberOfDaughters()) {
	KalmanVertexFitter kvf(true);
	TransientVertex vtx = kvf.vertex(tracks);
	vtxChi2 = vtx.totalChiSquared();
	vtxNDOF = vtx.degreesOfFreedom();
      }
      clone->addUserFloat("vtxChi2", vtxChi2);
      clone->addUserFloat("vtxNDOF", vtxNDOF);
    }
    output->push_back(clone);
  }
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateVertexFitter);
