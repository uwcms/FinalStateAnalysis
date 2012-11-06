/*
 * Embed the rochester corrections and associated errors in pat::Muons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATMuonRochesterCorrection.h"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;

using pat::Muon;
using pat::MuonRef;
using pat::MuonCollection;

using pattools::PATMuonRochesterCorrection;

class PATMuonRochesterCorrectionEmbedder : public EDProducer {
public:
  PATMuonRochesterCorrectionEmbedder(const ParameterSet& pset);
  virtual ~PATMuonRochesterCorrectionEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src;
  PATMuonRochesterCorrection _corr;  
};

PATMuonRochesterCorrectionEmbedder::
PATMuonRochesterCorrectionEmbedder(const 
				    ParameterSet& pset):
  _corr(PATMuonRochesterCorrection(pset,
				   pset.getParameter<bool>("isMC"))) {

  _src = pset.getParameter<InputTag>("src");  
  produces<MuonCollection>();
}

void PATMuonRochesterCorrectionEmbedder::produce(Event& evt, 
						 const EventSetup& es) {
  
  std::auto_ptr<MuonCollection> out(new MuonCollection);

  edm::Handle<MuonCollection> mus;
  evt.getByLabel(_src,mus);

  MuonCollection::const_iterator b = mus->begin();
  MuonCollection::const_iterator i = b;
  MuonCollection::const_iterator e = mus->end();

  for( ; i != e; ++i ) {
    MuonRef ref(mus,i - b);
    pat::Muon cMu = _corr(ref);
    out->push_back(cMu);
  }
  
  evt.put(out);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonRochesterCorrectionEmbedder);
