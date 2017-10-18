/*
 * =====================================================================================
 *
 *       Filename:  rooFitTools.cc
 *
 *    Description:
 *
 *        Version:  1.0
 *        Created:  08/19/2011 14:05:14
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Evan Friis (), evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

//#include "FinalStateAnalysis/Utilities/interface/rooFitTools.h"

#include "RooDataHist.h"
#include "RooCategory.h"
#include "TList.h"
#include "TH1.h"
#include "TObjString.h"
#include <string>
#include <map>

RooDataHist* makeComboDataSet(const char* name, const char* title,
    const RooArgList& vars, RooCategory& cat,
    const TList& names, const TList& rooDataHists) {

  TIter nameIter(&names);
  TIter dataIter(&rooDataHists);

  std::map<std::string, TH1*> histoMap;

  TObjString* nameStr;
  TH1* histo;
  while ((nameStr = dynamic_cast<TObjString*>(nameIter.Next()))) {
    histo = dynamic_cast<TH1*>(dataIter.Next());
    histoMap[nameStr->String().Data()] = histo;
  }

  RooDataHist* output = new RooDataHist(name, title, vars, cat, histoMap);
  return output;
}
