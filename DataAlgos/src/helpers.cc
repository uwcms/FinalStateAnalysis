#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"

#include "TMatrixD.h"
#include "TMath.h"

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

}
