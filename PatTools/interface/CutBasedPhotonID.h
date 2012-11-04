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
    static constexpr unsigned _passAll = kHighestBit - 1;
    //bitsets allowing us to mask out or veto part of the ID
    //This is defined per-cut in the ParameterSet.     
    unsigned _mask;
    unsigned _veto;    

    id_params _theid;    
  public:
    CutSet(const edm::ParameterSet&);
    
    //apply ID with option to apply an extra mask
    bool operator() (const pat::Photon&, const unsigned short mask=0xffffffff);
  };

  class CutBasedPhotonID {
    typedef std::map<std::string, CutSet> cut_map;
  private:
    const edm::Event* _event;
    const edm::EventSetup* _eventSetup;
    cut_map _passesID;
    ElectronHcalHelper* _hcalHelper;
  public:    
    
    CutBasedPhotonID(const std::vector<edm::ParameterSet>&);

    bool operator() (const pat::Photon&, working_point);

    void setEvent(const edm::Event& ev)   { _event      = &ev; }
    void setES(const edm::EventSetup& es) { _eventSetup = &es; }
  };

}

#endif
