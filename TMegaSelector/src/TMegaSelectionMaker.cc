#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionMaker.h"

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionFactory.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelector.h"

ClassImp(TMegaSelectionMaker)

TMegaSelectionMaker::~TMegaSelectionMaker() {}

TMegaSelectionMaker::TMegaSelectionMaker(TMegaSelector* selector,
    ROOT::TBranchProxyDirector* dir)
  :selector_(selector),factory_(new TMegaSelectionFactory(dir)){}

void TMegaSelectionMaker::MakeIntCut(const std::string& selection,
    const std::string& branch, const std::string& op, Int_t value, bool abs)
  const {
    selector_->AddToSelection(selection, factory_->MakeIntCut(branch, op, value, abs));
}

void TMegaSelectionMaker::MakeFloatCut(const std::string& selection,
    const std::string& branch, const std::string& op, Float_t value, bool abs)
  const {
    selector_->AddToSelection(selection, factory_->MakeFloatCut(branch, op, value, abs));
}

void TMegaSelectionMaker::MakeDoubleCut(const std::string& selection,
    const std::string& branch, const std::string& op, Double_t value, bool abs)
  const {
    selector_->AddToSelection(selection, factory_->MakeDoubleCut(branch, op, value, abs));
}
