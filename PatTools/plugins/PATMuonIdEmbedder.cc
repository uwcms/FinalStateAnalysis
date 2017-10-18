/*
 * Embed a WW analysis style muon ID into a pat::Muon userInt.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATMuonIdSelector.h"
#include <algorithm>

class PATMuonIdEmbedder : public edm::EDProducer {
  public:
    PATMuonIdEmbedder(const edm::ParameterSet& pset);
    virtual ~PATMuonIdEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    std::string userIntLabel_;
    PATMuonIdSelectorImp selector_;
};

PATMuonIdEmbedder::PATMuonIdEmbedder(const edm::ParameterSet& pset)
  :selector_(pset, consumesCollector()) {
  src_ = pset.getParameter<edm::InputTag>("src");
  userIntLabel_ = pset.getParameter<std::string>("userIntLabel");
  produces<pat::MuonCollection>();
}

void PATMuonIdEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection());

  edm::Handle<pat::MuonCollection> handle;
  evt.getByLabel(src_, handle);

  // apply selection
  selector_.select(handle, evt, es);

  // Check if our inputs are in our outputs
  for (size_t iMuon = 0; iMuon < handle->size(); ++iMuon) {
    const pat::Muon* currentMuon = &(handle->at(iMuon));
    std::vector<const pat::Muon*>::const_iterator find_result =
      std::find(selector_.begin(), selector_.end(), currentMuon);
    bool passedId = false;
    if (find_result != selector_.end()) {
      passedId = true;
    }
    pat::Muon newMuon = *currentMuon;
    newMuon.addUserInt(userIntLabel_, passedId);
    output->push_back(newMuon);
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonIdEmbedder);
