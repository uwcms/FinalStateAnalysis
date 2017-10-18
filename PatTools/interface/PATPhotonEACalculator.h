/** \class PATPhotonEACalculator
 *
 * values from:
 * 
 * https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
 *
 * Returns the PAT Photon effective area for PF isolation.
 *
 * \author Lindsey Gray, UW Madison
 *
 *
 */

#ifndef __PATPHOTONEACALCULATOR_H__
#define __PATPHOTONEACALCULATOR_H__


#include <map>
#include <vector>
#include <string>

namespace edm {
  class ParameterSet;
  typedef std::vector<ParameterSet> VParameterSet;
}

namespace pat {
  class Photon;  
}

namespace pattools {
  class PATPhotonEACalculator {    
  private:    
    struct ea_info {  
      bool   needs_pfneut,needs_pfpho;
      double eta_max,eta_min;      
      double eff_area;
      double cone_size;
    };
    typedef std::map<std::string,std::vector<ea_info> > map_type;
    map_type _eamap;
    std::string _eatype;
  public:
    PATPhotonEACalculator(const edm::VParameterSet&);    

    double operator() (const pat::Photon&);

    void setEAType(const std::string& type) { _eatype = type; }
  };
}

#endif
