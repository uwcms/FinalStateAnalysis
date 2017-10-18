/*
 * Embed the the mass resolution (calculated analytically)
 * into the PATFinalState object. 
 * If the error is not available for daughter type the mass error is set to -1
 *
 * Author: L. Gray, FNAL
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include <string>
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FinalStateAnalysis/PatTools/interface/FinalStateMassResolution.h"

class PATFinalStateMassResolutionEmbedder : public edm::EDProducer {
public:
  PATFinalStateMassResolutionEmbedder(const edm::ParameterSet& pset);
  virtual ~PATFinalStateMassResolutionEmbedder(){ delete resoCalc_;}
  void produce(edm::Event& evt, const edm::EventSetup& es);
private:
  const bool debug_;
  edm::EDGetTokenT<edm::View<PATFinalState> > srcToken_;
  FinalStateMassResolution* resoCalc_;
  
};

PATFinalStateMassResolutionEmbedder::
PATFinalStateMassResolutionEmbedder(const edm::ParameterSet& pset):
  debug_(pset.getParameter<bool>("debug")),
  srcToken_(consumes<edm::View<PATFinalState> >(pset.getParameter<edm::InputTag>("src")))
{  
  resoCalc_ = new FinalStateMassResolution();    
  produces<PATFinalStateCollection>();
}
void 
PATFinalStateMassResolutionEmbedder::
produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  resoCalc_->init(es);

  edm::Handle<edm::View<PATFinalState> > finalStatesH;
  evt.getByToken(srcToken_, finalStatesH);
  
  for (size_t i = 0; i < finalStatesH->size(); ++i) {
    PATFinalState* embedInto = finalStatesH->ptrAt(i)->clone();    
    std::vector<double> components;
    double dM = 0;
    
    try {
      dM = resoCalc_->getMassResolutionWithComponents(*embedInto,
						      components);
    } catch (std::bad_cast& e) {
      dM = -1;
    }
    
    if( debug_ ) {
      std::cout << "Candidate " << i 
		<< " calculated dM = "<< dM  << " GeV" <<std::endl;
      std::cout << "\tComponents: ";
      for( size_t k = 0; k < components.size(); ++k )
	std::cout << components[k] 
		  << ( (k != components.size() - 1) ? " GeV, " : " GeV" );
      std::cout << std::endl;
    }

    embedInto->addUserFloat("cand_dM", dM);
    for( size_t k = 0; k < components.size(); ++k )
      embedInto->addUserFloat(Form("cand_dM_%lu",k), components[k]);
    
    output->push_back(embedInto); // takes ownership
  }
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateMassResolutionEmbedder);
