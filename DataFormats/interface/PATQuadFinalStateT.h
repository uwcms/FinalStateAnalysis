#ifndef FinalStateAnalysis_DataFormats_PATQuadFinalStateT_h
#define FinalStateAnalysis_DataFormats_PATQuadFinalStateT_h

class PATFinalStateProxy;
//class PATMultiCandFinalState;

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalStateFwd.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

template<class T1, class T2, class T3, class T4>
class PATQuadFinalStateT : public PATFinalState {
  public:
    typedef T1 daughter1_type;
    typedef T2 daughter2_type;
    typedef T3 daughter3_type;
    typedef T4 daughter4_type;

    PATQuadFinalStateT():PATFinalState(){}

    PATQuadFinalStateT(const edm::Ptr<T1>& p1, const edm::Ptr<T2>& p2,
        const edm::Ptr<T3>& p3,
        const edm::Ptr<T4>& p4,
        const edm::Ptr<PATFinalStateEvent>& evt)
      :PATFinalState(
          p1->charge() + p2->charge() + p3->charge() + p4->charge(),
          p1->p4() + p2->p4() + p3->p4() + p4->p4(), evt) {
        p1_ = p1;
        p2_ = p2;
        p3_ = p3;
        p4_ = p4;
      }

    virtual PATQuadFinalStateT<T1, T2, T3, T4>* clone() const {
      return new PATQuadFinalStateT<T1, T2, T3, T4>(*this);
    }

    virtual const reco::Candidate* daughterUnsafe(size_t i) const {
      const reco::Candidate* output = NULL;
      if (i == 0)
        output = p1_.get();
      else if (i == 1)
        output = p2_.get();
      else if (i == 2)
        output = p3_.get();
      else if (i == 3)
        output = p4_.get();
      return output;
    }

    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const {
      if (i == 0)
        return p1_;
      else if (i == 1)
        return p2_;
      else if (i == 2)
        return p3_;
      else if (i == 3)
        return p4_;
      else
        return reco::CandidatePtr();
    }

    size_t numberOfDaughters() const { return 4; }

    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const {
      if (i == 0)
        return p1_->userCand(tag);
      else if (i == 1)
        return p2_->userCand(tag);
      else if (i == 2)
        return p3_->userCand(tag);
      else if (i == 3)
        return p4_->userCand(tag);
      else
        return reco::CandidatePtr();
    }

    virtual bool daughterHasUserCand(size_t i,
                                     const std::string& tag) const
      {
      if (i == 0)
        return p1_->hasUserCand(tag);
      else if (i == 1)
        return p2_->hasUserCand(tag);
      else if (i == 2)
        return p3_->hasUserCand(tag);
      else if (i == 3)
        return p4_->hasUserCand(tag);
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
      else if (i == 3)
        return p4_->overlaps(label);
      throw cms::Exception("NullOverlaps") <<
        "PATQuadFinalState::daughterOverlaps(" << i << "," << label
        << ") is null!" << std::endl;
    }

    

  private:
    edm::Ptr<T1> p1_;
    edm::Ptr<T2> p2_;
    edm::Ptr<T3> p3_;
    edm::Ptr<T4> p4_;
};


#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATQuadFinalStateT_h */
