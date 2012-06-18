/*
 * Implementation of the various VBF selections used in the H2Tau analysis
 *
 * Authors: M. Bacthis, E. Friis, J. Swanson, UW Madison
 *
 */

#ifndef VBFSELECTIONS_9N7EKFZ2
#define VBFSELECTIONS_9N7EKFZ2

#include <vector>
#include "FinalStateAnalysis/DataAlgos/interface/VBFVariables.h"

namespace reco {
  class Candidate;
}

VBFVariables computeVBFInfo(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& jets);

#endif /* end of include guard: VBFSELECTIONS_9N7EKFZ2 */
