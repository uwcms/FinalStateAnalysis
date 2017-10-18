/** \class PATPhotonEnergyUncertainty
 *
 * For 42X this returns RecoEcal/EgammaCoreTools/EcalClusterEnergyUncertianty
 *
 * For 5XY it just returns the photon-level corrections from the reco::Photon
 *
 * This only gets you the 42X supercluster corrections or
 * the 52X ecal_photon corrections.
 *
 * \author Lindsey Gray, FNAL
 *
 */

#ifndef __PATPHOTONENERGYUNCERTAINTY_H__
#define __PATPHOTONENERGYUNCERTAINTY_H__
 

#include <map>
#include <vector>
#include <string>

namespace edm {
  class ParameterSet;
  typedef std::vector<ParameterSet> VParameterSet;
}
class EcalClusterFunctionBaseClass;

namespace pat {
  class Photon;  
}

namespace pattools {
  class PATPhotonEnergyUncertainty {    
  private:
    EcalClusterFunctionBaseClass *_uncertainty;
  public:
    PATPhotonEnergyUncertainty();    

    double operator() (const pat::Photon&);
  };
}

#endif
