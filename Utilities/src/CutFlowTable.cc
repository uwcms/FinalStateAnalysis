#include "FinalStateAnalysis/Utilities/interface/CutFlowTable.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include <string.h>
#include <iomanip>
#include <cassert>

namespace ek {

void CutFlowTable::addSample(const std::string& sample, const CutFlow* cuts) {
  samples_.push_back(std::make_pair(sample, cuts));
}

void CutFlowTable::print(std::ostream& out) const {
  // Write header
  out << std::setw(20) << std::left << "Cut" << "|";
  std::string underline = "---------------------";
  for (size_t i = 0; i << samples_.size(); ++i) {
    out << std::setw(15) << std::right << samples_[i].first;
    underline += "---------------";
  }
  out << std::endl << underline << std::endl;
  // Get the first set of cuts to figure out how many cuts there are
  const CutFlow* cuts = samples_[0].second;
  for (size_t iCut = 0; iCut < cuts->nCuts(); ++iCut) {
    const char* name = cuts->name(iCut);
    out << std::setw(20) << std::left << name;
    for (size_t iSample = 0; iSample < samples_.size(); ++iCut) {
      const CutFlow* thisSamplesCuts = samples_[iSample].second;
      const char* thisSamplesName = thisSamplesCuts->name(iCut);
      // Make sure all the samples are using the same cuts
      assert(strncmp(name, thisSamplesName, 500) == 0);
      out << std::setw(15) << std::right << std::setprecision(1) <<
        cuts->passed(iCut);
    }
  }
}

}

std::ostream& operator<<(std::ostream& os, const ek::CutFlowTable& table) {
  table.print(os);
  return os;
}
