#ifndef PFMETSIGNINTERFACEBASE_U3K9O5CO
#define PFMETSIGNINTERFACEBASE_U3K9O5CO

/** \class PFMEtSignInterfaceBase
 *
 * Auxiliary class interfacing the TauAnalysis software to
 *  RecoMET/METAlgorithms/interface/significanceAlgo.h
 * for computing (PF)MEt significance
 * (see CMS AN-10/400 for description of the (PF)MEt significance computation)
 *
 * \author Christian Veelken, UC Davis
 *
 * \version $Revision: 1.1 $
 *
 * $Id: PFMEtSignInterfaceBase.h,v 1.1 2012/02/13 14:00:16 veelken Exp $
 *
 */

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "RecoMET/METAlgorithms/interface/SignAlgoResolutions.h"
#include "DataFormats/METReco/interface/SigInputObj.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include <TMatrixD.h>
#include "Math/SMatrixDfwd.h"

#include <list>

class PFMEtSignInterfaceBase
{
 public:

  PFMEtSignInterfaceBase(const edm::ParameterSet&);
  ~PFMEtSignInterfaceBase();

  TMatrixD operator()(const std::list<const reco::Candidate*>&) const;

 protected:

  TMatrixD operator()(const std::vector<metsig::SigInputObj>&) const;

  template <typename T>
  void addPFMEtSignObjects(std::vector<metsig::SigInputObj>& metSignObjects,
			   const std::list<const T*>& particles) const
  {
    if ( this->verbosity_ ) std::cout << "<PFMEtSignInterfaceBase::addPFMEtSignObjects>:" << std::endl;

    for ( typename std::list<const T*>::const_iterator particle = particles.begin();
	  particle != particles.end(); ++particle ) {
      double pt   = (*particle)->pt();
      double eta  = (*particle)->eta();
      double phi  = (*particle)->phi();

      if ( dynamic_cast<const reco::GsfElectron*>(*particle) != 0 ||
	   dynamic_cast<const pat::Electron*>(*particle) != 0 ) {
	std::string particleType = "electron";
	// WARNING: SignAlgoResolutions::PFtype2 needs to be kept in sync with reco::PFCandidate::e !!
	double dpt  = pfMEtResolution_->eval(metsig::PFtype2, metsig::ET,  pt, phi, eta);
	double dphi = pfMEtResolution_->eval(metsig::PFtype2, metsig::PHI, pt, phi, eta);
	//std::cout << "electron: pt = " << pt << ", eta = " << eta << ", phi = " << phi
	//          << " --> dpt = " << dpt << ", dphi = " << dphi << std::endl;
	metSignObjects.push_back(metsig::SigInputObj(particleType, pt, phi, dpt, dphi));
      } else if ( dynamic_cast<const pat::Muon*>(*particle) != 0 || dynamic_cast<const reco::Muon*>(*particle) != 0 ) {
	std::string particleType = "muon";
	double dpt, dphi;
	const reco::Track* muonTrack = 0;
	if ( dynamic_cast<const pat::Muon*>(*particle) != 0 ) {
	  const pat::Muon* muon = dynamic_cast<const pat::Muon*>(*particle);
	  if ( muon->track().isNonnull() && muon->track().isAvailable() ) muonTrack = muon->track().get();
	} else if ( dynamic_cast<const reco::Muon*>(*particle) != 0 ) {
	  const reco::Muon* muon = dynamic_cast<const reco::Muon*>(*particle);
	  if ( muon->track().isNonnull() && muon->track().isAvailable() ) muonTrack = muon->track().get();
	} else assert(0);
	if ( muonTrack ) {
	  dpt  = muonTrack->ptError();
	  dphi = pt*muonTrack->phiError(); // CV: pt*dphi is indeed correct
	} else {
	  // WARNING: SignAlgoResolutions::PFtype3 needs to be kept in sync with reco::PFCandidate::mu !!
	  dpt  = pfMEtResolution_->eval(metsig::PFtype3, metsig::ET,  pt, phi, eta);
	  dphi = pfMEtResolution_->eval(metsig::PFtype3, metsig::PHI, pt, phi, eta);
	}
	//std::cout << "muon: pt = " << pt << ", eta = " << eta << ", phi = " << phi
	//	  << " --> dpt = " << dpt << ", dphi = " << dphi << std::endl;
	metSignObjects.push_back(metsig::SigInputObj(particleType, pt, phi, dpt, dphi));
      } else if ( dynamic_cast<const pat::Tau*>(*particle) != 0 || dynamic_cast<const reco::PFTau*>(*particle) != 0 ) {
	// CV: use PFJet resolutions for PFTaus for now...
	//    (until PFTau specific resolutions are available)
	if ( dynamic_cast<const pat::Tau*>(*particle) != 0 ) {
	  const pat::Tau* pfTau = dynamic_cast<const pat::Tau*>(*particle);
	  //std::cout << "tau: pt = " << pt << ", eta = " << eta << ", phi = " << phi << std::endl;
	  metSignObjects.push_back(pfMEtResolution_->evalPFJet(pfTau->pfJetRef().get()));
	} else if ( dynamic_cast<const reco::PFTau*>(*particle) != 0  ) {
	  const reco::PFTau* pfTau = dynamic_cast<const reco::PFTau*>(*particle);
	  //std::cout << "tau: pt = " << pt << ", eta = " << eta << ", phi = " << phi << std::endl;
	  metSignObjects.push_back(pfMEtResolution_->evalPFJet(pfTau->jetRef().get()));
	} else assert(0);
      } else if ( dynamic_cast<const reco::PFJet*>(*particle) != 0 ) {
	const reco::PFJet* pfJet = dynamic_cast<const reco::PFJet*>(*particle);
	//std::cout << "pfJet: pt = " << pt << ", eta = " << eta << ", phi = " << phi << std::endl;
	metSignObjects.push_back(pfMEtResolution_->evalPFJet(pfJet));
      } else if ( dynamic_cast<const reco::PFCandidate*>(*particle) != 0 ) {
	const reco::PFCandidate* pfCandidate = dynamic_cast<const reco::PFCandidate*>(*particle);
	//std::cout << "pfCandidate: pt = " << pt << ", eta = " << eta << ", phi = " << phi << std::endl;
	metSignObjects.push_back(pfMEtResolution_->evalPF(pfCandidate));
      } else throw cms::Exception("addPFMEtSignObjects")
	  << "Invalid type of particle:"
	  << " valid types = { pat::Electron, pat::Muon, pat::Tau, reco::PFJet, reco::PFCandidate } !!\n";
    }
  }

 private:

  TMatrixD convert_matrix(const ROOT::Math::SMatrix2D& mat) const;
  TMatrixD convert_matrix(const TMatrixD& mat) const; 

  metsig::SignAlgoResolutions* pfMEtResolution_;

  int verbosity_;
};

#endif /* end of include guard: PFMETSIGNINTERFACEBASE_U3K9O5CO */
