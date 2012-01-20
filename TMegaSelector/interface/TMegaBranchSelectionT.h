/*
 * Template class for making a selection one single branch
 *
 * Different types of selectors should implement "selectValue"
 */

#ifndef TMEGABRANCHSELECTIONT_HENJDCUZ
#define TMEGABRANCHSELECTIONT_HENJDCUZ

#include <string>
#include "TTree.h"
#include "TBranch.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"

template<typename T>
class TMegaBranchSelectionT : public TMegaSelection {
  ClassDef(TMegaBranchSelectionT, 1);
  public:
    TMegaBranchSelectionT(){} // Default constructor for I/O
    /// Normal constructor giving branch name
    TMegaBranchSelectionT(const std::string& branchName)
      :branchName_(branchName){}

    // Set the current tree
    void init(TTree* tree) {
      tree_ = tree;
    }

    // When we load a new tree, get the branch address
    Bool_t notify() {
      if (!tree_)
        return false;
      branch_ = tree_->GetBranch(branchName_);
      return branch_;
    }

    Bool_t select(Long64_t entry) const {
      // Make sure the branch is pointing to our object
      branch_->SetAddress(&object_);
      branch_->GetEntry(entry);
      // Call the abstract decision function
      return selectValue(object_);
    }

    // The select function is still abstract as we don't know what to do with
    // our branch address.
    virtual Bool_t selectValue(const T& value) const=0;

  private:
    const std::string branchName_;
    TTree* tree_;
    TBranch* branch_;
    T object_;
};

#endif /* end of include guard: TMEGABRANCHSELECTIONT_HENJDCUZ */
