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

// Smooth a graph
TGraph smooth(const TGraph& graph, double width);

// Smooth a graph and its error band
TGraphAsymmErrors smoothWithErrors(const TGraphAsymmErrors& graph,
    double width);


#endif /* end of include guard: GRAPHSMOOTHER_2GUEYRBN */
