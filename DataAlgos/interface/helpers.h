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

#include <utility>

#include "DataFormats/Candidate/interface/Candidate.h"
#include "TMatrixD.h"

namespace fshelpers {

/// Compute the significance of a vector given the covariance
double xySignficance(const reco::Candidate::Vector& vector,
    const TMatrixD& covariance);

// By C. Veelken - returns pZeta, pZetaVis
std::pair<double, double> pZeta(const reco::Candidate::LorentzVector& leg1,
    const reco::Candidate::LorentzVector& leg2, double metPx, double metPy);

double transverseMass(const reco::Candidate::LorentzVector& p1,
    const reco::Candidate::LorentzVector& p2);

// Taken from CommonTools/CandUtils/AddFourMomenta.h
// makes sure the composite objects P4 = sum of daughters
void addFourMomenta(reco::Candidate & c);

}

#endif /* end of include guard: HELPERS_TAQ1PE50 */
