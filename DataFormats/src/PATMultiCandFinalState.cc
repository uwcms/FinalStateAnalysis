#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "TLorentzVector.h"

PATMultiCandFinalState::PATMultiCandFinalState():PATFinalState(){}

PATMultiCandFinalState::PATMultiCandFinalState(
    const std::vector<reco::CandidatePtr>& cands,
    const edm::Ptr<PATFinalStateEvent>& evt):
  PATFinalState(0, reco::Candidate::LorentzVector(), evt),
  cands_(cands) {
  
  // Setup p4 in base class
  int charge = 0;
  reco::Candidate::LorentzVector totalP4;
  for (size_t i = 0; i < cands_.size(); ++i) {
    charge += cands_[i]->charge();
    totalP4 += cands_[i]->p4();
  }
  this->setCharge(charge);
  this->setP4(totalP4);
}

PATMultiCandFinalState* PATMultiCandFinalState::clone() const {
  return new PATMultiCandFinalState(*this);
}

const reco::Candidate* PATMultiCandFinalState::daughterUnsafe(size_t i) const {
  try {
    return cands_.at(i).get();
  } catch ( std::out_of_range &oor) {
    std::cerr << "Daughter index out of range! : " << oor.what() << std::endl;
    return NULL;
  }
}

const reco::CandidatePtr
PATMultiCandFinalState::daughterPtrUnsafe(size_t i) const {
  try {
    return cands_.at(i);
  } catch ( std::out_of_range &oor) {
    std::cerr << "Daughter index out of range! : " << oor.what() << std::endl;
    return reco::CandidatePtr();
  }
}

reco::CandidatePtr PATMultiCandFinalState::daughterUserCandUnsafe(size_t i,
    const std::string& tag) const {
  reco::CandidatePtr theCand;

  try {// will throw OOB exception
    theCand = cands_.at(i);
  } catch ( std::out_of_range &oor ) {
    throw cms::Exception("CandidateIndexOutOfRange") 
      << "The edm::Ptr at index " << i 
      << "is out of range for candidate with "
      << cands_.size() << " daughters." << std::endl;
  }

  if( theCand->isElectron() && 
      dynamic_cast<const pat::Electron*>(theCand.get()) ) {
    edm::Ptr<pat::Electron> asEle(theCand);
    return asEle->userCand(tag); 
  } else if ( theCand->isMuon() &&
	      dynamic_cast<const pat::Muon*>(theCand.get()) ) {
    edm::Ptr<pat::Muon> asMuon(theCand);
    return asMuon->userCand(tag); 
  } else if ( abs(theCand->pdgId()) == 15 && 
	      dynamic_cast<const pat::Tau*>(theCand.get()) ) {
    edm::Ptr<pat::Tau> asTau(theCand);
    return asTau->userCand(tag); 
  } else if ( theCand->isPhoton() &&
	      dynamic_cast<const pat::Photon*>(theCand.get()) ) {
    edm::Ptr<pat::Photon> asPho(theCand);
    return asPho->userCand(tag); 
  } else if ( theCand->isJet() &&
	      dynamic_cast<const pat::Jet*>(theCand.get()) ) {
    edm::Ptr<pat::Jet> asJet(theCand);
    return asJet->userCand(tag); 
  } else if ( dynamic_cast<const pat::MET*>(theCand.get()) ) { //no lazy false
    edm::Ptr<pat::MET> asMET(theCand);
    return asMET->userCand(tag); 
  } else {
    throw cms::Exception("Uncastable") 
      << "The edm::Ptr at index " << i 
      << "is not castable to a PAT Object." << std::endl;
  }
}

bool PATMultiCandFinalState::daughterHasUserCand(size_t i,
    const std::string& tag) const {
  reco::CandidatePtr theCand;

  try {// will throw OOB exception
    theCand = cands_.at(i);
  } catch ( std::out_of_range &oor ) {
    throw cms::Exception("CandidateIndexOutOfRange") 
      << "The edm::Ptr at index " << i 
      << "is out of range for candidate with "
      << cands_.size() << " daughters." << std::endl;
  }

  if( theCand->isElectron() && 
      dynamic_cast<const pat::Electron*>(theCand.get()) ) {
    edm::Ptr<pat::Electron> asEle(theCand);
    return asEle->hasUserCand(tag); 
  } else if ( theCand->isMuon() &&
	      dynamic_cast<const pat::Muon*>(theCand.get()) ) {
    edm::Ptr<pat::Muon> asMuon(theCand);
    return asMuon->hasUserCand(tag); 
  } else if ( abs(theCand->pdgId()) == 15 && 
	      dynamic_cast<const pat::Tau*>(theCand.get()) ) {
    edm::Ptr<pat::Tau> asTau(theCand);
    return asTau->hasUserCand(tag); 
  } else if ( theCand->isPhoton() &&
	      dynamic_cast<const pat::Photon*>(theCand.get()) ) {
    edm::Ptr<pat::Photon> asPho(theCand);
    return asPho->hasUserCand(tag); 
  } else if ( theCand->isJet() &&
	      dynamic_cast<const pat::Jet*>(theCand.get()) ) {
    edm::Ptr<pat::Jet> asJet(theCand);
    return asJet->hasUserCand(tag); 
  } else if ( dynamic_cast<const pat::MET*>(theCand.get()) ) { //no lazy false
    edm::Ptr<pat::MET> asMET(theCand);
    return asMET->hasUserCand(tag); 
  } else {
    throw cms::Exception("Uncastable") 
      << "The edm::Ptr at index " << i 
      << "is not castable to a PAT Object." << std::endl;
  }
}

const reco::CandidatePtrVector& PATMultiCandFinalState::daughterOverlaps(
    size_t i, const std::string& label) const {
  reco::CandidatePtr theCand; // will throw OOB exception

  try {// will throw OOB exception
    theCand = cands_.at(i);
  } catch ( std::out_of_range &oor ) {
    throw cms::Exception("CandidateIndexOutOfRange") 
      << "The edm::Ptr at index " << i 
      << "is out of range for candidate with "
      << cands_.size() << " daughters." << std::endl;
  }

  if( theCand->isElectron() &&
      dynamic_cast<const pat::Electron*>(theCand.get()) ) {
    edm::Ptr<pat::Electron> asEle(theCand);
    return asEle->overlaps(label); 
  } else if ( theCand->isMuon() && 
	      dynamic_cast<const pat::Muon*>(theCand.get()) ) {
    edm::Ptr<pat::Muon> asMuon(theCand);
    return asMuon->overlaps(label); 
  } else if ( abs(theCand->pdgId()) == 15 && 
	      dynamic_cast<const pat::Tau*>(theCand.get()) ) {
    edm::Ptr<pat::Tau> asTau(theCand);
    return asTau->overlaps(label); 
  } else if ( theCand->isPhoton() && 
	      dynamic_cast<const pat::Photon*>(theCand.get()) ) {
    edm::Ptr<pat::Photon> asPho(theCand);
    return asPho->overlaps(label); 
  } else if ( theCand->isJet() && 
	      dynamic_cast<const pat::Jet*>(theCand.get()) ) {
    edm::Ptr<pat::Jet> asJet(theCand);
    return asJet->overlaps(label); 
  } else if ( dynamic_cast<const pat::MET*>(theCand.get()) ) {
    edm::Ptr<pat::MET> asMET(theCand);
    return asMET->overlaps(label); 
  } else {
    throw cms::Exception("Uncastable") 
      << "The edm::Ptr at index " << i 
      << "is not castable to a PAT Object." << std::endl;
  }
}

const double PATMultiCandFinalState::daughterCosThetaStar(
      size_t i) const
{
  reco::Candidate::LorentzVector totalP4 = p4();
  TLorentzVector sub_cand_p4(totalP4.x(),totalP4.y(),totalP4.z(),totalP4.T()); //reco::Candidate::LorentzVector does not boost, that I know
  reco::Candidate::LorentzVector dauP4   = daughterUnsafe(i)->p4();
  TLorentzVector dau_p4(dauP4.x(), dauP4.y(), dauP4.z(), dauP4.T());

  dau_p4.Boost(-sub_cand_p4.BoostVector()); //boost in sub-candidate CM frame
  return (dau_p4.Vect().Unit()).Dot(sub_cand_p4.Vect().Unit());
}
