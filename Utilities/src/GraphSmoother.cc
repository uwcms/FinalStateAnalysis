#include "FinalStateAnalysis/Utilities/interface/GraphSmoother.h"
#include "TGraphSmooth.h"
#include "TF1.h"

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

double smoothWithPolyFit(TGraph& graph, double x0, double width,
    const std::string& formula) {
  graph.Fit(formula.c_str(), "Q", "", x0 - width, x0 + width);
  return graph.GetFunction(formula.c_str())->Eval(x0);
}


TGraph smooth(const TGraph& graph, double width) {
  TGraphSmooth smoother;
  TGraph temp(graph); // not const
  TGraph output(graph); // don't leak memory

  for (int i = 0; i < graph.GetN(); ++i) {
    //double origy = temp.GetY()[i];
    double y = smoothWithPolyFit(temp, temp.GetX()[i], width, "pol2");
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
