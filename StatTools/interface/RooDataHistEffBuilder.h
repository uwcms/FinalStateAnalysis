/*
 * =====================================================================================
 *
 *       Filename:  RooDataHistEffBuilder.cc
 *
 *    Description:  Builds a RooDataHist from two TH1s
 *
 *         Author:  Evan Friis (), evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef ROODATAHISTEFFBUILDER_B8PM4JNC
#define ROODATAHISTEFFBUILDER_B8PM4JNC


#include "TH1.h"
#include "RooDataHist.h"
#include "RooCategory.h"
#include "RooArgList.h"
#include <string>
#include <map>

class RooDataHistEffBuilder {
  public:
    RooDataHistEffBuilder(const std::string& name, const std::string& title,
        const RooArgList& vars, RooCategory& categories);
    // Add another histogram w/ given category
    void addHist(const std::string& cat, TH1* hist);
    // Buidl the roo data  hist
    RooDataHist build() const;
  private:
    std::string name_;
    std::string title_;
    RooArgList vars_;
    RooCategory& categories_;
    std::map<std::string, TH1*> histos_;
};

#endif /* end of include guard: ROODATAHISTEFFBUILDER_B8PM4JNC */
