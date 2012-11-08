#include "FinalStateAnalysis/PatTools/interface/PATMuonRochesterCorrection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <stdio.h>

namespace pattools { 

  namespace { // hide a bunch of convenient typedefs
    typedef edm::ParameterSet PSet;
    typedef edm::VParameterSet VPSet;
        
    typedef std::auto_ptr<pat::Muon> pmuon;
    typedef std::vector<pmuon> vpmuon;
    typedef pat::MuonRef muRef;
    
    typedef std::vector<std::string> vstring;
  }

  PATMuonRochesterCorrection::PATMuonRochesterCorrection(const PSet& conf,
							 const bool isMC):
    _errupPostfix("_errUp"),
    _errdownPostfix("_errDown"){
    
    _userP4Prefix = conf.getParameter<std::string>("userP4Prefix");
        
    // setup calibration pool
    VPSet available_corrections = 
      conf.getParameterSetVector("available_corrections");  
    // get applied calibrations
    _apply = conf.getParameter<vstring>("applyCorrections");
    
    { // make iterators descope
      VPSet::const_iterator i = available_corrections.begin();
      VPSet::const_iterator e = available_corrections.end();

      for( ; i != e; ++i) {
	std::string name     = i->getParameter<std::string>("name");
	std::string dataSet = i->getParameter<std::string>("dataSet");
	double      syst     = i->getParameter<double>("systematic_error");
	
	_calibs[name].syst_err = syst;
	if( dataSet == "2011A" ) {
	  _calibs[name].central_value = new RochCor2011ANoSyst(isMC);
	  _calibs[name].syst_smear    = new RochCor2011ASyst(isMC);
	} else if ( dataSet == "2011B" ) {
	  _calibs[name].central_value = new RochCor2011BNoSyst(isMC);
	  _calibs[name].syst_smear    = new RochCor2011BSyst(isMC);
	} else if ( dataSet == "2012" ) {
	  _calibs[name].central_value = new RochCor2012NoSyst(isMC);
	  _calibs[name].syst_smear    = new RochCor2012Syst(isMC);
	} else {
	  throw cms::Exception("PATMuonRochesterCorrection::ctor")
	    << "dataSet must be one of: 2011A, 2011B, 2012!\n";
	}
	
      }      
    }    
    
  }
 
  PATMuonRochesterCorrection::~PATMuonRochesterCorrection() {
    calib_map::iterator i = _calibs.begin();
    calib_map::iterator e = _calibs.end();
    for(; i != e; ++i) {
      if(i->second.central_value)  delete i->second.central_value;
      if(i->second.syst_smear) delete i->second.syst_smear;
    }
  }

  pat::Muon
  PATMuonRochesterCorrection::operator() (const muRef& mu) {    
    pat::Muon out = *mu;

    vstring::const_iterator app = _apply.begin();
    vstring::const_iterator end = _apply.end();
    
    for( ; app != end; ++app ) {
      math::XYZTLorentzVector corr_p4, errup_p4, errdown_p4;
      float syst = _calibs[*app].syst_err;

      corr_p4    = _calibs[*app].central_value->correct(mu->p4(),
							mu->charge(),
							syst);      
      errup_p4   = _calibs[*app].syst_smear->correct(mu->p4(),
						     mu->charge(),
						     syst);
      errdown_p4 = _calibs[*app].syst_smear->correct(mu->p4(),
						     mu->charge(),
						     -syst);

      out.addUserData<math::XYZTLorentzVector>(_userP4Prefix+
					       *app,
					       corr_p4);
      out.addUserData<math::XYZTLorentzVector>(_userP4Prefix+
					       *app+
					       _errupPostfix,
					       errup_p4);
      out.addUserData<math::XYZTLorentzVector>(_userP4Prefix+
					       *app+
					       _errdownPostfix,
					       errdown_p4);
    }
    
    return out;
  }  
  
}
