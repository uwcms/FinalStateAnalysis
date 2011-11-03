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

#include "DataFormats/Math/interface/deltaR.h"

// Helper functions to extract the 4 vector information from the object
namespace {
  // Taus we can get the value straight from the jet
  reco::Candidate::LorentzVector extractObjectP4(const pat::Tau& tau) {
    return tau.pfJetRef()->p4();
  }

  reco::Candidate::LorentzVector extractObjectP4(const pat::Muon& mu) {
    return mu.p4();
  }

  reco::Candidate::LorentzVector extractObjectP4(const pat::Electron& e) {
    return e.p4();
  }
}

template<class T>
class PATObjectJetInfoEmbedder : public edm::EDProducer {
  public:
    typedef std::vector<T> TCollection;
    PATObjectJetInfoEmbedder(const edm::ParameterSet& pset);
    virtual ~PATObjectJetInfoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag jetSrc_;
    double maxDeltaR_;
    bool embedBtags_;
    std::string suffix_;
};

template<class T>
PATObjectJetInfoEmbedder<T>::PATObjectJetInfoEmbedder(
    const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  jetSrc_ = pset.getParameter<edm::InputTag>("jetSrc");
  suffix_ = pset.getParameter<std::string>("suffix");
  embedBtags_ = pset.getParameter<bool>("embedBtags");
  maxDeltaR_ = pset.getParameter<double>("maxDeltaR");
  produces<TCollection>();
}

template<class T>
void PATObjectJetInfoEmbedder<T>::produce(
    edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<TCollection> output(new TCollection);

  edm::Handle<edm::View<T> > objects;
  evt.getByLabel(src_, objects);
  output->reserve(objects->size());

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByLabel(jetSrc_, jets);

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
      // Use the uncorrected P4. Embedded in the UncorrectedEmbedder module.
      assert(jet->userCand("uncorr").isNonnull());
      reco::Candidate::LorentzVector jetP4 = jet->userCand("uncorr")->p4();
      double deltaR = reco::deltaR(objectP4, jetP4);
      if (deltaR < closestDeltaR) {
        closestDeltaR = deltaR;
        closestJet = jet;
      }
    }
    assert(closestJet.isNonnull());
    if (closestDeltaR > maxDeltaR_) {
      edm::LogWarning("BadJetMatch") << "Couldn't find a jet close to the"
        << " object in PATObjectJetInfoEmbedder. "
        << "The object jetref has (pt/eta/phi): ("
        << objectP4.pt() << "/" << objectP4.eta() << "/" << objectP4.phi()
        << ") and the closest jet is at "
        << closestJet->pt() << "/" << closestJet->eta()
        << "/" << closestJet->phi()
        << ") giving a deltaR of " << closestDeltaR << std::endl;
    }
    object.addUserCand("patJet" + suffix_, closestJet);
    if (embedBtags_) {
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
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
typedef PATObjectJetInfoEmbedder<pat::Tau> PATTauJetInfoEmbedder;
typedef PATObjectJetInfoEmbedder<pat::Muon> PATMuonJetInfoEmbedder;
typedef PATObjectJetInfoEmbedder<pat::Electron> PATElectronJetInfoEmbedder;
DEFINE_FWK_MODULE(PATTauJetInfoEmbedder);
DEFINE_FWK_MODULE(PATMuonJetInfoEmbedder);
DEFINE_FWK_MODULE(PATElectronJetInfoEmbedder);
