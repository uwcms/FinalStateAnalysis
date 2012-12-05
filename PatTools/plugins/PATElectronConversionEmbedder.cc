/*
 * Embed bool saying whether or not we're matched to a conversion
 * into pat::Electron
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
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

namespace {
  typedef std::vector<std::string> vstring;
}

class PATElectronConversionEmbedder : public EDProducer {
public:
  PATElectronConversionEmbedder(const ParameterSet& pset);
  virtual ~PATElectronConversionEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src,_convSrc,_beamSpotSrc;
};

PATElectronConversionEmbedder::PATElectronConversionEmbedder(const 
					     ParameterSet& pset) { 
  _src     = pset.getParameter<InputTag>("src");  
  _convSrc = pset.getParameter<InputTag>("conversionSrc");
  _beamSpotSrc = pset.getParameter<InputTag>("beamSpotSrc");
  produces<ElectronCollection>();
}

void PATElectronConversionEmbedder::produce(Event& evt, 
				    const EventSetup& es) {
  

  std::auto_ptr<ElectronCollection> output(new ElectronCollection());

  edm::Handle<ElectronCollection> handle;
  evt.getByLabel(_src, handle);
 
  edm::Handle<reco::ConversionCollection> convH;
  evt.getByLabel(_convSrc,convH);

  edm::Handle<reco::BeamSpot> bsHandle;
  evt.getByLabel(_beamSpotSrc,bsHandle);

  // Check if our inputs are in our outputs
  for (size_t iEle = 0; iEle < handle->size(); ++iEle) {
    const reco::GsfElectron* currentElectron = 
      dynamic_cast<const reco::GsfElectron*>(handle->at(iEle).
					     originalObjectRef().get());
    Electron newElectron = handle->at(iEle); 

    int match = 
      (int) ConversionTools::hasMatchedConversion(*currentElectron, convH, 
						  bsHandle->position(), 
						  true, 2.0, 1e-6, 0);
    newElectron.addUserInt("HasMatchedConversion",match); 
    output->push_back(newElectron);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronConversionEmbedder);
