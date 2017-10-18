/*
 * Embed PF Isolation for photons into the pat::Photon object
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATPhotonPFIsolation.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using reco::VertexCollection;
using reco::VertexRef;

using pat::Photon;
using pat::PhotonCollection;

using pattools::PATPhotonPFIsolation;
using pattools::pfisolation;

class PATPhotonPFIsolationEmbedder : public EDProducer {
public:
  PATPhotonPFIsolationEmbedder(const ParameterSet& pset);
  virtual ~PATPhotonPFIsolationEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src,_pfcollsrc,_vtxsrc;
  std::string _userFloatPrefix;
  unsigned _defaultVertex;
  PATPhotonPFIsolation _iso;
  const std::string _i_chad,_i_nhad,_i_pho,_cone;  
  char buf[20];
};

PATPhotonPFIsolationEmbedder::PATPhotonPFIsolationEmbedder(const 
							   ParameterSet& pset)
  :_iso(PATPhotonPFIsolation(pset.getParameter<double>("coneSize"))),
   _i_chad("_charged_hadron_iso"),
   _i_nhad("_neutral_hadron_iso"),
   _i_pho ("_photon_iso"),
   _cone("_cone") {
  _src = pset.getParameter<InputTag>("src");
  _pfcollsrc = pset.getParameter<InputTag>("pfCollectionSrc");
  _vtxsrc = pset.getParameter<InputTag>("vtxSrc"); 
  _defaultVertex = pset.getParameter<unsigned>("defaultVertex");
  _userFloatPrefix = pset.getParameter<std::string>("userFloatPrefix");
  produces<PhotonCollection>();
}

void PATPhotonPFIsolationEmbedder::produce(Event& evt, 
					   const EventSetup& es) {
  

  std::unique_ptr<PhotonCollection> output(new PhotonCollection());

  edm::Handle<PhotonCollection> handle;
  evt.getByLabel(_src, handle);

  edm::Handle<VertexCollection> vtxs;
  evt.getByLabel(_vtxsrc,vtxs);

  edm::Handle<reco::PFCandidateCollection> pfparts;
  evt.getByLabel(_pfcollsrc,pfparts);
  
  // Check if our inputs are in our outputs
  for (size_t iPho = 0; iPho < handle->size(); ++iPho) {
    const Photon* currentPhoton = &(handle->at(iPho));   
    Photon newPhoton = *currentPhoton;    

    for (size_t iVtx = 0; iVtx < vtxs->size(); ++iVtx) {
      memset(buf,0,20*sizeof(char));
      sprintf(buf,"_vtx%lu",iVtx);
      std::string postfix(buf);

      VertexRef the_pv = VertexRef(vtxs,iVtx);
      pfisolation the_iso = _iso(currentPhoton,pfparts.product(),the_pv,vtxs);
      
      if (iVtx == _defaultVertex) {
	newPhoton.setIsolation(pat::PfChargedHadronIso,the_iso.iso_chg_had);
	newPhoton.setIsolation(pat::PfNeutralHadronIso,the_iso.iso_neut_had);
	newPhoton.setIsolation(pat::PfGammaIso,the_iso.iso_photon);
	newPhoton.addUserFloat(_userFloatPrefix+_i_chad+postfix, 
			       the_iso.iso_chg_had);
	newPhoton.addUserFloat(_userFloatPrefix+_i_nhad+postfix, 
			       the_iso.iso_neut_had);
	newPhoton.addUserFloat(_userFloatPrefix+_i_pho+postfix,  
			       the_iso.iso_photon);
	newPhoton.addUserFloat(_userFloatPrefix+_cone+postfix,
			       the_iso.cone_size);
	
	newPhoton.setIsolation(pat::PfAllParticleIso,
			       the_iso.iso_chg_had  +
			       the_iso.iso_neut_had +
			       the_iso.iso_photon     );	
	
      } else {
	newPhoton.addUserFloat(_userFloatPrefix+_i_chad+postfix, 
			       the_iso.iso_chg_had);
	newPhoton.addUserFloat(_userFloatPrefix+_i_nhad+postfix, 
			       the_iso.iso_neut_had);
	newPhoton.addUserFloat(_userFloatPrefix+_i_pho+postfix,  
			       the_iso.iso_photon);
	newPhoton.addUserFloat(_userFloatPrefix+_cone+postfix,
			       the_iso.cone_size);
      }
    }    
    output->push_back(newPhoton);
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATPhotonPFIsolationEmbedder);
