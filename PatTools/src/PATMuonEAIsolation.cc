#include "FinalStateAnalysis/PatTools/interface/PATMuonEAIsolation.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

namespace pattools {

  namespace {
    typedef edm::ParameterSet PSet;
    typedef edm::VParameterSet VPSet;
    typedef std::vector<double> vdouble;    
  }

  PATMuonEAIsolation::PATMuonEAIsolation(const VPSet& areas){
    VPSet::const_iterator i = areas.begin();
    VPSet::const_iterator e = areas.end();

    for( ; i != e; ++i) {
      std::string name = i->getParameter<std::string>("name");
      double cone_size = i->getParameter<double>("cone_size");
      vdouble etas     = i->getParameter<vdouble>("eta_boundaries");
      vdouble eas      = i->getParameter<vdouble>("effective_areas");
      
      if( etas.size() != eas.size()+1 ) 
	throw cms::Exception("PATMuonEAIsolation") << "eta_boundaries size"
						   << " must be one greater"
						   << " than effective_areas"
						   << "!\n";
      for( size_t k = 1; k < etas.size(); ++k ) {
	ea_info temp;
	temp.eta_max  = etas[k];
	temp.eta_min  = etas[k-1];
	temp.eff_area = eas[k-1];
	temp.cone_size = cone_size;

	_eamap[name] = temp;
      }
    }
  }

  double PATMuonEAIsolation::operator() (const pat::Muon& mu, double rho) {
    if( _eatype == "" ) 
      throw cms::Exception("PATMuonEAIsolation::()") << "_eatype not set!\n";
    double result = 0.0;

    _eatype ea = _eamap[_eatype];

    std::vector<ea_info>::const_iterator i = eas.begin();
    std::vector<ea_info>::const_iterator e = eas.end();

    double chg_iso = (mu.pfIsolationDR

    for( ; i != e; ++i ) 
      
    }

    return result;
  }  

}
