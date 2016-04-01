/*
 * Implementation of the various Jet selections used in the H2Tau analysis
 *
 * Authors: truggles 
 *
 */

#ifndef JETSELECTIONS_9N7EKFZ2
#define JETSELECTIONS_9N7EKFZ2

#include <vector>
#include "DataFormats/Candidate/interface/Candidate.h"

std::vector<double> computeJetInfo(
    const std::vector<const reco::Candidate*>& jets);

std::vector<int> btagPromoteDemote(
    const std::vector<const reco::Candidate*>& jets);

#endif /* end of include guard: JETSELECTIONS_9N7EKFZ2 */
