#ifndef FinalStateAnalysis_DataFormats_PATTripletFinalStateT_h
#define FinalStateAnalysis_DataFormats_PATTripletFinalStateT_h

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

template<class T1, class T2, class T3>
class PATTripletFinalStateT : public PATFinalState {
  public:
    typedef T1 daughter1_type;
    typedef T2 daughter2_type;
    typedef T3 daughter3_type;

    PATTripletFinalStateT():PATFinalState(){}

    PATTripletFinalStateT(const edm::Ptr<T1>& p1, const edm::Ptr<T2>& p2,
        const edm::Ptr<T3>& p3,
        const edm::Ptr<PATFinalStateEvent>& evt)
      :PATFinalState(p1->charge() + p2->charge() + p3->charge(),
          p1->p4() + p2->p4() + p3->p4(), evt) {
        p1_ = p1;
        p2_ = p2;
        p3_ = p3;
      }

    virtual PATTripletFinalStateT<T1, T2, T3>* clone() const {
      return new PATTripletFinalStateT<T1, T2, T3>(*this);
    }

    virtual const reco::Candidate* daughterUnsafe(size_t i) const {
      const reco::Candidate* output = NULL;
      if (i == 0)
        output = p1_.get();
      else if (i == 1)
        output = p2_.get();
      else if (i == 2)
        output = p3_.get();
      return output;
    }

    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const {
      if (i == 0)
        return p1_;
      else if (i == 1)
        return p2_;
      else if (i == 2)
        return p3_;
      else
        return reco::CandidatePtr();
    }

    size_t numberOfDaughters() const { return 3; }

    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const {
      if (i == 0)
        return p1_->userCand(tag);
      else if (i == 1)
        return p2_->userCand(tag);
      else if (i == 2)
        return p3_->userCand(tag);
      else
        return reco::CandidatePtr();
    }

    virtual bool daughterHasUserCand(size_t i,
        const std::string& tag) const {
      if (i == 0)
        return p1_->hasUserCand(tag);
      else if (i == 1)
        return p2_->hasUserCand(tag);
      else if (i == 2)
        return p3_->hasUserCand(tag);
      else
        return false;
    }

    virtual const reco::CandidatePtrVector& daughterOverlaps(
        size_t i, const std::string& label) const {
      if (i == 0)
        return p1_->overlaps(label);
      else if (i == 1)
        return p2_->overlaps(label);
      else if (i == 2)
        return p3_->overlaps(label);
      throw cms::Exception("NullOverlaps") <<
        "PATTripletFinalState::daughterOverlaps(" << i << "," << label
        << ") is null!" << std::endl;
    }

  private:
    edm::Ptr<T1> p1_;
    edm::Ptr<T2> p2_;
    edm::Ptr<T3> p3_;
};


#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATTripletFinalStateT_h */
