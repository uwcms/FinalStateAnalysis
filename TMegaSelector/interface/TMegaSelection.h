/*
 * Abstract base class for a selection on a TTree.
 *
 * Optionally holds a pointer to the current TTree and entry number in some
 * owning class.  The class can keep track if this value has changed since the
 * last call to emitChanged();
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#ifndef TMEGASELECTION_M8MSCS4R
#define TMEGASELECTION_M8MSCS4R

#include "Rtypes.h"

class TTree;

class TMegaSelection {
  public:
    TMegaSelection():currentTTree_(NULL){}
    virtual ~TMegaSelection(){}
    virtual TMegaSelection* Clone() const=0;

    /// Apply the selection implementation
    virtual Bool_t Select() =0;

    virtual void SetCachePointers(TTree** tree, Long_t* entry) {
      currentEntryPtr_ = entry;
      currentTTree_ = tree;
    }

    /// Check if "current" tree and entry has changed or if the cache is not set
    /// up. Emits true *once*
    /// when this happens.  Calling this function will update the values.
    Bool_t emitChanged() {
      // Check if we aren't caching at all
      if (currentTTree_ == NULL)
        return true;
      // Check if nothing has changed
      if (*currentTTree_ == lastTTree_ && *currentEntryPtr_ == lastEntry_)
        return false;
      lastTTree_ = *currentTTree_;
      lastEntry_ = *currentEntryPtr_;
      return true;
    }

    ClassDef( TMegaSelection, 1 );

  private:
    TTree* lastTTree_;
    Long_t lastEntry_;
    Long_t* currentEntryPtr_;
    TTree** currentTTree_;
};

#endif /* end of include guard: TMEGASELECTION_M8MSCS4R */
