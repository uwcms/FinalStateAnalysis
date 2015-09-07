/*
 * Embed effective area corrections into pat::Muons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATElectronEACalculator.h"
#include <algorithm>

#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDGetToken.h"

#include "DataFormats/PatCandidates/interface/Electron.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;

using pat::Electron;
using pat::ElectronCollection;

using pattools::PATElectronEACalculator;

namespace {
  typedef std::vector<std::string> vstring;
}

class PATElectronEAEmbedder : public edm::stream::EDProducer<> {
public:
  PATElectronEAEmbedder(const ParameterSet& pset);
  virtual ~PATElectronEAEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  PATElectronEACalculator _eacalc;
  const vstring _eas_to_get;  
  const edm::EDGetTokenT<ElectronCollection> _src;
};

PATElectronEAEmbedder::PATElectronEAEmbedder(const 
					     ParameterSet& pset) :
  _eacalc(PATElectronEACalculator(pset.getParameterSetVector("effective_areas"))),
  _eas_to_get(pset.getParameter<vstring>("applied_effective_areas")),
  _src(consumes<ElectronCollection>(pset.getParameter<edm::InputTag>("src")))
{
  produces<ElectronCollection>();
}

void PATElectronEAEmbedder::produce(Event& evt, 
				    const EventSetup& es) {
  

  std::auto_ptr<ElectronCollection> output(new ElectronCollection());

  edm::Handle<ElectronCollection> handle;
  evt.getByToken(_src, handle);
  
  vstring::const_iterator i;
  vstring::const_iterator e = _eas_to_get.end();

  // Check if our inputs are in our outputs
  for (size_t iEle = 0; iEle < handle->size(); ++iEle) {
    const Electron* currentElectron = &(handle->at(iEle));   
    Electron newElectron = *currentElectron;    
      
    for( i = _eas_to_get.begin(); i != e; ++i ) {
      
      _eacalc.setEAType(*i);

      double the_ea = _eacalc(*currentElectron);

      //std::cout << "electron effective area = " << the_ea << std::endl;

      newElectron.addUserFloat(*i,the_ea);    
    }
    output->push_back(newElectron);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronEAEmbedder);
