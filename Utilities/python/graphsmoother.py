'''

Tools for smoothing TGraphs and TGraphAsymmErrors

Author: Evan K. Friis, UW Madison

Check with a linear function with an outlier at x = 3

>>> import ROOT
>>> graph = ROOT.TGraph(5)
>>> graph.SetPoint(0, 1, 1)
>>> graph.SetPoint(1, 2, 2)
>>> graph.SetPoint(2, 3, 6)
>>> graph.SetPoint(3, 4, 4)
>>> graph.SetPoint(4, 5, 5)
>>>
>>> smoothed = smooth_graph(graph, 3)
>>> graph.GetY()[2]
6.0
>>> smoothed_y = smoothed.GetY()[2]
>>> 3 < smoothed_y < 6
True
>>> "%0.2f" % smoothed_y
'4.46'

'''


import ROOT

ROOT.gSystem.Load('libFinalStateAnalysisUtilities')

def smooth_graph(tgraph, width):
    if isinstance(tgraph, ROOT.TGraphAsymmErrors):
        return ROOT.smoothWithErrors(tgraph, width)
    else:
        return ROOT.smooth(tgraph, width)

if __name__ == "__main__":
    import doctest; doctest.testmod()
