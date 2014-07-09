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
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

namespace fshelpers {

/// Compute the significance of a vector given the covariance
double xySignficance(const reco::Candidate::Vector& vector,
    const TMatrixD& covariance);

// By C. Veelken - returns pZeta, pZetaVis
std::pair<double, double> pZeta(const reco::Candidate::LorentzVector& leg1,
    const reco::Candidate::LorentzVector& leg2, double metPx, double metPy);

double transverseMass(const reco::Candidate::LorentzVector& p1,
    const reco::Candidate::LorentzVector& p2);

const reco::Candidate::LorentzVector metPhiCorrection(const reco::Candidate::LorentzVector& vector, int nvertices, bool isMC);

// Taken from CommonTools/CandUtils/AddFourMomenta.h
// makes sure the composite objects P4 = sum of daughters
void addFourMomenta(reco::Candidate & c);

/// Helper function to get the matched gen particle 
const reco::GenParticleRef getGenParticle(const reco::Candidate*   daughter,const reco::GenParticleRefProd genCollectionRef, int pdgIdToMatch, bool checkCharge);
const pat::PackedGenParticleRef getGenParticle(const reco::Candidate*   daughter,const pat::PackedGenParticleRefProd genCollectionRef, int pdgIdToMatch, bool checkCharge);

///Helper function to find a gen particle given pdgid and status
const bool findDecay(const reco::GenParticleRefProd genCollectionRef, int pdgIdMother, int pdgIdDaughter);
const bool findDecay(const pat::PackedGenParticleRefProd genCollectionRef, int pdgIdMother, int pdgIdDaughter);

/// Helper function to get the first interesting mother particle 
const reco::GenParticleRef getMotherSmart(const reco::GenParticleRef genPart, int idNOTtoMatch = -999);

/// Helper function to get if the gen particle associated comes from higgs 
const bool comesFromHiggs(const reco::GenParticleRef genPart);

float jetQGVariables(const reco::CandidatePtr  jetptr, const std::string& myvar, const edm::PtrVector<reco::Vertex> recoVertices);

}

#endif /* end of include guard: HELPERS_TAQ1PE50 */
