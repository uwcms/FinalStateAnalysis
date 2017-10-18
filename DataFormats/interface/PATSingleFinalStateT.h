#ifndef FinalStateAnalysis_DataFormats_PATSingleFinalStateT_h
#define FinalStateAnalysis_DataFormats_PATSingleFinalStateT_h

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

template<class T1>
class PATSingleFinalStateT : public PATFinalState {
  public:
    typedef T1 daughter1_type;

    PATSingleFinalStateT():PATFinalState(){}

    PATSingleFinalStateT(const edm::Ptr<T1>& p1, 
        const edm::Ptr<PATFinalStateEvent>& evt)
      :PATFinalState(p1->charge(), p1->p4(), evt) {
        p1_ = p1;
      }

    virtual PATSingleFinalStateT<T1>* clone() const {
      return new PATSingleFinalStateT<T1>(*this);
    }

    virtual const reco::Candidate* daughterUnsafe(size_t i) const {
      const reco::Candidate* output = NULL;
      if (i == 0)
        output = p1_.get();
      return output;
    }

    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const {
      reco::CandidatePtr output;
      if (i == 0)
        output = p1_;
      return output;
    }

    size_t numberOfDaughters() const { return 1; }

    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const {
      reco::CandidatePtr output;
      if (i == 0)
        output = p1_->userCand(tag);
      return output;
    }

    virtual bool daughterHasUserCand(size_t i,
        const std::string& tag) const {
      if (i == 0)
        return p1_->hasUserCand(tag);
      return false;
    }

    virtual const reco::CandidatePtrVector& daughterOverlaps(
        size_t i, const std::string& label) const {
      if (i == 0)
        return p1_->overlaps(label);
      throw cms::Exception("NullOverlaps") <<
        "PATSingleFinalState::daughterOverlaps(" << i << "," << label
        << ") is null!" << std::endl;
    }

  private:
    edm::Ptr<T1> p1_;
};


#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATSingleFinalStateT_h */
