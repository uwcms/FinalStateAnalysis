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

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"


class MiniAODJetCleaningEmbedder : public edm::EDProducer {
  public:
    MiniAODJetCleaningEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetCleaningEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<pat::Jet> > srcJetToken_;
    edm::EDGetTokenT<edm::View<pat::Muon> > srcMuonToken_;
    edm::EDGetTokenT<edm::View<pat::Electron> > srcElectronToken_;
    std::string eID_;
    double eDR_;
    std::string mID_;
    double mDR_;
    std::string jID_;
    
};

MiniAODJetCleaningEmbedder::MiniAODJetCleaningEmbedder(const edm::ParameterSet& pset) {
  srcJetToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("jetSrc"));
  srcMuonToken_ = consumes<edm::View<pat::Muon> >(pset.getParameter<edm::InputTag>("muSrc"));
  srcElectronToken_ = consumes<edm::View<pat::Electron> >(pset.getParameter<edm::InputTag>("eSrc"));
  eID_ = pset.getParameter<std::string>("eID");
  eDR_ = pset.getParameter<double>("eDR");
  mID_ = pset.getParameter<std::string>("mID");
  mDR_ = pset.getParameter<double>("mDR");
  jID_ = pset.getParameter<std::string>("jID");
  produces<pat::JetCollection>();
}

void MiniAODJetCleaningEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > inputJet;
  edm::Handle<edm::View<pat::Muon> > inputMuon;
  edm::Handle<edm::View<pat::Electron> > inputElectron;
  evt.getByToken(srcJetToken_, inputJet);
  evt.getByToken(srcMuonToken_, inputMuon);
  evt.getByToken(srcElectronToken_, inputElectron);
  output->reserve(inputJet->size());
  StringCutObjectSelector<pat::Electron> EleCut(eID_);
  StringCutObjectSelector<pat::Muon> MuCut(mID_);
  StringCutObjectSelector<pat::Jet> JetCut(jID_);

  for (size_t i = 0; i < inputJet->size(); ++i) {
    pat::Jet jet = inputJet->at(i);
    bool cleanJet = true;
    if (JetCut(jet)){
      for (size_t j = 0; j < inputElectron->size(); ++j){
        pat::Electron electron = inputElectron->at(j);
        if(EleCut(electron)){
          float dR_EJ = reco::deltaR(jet.p4(),electron.p4());
          if (dR_EJ < eDR_){
            cleanJet = false;
          }
        }
      }
 
      for (size_t k = 0; k < inputMuon->size(); ++k){
        pat::Muon muon = inputMuon->at(k);
        if(MuCut(muon)){
          float dR_MJ = reco::deltaR(jet.p4(),muon.p4());
          if (dR_MJ < mDR_){
            cleanJet = false;
          }
        }
      }
      jet.addUserFloat("cleanJet", float(cleanJet));
      output->push_back(jet);
    }
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetCleaningEmbedder);
