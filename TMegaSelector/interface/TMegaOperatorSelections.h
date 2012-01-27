#ifndef TMEGAOPERATORSELECTIONS_QMF0NE04
#define TMEGAOPERATORSELECTIONS_QMF0NE04

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaBranchSelectionT.h"

template<typename T, template <typename> class F>
class TMegaOperatorSelectionT : public TMegaBranchSelectionT<T> {
  public:
    TMegaOperatorSelectionT(){};
    TMegaOperatorSelectionT(const std::string& branchName, const T& cut)
      :TMegaBranchSelectionT(branchName),cut_(cut){}
    Bool_t selectValue(const T& value) const {
      return functor_(value, cut_);
    }
  private:
    const F<T> functor_;
    const T cut_;
};

namespace {
  template<typename T> struct GreaterThan {
    Bool_t operator()(const T& a, const T& b) const { return a > b; }
  };

  template<typename T> struct GreaterEqThan {
    Bool_t operator()(const T& a, const T& b) const { return a >= b; }
  };

  template<typename T> struct LessThan {
    Bool_t operator()(const T& a, const T& b) const { return a < b; }
  };

  template<typename T> struct LessEqThan {
    Bool_t operator()(const T& a, const T& b) const { return a <= b; }
  };



#endif /* end of include guard: TMEGAOPERATORSELECTIONS_QMF0NE04 */
