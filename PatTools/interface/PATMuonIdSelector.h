
/** \class PATMuonIdSelector
 *
 * Selection of "good quality" muons according to criteria
 * defined by Vector Boson Task Force and documented in Analysis Note CMS AN-10/264
 * (including extension to WW cross-section analysis documented in CMS AN-10/344)
 *
 * \author Michail Bachtis,
 *         Christian Veelken
 *
 * \version $Revision: 1.1 $
 *
 * $Id: PATMuonIdSelector.h,v 1.1 2011/08/30 09:58:54 friis Exp $
 *
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <vector>

class PATMuonIdSelectorImp
{
 public:
  typedef pat::MuonCollection collection;

  PATMuonIdSelectorImp(const edm::ParameterSet&, edm::ConsumesCollector);
  ~PATMuonIdSelectorImp();

  std::vector<const pat::Muon*>::const_iterator begin() const { return selected_.begin(); }
  std::vector<const pat::Muon*>::const_iterator end()   const { return selected_.end();   }

  void select(const edm::Handle<collection>&, edm::Event&, const edm::EventSetup&);

  size_t size() const { return selected_.size(); }

 private:
  void print();

  std::vector<const pat::Muon*> selected_;

//--- configuration parameters
  edm::InputTag srcBeamSpot_;
  edm::InputTag srcVertex_;

  bool     applyGlobalMuonPromptTight_;
  bool     applyAllArbitrated_;  
  bool     use2012IDVariables_; // use the 2012 ID variables from the Muon POG
  bool     usePFMuonReq_;

  double   maxIPxy_;                    // max. transverse   impact parameter of muon track
  double   maxIPz_;                     // max. longitudinal impact parameter of muon track
  int      IPtrackType_;                // compute impact parameters for inner/global track of muon
  int      IPrefType_;                  // compute impact parameters wrt. beam spot/reconstructed event vertex
  double   maxChi2red_;                 // max. (normalized) chi^2 of global muon track fit per degree of freedom
  double   maxDptOverPt_;               // max. relative error on muon momentum (computed for inner track)
  unsigned minTrackerHits_;             // min. number of hits in SiStrip + Pixel detectors
  unsigned minTkLayersWithMeasurement_; // min. number of TkLayers with a valid measurement (2012 ID)
  unsigned minPixelHits_;               // min. number of hits in Pixel detector
  unsigned minMuonHits_;
  unsigned minMuonStations_;            // min. number of hits in Muon chambers
  unsigned minMatchedSegments_;         // min. number of segments in Muon stations matched to inner track
};
