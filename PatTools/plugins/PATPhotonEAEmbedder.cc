/*
 * Embed effective area corrections into pat::Photons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATPhotonEACalculator.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Photon.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using pat::Photon;
using pat::PhotonCollection;

using pattools::PATPhotonEACalculator;

namespace {
  typedef std::vector<std::string> vstring;
}

class PATPhotonEAEmbedder : public EDProducer {
public:
  PATPhotonEAEmbedder(const ParameterSet& pset);
  virtual ~PATPhotonEAEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src;
  vstring _eas_to_get;  
  PATPhotonEACalculator _eacalc;
  
};

PATPhotonEAEmbedder::PATPhotonEAEmbedder(const 
				     ParameterSet& pset)
  :_eacalc(PATPhotonEACalculator(pset.getParameterSetVector("effective_areas"))){
  _eas_to_get = pset.getParameter<vstring>("applied_effective_areas");
  _src = pset.getParameter<InputTag>("src");  
  produces<PhotonCollection>();
}

void PATPhotonEAEmbedder::produce(Event& evt, 
				const EventSetup& es) {
    

  std::unique_ptr<PhotonCollection> output(new PhotonCollection());

  edm::Handle<PhotonCollection> handle;
  evt.getByLabel(_src, handle);
  
  vstring::const_iterator i;
  vstring::const_iterator e = _eas_to_get.end();

  // Check if our inputs are in our outputs
  for (size_t iPho = 0; iPho < handle->size(); ++iPho) {
    const Photon* currentPhoton = &(handle->at(iPho));   
    Photon newPhoton = *currentPhoton;    
      
    for( i = _eas_to_get.begin(); i != e; ++i ) {
      
      _eacalc.setEAType(*i);

      double the_ea = _eacalc(*currentPhoton);
      
      newPhoton.addUserFloat(*i,the_ea);    
    }
    output->push_back(newPhoton);
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATPhotonEAEmbedder);
