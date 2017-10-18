/*
 * Embed PF Jet IDs (see https://twiki.cern.ch/twiki/bin/view/CMS/JetID)
 * into pat::Jets
 *
 * Author: Evan K. Friis, UW Madison
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

class PATJetIdEmbedder : public edm::EDProducer {
  public:
    PATJetIdEmbedder(const edm::ParameterSet& pset);
    virtual ~PATJetIdEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
};

PATJetIdEmbedder::PATJetIdEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  produces<pat::JetCollection>();
}

void PATJetIdEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > input;
  evt.getByLabel(src_, input);

  output->reserve(input->size());
  for (size_t i = 0; i < input->size(); ++i) {
    pat::Jet jet = input->at(i);
    bool loose = true;
    bool medium = true;
    bool tight = true;
    if (jet.neutralHadronEnergyFraction() >= 0.99)
      loose = false;
    if (jet.neutralHadronEnergyFraction() >= 0.95)
      medium = false;
    if (jet.neutralHadronEnergyFraction() >= 0.90)
      tight = false;

    if (jet.neutralEmEnergyFraction() >= 0.99)
      loose = false;
    if (jet.neutralEmEnergyFraction() >= 0.95)
      medium = false;
    if (jet.neutralEmEnergyFraction() >= 0.90)
      tight = false;

    if (jet.getPFConstituents().size() <= 1) {
      loose = false;
      medium = false;
      tight = false;
    }

    if (std::abs(jet.eta()) < 2.4) {
      if (jet.chargedHadronEnergyFraction() == 0) {
        loose = false;
        medium = false;
        tight = false;
      }
      if (jet.chargedHadronMultiplicity() == 0) {
        loose = false;
        medium = false;
        tight = false;
      }
      if (jet.chargedEmEnergyFraction() >= 0.99) {
        loose = false;
        medium = false;
        tight = false;
      }
    }
    jet.addUserFloat("idLoose", loose);
    jet.addUserFloat("idMedium", medium);
    jet.addUserFloat("idTight", tight);
    output->push_back(jet);
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetIdEmbedder);
