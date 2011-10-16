#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"


PATMultiCandFinalState::PATMultiCandFinalState():PATFinalState(){}

PATMultiCandFinalState::PATMultiCandFinalState(
    const std::vector<reco::CandidatePtr>& cands,
    const edm::Ptr<pat::MET>& met, const edm::Ptr<reco::Vertex>& vertex,
    const edm::Ptr<PATFinalStateEvent>& evt):
  PATFinalState(0, reco::Candidate::LorentzVector(), met, vertex, evt),
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
  throw cms::Exception("NotImplemented") <<
    "The daughterUserCand functionality is not implemented for instances of" <<
    " PATMultiCandFinalState." << std::endl;
}
