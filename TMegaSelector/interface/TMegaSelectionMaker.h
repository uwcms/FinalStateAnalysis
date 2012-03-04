/*
 *
 * Glue between the MegaSelector and MegaSelectionMaker.
 *
 * Allows the MegaSelector to build a factory which adds the built objects
 * directory to itself.
 *
 * Author: Evan K. Friis
 *
 */

#ifndef TMEGASELECTIONMAKER_VN6JHXNH
#define TMEGASELECTIONMAKER_VN6JHXNH

#include <memory>
#include <string>
#include "Rtypes.h"

namespace ROOT {
  class TBranchProxyDirector;
}
class TMegaSelector;
class TMegaSelectionFactory;

class TMegaSelectionMaker {
  public:
    TMegaSelectionMaker(TMegaSelector* selector,
        ROOT::TBranchProxyDirector* director);

    ~TMegaSelectionMaker();

    /// Build a cut on an integer branch and add it to [selection]
    void MakeIntCut(const std::string& selection, const std::string& branch,
        const std::string& op, Int_t value, bool abs=false) const;

    /// Build a cut on an float branch  and add it to [selection]
    void MakeFloatCut(const std::string& selection, const std::string& branch,
        const std::string& op, Float_t value, bool abs=false) const;

    /// Build a cut on an double branch and add it to [selection]
    void MakeDoubleCut(const std::string& selection, const std::string& branch,
        const std::string& op, Double_t value, bool abs=false) const;

    ClassDef( TMegaSelectionMaker, 1 );   // Builder of selectors

  private:
    TMegaSelector* selector_;
    std::auto_ptr<TMegaSelectionFactory> factory_;
};

#endif /* end of include guard: TMEGASELECTIONMAKER_VN6JHXNH */
