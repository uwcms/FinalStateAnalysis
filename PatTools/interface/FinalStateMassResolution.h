/*
 *
 * This has been shamelessly stolen and ported to FSA from:
 * http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/CJLST/ZZAnalysis/AnalysisStep/src/CompositeCandMassResolution.cc?revision=1.2&view=markup
 * Original Authors: Boris Mangano, Stefano Argiro, Christina Botta
 * Port (and parts for reco::Photon) by: L. Gray (FNAL)
 *
 */

#ifndef PatTools_FinalStateMassResolution_h
#define PatTools_FinalStateMassResolution_h

namespace reco {
  class Candidate;
  class Muon;
  class Photon;
  class GsfElectron;
  class Track;
  class PFCandidate;
  class LeafCandidate;
}

namespace pat {
  class Jet;
}

namespace edm { class EventSetup; }
class EcalClusterFunctionBaseClass;

#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <vector>
#include "FWCore/Framework/interface/ESHandle.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include <TMatrixDSym.h>

/* Mutuated from
   /UserCode/Mangano/WWAnalysis/AnalysisStep/src/CompositeCandMassResolution.cc

 */

class FinalStateMassResolution  {
  typedef std::vector<std::string> vstring;
 public:
  FinalStateMassResolution();
  ~FinalStateMassResolution() {}
  void init(const edm::EventSetup &iSetup);
  double getMassResolution(const reco::Candidate &c) const ;
  double getMassResolutionWithComponents(const reco::Candidate &c,
					 std::vector<double> &errI) const;
 private:
  void   fillP3Covariance(const reco::Candidate &c,
			  TMatrixDSym &bigCov,
			  int offset) const ;
  void   fillP3Covariance(const reco::GsfElectron &c,
			  TMatrixDSym &bigCov,
			  int offset) const ;
  void   fillP3Covariance(const reco::Photon &c,
			  TMatrixDSym &bigCov,
			  int offset) const;
  void   fillP3Covariance(const reco::Muon &c,
			  TMatrixDSym &bigCov,
			  int offset) const ;
  void   fillP3Covariance(const reco::PFCandidate &c,
			  TMatrixDSym &bigCov,
			  int offset) const ;
  void   fillP3Covariance(const pat::Jet &c,
			  TMatrixDSym &bigCov,
			  int offset) const ;
  void   fillP3Covariance(const reco::Candidate &c,
			  const reco::Track &t,
			  TMatrixDSym &bigCov,
			  int offset) const ;
  void   fillP3Covariance(const reco::LeafCandidate &c,
			  TMatrixDSym &bigCov,
			  int offset) const ;

  edm::ESHandle<MagneticField> magfield_;
  EcalClusterFunctionBaseClass* uncertainty_;
  std::string mu_corr, e_corr;

  // 1 if this is a lead, recursive number of leafs if composite
  void getLeaves(const reco::Candidate &c,
		 std::vector<const reco::Candidate *> &out) const ;

  double getMassResolution_(const reco::Candidate &c,
			    std::vector<double> &errI,
			    bool doComponents) const;
};

#endif
