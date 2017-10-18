#ifndef FinalStateAnalysis_DataFormats_PATPairFinalStateT_h
#define FinalStateAnalysis_DataFormats_PATPairFinalStateT_h

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

template<class T1, class T2>
class PATPairFinalStateT : public PATFinalState {
  public:
    typedef T1 daughter1_type;
    typedef T2 daughter2_type;

    PATPairFinalStateT():PATFinalState(){}

    PATPairFinalStateT(const edm::Ptr<T1>& p1, const edm::Ptr<T2>& p2,
        const edm::Ptr<PATFinalStateEvent>& evt)
      :PATFinalState(p1->charge() + p2->charge(),
          p1->p4() + p2->p4(), evt) {
        p1_ = p1;
        p2_ = p2;
      }

    virtual PATPairFinalStateT<T1, T2>* clone() const {
      return new PATPairFinalStateT<T1, T2>(*this);
    }

    virtual const reco::Candidate* daughterUnsafe(size_t i) const {
      const reco::Candidate* output = NULL;
      if (i == 0)
        output = p1_.get();
      else if (i == 1)
        output = p2_.get();
      return output;
    }

    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const {
      reco::CandidatePtr output;
      if (i == 0)
        output = p1_;
      else if (i == 1)
        output = p2_;
      return output;
    }

    size_t numberOfDaughters() const { return 2; }

    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const {
      reco::CandidatePtr output;
      if (i == 0)
        output = p1_->userCand(tag);
      else if (i == 1)
        output = p2_->userCand(tag);
      return output;
    }

    virtual bool daughterHasUserCand(size_t i,
        const std::string& tag) const {
      if (i == 0)
        return p1_->hasUserCand(tag);
      else if (i == 1)
        return p2_->hasUserCand(tag);
      return false;
    }

    virtual const reco::CandidatePtrVector& daughterOverlaps(
        size_t i, const std::string& label) const {
      if (i == 0)
        return p1_->overlaps(label);
      else if (i == 1)
        return p2_->overlaps(label);
      throw cms::Exception("NullOverlaps") <<
        "PATPairFinalState::daughterOverlaps(" << i << "," << label
        << ") is null!" << std::endl;
    }

  private:
    edm::Ptr<T1> p1_;
    edm::Ptr<T2> p2_;
};


#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATPairFinalStateT_h */
