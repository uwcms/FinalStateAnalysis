#include "FinalStateAnalysis/Utilities/interface/GraphSmoother.h"
#include "TGraphSmooth.h"
#include "TF1.h"
#include "TVectorD.h"
#include "TDecompBK.h"
#include <cmath>

namespace {

std::vector<TGraph> splitTGraphAsymmErrors(const TGraphAsymmErrors& graph) {
  std::vector<TGraph>  output;
  TGraph errUpOut(graph.GetN());
  TGraph nomOut(graph.GetN());
  TGraph errDownOut(graph.GetN());

  for (int i = 0; i < graph.GetN(); ++i) {
    double x = graph.GetX()[i];
    double nom = graph.GetY()[i];
    double errUp = nom + graph.GetEYhigh()[i];
    double errDown = nom - graph.GetEYlow()[i];
    nomOut.SetPoint(i, x, nom);
    errUpOut.SetPoint(i, x, errUp);
    errDownOut.SetPoint(i, x, errDown);
  }

  output.push_back(errUpOut);
  output.push_back(nomOut);
  output.push_back(errDownOut);
  return output;
}

void mergeTGraphAsymmErrors(TGraphAsymmErrors& graph,
    const TGraph& errup, const TGraph& nom, const TGraph& errdown) {
  for (int i = 0; i < nom.GetN(); ++i) {
    graph.SetPoint(i, nom.GetX()[i], nom.GetY()[i]);
    graph.SetPointEYhigh(i, errup.GetY()[i] - nom.GetY()[i]);
    graph.SetPointEYlow(i, nom.GetY()[i] - errdown.GetY()[i]);
  }
}

// Evans version
double smoothWithPolyFitEK(TGraph& graph, double x0, double width,
    const std::string& formula) {
  size_t pointsInFit = 0;
  double min = x0 - width;
  double max = x0 + width;
  for (int i = 0; i < graph.GetN(); ++i) {
    if (graph.GetX()[i] > min && graph.GetX()[i] < max) {
      pointsInFit++;
    }
  }
  if (pointsInFit > 2) {
    graph.Fit(formula.c_str(), "Q", "", x0 - width, x0 + width);
    return graph.GetFunction(formula.c_str())->Eval(x0);
  }
  // if we don't have enough points to fit, just return y
  return graph.Eval(x0);
}

// BandUtils version
TVectorD polyFit(double x0, double y0, int npar, int n, double *xi, double *yi) {
    //std::cout << "smoothWithPolyFit(x = " << x <<", npar = " << npar << ", n = " << n << ", xi = {" << xi[0] << ", " << xi[1] << ", ...}, yi = {" << yi[0] << ", " << yi[1] << ", ...})" << std::endl;
    TMatrixDSym mat(npar);
    TVectorD    vec(npar);
    for (int j = 0; j < npar; ++j) {
        for (int j2 = j; j2 < npar; ++j2) {
            mat(j,j2) = 0;
        }
        vec(j) = 0;
    }
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < npar; ++j) {
            for (int j2 = j; j2 < npar; ++j2) {
                mat(j,j2) += std::pow(xi[i]-x0, j+j2);
            }
            vec(j) += (yi[i]-y0)*std::pow(xi[i]-x0, j);
        }
    }
    TDecompBK bk(mat);
    bk.Solve(vec);
    return vec;
}

double smoothWithPolyFit(double x, int npar, int n, double *xi, double *yi) {
    TVectorD fitRes = polyFit(x, yi[n/2], npar, n, xi, yi);
    return fitRes(0)+yi[n/2];
}

} // end anon namespace


TGraph smooth(const TGraph& graph, double width) {
  TGraphSmooth smoother;
  TGraph temp(graph); // not const
  TGraph output(graph); // don't leak memory

  for (int i = 0; i < graph.GetN(); ++i) {
    double y = smoothWithPolyFitEK(temp, temp.GetX()[i], width, "pol2");
    double x = temp.GetX()[i];
    output.SetPoint(i, x, y);
  }

  //delete smoothed;
  return output;
}

TGraphAsymmErrors smoothWithErrors(const TGraphAsymmErrors& graph, double width) {
  std::vector<TGraph> input = splitTGraphAsymmErrors(graph);
  std::vector<TGraph> smoothed;
  for (size_t i = 0; i < input.size(); ++i) {
    TGraph smoothy = smooth(input[i], width);
    smoothed.push_back(smoothy);
  }
  TGraphAsymmErrors output(graph);

  mergeTGraphAsymmErrors(output, smoothed[0], smoothed[1], smoothed[2]);
  return output;
}


TGraph smoothBandUtils(const TGraph& graph, int order) {
  TGraphSmooth smoother;
  TGraph temp(graph); // not const
  TGraph output(graph); // don't leak memory

  for (int i = 0; i < graph.GetN(); ++i) {
    double x = temp.GetX()[i];
    double y = smoothWithPolyFit(x, order+1, graph.GetN(),
        graph.GetX(), graph.GetY());
    output.SetPoint(i, x, y);
  }

  //delete smoothed;
  return output;
}

TGraphAsymmErrors smoothBandUtilsWithErrors(const TGraphAsymmErrors& graph,
    int order) {
  std::vector<TGraph> input = splitTGraphAsymmErrors(graph);
  std::vector<TGraph> smoothed;
  for (size_t i = 0; i < input.size(); ++i) {
    TGraph smoothy = smoothBandUtils(input[i], order);
    smoothed.push_back(smoothy);
  }
  TGraphAsymmErrors output(graph);

  mergeTGraphAsymmErrors(output, smoothed[0], smoothed[1], smoothed[2]);
  return output;
}
