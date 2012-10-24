/** \class PATPhotonPFIsolation
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

//forward decls
class ElectronEnergyCalibrator;
class CaloTopology;
class CaloGeometry;
#include "DataFormats/PatCandidates/interface/Electron.h"
namespace edm {
  class Event;
  class EventSetup;
  template<typename T> class ESHandle;
}


namespace pattools {
  
  class PATElectronEnergyCorrection {
  public:
    typedef ElectronEnergyCalibrator eCalib;
    typedef ElectronEnergyCalibrator* pcalib;
    typedef std::map<std::string,pcalib> map_type;
    typedef std::pair<std::string,int> key_type; // external key type
    typedef std::map<std::string,pcalib>::value_type value_type;
  private:
    std::string formIdent(const key_type&) const;

    const CaloTopology* _topo;
    const CaloGeometry* _geom;
    const edm::Event* _event;
    const edm::EventSetup* _esetup;
    
    map_type _corrs;
    
  public:
    PATElectronEnergyCorrection(const std::vector<key_type>&,
				const bool,
				const bool);
    ~PATElectronEnergyCorrection();
    
    std::auto_ptr<pat::Electron> operator() (const key_type&,
					     const pat::ElectronRef&);
    
    std::auto_ptr<pat::Electron> operator() (const std::string&,
					     const int,
					     const pat::ElectronRef&);

    void setES(const edm::EventSetup& es) { _esetup = &es; }
    void setEvent(const edm::Event& ev)   { _event  = &ev; }

    void update_topo_geo(edm::ESHandle<CaloTopology>,
			 edm::ESHandle<CaloGeometry>);

    std::vector<key_type> corrections() const;    
  };

}

#endif
