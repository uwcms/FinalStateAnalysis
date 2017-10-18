/**
 * A class to apply the 2012 photon IDs as given by:
 * https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
 *
 * This is meant to work only within CMSSW.
 * The user must ensure that the photon has proper isolations calculated.
 *
 * \author L. Gray (UW-Madison)
 */

#ifndef __CUTBASEDPHOTONID_H__
#define __CUTBASEDPHOTONID_H__

#include <vector>
#include <map>

#include "DataFormats/PatCandidates/interface/Photon.h"

//forward decls
namespace edm{
  class ParameterSet;  
  class Event;
  class EventSetup;
  class InputTag;
}

class ElectronHcalHelper;

namespace photontools {
  class CutSet {
  private:
    enum selector_bits{ kElectronVeto   = 1 << 0,
                        kSingleTowerHoE = 1 << 1,
                        kSihih          = 1 << 2,
                        kPFChargedIso   = 1 << 3,
                        kPFNeutralIso   = 1 << 4,
                        kPFPhotonIso    = 1 << 5,
			// if you add cuts remember to increment this bit
                        kHighestBit     = 1 << 6 }; 


    // trying to be maximally covering here... may save us later
    struct id_params {
      bool electronVeto;
      double singleTowerHoE_min_eb, singleTowerHoE_max_eb;
      double singleTowerHoE_min_ee, singleTowerHoE_max_ee;
      double sihih_min_eb, sihih_max_eb;
      double sihih_min_ee, sihih_max_ee;
      double pfChargedIso_pt_slope_eb, pfChargedIso_pt_slope_ee;
      double pfChargedIso_min_eb, pfChargedIso_max_eb;
      double pfChargedIso_min_ee, pfChargedIso_max_ee;
      double pfNeutralIso_pt_slope_eb, pfNeutralIso_pt_slope_ee;
      double pfNeutralIso_min_eb, pfNeutralIso_max_eb;
      double pfNeutralIso_min_ee, pfNeutralIso_max_ee;
      double pfPhotonIso_pt_slope_eb, pfPhotonIso_pt_slope_ee;
      double pfPhotonIso_min_eb, pfPhotonIso_max_eb;
      double pfPhotonIso_min_ee, pfPhotonIso_max_ee;      
    };
    
    // active bits mask
    static const unsigned _passAll = kHighestBit - 1;
    //bitsets allowing us to mask out or veto part of the ID
    //This is defined per-cut in the ParameterSet.     
    unsigned _mask;
    unsigned _veto;    

    id_params _theid;    
  public:
    CutSet() {}
    CutSet(const edm::ParameterSet&);
    CutSet(const CutSet& o) { this->operator=(o); }

    void operator=(const CutSet& o) { this->_mask=o._mask;
                                      this->_veto=o._veto;
				      this->_theid=o._theid; }
    
    //apply ID with option to apply an extra mask
    bool operator() (const pat::Photon&, const unsigned mask=0xffffffff) const;
  };

  class CutBasedPhotonID {
  private:
    typedef std::map<std::string, const CutSet> cut_map;
    cut_map _passesID;
  public:    
    CutBasedPhotonID(const edm::ParameterSet&);

    bool operator() (const pat::Photon&, const std::string&);
  };

}

#endif
