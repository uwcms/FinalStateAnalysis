#ifndef FinalStateAnalysis_DataFormats_PATMultiCandFinalState_h
#define FinalStateAnalysis_DataFormats_PATMultiCandFinalState_h

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

class PATMultiCandFinalState : public PATFinalState {
  public:
    PATMultiCandFinalState();

    PATMultiCandFinalState(const std::vector<reco::CandidatePtr>& cands,
        const edm::Ptr<PATFinalStateEvent>& evt);

    virtual PATMultiCandFinalState* clone() const;

    virtual const reco::Candidate* daughterUnsafe(size_t i) const;

    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const;

    size_t numberOfDaughters() const;

    /// These functions are not implemented (we don't have the concrete type of
    /// the daughters, so this will just throw an exception if used.)
    /// Perhaps in the future some reflex trickery could make it work.
    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const;

    virtual const reco::CandidatePtrVector& daughterOverlaps(
        size_t i, const std::string& label) const;

  private:
    std::vector<reco::CandidatePtr> cands_;
};

#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATMultiCandFinalState_h */
