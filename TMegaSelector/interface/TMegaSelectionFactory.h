#ifndef TMEGASELECTIONFACTORY_6BUR3EN9
#define TMEGASELECTIONFACTORY_6BUR3EN9
/*
 * TMegaSelectionFactory contains logic on how to build TMegaSelections.
 *
 * Author: Evan K. Friis, UW Madison
 */

#include <memory>
#include <string>

#include "Rtypes.h"

namespace ROOT {
  class TBranchProxyDirector;
}
class TMegaSelection;

class TMegaSelectionFactory {
  public:
    TMegaSelectionFactory(ROOT::TBranchProxyDirector* director);

    /// Build a cut on an integer branch
    std::auto_ptr<TMegaSelection> MakeIntCut(const std::string& branch,
        const std::string& op, Int_t value, bool abs=false) const;

    /// Build a cut on an float branch
    std::auto_ptr<TMegaSelection> MakeFloatCut(const std::string& branch,
        const std::string& op, Float_t value, bool abs=false) const;

    /// Build a cut on an double branch
    std::auto_ptr<TMegaSelection> MakeDoubleCut(const std::string& branch,
        const std::string& op, Double_t value, bool abs=false) const;

  private:
    ROOT::TBranchProxyDirector* director_;
};
#endif /* end of include guard: TMEGASELECTIONFACTORY_6BUR3EN9 */
