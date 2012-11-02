/** \class PATElectronEnergyCorrection
 *
 * Auxiliary class to encapsulate the prescription
 * for applying the regression-based electron energy
 * corrections.
 * Constructed by giving a list of datasets and 
 * correction types defined in 
 * https://twiki.cern.ch/twiki/bin/view/CMS/EgammaElectronEnergyScale.
 * The user may then apply any one of the given 
 * corrections to an input electron.
 *
 * \author Lindsey Gray, UW Madison
 *
 *
 */

#ifndef __PATELECTRONENERGYCORRECTION_H__
#define __PATELECTRONENERGYCORRECTION_H__

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

      virtual TLorentzVector operator() (const TLorentzVector& pin,
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

      virtual TLorentzVector operator() ( const TLorentzVector& pin,
					  float charge,
					  float sysdev ) {
	TLorentzVector result = pin;
	
	if( doSyst ){
	  if( _isMC ) _corr->momcor_mc(result,charge,sysdev,runopt);
	  else        _corr->momcor_data(result,charge,sysdev,runopt);
	} else {
	  if( _isMC ) _corr->momcor_mc(result,charge,0.0,runopt);
	  else        _corr->momcor_data(result,charge,0.0,runopt);
	}

	return result;
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

    const std::string _errupPostfix,_errdownPostfix;
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
