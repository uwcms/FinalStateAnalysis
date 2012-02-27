#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionFactory.h"

#include <stdexcept>

#include <TBranchProxyDirector.h>
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaOperatorSelections.h"

TMegaSelectionFactory::TMegaSelectionFactory(ROOT::TBranchProxyDirector* dir)
  :director_(dir){}

  // Main meat
namespace {
  // put all the verbosity here
  template<typename T, template <typename> class F>
  std::auto_ptr<TMegaSelection> buildOpCut(
      ROOT::TBranchProxyDirector* director,
      const std::string& branch, const T& value) {
    return std::auto_ptr<TMegaSelection>(new
        TMegaOperatorSelectionT<T, F>(director, branch.c_str(), value));
  }

  template<typename T>
    std::auto_ptr<TMegaSelection> makeOperatorCutImpl(
        ROOT::TBranchProxyDirector* dir, const std::string& branch,
        const std::string& op, const T& value, bool isAbs) {

      if (!isAbs) {
        if (op == ">") {
          return buildOpCut<T, tmega::GreaterThan>(dir, branch, value);
        } else if (op == ">=") {
          return buildOpCut<T, tmega::GreaterEqThan>(dir, branch, value);
        } else if (op == "<") {
          return buildOpCut<T, tmega::LessThan>(dir, branch, value);
        } else if (op == "<=") {
          return buildOpCut<T, tmega::LessEqThan>(dir, branch, value);
        } else if (op == "==") {
          return buildOpCut<T, tmega::EqualTo>(dir, branch, value);
        } else if (op == "!=") {
          return buildOpCut<T, tmega::NotEqualTo>(dir, branch, value);
        }
      } else {
        if (op == ">") {
          return buildOpCut<T, tmega::AbsGreaterThan>(dir, branch, value);
        } else if (op == ">=") {
          return buildOpCut<T, tmega::AbsGreaterEqThan>(dir, branch, value);
        } else if (op == "<") {
          return buildOpCut<T, tmega::AbsLessThan>(dir, branch, value);
        } else if (op == "<=") {
          return buildOpCut<T, tmega::AbsLessEqThan>(dir, branch, value);
        } else if (op == "==") {
          return buildOpCut<T, tmega::AbsEqualTo>(dir, branch, value);
        } else if (op == "!=") {
          return buildOpCut<T, tmega::AbsNotEqualTo>(dir, branch, value);
        }
      }

      throw std::runtime_error("Unknown opcode: " + op);
    }

}

std::auto_ptr<TMegaSelection> TMegaSelectionFactory::MakeIntCut(
    const std::string& branch, const std::string& op, Int_t value, bool abs)
  const {
    return makeOperatorCutImpl<Int_t>(director_, branch, op, value, abs);
}

std::auto_ptr<TMegaSelection> TMegaSelectionFactory::MakeFloatCut(
    const std::string& branch, const std::string& op, Float_t value, bool abs)
  const {
    return makeOperatorCutImpl<Float_t>(director_, branch, op, value, abs);
}

std::auto_ptr<TMegaSelection> TMegaSelectionFactory::MakeDoubleCut(
    const std::string& branch, const std::string& op, Double_t value, bool abs)
  const {
    return makeOperatorCutImpl<Double_t>(director_, branch, op, value, abs);
}

