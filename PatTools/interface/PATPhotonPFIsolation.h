/** \class PATPhotonPFIsolation
 *
 * Auxiliary class to encapsulate the prescription 
 * for PF isolation for photons in 42X and 5YX.
 * Provides a clean interface to the PFIsolationEstimator. 
 *
 * \author Lindsey Gray, UW Madison
 *

 *
 */

#ifndef __PATPHOTON_PF_ISOLATION_H__
#define __PATPHOTON_PF_ISOLATION_H__


#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/Handle.h"


// forward decls
class PFIsolationEstimator;
namespace pat {
  class Photon;
}

namespace pattools {

  struct pfisolation {
    double iso_chg_had;
    double iso_neut_had;
    double iso_photon;
    float cone_size;
  };

  // PFIsolationEstimator callable class wrapper
  class PATPhotonPFIsolation {
  private:
    PFIsolationEstimator * const _iso;
    const float _cone_size;
  public:
    PATPhotonPFIsolation(const float cone_size);
    ~PATPhotonPFIsolation();

    pfisolation operator() (const pat::Photon*,
			    const reco::PFCandidateCollection*,
			    reco::VertexRef,
			    edm::Handle< reco::VertexCollection >);
    
  };

}


#endif
