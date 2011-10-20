import ROOT
import os
import sys

ROOT.gROOT.ProcessLine(".L " + os.path.join(
    os.environ['CMSSW_BASE'], 'src',
    "HiggsAnalysis/CombinedLimit/test/plotting/bandUtils.cxx+"))

if __name__ == "__main__":
    file = sys.argv[1]
    temp_file = ROOT.TFile("temp.root", "RECREATE")
    tfile = ROOT.TFile(file, "READ")
    onesig = ROOT.theBand(tfile, 1, 0, 2, 0.68)
    twosig = ROOT.theBand(tfile, 1, 0, 2, 0.95)
    median = ROOT.theBand(tfile, 1, 0, 2, 0.5)
    canvas = ROOT.TCanvas("basdf", "aasdf", 1200, 600)
    median.Draw("alp")
    canvas.SaveAs('wtf.png')

