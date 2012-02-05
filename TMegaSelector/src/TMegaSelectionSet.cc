#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionSet.h"

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

// Add a new selector to this list
void TMegaSelectionSet::AddSelection(const TMegaSelection& selector) {
  TMegaSelection* ownedcopy = selector.Clone();
  subselections_.push_back(ownedcopy);
}

Bool_t TMegaSelectionSet::Select() {
  if (isCached_)
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

void TMegaSelectionSet::ResetCache() {
  isCached_ = false;
}
