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
}

typedef TMegaOperatorSelectionT<Int_t, GreaterThan> TMegaSelectGTI;
typedef TMegaOperatorSelectionT<Int_t, LessThan> TMegaSelectLTI;
typedef TMegaOperatorSelectionT<Int_t, GreaterEqThan> TMegaSelectGEQI;
typedef TMegaOperatorSelectionT<Int_t, LessEqThan> TMegaSelectLEQI;

typedef TMegaOperatorSelectionT<Int_t, AbsGreaterThan> TMegaSelectAbsGTI;
typedef TMegaOperatorSelectionT<Int_t, AbsLessThan> TMegaSelectAbsLTI;
typedef TMegaOperatorSelectionT<Int_t, AbsGreaterEqThan> TMegaSelectAbsGEQI;
typedef TMegaOperatorSelectionT<Int_t, AbsLessEqThan> TMegaSelectAbsLEQI;

typedef TMegaOperatorSelectionT<Float_t, GreaterThan> TMegaSelectGTF;
typedef TMegaOperatorSelectionT<Float_t, LessThan> TMegaSelectLTF;
typedef TMegaOperatorSelectionT<Float_t, GreaterEqThan> TMegaSelectGEQF;
typedef TMegaOperatorSelectionT<Float_t, LessEqThan> TMegaSelectLEQF;

typedef TMegaOperatorSelectionT<Float_t, AbsGreaterThan> TMegaSelectAbsGTF;
typedef TMegaOperatorSelectionT<Float_t, AbsLessThan> TMegaSelectAbsLTF;
typedef TMegaOperatorSelectionT<Float_t, AbsGreaterEqThan> TMegaSelectAbsGEQF;
typedef TMegaOperatorSelectionT<Float_t, AbsLessEqThan> TMegaSelectAbsLEQF;

typedef TMegaOperatorSelectionT<Double_t, GreaterThan> TMegaSelectGTD;
typedef TMegaOperatorSelectionT<Double_t, LessThan> TMegaSelectLTD;
typedef TMegaOperatorSelectionT<Double_t, GreaterEqThan> TMegaSelectGEQD;
typedef TMegaOperatorSelectionT<Double_t, LessEqThan> TMegaSelectLEQD;

typedef TMegaOperatorSelectionT<Double_t, AbsGreaterThan> TMegaSelectAbsGTD;
typedef TMegaOperatorSelectionT<Double_t, AbsLessThan> TMegaSelectAbsLTD;
typedef TMegaOperatorSelectionT<Double_t, AbsGreaterEqThan> TMegaSelectAbsGEQD;
typedef TMegaOperatorSelectionT<Double_t, AbsLessEqThan> TMegaSelectAbsLEQD;

#endif /* end of include guard: TMEGAOPERATORSELECTIONS_QMF0NE04 */
