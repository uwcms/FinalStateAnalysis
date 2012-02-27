#ifndef TMEGASELECTIONSET_D8IXOPVD
#define TMEGASELECTIONSET_D8IXOPVD
/*
 * A *cached* group of selections on a TTree
 *
 * Inherits from TNamed, so it can be stored in a TList
 *
 * If SetCachePointers(...) is setup by the owning class, the result
 * will be cached.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "TNamed.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"
#include <vector>
#include <memory>

class TMegaSelectionSet : public TMegaSelection, public TNamed {
  public:
    TMegaSelectionSet();

    // Named constructor
    TMegaSelectionSet(const char* name, const char* title="");

    // Copy constructor
    TMegaSelectionSet(const TMegaSelectionSet& tocopy);

    // Clone constructor
    TMegaSelectionSet* Clone() const;

    // Clone constructor with new name
    TMegaSelectionSet* Clone(const char* newname) const;

    virtual ~TMegaSelectionSet();

    // This is overridden so the call gets dispatched to the subselections.
    void SetCachePointers(TTree** tree, Long_t* entry);

    // Add a new selection to the set.  Takes ownership.
    void AddSelection(std::auto_ptr<TMegaSelection> selector);

    // Add a new selection to the set.  Creates a clone and does not take
    // ownership of the passed object.
    void AddSelection(const TMegaSelection& selector);

    /// Compute the selection
    Bool_t Select();

    ClassDef( TMegaSelectionSet, 1 );

  private:
    bool lastResult_;
    std::vector<TMegaSelection*> subselections_;
};
#endif /* end of include guard: TMEGASELECTIONSET_D8IXOPVD */
