#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

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
  const reco::Candidate* output = NULL;
  if (i < cands_.size())
    output = cands_[i].get();
  return output;
}

const reco::CandidatePtr
PATMultiCandFinalState::daughterPtrUnsafe(size_t i) const {
  reco::CandidatePtr output;
  if (i < cands_.size())
    output = cands_[i];
  return output;
}

size_t PATMultiCandFinalState::numberOfDaughters() const {
  return cands_.size();
}

reco::CandidatePtr PATMultiCandFinalState::daughterUserCandUnsafe(size_t i,
    const std::string& tag) const {
  reco::CandidatePtr theCand = cands_.at(i); // will throw OOB exception

  if( dynamic_cast<const pat::Electron*>(theCand.get()) ) {
    edm::Ptr<pat::Electron> asEle(theCand);
    return asEle->userCand(tag); 
  } else if ( dynamic_cast<const pat::Muon*>(theCand.get()) ) {
    edm::Ptr<pat::Muon> asMuon(theCand);
    return asMuon->userCand(tag); 
  } else if ( dynamic_cast<const pat::Tau*>(theCand.get()) ) {
    edm::Ptr<pat::Tau> asTau(theCand);
    return asTau->userCand(tag); 
  } else if ( dynamic_cast<const pat::Photon*>(theCand.get()) ) {
    edm::Ptr<pat::Photon> asPho(theCand);
    return asPho->userCand(tag); 
  } else if ( dynamic_cast<const pat::Jet*>(theCand.get()) ) {
    edm::Ptr<pat::Jet> asJet(theCand);
    return asJet->userCand(tag); 
  } else if ( dynamic_cast<const pat::MET*>(theCand.get()) ) {
    edm::Ptr<pat::MET> asMET(theCand);
    return asMET->userCand(tag); 
  } else {
    throw cms::Exception("Uncastable") 
      << "The edm::Ptr at index " << i 
      << "is not castable to a PAT Object." << std::endl;
  }
}

const reco::CandidatePtrVector& PATMultiCandFinalState::daughterOverlaps(
    size_t i, const std::string& label) const {
  reco::CandidatePtr theCand = cands_.at(i); // will throw OOB exception

  if( dynamic_cast<const pat::Electron*>(theCand.get()) ) {
    edm::Ptr<pat::Electron> asEle(theCand);
    return asEle->overlaps(label); 
  } else if ( dynamic_cast<const pat::Muon*>(theCand.get()) ) {
    edm::Ptr<pat::Muon> asMuon(theCand);
    return asMuon->overlaps(label); 
  } else if ( dynamic_cast<const pat::Tau*>(theCand.get()) ) {
    edm::Ptr<pat::Tau> asTau(theCand);
    return asTau->overlaps(label); 
  } else if ( dynamic_cast<const pat::Photon*>(theCand.get()) ) {
    edm::Ptr<pat::Photon> asPho(theCand);
    return asPho->overlaps(label); 
  } else if ( dynamic_cast<const pat::Jet*>(theCand.get()) ) {
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
