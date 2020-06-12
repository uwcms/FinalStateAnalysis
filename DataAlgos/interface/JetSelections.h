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
std::vector<double> computeDeepCSVJetInfo(
    const std::vector<const reco::Candidate*>& jets);
std::vector<double> computeDeepFlavourJetInfo(
    const std::vector<const reco::Candidate*>& jets);
std::vector<double> computeBInfo(
    const std::vector<const reco::Candidate*>& jets);

#endif /* end of include guard: JETSELECTIONS_9N7EKFZ2 */
