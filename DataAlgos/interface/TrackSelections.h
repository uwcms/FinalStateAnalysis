/*
 * Implementation of the various Track selections used in the H2Tau analysis
 *
 * Authors: truggles 
 *
 */

#ifndef TRACKSELECTIONS_9N7EKFZ2
#define TRACKSELECTIONS_9N7EKFZ2

#include <vector>
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

std::vector<double> computeTrackInfo(
    const std::vector<const reco::Candidate*>& tracks, const std::vector<pat::PackedCandidate> pfs, const reco::GenParticleRefProd genCollectionRef, bool has_gen);

#endif /* end of include guard: TRACKSELECTIONS_9N7EKFZ2 */
