/*
 * A *cached* group of selections on a TTree
 *
 * Inherits from TNamed, so it can be stored in a TList
 *
 * Note that "ResetCache" must be called at the end of each entry!
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "TNamed.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"
#include <vector>

class TMegaSelectionSet : public TMegaSelection, public TNamed {
  public:
    TMegaSelectionSet();

    // Named constructor
    TMegaSelectionSet(const char* name, const char* title="");

    // Copy constuctor
    TMegaSelectionSet(const TMegaSelectionSet& tocopy);

    // Clone constructor
    TMegaSelectionSet* Clone() const;

    // Clone constructor with new name
    TMegaSelectionSet* Clone(const char* newname) const;

    virtual ~TMegaSelectionSet();

    // Add a clone of a new selection to the set.  Does not take ownership.
    void AddSelection(const TMegaSelection& selector);

    /// Compute the selection
    Bool_t Select();

    /// Reset cache
    void ResetCache();

  private:
    bool isCached_;
    bool lastResult_;
    std::vector<TMegaSelection*> subselections_;
};
