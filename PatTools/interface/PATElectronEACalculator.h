/** \class PATElectronEACalculator
 *
 * values from:
 * 
 * https://twiki.cern.ch/twiki/bin/view/CMS/EgammaEARhoCorrection
 * Using: EGammaAnalysisTools/interface/ElectronEffectiveArea.h
 *
 * Returns the PAT Electron effective area for PF isolation.
 *
 * \author Lindsey Gray, UW Madison
 *
 *
 */

#ifndef __PATELECTRONEAISOLATION_H__
#define __PATELECTRONEAISOLATION_H__


#include <map>
#include <vector>
#include <string>

namespace edm {
  class ParameterSet;
  typedef std::vector<ParameterSet> VParameterSet;
}

namespace pat {
  class Electron;  
}

namespace pattools {
  class PATElectronEACalculator {    
  private:    
    struct ea_info {
      int ea_type;
      int ea_target;      
    };
    typedef std::map<std::string,ea_info> map_type;
    map_type _eamap;
    std::string _eatype;
  public:
    PATElectronEACalculator(const edm::VParameterSet&);    

    double operator() (const pat::Electron&);

    void setEAType(const std::string& type) { _eatype = type; }
  };
}

#endif
