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

#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "RecoTauTag/RecoTau/interface/PFTauDecayModeTools.h"

class PATTauGenInfoEmbedder : public edm::EDProducer {
  public:
    PATTauGenInfoEmbedder(const edm::ParameterSet& pset);
    virtual ~PATTauGenInfoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<pat::Tau> > srcToken_;

};
PATTauGenInfoEmbedder::PATTauGenInfoEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Tau> >(pset.getParameter<edm::InputTag>("src"));
  produces<pat::TauCollection>();
}

void PATTauGenInfoEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);
  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByToken(srcToken_, taus);
  output->reserve(taus->size());

  // Loop over input taus
  for (size_t i = 0; i < taus->size(); ++i) {
    pat::Tau copy = *taus->ptrAt(i);
    int decayModeIndex = -2;
    double genJetPt=-2;
    double genJetEta=-10;
    double genJetPhi=-2;
    double genJetCharge=-2;

    if (copy.genJet() != NULL) {
      decayModeIndex = reco::tau::getDecayMode(copy.genJet());
      genJetPt = copy.genJet()->pt();
      genJetEta = copy.genJet()->eta();
      genJetPhi = copy.genJet()->phi();
      genJetCharge = copy.genJet()->charge();
    }
    copy.addUserInt("genDecayMode", decayModeIndex);
    copy.addUserFloat("genJetPt", genJetPt);
    copy.addUserFloat("genJetEta", genJetEta);
    copy.addUserFloat("genJetPhi", genJetPhi);
    copy.addUserFloat("genJetCharge", genJetCharge);

    output->push_back(copy);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauGenInfoEmbedder);
