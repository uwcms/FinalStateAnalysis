#include "FinalStateAnalysis/PatTools/interface/PATPhotonEACalculator.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

namespace pattools {

  namespace {
    typedef edm::ParameterSet PSet;
    typedef edm::VParameterSet VPSet;
    typedef std::vector<double> vdouble;    
  }

  PATPhotonEACalculator::PATPhotonEACalculator(const VPSet& areas){
    VPSet::const_iterator i = areas.begin();
    VPSet::const_iterator e = areas.end();

    for( ; i != e; ++i) {
      std::string name = i->getParameter<std::string>("name");
      double cone_size = i->getParameter<double>("cone_size");
      vdouble etas     = i->getParameter<vdouble>("eta_boundaries");
      vdouble eas      = i->getParameter<vdouble>("effective_areas");
      bool needs_neuts = i->getParameter<bool>("needs_pfneutral");
      bool needs_phos  = i->getParameter<bool>("needs_pfphoton");
      
      if( etas.size() != eas.size()+1 ) 
	throw cms::Exception("PATPhotonEACalculator") << "eta_boundaries size"
						   << " must be one greater"
						   << " than effective_areas"
						   << "!\n";
      for( size_t k = 1; k < etas.size(); ++k ) {
	ea_info temp;
	temp.eta_max  = etas[k];
	temp.eta_min  = etas[k-1];
	temp.eff_area = eas[k-1];
	temp.cone_size = cone_size;

	temp.needs_pfneut = needs_neuts;
	temp.needs_pfpho  = needs_phos;

	_eamap[name].push_back(temp);
      }
    }
  }

  double PATPhotonEACalculator::operator() (const pat::Photon& pho) {
    if( _eatype == "" ) 
      throw cms::Exception("PATPhotonEACalculator::()") 
	<< "_eatype not set!\n";
    
    map_type::mapped_type eas = _eamap[_eatype];

    std::vector<ea_info>::const_iterator i = eas.begin();
    std::vector<ea_info>::const_iterator e = eas.end();
    --e;  //To take care of the cases when eta > 3.0
    while(fabs(pho.superCluster()->eta()) >= i->eta_max && i != e) ++i;    
    
    return i->eff_area;
  }  

}
