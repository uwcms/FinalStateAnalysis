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

#include "DataFormats/PatCandidates/interface/Electron.h"

#include <math.h>

// class declaration
class MiniAODElectronTriggerFilterEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODElectronTriggerFilterEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODElectronTriggerFilterEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::ElectronCollection> electronsCollection_;
    edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
};

// class member functions
MiniAODElectronTriggerFilterEmbedder::MiniAODElectronTriggerFilterEmbedder(const edm::ParameterSet& pset) {
  electronsCollection_ = consumes<pat::ElectronCollection>(pset.getParameter<edm::InputTag>("src"));
  triggerBits_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("bits"));
  triggerObjects_ = consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("objects"));

  produces<pat::ElectronCollection>();
}

void MiniAODElectronTriggerFilterEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<std::vector<pat::Electron>> electronsCollection;
  evt.getByToken(electronsCollection_ , electronsCollection);

  edm::Handle<edm::TriggerResults> triggerBits;
  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  evt.getByToken(triggerBits_, triggerBits);
  evt.getByToken(triggerObjects_, triggerObjects);

  const edm::TriggerNames &names = evt.triggerNames(*triggerBits);

  const std::vector<pat::Electron> * electrons = electronsCollection.product();

  unsigned int nbElectron =  electrons->size();

  std::unique_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(nbElectron);

  for(unsigned i = 0 ; i < nbElectron; i++){
    pat::Electron electron(electrons->at(i));
    int matchEle27=0;
    int matchEle32=0;
    int matchEle32DoubleL1_v1=0;
    int matchEle32DoubleL1_v2=0;
    int matchEle35=0;
    int matchEle24Tau30=0;
    for (pat::TriggerObjectStandAlone obj : *triggerObjects) {
        if (reco::deltaR(electron, obj) > 0.5) continue;
        obj.unpackPathNames(names);
        obj.unpackFilterLabels(evt,*triggerBits.product());

        for (unsigned h = 0; h < obj.filterLabels().size(); ++h) {
          std::string filter = obj.filterLabels()[h];
          if (filter.compare("hltEle27WPTightGsfTrackIsoFilter")==0) {
               matchEle27++;
          }
          if (filter.compare("hltEle32WPTightGsfTrackIsoFilter")==0) {
               matchEle32++;
          }
          if (filter.compare("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter")==0) {
               matchEle32DoubleL1_v1++;
          }
          if (filter.compare("hltEGL1SingleEGOrFilter")==0) {
               matchEle32DoubleL1_v2++;
          }
          if (filter.compare("hltEle35noerWPTightGsfTrackIsoFilter")==0) {
               matchEle35++;
          }
          if (filter.compare("hltEle24erWPTightGsfTrackIsoFilterForTau")==0) {
               matchEle24Tau30++;
          }
        }
    }

    electron.addUserInt("matchEmbeddedFilterEle27",matchEle27);
    electron.addUserInt("matchEmbeddedFilterEle32",matchEle32);
    electron.addUserInt("matchEmbeddedFilterEle32DoubleL1_v1",matchEle32DoubleL1_v1);
    electron.addUserInt("matchEmbeddedFilterEle32DoubleL1_v2",matchEle32DoubleL1_v2);
    electron.addUserInt("matchEmbeddedFilterEle35",matchEle35);
    electron.addUserInt("matchEmbeddedFilterEle24Tau30",matchEle24Tau30);

    output->push_back(electron);
  }

  evt.put(std::move(output));
}

// define plugin
DEFINE_FWK_MODULE(MiniAODElectronTriggerFilterEmbedder);
