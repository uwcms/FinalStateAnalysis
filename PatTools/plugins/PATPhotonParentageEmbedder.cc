/*
 * Embed properly resolved parentage information into photons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Photon.h"

#include "FinalStateAnalysis/DataAlgos/interface/PhotonParentage.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using pat::Photon;
using pat::PhotonCollection;

using phohelpers::PhotonParentage;

namespace {
  typedef std::vector<std::string> vstring;
}

class PATPhotonParentageEmbedder : public EDProducer {
public:
  PATPhotonParentageEmbedder(const ParameterSet& pset);
  virtual ~PATPhotonParentageEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src;
  
  
};

PATPhotonParentageEmbedder::PATPhotonParentageEmbedder(const 
						       ParameterSet& pset){  
  _src = pset.getParameter<InputTag>("src");  
  produces<PhotonCollection>();
}

void PATPhotonParentageEmbedder::produce(Event& evt, 
				const EventSetup& es) {
    

  std::unique_ptr<PhotonCollection> output(new PhotonCollection());

  edm::Handle<PhotonCollection> handle;
  evt.getByLabel(_src, handle);
  
  // Check if our inputs are in our outputs
  for (size_t iPho = 0; iPho < handle->size(); ++iPho) {
    const Photon* currentPhoton = &(handle->at(iPho));   
    Photon newPhoton = *currentPhoton;    
    
    edm::Ref<std::vector<Photon> >phoRef(handle, iPho);
    PhotonParentage test(phoRef);
    
    output->push_back(newPhoton);
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATPhotonParentageEmbedder);
