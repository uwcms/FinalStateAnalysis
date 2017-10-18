#ifndef FinalStateAnalysis_Utilities_CutFlowTable_h
#define FinalStateAnalysis_Utilities_CutFlowTable_h

/*
 * Interface which holds cut flow corresponds to different samples, then prints
 * them in a nice tabular form.
 *
 * Author: Evan K. Friis UW Madison
 *
 */

#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"
#include <iostream>
#include <string>
#include <vector>

namespace ek {

class CutFlowTable {
  public:
    CutFlowTable(){};
    // Add a column to the cutflow table
    void addSample(const std::string& sample, const CutFlow* cuts);
    // Print the table
    void print(std::ostream& out) const;
    // Print the table, in latex tabular format
    void printTeX(std::ostream& out) const;
  private:
    std::vector<std::pair<std::string, const CutFlow*> > samples_;
};

}

std::ostream& operator<<(std::ostream& os, const ek::CutFlowTable& table);

#endif
