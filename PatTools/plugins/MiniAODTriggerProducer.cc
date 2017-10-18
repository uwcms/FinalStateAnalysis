// Original Author:  Devin Taylor

#include <iostream>

// system include files
#include <memory>
#include <map>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"

//
// class declaration
//

class MiniAODTriggerProducer : public edm::stream::EDProducer<> {
   public:
      explicit MiniAODTriggerProducer(const edm::ParameterSet&);
      ~MiniAODTriggerProducer();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;

      // ----------member data ---------------------------

      // parameters
      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      //edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
      //edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;
      std::vector<std::string> triggers_;
      std::vector<std::string> labels_;

      // other members
      std::map<std::string, bool> decisionMap_;
};


//
// constructors and destructor
//

MiniAODTriggerProducer::MiniAODTriggerProducer(const edm::ParameterSet& iConfig):
  triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
  //triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
  //triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
  triggers_(iConfig.exists("triggers") ?
	    iConfig.getParameter<std::vector<std::string> >("triggers") :
	    std::vector<std::string>()),
  labels_(iConfig.exists("labels") ?
	    iConfig.getParameter<std::vector<std::string> >("labels") :
	    std::vector<std::string>())
{
  for(unsigned int i = 0; (i < triggers_.size() && i < labels_.size()); ++i) {
    produces<bool>(labels_.at(i));
  }
}


MiniAODTriggerProducer::~MiniAODTriggerProducer()
{

}


//
// member functions
//

// ------------ method called on each new Event  ------------
void
MiniAODTriggerProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<edm::TriggerResults> triggerBits;
  //edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  //edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;

  iEvent.getByToken(triggerBits_, triggerBits);
  //iEvent.getByToken(triggerObjects_, triggerObjects);
  //iEvent.getByToken(triggerPrescales_, triggerPrescales);

  const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);

  for (unsigned int i = 0; i < triggers_.size(); ++i) {
    decisionMap_[labels_.at(i)] = false;
  }

  for (unsigned int i = 0; i < triggerBits->size(); ++i) {
    std::string trigName = names.triggerName(i);
    for (unsigned int t = 0; t < triggers_.size(); ++t) {
      std::string matchName = triggers_.at(t);
      if (trigName == matchName) {
        decisionMap_[labels_.at(t)] = triggerBits->accept(i);
      }
    }
  }

  std::unique_ptr<bool> pOut;
  for (std::map<std::string, bool>::const_iterator it = decisionMap_.begin();
       it != decisionMap_.end(); ++it)
  {
      pOut = std::auto_ptr<bool>(new bool(!it->second));
      iEvent.put(std::move(pOut), it->first);
  }

  return;
}

//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODTriggerProducer);
