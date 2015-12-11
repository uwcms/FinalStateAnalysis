/*
 * Embed jet cleaning ids
 * into slimmed jets
 *
 * Author: Aaron Levine, UW Madison
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

class MiniAODJetCleaningEmbedder : public edm::EDProducer {
  public:
    MiniAODJetCleaningEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetCleaningEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag srcJet_;
    edm::InputTag srcMuon_;
    edm::InputTag srcElectron_;
};

MiniAODJetCleaningEmbedder::MiniAODJetCleaningEmbedder(const edm::ParameterSet& pset) {
  srcJet_ = pset.getParameter<edm::InputTag>("jetSrc");
  srcMuon_ = pset.getParameter<edm::InputTag>("muSrc");
  srcElectron_ = pset.getParameter<edm::InputTag>("eSrc");
  produces<pat::JetCollection>();
}

void MiniAODJetCleaningEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > inputJet;
  edm::Handle<edm::View<pat::Muon> > inputMuon;
  edm::Handle<edm::View<pat::Electron> > inputElectron;
  evt.getByLabel(srcJet_, inputJet);
  evt.getByLabel(srcMuon_, inputMuon);
  evt.getByLabel(srcElectron_, inputElectron);
  
  std::cout << inputJet->size() << std::endl;
  std::cout << inputElectron->size() << std::endl;
  std::cout << inputMuon->size() << std::endl;

  output->reserve(inputJet->size());
  for (size_t i = 0; i < inputJet->size(); ++i) {
    pat::Jet jet = inputJet->at(i);
    bool cleanJet = true;

    for (size_t j = 0; j < inputElectron->size(); ++j){
      pat::Electron electron = inputElectron->at(j);
      float isoElectron = electron.neutralHadronIso()+electron.photonIso()-electron.userFloat("rho_fastjet")*electron.userFloat("EffectiveArea");
      if (isoElectron < 0.0){
        isoElectron = 0.0;
      }
      if(electron.pt() > 10 && electron.userInt("CBIDLoose") > 0 && (electron.chargedHadronIso()+isoElectron)/electron.pt() < 0.2){
        float dR_EJ = reco::deltaR(jet.p4(),electron.p4());
        if (dR_EJ < 0.4){
          cleanJet = false;
        }
      }
    }

    for (size_t k = 0; k < inputMuon->size(); ++k){
      pat::Muon muon = inputMuon->at(k);
      float isoMuon = muon.photonIso() + muon.neutralHadronIso() - 0.5*muon.puChargedHadronIso();
      if (isoMuon < 0.0){
        isoMuon = 0.0;
      }
      if(muon.pt() > 10 && muon.isLooseMuon() && (muon.chargedHadronIso() + isoMuon)/muon.pt()<0.2){
        float dR_MJ = reco::deltaR(jet.p4(),muon.p4());
        if (dR_MJ < 0.4){
          cleanJet = false;
        }
      }
    }
    std::cout << "Adding userfloat " << cleanJet << " to jet" << std::endl;
    jet.addUserFloat("cleanJet", float(cleanJet));
    std::cout << "jet userfloat: " << jet.userFloat("cleanJet") << std::endl;
    if (cleanJet == true){
      output->push_back(jet);
    }
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetCleaningEmbedder);
