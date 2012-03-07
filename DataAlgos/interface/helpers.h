/*
 * =====================================================================================
 *
 *       Filename:  helpers.h
 *
 *    Description:  General helper functions used by the FS data format
 *
 *         Author:  Evan Friis evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef HELPERS_TAQ1PE50
#define HELPERS_TAQ1PE50

#include "DataFormats/Candidate/interface/Candidate.h"
#include "TMatrixD.h"

namespace fshelpers {

/// Compute the significance of a vector given the covariance
double xySignficance(const reco::Candidate::Vector& vector,
    const TMatrixD& covariance);

}

#endif /* end of include guard: HELPERS_TAQ1PE50 */
