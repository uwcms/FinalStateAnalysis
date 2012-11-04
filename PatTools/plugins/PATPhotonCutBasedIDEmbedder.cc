/*
 * Embed ID bools for photons into the pat::Photon object
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/CutBasedPhotonID.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using pat::Photon;
using pat::PhotonRef;
using pat::PhotonCollection;

using photontools::CutBasedPhotonID;

class PATPhotonCutBasedIDEmbedder : public EDProducer {
public:
  PATPhotonCutBasedIDEmbedder(const ParameterSet& pset);
  virtual ~PATPhotonCutBasedIDEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src;
  CutBasedPhotonID _theID;
};

PATPhotonCutBasedIDEmbedder::
PATPhotonCutBasedIDEmbedder(const 
			    ParameterSet& pset):
  _theID(pset) {
  _src = pset.getParameter<InputTag>("src");  
  produces<PhotonCollection>();
}

void PATPhotonCutBasedIDEmbedder::produce(Event& evt, 
					  const EventSetup& es) {
  
  std::auto_ptr<PhotonCollection> out(new PhotonCollection);

  edm::Handle<PhotonCollection> phos;
  evt.getByLabel(_src,phos);

  PhotonCollection::const_iterator b = phos->begin();
  PhotonCollection::const_iterator i = b;
  PhotonCollection::const_iterator e = phos->end();

  for( ; i != e; ++i ) {
    out->push_back(*i);
  }
  
  evt.put(out);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATPhotonCutBasedIDEmbedder);
