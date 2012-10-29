/** \class PATMuonEAIsolation
 *
 * values from:
 * https://indico.cern.ch/getFile.py/access?contribId=1&resId=0&materialId=slides&confId=188494
 * page 9
 *
 * Calculates the muon combined PF isolation based on effective areas.
 *
 * \author Lindsey Gray, UW Madison
 *
 *
 */

#ifndef __PATMUONEAISOLATION_H__
#define __PATMUONEAISOLATION_H__


#include <map>
#include <vector>
#include <string>

namespace edm {
  class ParameterSet;
  typedef std::vector<ParameterSet> VParameterSet;
}

namespace pat {
  class Muon;
}

namespace pattools {
  class PATMuonEAIsolation {    
  private:    
    struct ea_info {  
      bool   needs_pfneut,needs_pfpho;
      double eta_max,eta_min;      
      double eff_area;
      double cone_size;
    }
    typedef std::map<std::string,std::vector<ea_info> > map_type;
    map_type _eamap;
    std::string _eatype;
  public:
    PATMuonEAIsolation(const edm::VParameterSet&);    

    double operator() (const pat::Muon&, double rho);

    void setEAType(const std::string& type) { _eatype = type; }
  };
}

#endif
