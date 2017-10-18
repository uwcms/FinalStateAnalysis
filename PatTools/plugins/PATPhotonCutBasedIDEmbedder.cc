/*
 * Embed ID bools for photons into the pat::Photon object
 * This class calculates and embeds the SingleTower H/E and 
 * Conversion Safe electron veto.
 *
 * \author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/CutBasedPhotonID.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/EDGetToken.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

// for the conversion safe electron veto
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

// for the single tower H/E
#include "RecoEgamma/EgammaElectronAlgos/interface/ElectronHcalHelper.h"

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

namespace {
  typedef std::vector<std::string> vstring;
}

class PATPhotonCutBasedIDEmbedder : public EDProducer {
public:
  PATPhotonCutBasedIDEmbedder(const ParameterSet& pset);
  virtual ~PATPhotonCutBasedIDEmbedder(){ delete _hcalHelper; }
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src,_bsSrc,_convSrc,_eleSrc;
  vstring _apply;
  CutBasedPhotonID _theID;
  const std::string _pfix;
  ElectronHcalHelper::Configuration _helperCfg;
  ElectronHcalHelper* _hcalHelper;
};

PATPhotonCutBasedIDEmbedder::
PATPhotonCutBasedIDEmbedder(const 
			    ParameterSet& pset):
  _theID(pset),
  _pfix("CBID_") {

  _src = pset.getParameter<InputTag>("src");
  _bsSrc = pset.getParameter<InputTag>("beamSpotSrc");
  _convSrc = pset.getParameter<InputTag>("conversionSrc");
  _eleSrc = pset.getParameter<InputTag>("electronSrc");

  _apply = pset.getParameter<vstring>("idsToApply"); 

  _helperCfg.hOverEConeSize = pset.getParameter<double>("hOverEConeSize");
  _helperCfg.useTowers = true;
  _helperCfg.hcalTowers = consumes<CaloTowerCollection>(pset.getParameter<edm::InputTag>("hOverETowerSrc"));
  _helperCfg.hOverEPtMin = pset.getParameter<double>("hOverEPtMin");

  _hcalHelper = new ElectronHcalHelper(_helperCfg);
 
  produces<PhotonCollection>();
}

void PATPhotonCutBasedIDEmbedder::produce(Event& evt, 
					  const EventSetup& es) {
  //grab the necessary bits for the electron veto
  edm::Handle<reco::BeamSpot> bsHandle; //hah
  evt.getByLabel(_bsSrc,bsHandle);
  const reco::BeamSpot &beamspot = *(bsHandle.product());

  edm::Handle<reco::ConversionCollection> convHandle;
  evt.getByLabel(_convSrc,convHandle);
  
  edm::Handle<reco::GsfElectronCollection> eleHandle;
  evt.getByLabel(_eleSrc,eleHandle);

  edm::Handle<CaloTowerCollection> hcalTowersHandle;
  evt.getByToken(_helperCfg.hcalTowers,hcalTowersHandle);

  //setup H/E for this event
  _hcalHelper->checkSetup(es);
  _hcalHelper->readEvent(evt);    

  std::unique_ptr<PhotonCollection> out(new PhotonCollection);

  edm::Handle<PhotonCollection> phos;
  evt.getByLabel(_src,phos);

  PhotonCollection::const_iterator i = phos->begin();
  PhotonCollection::const_iterator e = phos->end();

  vstring::const_iterator iapp;
  vstring::const_iterator bapp = _apply.begin();
  vstring::const_iterator eapp = _apply.end();

  for( ; i != e; ++i ) {
    pat::Photon aPho = *i;

    //get the original photon
    const reco::Photon* oPho = 
      dynamic_cast<const reco::Photon*>(aPho.originalObjectRef().get());

    //calculate the conversion safe electron veto
    bool passelectronveto = 
      !ConversionTools::hasMatchedPromptElectron(oPho->superCluster(),
						 eleHandle,
						 convHandle,
						 beamspot.position());

    aPho.addUserInt("ConvSafeElectronVeto",(int32_t)passelectronveto);
    
    //calculate the single-tower H/E
    std::vector<CaloTowerDetId> hcalTowersBehindClusters =
      _hcalHelper->hcalTowersBehindClusters(*(oPho->superCluster()));
    float hcalDepth1 = 
      _hcalHelper->hcalESumDepth1BehindClusters(hcalTowersBehindClusters);
    float hcalDepth2 = 
      _hcalHelper->hcalESumDepth2BehindClusters(hcalTowersBehindClusters);
    float hOverE2012 = 
      (hcalDepth1 + hcalDepth2)/oPho->superCluster()->energy();
    float hOverE2012Depth1 = hcalDepth1/oPho->superCluster()->energy();
    float hOverE2012Depth2 = hcalDepth2/oPho->superCluster()->energy();

    aPho.addUserFloat("SingleTowerHoE",hOverE2012);
    aPho.addUserFloat("SingleTowerHoEDepth1",hOverE2012Depth1);
    aPho.addUserFloat("SingleTowerHoEDepth2",hOverE2012Depth2);

    // apply and embed the selected IDs from the config file.
    for( iapp=bapp; iapp != eapp; ++iapp ) {      
      bool ipass = _theID(aPho,*iapp);
      aPho.addUserInt(_pfix+*iapp,(int32_t)ipass);
    }    
    out->push_back(aPho);
  }
  
  evt.put(std::move(out));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATPhotonCutBasedIDEmbedder);
