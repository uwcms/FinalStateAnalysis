/*
 * Define a set of TMegaSelections which operate a simple cut on a single
 * branch.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */
#ifndef TMEGAOPERATORSELECTIONS_QMF0NE04
#define TMEGAOPERATORSELECTIONS_QMF0NE04

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaBranchSelectionT.h"
#include <cmath>

template<typename T, template <typename> class F>
class TMegaOperatorSelectionT : public TMegaBranchSelectionT<T> {
  public:
    TMegaOperatorSelectionT(){};
    TMegaOperatorSelectionT(ROOT::TBranchProxyDirector* director,
        const char* name, const T& cut)
      :TMegaBranchSelectionT<T>(director, name),cut_(cut){}

    virtual TMegaOperatorSelectionT<T,F>* Clone() const {
      return new TMegaOperatorSelectionT<T,F>(*this);
    }

    // Apply our functor
    Bool_t SelectValue(const T& value) const {
      return functor_(value, cut_);
    }
  private:
    F<T> functor_;
    T cut_;
};

namespace tmega {
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

  template<typename T> struct AbsGreaterThan {
    Bool_t operator()(const T& a, const T& b) const { return std::abs(a) > b; }
  };

  template<typename T> struct AbsGreaterEqThan {
    Bool_t operator()(const T& a, const T& b) const { return std::abs(a) >= b; }
  };

  template<typename T> struct AbsLessThan {
    Bool_t operator()(const T& a, const T& b) const { return std::abs(a) < b; }
  };

  template<typename T> struct AbsLessEqThan {
    Bool_t operator()(const T& a, const T& b) const { return std::abs(a) <= b; }
  };

  template<typename T> struct EqualTo {
    Bool_t operator()(const T& a, const T& b) const { return a == b; }
  };

  template<typename T> struct AbsEqualTo {
    Bool_t operator()(const T& a, const T& b) const { return std::abs(a) == b; }
  };

  template<typename T> struct NotEqualTo {
    Bool_t operator()(const T& a, const T& b) const { return a != b; }
  };

  template<typename T> struct AbsNotEqualTo {
    Bool_t operator()(const T& a, const T& b) const { return std::abs(a) != b; }
  };
}

#endif /* end of include guard: TMEGAOPERATORSELECTIONS_QMF0NE04 */
