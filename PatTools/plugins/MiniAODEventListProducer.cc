// Original Author:  Devin Taylor

#include <iostream>

// system include files
#include <memory>
#include <map>
#include <fstream>
#include <sstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


//
// class declaration
//

class MiniAODEventListProducer : public edm::stream::EDProducer<> {
   public:
      explicit MiniAODEventListProducer(const edm::ParameterSet&);
      ~MiniAODEventListProducer();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;

      // ----------member data ---------------------------

      // parameters
      const std::string label_;
      const std::string eventListFilename_;

      // other members
      std::map<std::string, bool> decisionMap_;
      std::vector<std::string> eventList_;
};


//
// constructors and destructor
//

MiniAODEventListProducer::MiniAODEventListProducer(const edm::ParameterSet& iConfig):
  label_(iConfig.exists("label") ?
	    iConfig.getParameter<std::string>("label") :
	    std::string()),
  eventListFilename_(iConfig.exists("eventList") ?
	    (iConfig.getParameter<edm::FileInPath>("eventList")).fullPath() :
	    std::string())
{
  // store txt file in event list
  std::ifstream infile(eventListFilename_);
  std::string line;
  while (std::getline(infile,line)) {
    eventList_.push_back(line);
  }

  produces<bool>(label_);

}


MiniAODEventListProducer::~MiniAODEventListProducer()
{

}


//
// member functions
//

// ------------ method called on each new Event  ------------
void
MiniAODEventListProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  // Default value
  decisionMap_[label_] = false;

  // iterate through event list of run:lumi:event
  std::stringstream currEvent;
  currEvent << iEvent.id().run() << ":" << iEvent.id().luminosityBlock() << ":" << iEvent.id().event();
  std::string evt = currEvent.str();
  for (std::vector<std::string>::iterator it = eventList_.begin(); it != eventList_.end(); ++it) {
    if (evt.compare(*it)==0) {
      decisionMap_[label_] = true;
    }
  }

  // store in the event
  std::auto_ptr<bool> pOut;
  for (std::map<std::string, bool>::const_iterator it = decisionMap_.begin();
       it != decisionMap_.end(); ++it)
  {
      pOut = std::auto_ptr<bool>(new bool(!it->second));
      iEvent.put(pOut, it->first);
  }

  return;
}

//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODEventListProducer);
