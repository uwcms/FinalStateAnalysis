/*
 * Embed effective area corrections into pat::Muons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PATMuonEACalculator.h"
#include <algorithm>

#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDGetToken.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;

using pat::Muon;
using pat::MuonCollection;

using pattools::PATMuonEACalculator;

namespace {
  typedef std::vector<std::string> vstring;
}

class PATMuonEAEmbedder : public edm::stream::EDProducer<> {
public:
  PATMuonEAEmbedder(const ParameterSet& pset);
  virtual ~PATMuonEAEmbedder(){}
  void produce(Event& evt, const EventSetup& es);
private:
  PATMuonEACalculator _eacalc;
  const vstring _eas_to_get;  
  const edm::EDGetTokenT<MuonCollection> _src;  
};

PATMuonEAEmbedder::PATMuonEAEmbedder(const 
				     ParameterSet& pset) :
  _eacalc(PATMuonEACalculator(pset.getParameterSetVector("effective_areas"))),
  _eas_to_get(pset.getParameter<vstring>("applied_effective_areas")),
  _src(consumes<MuonCollection>(pset.getParameter<edm::InputTag>("src")))
{
  produces<MuonCollection>();
}

void PATMuonEAEmbedder::produce(Event& evt, 
				const EventSetup& es) {
    

  std::auto_ptr<MuonCollection> output(new MuonCollection());

  edm::Handle<MuonCollection> handle;
  evt.getByToken(_src, handle);
  
  vstring::const_iterator i;
  vstring::const_iterator e = _eas_to_get.end();

  // Check if our inputs are in our outputs
  for (size_t iMu = 0; iMu < handle->size(); ++iMu) {
    const Muon* currentMuon = &(handle->at(iMu));   
    Muon newMuon = *currentMuon;    
      
    for( i = _eas_to_get.begin(); i != e; ++i ) {
      
      _eacalc.setEAType(*i);

      double the_ea = _eacalc(*currentMuon);
      
      newMuon.addUserFloat(*i,the_ea);    
    }
    output->push_back(newMuon);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonEAEmbedder);
