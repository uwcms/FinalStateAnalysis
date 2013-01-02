#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "TMatrixD.h"
#include "TMath.h"
//#include <iostream>

namespace fshelpers {

double xySignficance(const reco::Candidate::Vector& vector,
    const TMatrixD& covariance) {
  // Instead of playing around w/ vector types to get ROOT
  // to do this for us, just do it manually.
  double vx = vector.x();
  double vy = vector.y();
  double mag2 = vx*vx + vy*vy;
  double mag = TMath::Sqrt(mag2);

  if (mag < 1.0e-9)
    return -1;

  // vT dot cov dot v
  double c00 = covariance(0,0);
  double c01 = covariance(0,1);
  double c10 = covariance(1,0);
  double c11 = covariance(1,1);

  double covDotVx = (c00*vx + c01*vy);
  double covDotVy = (c10*vx + c11*vy);

  double vTdotCovDotV = vx*covDotVx + vy*covDotVy;

  if (vTdotCovDotV < 0)
    return -2;

  // compute error pointing along the vector
  double error = TMath::Sqrt(vTdotCovDotV)/mag;

  return mag/error;
}

// By C. Veelken
std::pair<double, double> pZeta( const reco::Candidate::LorentzVector& leg1,
    const reco::Candidate::LorentzVector& leg2, double metPx, double metPy) {
  //std::cout << "<CompositePtrCandidateT1T2MEtAlgorithm::compZeta>:" << std::endl;

  double leg1x = cos(leg1.phi());
  double leg1y = sin(leg1.phi());
  double leg2x = cos(leg2.phi());
  double leg2y = sin(leg2.phi());
  double zetaX = leg1x + leg2x;
  double zetaY = leg1y + leg2y;
  double zetaR = TMath::Sqrt(zetaX*zetaX + zetaY*zetaY);
  if ( zetaR > 0. ) {
    zetaX /= zetaR;
    zetaY /= zetaR;
  }

  //std::cout << " leg1Phi = " << leg1.phi()*180./TMath::Pi() << std::endl;
  //std::cout << " leg2Phi = " << leg2.phi()*180./TMath::Pi() << std::endl;

  //std::cout << " zetaX = " << zetaX << std::endl;
  //std::cout << " zetaY = " << zetaY << std::endl;

  //std::cout << " zetaPhi = " << normalizedPhi(atan2(zetaY, zetaX))*180./TMath::Pi() << std::endl;

  double visPx = leg1.px() + leg2.px();
  double visPy = leg1.py() + leg2.py();
  double pZetaVis = visPx*zetaX + visPy*zetaY;

  //std::cout << " visPx = " << visPx << std::endl;
  //std::cout << " visPy = " << visPy << std::endl;

  double px = visPx + metPx;
  double py = visPy + metPy;
  double pZeta = px*zetaX + py*zetaY;

  //std::cout << " metPhi = " << normalizedPhi(atan2(metPy, metPx))*180./TMath::Pi() << std::endl;

  //assert(pZetaVis >= 0.);

  return std::make_pair(pZeta, pZetaVis);
}

double transverseMass(const reco::Candidate::LorentzVector& p1,
    const reco::Candidate::LorentzVector& p2){
  double totalEt = p1.Et() + p2.Et();
  double totalPt = (p1 + p2).pt();
  double mt2 = totalEt*totalEt - totalPt*totalPt;
  if (mt2 < 0) {
    std::cout << "P1 = " << p1 << " P2 = " << p2 << " " << mt2 << std::endl;
  }
  return std::sqrt(std::abs(mt2));
}

// Taken from CommonTools/CandUtils/AddFourMomenta.h
void addFourMomenta( reco::Candidate & c ) {
  reco::Candidate::LorentzVector p4( 0, 0, 0, 0 );
  reco::Candidate::Charge charge = 0;
  size_t n = c.numberOfDaughters();
  for(size_t i = 0; i < n; ++i) {
    const reco::Candidate * d = (const_cast<const reco::Candidate &>(c)).daughter(i);
    p4 += d->p4();
    charge += d->charge();
  }
  c.setP4( p4 );
  c.setCharge( charge );
}

/// Helper function to get the matched gen particle 
const reco::GenParticleRef getGenParticle(const reco::Candidate*   daughter)
{
  const pat::Tau* dauTau = dynamic_cast<const pat::Tau*>(daughter);
  if( dauTau ){
    return dauTau->genParticleRef();
  }

  const pat::Muon* dauMu = dynamic_cast<const pat::Muon*>(daughter);
  if( dauMu){
    return dauMu->genParticleRef();
  }

  const pat::Electron* dauE = dynamic_cast<const pat::Electron*>(daughter);
  if( dauE){
    return dauE->genParticleRef();
  }

  const pat::Jet* dauJet = dynamic_cast<const pat::Jet*>(daughter);
  if( dauJet){
    return dauJet->genParticleRef();
  }

  const pat::Photon* dauPho = dynamic_cast<const pat::Photon*>(daughter);
  if( dauPho){
    return dauPho->genParticleRef();
  }
  else{
    cms::Exception ex("ImplementationMissing");
    ex << "No implementation was found to get gen particle from a requested daughter, please consider either fixing the configuration or adding the implementation in FinalStateAnalysis/DataAlgos/src/helpers.cc\n";
    ex << "Available objects are pat::Tau, pat::Muon, pat::Electron, pat::Jet, pat::Photon\n";
    throw ex;
  }
}

/// Helper function to get the first interesting mother particle 
const reco::GenParticleRef getMotherSmart(const reco::GenParticleRef genPart, int idNOTtoMatch)
{
  if( genPart->numberOfMothers() == 0 ) return getPart; // if we've recursed all the way back we need to stop

  const reco::GenParticleRef mother = genPart->motherRef();
  if( !(mother.isAvailable() && mother.isNonnull())  ) return mother;
  if( mother.isAvailable() && mother.isNonnull() && mother->status() == 3 && mother->pdgId() != idNOTtoMatch )
    return mother;
  else
    return getMotherSmart(mother, idNOTtoMatch);
}

const bool comesFromHiggs(const reco::GenParticleRef genPart)
{
  //std::cout << "comesFromHiggs::start" << std::endl;
  if( genPart->numberOfMothers() >= 1 ){
    const reco::GenParticleRef mother = /*dynamic_cast<reco::GenParticleRef>*/ (genPart->motherRef());
    //std::cout << "comesFromHiggs::if statements" << std::endl;
    if( !(mother.isAvailable() && mother.isNonnull()) ){
      //std::cout << "comesFromHiggs::ret false" << std::endl;
      return false;
    }
    if( mother.isAvailable() && mother.isNonnull() && (mother->pdgId() == 25 || mother->pdgId() == 35 ) ){ // h^0 or H^0
      //std::cout << "comesFromHiggs::ret true" << std::endl;
      return true;
    }
    else{
      //std::cout << "comesFromHiggs::ret recursive" << std::endl;
      return comesFromHiggs(mother);
    }
  }
  else{
    //std::cout << "comesFromHiggs::ret false from no mother" << std::endl;
    return false;
  }
}

}
