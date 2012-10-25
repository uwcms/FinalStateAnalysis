/*
 * Embed PF Isolation for photons into the pat::Photon object
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATElectronEnergyCorrection.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using pat::Electron;
using pat::ElectronRef;
using pat::ElectronCollection;

using pattools::PATElectronEnergyCorrection;

class PATElectronEnergyCorrectionEmbedder : public EDProducer {
public:
  PATElectronEnergyCorrectionEmbedder(const ParameterSet& pset);
  virtual ~PATElectronEnergyCorrectionEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src;
  PATElectronEnergyCorrection _corr;  
};

PATElectronEnergyCorrectionEmbedder::
PATElectronEnergyCorrectionEmbedder(const 
				    ParameterSet& pset):
  _corr(PATElectronEnergyCorrection(pset,
				    pset.getParameter<bool>("isAOD"),
				    pset.getParameter<bool>("isMC"))) {

  _src = pset.getParameter<InputTag>("src");  
  produces<ElectronCollection>();
}

void PATElectronEnergyCorrectionEmbedder::produce(Event& evt, 
						  const EventSetup& es) {
  
  _corr.setES(es);
  _corr.setEvent(evt);

  std::auto_ptr<ElectronCollection> out(new ElectronCollection);

  edm::Handle<ElectronCollection> eles;
  evt.getByLabel(_src,eles);

  ElectronCollection::const_iterator b = eles->begin();
  ElectronCollection::const_iterator i = b;
  ElectronCollection::const_iterator e = eles->end();

  for( ; i != e; ++i ) {
    ElectronRef ref(eles,i - b);
    std::auto_ptr<pat::Electron> cEle = _corr(ref);

    out->push_back(*cEle);
  }
  
  evt.put(out);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronEnergyCorrectionEmbedder);
