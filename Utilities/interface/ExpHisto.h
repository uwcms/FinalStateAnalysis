#ifndef FinalStateAnalysis_Utilities_ExpHisto_h
#define FinalStateAnalysis_Utilities_ExpHisto_h

#include "FinalStateAnalysis/Utilities/interface/Histo.h"
#include <boost/shared_ptr.hpp>

class TH1*;

namespace ek {

template<typename T>
class ExpHisto1D : public Histo<T> {
  public:
    ExpHisto(const edm::ParameterSet& pset, TFileDirectory& fs);
    void fill(const T& t, double weight = 1.0,
        const edm::EventBase* evt = NULL, const edm::EventSetup* es = NULL);
  private:
    boost::shared_ptr<TH1F*> histogram_;
    boost::shared_ptr<T> xExpr_;
};

}

#endif /* end of include guard: FinalStateAnalysis_Utilities_ExpHisto_h */
