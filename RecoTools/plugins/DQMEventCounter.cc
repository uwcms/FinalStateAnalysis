/*
 * =====================================================================================
 *
 *       Filename:  DQMEventCounter.cc
 *
 *    Description:  Embed the event count in the DQM.
 *
 *         Author:  M. Bachtis
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DQMServices/Core/interface/MonitorElement.h"
#include "DQMServices/Core/interface/DQMStore.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


class DQMEventCounter : public edm::EDProducer {
   public:
      explicit DQMEventCounter(const edm::ParameterSet&);
      ~DQMEventCounter();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      MonitorElement *evCount;
      std::string name_;
};

DQMEventCounter::DQMEventCounter(const edm::ParameterSet& iConfig):
  name_(iConfig.getParameter<std::string>("name"))
{
     DQMStore* store = &*edm::Service<DQMStore>();
     evCount = store->bookFloat(name_.c_str());
     if(evCount)
       {
	 evCount->Fill(0);
       }

}


DQMEventCounter::~DQMEventCounter()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
DQMEventCounter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   if(evCount)
     {
       evCount->Fill(evCount->getFloatValue()+1.0);
     }
}

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"
DEFINE_FWK_MODULE(DQMEventCounter);
