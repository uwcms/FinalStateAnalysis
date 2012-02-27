#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionSet.h"
#include <iostream>

// Default ctor for I/O
TMegaSelectionSet::TMegaSelectionSet(){}

TMegaSelectionSet::TMegaSelectionSet(const char* name, const char* title)
  :TNamed(name, title){}

// Destructor - clean up owned selections
TMegaSelectionSet::~TMegaSelectionSet() {
  for (size_t i = 0; i < subselections_.size(); ++i) {
    delete subselections_[i];
  }
}

TMegaSelectionSet* TMegaSelectionSet::Clone() const {
  return this->Clone(0);
}

TMegaSelectionSet* TMegaSelectionSet::Clone(const char* newname) const {
  TMegaSelectionSet* output = NULL;
  if (newname) {
    output = new TMegaSelectionSet(newname, this->GetTitle());
  } else {
    output = new TMegaSelectionSet(this->GetName(), this->GetTitle());
  }
  // Copy over the subselections
  for (size_t i = 0; i < subselections_.size(); ++i) {
    output->AddSelection(*subselections_[i]);
  }
  return output;
}

TMegaSelectionSet::TMegaSelectionSet(const TMegaSelectionSet& other) {
  this->SetName(other.GetName());
  // Copy over the subselections
  for (size_t i = 0; i < other.subselections_.size(); ++i) {
    this->AddSelection(*other.subselections_[i]);
  }
}

void TMegaSelectionSet::SetCachePointers(TTree** tree, Long_t* entry) {
  // Setup this class
  TMegaSelection::SetCachePointers(tree, entry);
  // Setup each of the sub selections
  for (size_t i=0; i < subselections_.size(); ++i) {
    subselections_[i]->SetCachePointers(tree, entry);
  }
}

// Add a new selector to this list via a clone.
void TMegaSelectionSet::AddSelection(const TMegaSelection& selector) {
  TMegaSelection* ownedcopy = selector.Clone();
  subselections_.push_back(ownedcopy);
}

// Add a new selector to this list and take ownership
void TMegaSelectionSet::AddSelection(std::auto_ptr<TMegaSelection> selector) {
  subselections_.push_back(selector.release());
}

Bool_t TMegaSelectionSet::Select() {
  bool isCached = !this->emitChanged();
  if (isCached)
    return lastResult_;

  for (size_t i = 0; i < subselections_.size(); ++i) {
    Bool_t subresult = subselections_[i]->Select();
    if (!subresult) {
      lastResult_ = false;
      return false;
    }
  }
  lastResult_ = true;
  return true;
}
