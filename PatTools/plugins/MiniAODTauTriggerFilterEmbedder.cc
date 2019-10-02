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

#include "DataFormats/PatCandidates/interface/Tau.h"

#include <math.h>

// class declaration
class MiniAODTauTriggerFilterEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODTauTriggerFilterEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODTauTriggerFilterEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::TauCollection> tausCollection_;
    edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
};

// class member functions
MiniAODTauTriggerFilterEmbedder::MiniAODTauTriggerFilterEmbedder(const edm::ParameterSet& pset) {
  tausCollection_ = consumes<pat::TauCollection>(pset.getParameter<edm::InputTag>("src"));
  triggerBits_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("bits"));
  triggerObjects_ = consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("objects"));

  produces<pat::TauCollection>();
}

void MiniAODTauTriggerFilterEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<std::vector<pat::Tau>> tausCollection;
  evt.getByToken(tausCollection_ , tausCollection);

  edm::Handle<edm::TriggerResults> triggerBits;
  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  evt.getByToken(triggerBits_, triggerBits);
  evt.getByToken(triggerObjects_, triggerObjects);

  const edm::TriggerNames &names = evt.triggerNames(*triggerBits);

  const std::vector<pat::Tau> * taus = tausCollection.product();

  unsigned int nbTau =  taus->size();

  std::unique_ptr<pat::TauCollection> output(new pat::TauCollection);
  output->reserve(nbTau);

  for(unsigned i = 0 ; i < nbTau; i++){
    pat::Tau tau(taus->at(i));
    int matchMu20Tau27=0;
    int matchMu19Tau20=0;
    int matchMu20HPSTau27=0;
    int matchEle24Tau30=0;
    int matchTauTau=0;
    int matchTauTau2016=0;
    for (pat::TriggerObjectStandAlone obj : *triggerObjects) {
        if (reco::deltaR(tau, obj) > 0.5) continue;
        obj.unpackPathNames(names);
        obj.unpackFilterLabels(evt,*triggerBits.product());

        for (unsigned h = 0; h < obj.filterLabels().size(); ++h) {
          std::string filter = obj.filterLabels()[h];
          if (filter.compare("hltL1sMu18erTau24erIorMu20erTau24er")==0) {
               matchMu20Tau27++;
          }
          if (filter.compare("hltL1sMu18erTau20er")==0) {
               matchMu19Tau20++;
          }
          if (filter.compare("hltL1sBigORMu18erTauXXer2p1")==0) {
               matchMu20HPSTau27++;
          }
          if (filter.compare("hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3")==0) {
               matchEle24Tau30++;
          }
          if (filter.compare("hltDoubleL2IsoTau26eta2p2")==0) {
               matchTauTau++;
          }
          if (filter.compare("hltDoublePFTau35Reg")==0) {
               matchTauTau2016++;
          }
        }
    }

    tau.addUserInt("matchEmbeddedFilterMu20Tau27",matchMu20Tau27);
    tau.addUserInt("matchEmbeddedFilterMu19Tau20",matchMu19Tau20);
    tau.addUserInt("matchEmbeddedFilterMu20HPSTau27",matchMu20HPSTau27);
    tau.addUserInt("matchEmbeddedFilterEle24Tau30",matchEle24Tau30);
    tau.addUserInt("matchEmbeddedFilterTauTau",matchTauTau);
    tau.addUserInt("matchEmbeddedFilterTauTau2016",matchTauTau2016);

    output->push_back(tau);
  }

  evt.put(std::move(output));
}

// define plugin
DEFINE_FWK_MODULE(MiniAODTauTriggerFilterEmbedder);
