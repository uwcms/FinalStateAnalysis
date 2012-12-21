#include "FinalStateAnalysis/PatTools/interface/PATPhotonEnergyUncertainty.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterFunctionFactory.h"

namespace pattools {

  PATPhotonEnergyUncertainty::PATPhotonEnergyUncertainty(){
    _uncertainty = 
      EcalClusterFunctionFactory::get()->
      create( "EcalClusterEnergyUncertainty", 
	      edm::ParameterSet() );
  }

  double PATPhotonEnergyUncertainty::operator() (const pat::Photon& pho) {
    
#if CMSSW_VERSION<500
    double dE = _uncertainty->getValue( *(pho.superCluster()) ,
				        0 );
#else
    double dE = pho.getCorrectedEnergyError(reco::Photon::ecal_photons);
#endif
    
    return dE;
  }  

}
