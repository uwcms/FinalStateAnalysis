/*
 * =====================================================================================
 *
 *       Filename:  RooFitTools.C
 *
 *    Description:
 *
 *        Version:  1.0
 *        Created:  08/19/2011 13:40:10
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Evan Friis (), evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */


#include "RooDataHist.h"
#include "RooCategory.h"
#include "TList.h"

RooDataHist* makeComboDataSet(const char* name, const char* title,
    const RooArgList& vars, RooCategory& cat,
    const TList& names, const TList& rooDataHists);
