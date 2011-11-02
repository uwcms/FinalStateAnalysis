#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "DataFormats/Math/interface/deltaR.h"

class PATTauJetInfoEmbedder : public edm::EDProducer {
  public:
    PATTauJetInfoEmbedder(const edm::ParameterSet& pset);
    virtual ~PATTauJetInfoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag jetSrc_;
    bool embedBtags_;
    std::string suffix_;
};

PATTauJetInfoEmbedder::PATTauJetInfoEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  jetSrc_ = pset.getParameter<edm::InputTag>("jetSrc");
  suffix_ = pset.getParameter<std::string>("suffix");
  /*code*/
  embedBtags_ = pset.getParameter<bool>("embedBtags");
  /*code*/
  produces<pat::TauCollection>();
}

void PATTauJetInfoEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);

  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByLabel(src_, taus);
  output->reserve(taus->size());

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByLabel(jetSrc_, jets);

  assert(jets->size() == taus->size());

  typedef edm::Ptr<pat::Jet> JetPtr;

  for (size_t i = 0; i < taus->size(); ++i) {
    // Make a copy that we own
    pat::Tau tau = taus->at(i);
    const reco::Candidate::LorentzVector& tauP4 = tau.pfJetRef()->p4();
    // Find the closest jet
    JetPtr closestJet;
    double closestDeltaR = std::numeric_limits<double>::infinity();
    for (size_t j = 0; j < jets->size(); ++j) {
      JetPtr jet = jets->ptrAt(j);
      // Use the uncorrected P4. Embedded in the UncorrectedEmbedder module.
      assert(jet->userCand("uncorr").isNonnull());
      reco::Candidate::LorentzVector jetP4 = jet->userCand("uncorr")->p4();
      double deltaR = reco::deltaR(tauP4, jetP4);
      if (deltaR < closestDeltaR) {
        closestDeltaR = deltaR;
        closestJet = jet;
      }
    }
    assert(closestJet.isNonnull());
    if (closestDeltaR > 0.1) {
      std::cout << closestJet->currentJECLevel() << " " << closestJet->currentJECSet() << std::endl;
      throw cms::Exception("BadJetMatch") << "Couldn't find a jet close to the"
        << " tau in PATTauJetInfoEmbedder. The tau jetref has (pt/eta/phi): ("
        << tauP4.pt() << "/" << tauP4.eta() << "/" << tauP4.phi()
        << ") and the closest jet is at "
        << closestJet->pt() << "/" << closestJet->eta() << "/" << closestJet->phi()
        << ") giving a deltaR of " << closestDeltaR << std::endl;
    }
    assert(closestDeltaR < 0.25);
    tau.addUserCand("patJet" + suffix_, closestJet);
    if (embedBtags_) {
      typedef std::pair<std::string, float> IdPair;
      typedef std::vector<IdPair> IdPairs;
      const IdPairs& bTags = closestJet->getPairDiscri();
      for (size_t iTag = 0; iTag < bTags.size(); ++iTag) {
        std::string name = "btag_" + suffix_ + bTags[iTag].first;
        tau.addUserFloat(name, bTags[iTag].second);
      }
    }
    output->push_back(tau);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauJetInfoEmbedder);
