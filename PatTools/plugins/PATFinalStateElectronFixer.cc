/*
 * =====================================================================================
 *
 *       Filename:  PATFinalStateElectronFixer.cc
 *
 *    Description:  The first pat tuples, use the wrong name for the electron
 *    		    ref collection, fix it.
 *
 *         Author:  Evan Friis (), evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

class PATFinalStateElectronFixer : public edm::EDProducer {
  public:
    PATFinalStateElectronFixer(const edm::ParameterSet& pset);
    virtual ~PATFinalStateElectronFixer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag fseSrc_;
    edm::InputTag electronSrc_;

};
PATFinalStateElectronFixer::PATFinalStateElectronFixer(const edm::ParameterSet& pset) {
  fseSrc_ = pset.getParameter<edm::InputTag>("fseSrc");
  electronSrc_ = pset.getParameter<edm::InputTag>("electronSrc");
  produces<PATFinalStateEventCollection>();
}
void PATFinalStateElectronFixer::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<PATFinalStateEventCollection> output(
      new PATFinalStateEventCollection);

  edm::Handle<PATFinalStateEventCollection> event;
  evt.getByLabel(fseSrc_, event);

  // Get refs to the objects in the event
  edm::Handle<pat::ElectronCollection> electrons;
  evt.getByLabel(electronSrc_, electrons);
  edm::RefProd<pat::ElectronCollection> electronRefProd(electrons);

  // Make new copy
  PATFinalStateEvent fixedEvent(event->at(0));
  fixedEvent.setElectrons(electronRefProd);

  output->push_back(fixedEvent);

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateElectronFixer);
