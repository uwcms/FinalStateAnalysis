/*
 * =====================================================================================
 *
 *       Filename:  MVAMet.h
 *
 *    Description:  Interface to the MVA MET regression
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef MVAMET_Y9S1R0EK
#define MVAMET_Y9S1R0EK

#include <utility>
#include <vector>

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "TMatrixD.h"

namespace edm {
  class EventID;
}

namespace reco {
  class Vertex;
}

// Minimal input-output of MVA MET algorithm
// Internal computation of event-invariant quantities are cached.
std::pair<math::XYZTLorentzVector, TMatrixD> computeMVAMet(
    const edm::EventID& evt,
    const std::vector<math::XYZTLorentzVector>& hardScatter,
    const reco::PFCandidateCollection& pflow,
    const reco::Vertex& pv,
    const pat::JetCollection& jets,
    const double& rho,
    const edm::PtrVector<reco::Vertex>& vertices);

#endif /* end of include guard: MVAMET_Y9S1R0EK */
