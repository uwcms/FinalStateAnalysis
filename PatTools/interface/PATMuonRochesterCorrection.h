/** \class PATMuonRochesterCorrection
 *
 * This class wrangles the Rochester Corrections
 * into a usable state within CMSSW for embedding.
 *
 * \author Lindsey Gray, UW Madison
 *
 *
 */

#ifndef __PATMUONROCHESTERCORRECTION_H__
#define __PATMUONROCHESTERCORRECTION_H__

#include <map>
#include <string>
#include <vector>
#include <memory>

#include "TLorentzVector.h"

//forward decls
#include "DataFormats/PatCandidates/interface/Muon.h"
namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class InputTag;  
}

#include "FinalStateAnalysis/PatTools/interface/RochesterCorrections2011.h"
#include "FinalStateAnalysis/PatTools/interface/RochesterCorrections2012.h"


namespace pattools {
  
  class PATMuonRochesterCorrection {
  private:
    typedef rochcor::RochesterCorrections2011 rc2011;
    typedef rochcor::RochesterCorrections2012 rc2012;
    
    class CorrectionBase {
    public:
      CorrectionBase() {}
      virtual ~CorrectionBase() {}

      virtual std::pair<math::XYZTLorentzVector,float> 
	correct(const math::XYZTLorentzVector& pin,
		float charge,
		float sysdev ) = 0;
    };

    // define a wrapper class to make the corrs not suck
    template<typename T, int runopt, bool doSyst> 
    class Correction : public CorrectionBase{
    private:
      T *_corr;
      bool _isMC;      
      
    public:
      Correction(bool isMC): _corr(new T(doSyst)), _isMC(isMC) {}
      virtual ~Correction() { delete _corr;}

      virtual std::pair<math::XYZTLorentzVector,float> 
	correct(const math::XYZTLorentzVector& pin,
		float charge,
		float sysdev ) {
	math::XYZTLorentzVector result = pin;
	float the_err = 0.0;
	TLorentzVector input(pin.x(),pin.y(),pin.z(),pin.t());

	if( doSyst ){
	  if( _isMC ) _corr->momcor_mc(input,charge,sysdev,runopt,the_err);
	  else        _corr->momcor_data(input,charge,sysdev,runopt,the_err);
	} else {
	  if( _isMC ) _corr->momcor_mc(input,charge,0.0,runopt,the_err);
	  else        _corr->momcor_data(input,charge,0.0,runopt,the_err);
	}
	
	result.SetXYZT(input.X(),input.Y(),input.Z(),input.T());
	return std::make_pair(result,the_err);
      }
	
    };
    
    //2011 corrections
    typedef Correction<rc2011,0,false> RochCor2011ANoSyst;
    typedef Correction<rc2011,0,true>  RochCor2011ASyst;
    typedef Correction<rc2011,1,false> RochCor2011BNoSyst;
    typedef Correction<rc2011,1,true>  RochCor2011BSyst;
    //2012 corrections
    typedef Correction<rc2012,0,false> RochCor2012NoSyst;
    typedef Correction<rc2012,0,true>  RochCor2012Syst;
    
    struct calib_container {
      float syst_err;
      CorrectionBase* central_value;
      CorrectionBase* syst_smear;
    };

    const std::string _errupPostfix,_errdownPostfix, _tkFitErr;
    typedef std::map<std::string, calib_container> calib_map;

    std::string _userP4Prefix;
    std::vector<std::string> _apply;    
    calib_map _calibs;    
    
  public:
    PATMuonRochesterCorrection(const edm::ParameterSet&,
			       const bool isMC);
    ~PATMuonRochesterCorrection();
    
    pat::Muon operator() (const pat::MuonRef&);    
    
  };

}

#endif
