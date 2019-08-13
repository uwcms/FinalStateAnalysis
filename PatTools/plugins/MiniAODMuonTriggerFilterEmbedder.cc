/*
 * Embeds the trigger filters
 * Author: Cecile Caillol, UW-Madison
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <math.h>

// class declaration
class MiniAODMuonTriggerFilterEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODMuonTriggerFilterEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODMuonTriggerFilterEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::MuonCollection> muonsCollection_;
    edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
};

// class member functions
MiniAODMuonTriggerFilterEmbedder::MiniAODMuonTriggerFilterEmbedder(const edm::ParameterSet& pset) {
  muonsCollection_ = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("src"));
  triggerBits_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("bits"));
  triggerObjects_ = consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("objects"));

  produces<pat::MuonCollection>();
}

void MiniAODMuonTriggerFilterEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<std::vector<pat::Muon>> muonsCollection;
  evt.getByToken(muonsCollection_ , muonsCollection);

  edm::Handle<edm::TriggerResults> triggerBits;
  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  evt.getByToken(triggerBits_, triggerBits);
  evt.getByToken(triggerObjects_, triggerObjects);

  const edm::TriggerNames &names = evt.triggerNames(*triggerBits);

  const std::vector<pat::Muon> * muons = muonsCollection.product();

  unsigned int nbMuon =  muons->size();

  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection);
  output->reserve(nbMuon);

  for(unsigned i = 0 ; i < nbMuon; i++){
    pat::Muon muon(muons->at(i));
    int matchMu24=0;
    int matchMu27=0;
    int matchMu20Tau27_2018=0;
    int matchMu20Tau27_2017=0;
    for (pat::TriggerObjectStandAlone obj : *triggerObjects) {
        if (reco::deltaR(muon, obj) > 0.5) continue;
        obj.unpackPathNames(names);
        obj.unpackFilterLabels(evt,*triggerBits.product());

        for (unsigned h = 0; h < obj.filterLabels().size(); ++h) {
          std::string filter = obj.filterLabels()[h];
          if (filter.compare("hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered0p07")==0) {
               matchMu20Tau27_2018++;
          }
          if (filter.compare("hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07")==0) {
               matchMu20Tau27_2017++;
          }
          if (filter.compare("hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07")==0) {
               matchMu24++;
          }
          if (filter.compare("hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07")==0) {
               matchMu27++;
          }
        }
    }

    muon.addUserInt("matchEmbeddedFilterMu24",matchMu24);
    muon.addUserInt("matchEmbeddedFilterMu27",matchMu27);
    muon.addUserInt("matchEmbeddedFilterMu20Tau27_2017",matchMu20Tau27_2017);
    muon.addUserInt("matchEmbeddedFilterMu20Tau27_2018",matchMu20Tau27_2018);

    output->push_back(muon);
  }

  evt.put(std::move(output));
}

// define plugin
DEFINE_FWK_MODULE(MiniAODMuonTriggerFilterEmbedder);
