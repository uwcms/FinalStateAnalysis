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

#include "DataFormats/Candidate/interface/Candidate.h"
#include "TMatrixD.h"
#include <utility>
#include <vector>
class PATFinalStateEvent;

// The output format
typedef std::pair<reco::Candidate::LorentzVector, TMatrixD> MVAMetResult;

// The input formats
typedef std::vector<std::pair<math::XYZTLorentzVector,double> > PFInfo;
typedef std::vector<math::XYZVector> VertexInfo;

// Main method
MVAMetResult computeMVAMet(const PATFinalStateEvent* evt,
    std::vector<const reco::Candidate*> hardScatter,
    double minPt = 0, double minDZ = 0.1);

#endif /* end of include guard: MVAMET_Y9S1R0EK */
