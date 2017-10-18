/*
 * Embed effective area corrections into pat::Muons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATElectronEACalculator.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Electron.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using pat::Electron;
using pat::ElectronCollection;

using pattools::PATElectronEACalculator;

namespace {
  typedef std::vector<std::string> vstring;
}

class PATElectronEAEmbedder : public EDProducer {
public:
  PATElectronEAEmbedder(const ParameterSet& pset);
  virtual ~PATElectronEAEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  edm::EDGetTokenT<ElectronCollection> _srcToken;
  vstring _eas_to_get;  
  PATElectronEACalculator _eacalc;
  
};

PATElectronEAEmbedder::PATElectronEAEmbedder(const 
					     ParameterSet& pset)
  :_eacalc(PATElectronEACalculator(pset.getParameterSetVector("effective_areas"))){
  _eas_to_get = pset.getParameter<vstring>("applied_effective_areas");
  _srcToken = consumes<ElectronCollection>(pset.getParameter<InputTag>("src"));  
  produces<ElectronCollection>();
}

void PATElectronEAEmbedder::produce(Event& evt, 
				    const EventSetup& es) {
  

  std::unique_ptr<ElectronCollection> output(new ElectronCollection());

  edm::Handle<ElectronCollection> handle;
  evt.getByToken(_srcToken, handle);
  
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

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronEAEmbedder);
