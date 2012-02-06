#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelector.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionSet.h"

TMegaSelector::TMegaSelector(TTree* tree):
  chain(0),
  director_(tree, -1) {}

TMegaSelector::~TMegaSelector(){}

void TMegaSelector::Init(TTree* tree) {
  //   Set branch addresses
  if (tree == 0) return;
  chain = tree;
  director_.SetTree(chain);
  this->MegaInit(tree);
}

Bool_t TMegaSelector::Notify() {
  director_.SetTree(chain);
  return this->MegaNotify();
}

void TMegaSelector::Begin(TTree* /*deprecated*/) {
  this->MegaBegin();
}

void TMegaSelector::SlaveBegin(TTree* /*deprecated*/) {
  this->MegaSlaveBegin();
}

Bool_t TMegaSelector::Process(Long64_t entry) {
  currentEntry_ = entry;
  director_.SetReadEntry(entry);
  // Check if we are apply a filter
  if (!filterSelection_ || filterSelection_->Select()) {
    return this->MegaProcess(entry);
  }
  return true;
}

void TMegaSelector::SlaveTerminate() {
  this->MegaSlaveTerminate();
}

void TMegaSelector::Terminate() {
  this->MegaTerminate();
}
