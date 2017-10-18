/*
 * Module which embeds the closest pat::Jet into another PATObject as a userCand
 *
 * Author: Evan K. Friis, UW Madison
 */
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

#include "DataFormats/Math/interface/deltaR.h"

// Helper functions to extract the 4 vector information from the object
namespace {
  // Taus we can get the value straight from the jet
  reco::Candidate::LorentzVector extractObjectP4(const pat::Tau& tau) {
    //return tau.pfEssential().p4Jet_;
    return tau.p4();
  }

  reco::Candidate::LorentzVector extractObjectP4(const pat::Muon& mu) {
    return mu.p4();
  }

  reco::Candidate::LorentzVector extractObjectP4(const pat::Electron& e) {
    return e.p4();
  }

  reco::Candidate::LorentzVector extractObjectP4(const pat::Photon& pho) {
    return pho.p4();
  }
}

template<class T>
class MiniAODObjectJetInfoEmbedder : public edm::EDProducer {
  public:
    typedef std::vector<T> TCollection;
    MiniAODObjectJetInfoEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODObjectJetInfoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<T> > srcToken_;
    edm::EDGetTokenT<edm::View<pat::Jet> > jetSrcToken_;
    double maxDeltaR_;
    bool embedBtags_;
    std::string suffix_;
};

template<class T>
MiniAODObjectJetInfoEmbedder<T>::MiniAODObjectJetInfoEmbedder(
    const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<T> >(pset.getParameter<edm::InputTag>("src"));
  jetSrcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("jetSrc"));
  suffix_ = pset.getParameter<std::string>("suffix");
  embedBtags_ = pset.getParameter<bool>("embedBtags");
  maxDeltaR_ = pset.getParameter<double>("maxDeltaR");
  produces<TCollection>();
}

template<class T>
void MiniAODObjectJetInfoEmbedder<T>::produce(
    edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<TCollection> output(new TCollection);

  edm::Handle<edm::View<T> > objects;
  evt.getByToken(srcToken_, objects);
  output->reserve(objects->size());

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByToken(jetSrcToken_, jets);

//  edm::Handle<edm::View<reco::Jet> > recoJets;
//  evt.getByToken("ak5PFJets", recoJets);
//
//  edm::Handle<edm::View<reco::PFCandidate> > pfCands;
//  evt.getByToken("particleFlow", pfCands);
//
  typedef edm::Ptr<pat::Jet> JetPtr;

  for (size_t i = 0; i < objects->size(); ++i) {
    // Make a copy that we own
    T object = objects->at(i);
    reco::Candidate::LorentzVector objectP4 = extractObjectP4(object);
    // Find the closest jet
    JetPtr closestJet;
    double closestDeltaR = std::numeric_limits<double>::infinity();
    for (size_t j = 0; j < jets->size(); ++j) {
      JetPtr jet = jets->ptrAt(j);
      reco::Candidate::LorentzVector jetP4 = jet->correctedP4(0);
      double deltaR = reco::deltaR(objectP4, jetP4);
      if (deltaR < closestDeltaR) {
        closestDeltaR = deltaR;
        closestJet = jet;
      }
    }
    if (closestDeltaR > maxDeltaR_) {
      // Null jet
      object.addUserCand("patJet" + suffix_, reco::CandidatePtr());
      // The jet pt is just the object pt
      object.addUserFloat("jetPt", objectP4.pt());
    } else {
      // Null jet
      object.addUserCand("patJet" + suffix_, closestJet);
      // The jet pt is just the object pt
      object.addUserFloat("jetPt", closestJet->pt());
    }
    object.addUserFloat("jetDR", closestDeltaR);

    if (embedBtags_ && closestJet.isNonnull()) {
      typedef std::pair<std::string, float> IdPair;
      typedef std::vector<IdPair> IdPairs;
      const IdPairs& bTags = closestJet->getPairDiscri();
      for (size_t iTag = 0; iTag < bTags.size(); ++iTag) {
        std::string name = "btag_" + suffix_ + bTags[iTag].first;
        object.addUserFloat(name, bTags[iTag].second);
      }
    }
    output->push_back(object);
  }
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
typedef MiniAODObjectJetInfoEmbedder<pat::Tau> MiniAODTauJetInfoEmbedder;
typedef MiniAODObjectJetInfoEmbedder<pat::Muon> MiniAODMuonJetInfoEmbedder;
typedef MiniAODObjectJetInfoEmbedder<pat::Electron> MiniAODElectronJetInfoEmbedder;
typedef MiniAODObjectJetInfoEmbedder<pat::Photon> MiniAODPhotonJetInfoEmbedder;
DEFINE_FWK_MODULE(MiniAODTauJetInfoEmbedder);
DEFINE_FWK_MODULE(MiniAODMuonJetInfoEmbedder);
DEFINE_FWK_MODULE(MiniAODElectronJetInfoEmbedder);
DEFINE_FWK_MODULE(MiniAODPhotonJetInfoEmbedder);
