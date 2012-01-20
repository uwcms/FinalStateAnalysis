/*
 * Abstract base class for a cached selection on a TTree.
 *
 * Mimics the interface of a TSelector.
 *
 */

#ifndef TMEGASELECTION_M8MSCS4R
#define TMEGASELECTION_M8MSCS4R

#include "TObject.h"
class TTree;

class TMegaSelection : public TObject {
  public:
    TMegaSelection():lastEntry_(-1){}
    ClassDef(TMegaSelection, 1);
    virtual ~TMegaSelection(){}

    /// Analogous to TSelector::Init
    void Init(TTree* tree) {
      this->init(tree);
    }

    /// Analogous to TSelector::Notify
    Bool_t Notify() {;
      // Clear cache
      lastEntry_ = -1;
      return this->notify();
    }

    /// Apply the selection on this entry.  Result is cached
    Bool_t Select(Long64_t entry) const {
      if (entry == lastEntry_)
        return lastResult_;
      return this->select();
    }

    /**************************************************************************
     * Abstract methods
     **************************************************************************/

    /// Apply the selection implementation
    virtual Bool_t select() const=0;
    /// Initialize given a new Tree
    virtual void init(TTree* tree)=0;
    /// Update the branch address on file change
    virtual Bool_t notify()=0;

  private:
    mutable Long64_t lastEntry_;
    mutable bool lastResult_;
};

#endif /* end of include guard: TMEGASELECTION_M8MSCS4R */
