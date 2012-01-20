#ifndef TMEGAOPERATORSELECTIONS_QMF0NE04
#define TMEGAOPERATORSELECTIONS_QMF0NE04

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaBranchSelectionT.h"

template<typename T, bool (*F)(const T&, const T&)>
class TMegaOperatorSelectionT : public TMegaBranchSelectionT<T> {
  public:
    TMegaOperatorSelectionT(){};
    TMegaOperatorSelectionT(const std::string& branchName, const T& cut)
      :TMegaBranchSelectionT(branchName),cut_(cut){}
    Bool_t selectValue(const T& value) const {
      return F(value, cut);
    }
  private:
    const T cut_;
};

namespace {
  inline bool Int_tGT(const Int_t& value, const Int_t& cut) { return value > cut; }
  inline bool Int_tLT(const Int_t& value, const Int_t& cut) { return value < cut; }
  inline bool Int_tGEQ(const Int_t& value, const Int_t& cut) { return value >= cut; }
  inline bool Int_tLEQ(const Int_t& value, const Int_t& cut) { return value <= cut; }

  inline bool Float_tGT(const Float_t& value, const Float_t& cut) { return value > cut; }
  inline bool Float_tLT(const Float_t& value, const Float_t& cut) { return value < cut; }
  inline bool Float_tGEQ(const Float_t& value, const Float_t& cut) { return value >= cut; }
  inline bool Float_tLEQ(const Float_t& value, const Float_t& cut) { return value <= cut; }
}

typedef TMegaOperatorSelectionT<Int_t, Int_tGT> TMegaIntGT;
typedef TMegaOperatorSelectionT<Int_t, Int_tGEQ> TMegaIntGEQ;
typedef TMegaOperatorSelectionT<Int_t, Int_tLT> TMegaIntLT;
typedef TMegaOperatorSelectionT<Int_t, Int_tLEQ> TMegaIntLEQ;

typedef TMegaOperatorSelectionT<Int_t, Int_tGT> TMegaIntGT;
typedef TMegaOperatorSelectionT<Int_t, Int_tGEQ> TMegaIntGEQ;
typedef TMegaOperatorSelectionT<Int_t, Int_tLT> TMegaIntLT;
typedef TMegaOperatorSelectionT<Int_t, Int_tLEQ> TMegaIntLEQ;

#endif /* end of include guard: TMEGAOPERATORSELECTIONS_QMF0NE04 */
