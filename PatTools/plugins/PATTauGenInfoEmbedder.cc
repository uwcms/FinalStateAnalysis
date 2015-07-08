/*
 * =====================================================================================
 *
 *       Filename:  PATTauGenInfoEmbedder.cc
 *
 *    Description:  Embed the gen decay mode into pat taus
 *         Author:  Evan Friis, evan.friis@cern.ch
 *                  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "RecoTauTag/RecoTau/interface/PFTauDecayModeTools.h"

class PATTauGenInfoEmbedder : public edm::EDProducer {
  public:
    PATTauGenInfoEmbedder(const edm::ParameterSet& pset);
    virtual ~PATTauGenInfoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;

};
PATTauGenInfoEmbedder::PATTauGenInfoEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  produces<pat::TauCollection>();
}

void PATTauGenInfoEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);
  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByLabel(src_, taus);
  output->reserve(taus->size());

  // Loop over input taus
  for (size_t i = 0; i < taus->size(); ++i) {
    pat::Tau copy = *taus->ptrAt(i);
    int decayModeIndex = -2;
    if (copy.genJet() != NULL) {
      decayModeIndex = reco::tau::getDecayMode(copy.genJet());
    }
    copy.addUserInt("genDecayMode", decayModeIndex);
    output->push_back(copy);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauGenInfoEmbedder);
