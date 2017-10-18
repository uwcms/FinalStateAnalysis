/*
 * Implementation of the various VBF selections used in the H2Tau analysis
 *
 * Authors: M. Bacthis, E. Friis, J. Swanson, UW Madison
 *
 */

#ifndef VBFSELECTIONS_9N7EKFZ2
#define VBFSELECTIONS_9N7EKFZ2

#include <vector>
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FinalStateAnalysis/DataAlgos/interface/VBFVariables.h"

VBFVariables computeVBFInfo(
    const std::vector<const reco::Candidate*>& hardScatter,
    const reco::Candidate::LorentzVector& metp4,
    const std::vector<const reco::Candidate*>& jets,
    const std::string& sysTag);

#endif /* end of include guard: VBFSELECTIONS_9N7EKFZ2 */
