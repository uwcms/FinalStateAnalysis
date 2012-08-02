#include "FinalStateAnalysis/StatTools/interface/RooDataHistEffBuilder.h"

RooDataHistEffBuilder::RooDataHistEffBuilder(const std::string& name,
    const std::string& title, const RooArgList& vars,
    RooCategory& categories):
  name_(name),
  title_(title),
  vars_(vars),
  categories_(categories){}

void RooDataHistEffBuilder::addHist(const std::string& cat, TH1* hist) {
  histos_[cat] = hist;
}

RooDataHist RooDataHistEffBuilder::build() const {
  return RooDataHist(name_.c_str(), title_.c_str(), vars_, categories_,
      histos_, 1.0);
}
