#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"

#include <iomanip>
#include <iostream>
#include <cassert>
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "TH1F.h"
#include "strings.h"

namespace ek {

CutFlow::CutFlow(const CutSet& cuts, const std::string& name,
    TFileDirectory& fs) {
  const std::vector<std::string> cutNames = cuts.strings();
  initialize(cutNames, name, fs);
}

CutFlow::CutFlow(const std::vector<const CutSet*>& cuts,
    const std::string& name, TFileDirectory& fs) {

  std::vector<std::string> cutNames;

  for (size_t i = 0; i < cuts.size(); ++i) {
    const std::vector<std::string> iCutNames = cuts[i]->strings();
    cutNames.insert(cutNames.end(), iCutNames.begin(), iCutNames.end());
  }
  initialize(cutNames, name, fs);
}

void CutFlow::initialize(const std::vector<std::string>& cutNames,
    const std::string& name, TFileDirectory& fs) {
  cutFlow_ = fs.make<TH1F>("cutFlow", "cutFlow",
      cutNames.size(), -0.5, cutNames.size() - 0.5);
  // The file service owns the histo
  mustCleanupHistogram_ = false;
  // Setup the bin names
  for (size_t i = 0; i < cutNames.size(); ++i) {
    cutFlow_->GetXaxis()->SetBinLabel(i+1, cutNames[i].c_str());
  }
}

// Constructor from an existing TH1F*
CutFlow::CutFlow(const TH1F& histo) {
  cutFlow_ = new TH1F(histo); // make a copy
  // cleanup on destruction
  mustCleanupHistogram_ = true;
}

CutFlow::~CutFlow() {
  if (mustCleanupHistogram_)
    delete cutFlow_;
}

void CutFlow::fill(const CutSet& cuts, double w) {
  fillImpl(cuts, w, 0);
}

void CutFlow::fill(const std::vector<const CutSet*>& cuts, double w) {
  size_t indexCounter = 0;
  for (size_t i = 0; i < cuts.size(); ++i) {
    const CutSet* cut = cuts[i];
    assert(cut);
    fillImpl(*cut, w, indexCounter);
    indexCounter += cut->bits().size();
  }
}

void CutFlow::fillImpl(const CutSet& cuts, double w, size_t idx) {
  const std::vector<bool>& bits = cuts.bits();
  for (size_t i = 0; i < bits.size(); ++i) {
    if (bits[i]) {
      cutFlow_->Fill(idx + i, w);
    }
  }
}

double CutFlow::passed(size_t n) const {
  return cutFlow_->GetBinContent(n+1);
}

double CutFlow::efficiency(size_t n) const {
  if (n == 0)
    return 1.0;
  double numerator = passed(n);
  double denominator = passed(n-1);
  return numerator/denominator;
}

double CutFlow::cumulativeEff(size_t n) const {
  if (n == 0)
    return 1.0;
  double numerator = passed(n);
  double denominator = passed(0);
  return numerator/denominator;
}

const char* CutFlow::name(size_t n) const {
  return cutFlow_->GetXaxis()->GetBinLabel(n+1);
}

size_t CutFlow::nCuts() const {
  return (size_t)cutFlow_->GetNbinsX();
}

void CutFlow::print(std::ostream& out) const {
  size_t longestName = 20;
  for (size_t i = 0; i < nCuts(); ++i) {
    if (strlen(name(i)) + 4 > longestName)
      longestName = strlen(name(i)) + 4;
  }
  out << std::setw(longestName) << std::left << "Cut";
  out << std::setw(15) << std::right << "Passed";
  out << std::setw(15) << std::right << "Mar. Eff.";
  out << std::setw(15) << std::right << "Cum. Eff." << std::endl;
  for (size_t i = 0; i < longestName + 45; ++i)
    out << "-";
  out << std::endl;

  out.setf(std::ios::fixed, std::ios::floatfield);

  for (size_t i = 0; i < nCuts(); ++i) {
    out << std::setw(longestName) << std::left << name(i);
    out << std::setw(15) << std::right
      << std::setprecision(1) << passed(i);
    out << std::setw(15) << std::right
      << std::setprecision(4) << efficiency(i);
    out << std::setw(15) << std::right
      << std::setprecision(4) << cumulativeEff(i) << std::endl;
  }
}

}
