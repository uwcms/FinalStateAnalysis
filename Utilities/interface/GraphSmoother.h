/*
 * =====================================================================================
 *
 *       Filename:  GraphSmoother.h
 *
 *    Description:  Tools for smoothing ROOT TGraph***
 *
 *         Author:  Evan Friis evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef GRAPHSMOOTHER_2GUEYRBN
#define GRAPHSMOOTHER_2GUEYRBN

#include <vector>
#include "TGraph.h"
#include "TGraphAsymmErrors.h"

// Smooth a graph over an interval of width.  At each data point,
// fit a 2nd order polynomial in the range x +- width.  The new x0 value is
// the fitted poly evaluated at x0
TGraph smooth(const TGraph& graph, double width);

// Smooth a graph and its error band
TGraphAsymmErrors smoothWithErrors(const TGraphAsymmErrors& graph,
    double width);

// HiggsAnalysis BandUtils.cxx version
TGraph smoothBandUtils(const TGraph& graph, int npar);

TGraphAsymmErrors smoothBandUtilsWithErrors(const TGraphAsymmErrors& graph,
    int npar);

#endif /* end of include guard: GRAPHSMOOTHER_2GUEYRBN */
