import ROOT
import sys
import glob
import json
import os
import re

mass_getter = re.compile('.*_(?P<mass>[0-9]+)\.card\.(exp|obs)\.json')

def get_mass(filename):
    file = os.path.basename(filename)
    mass = int(mass_getter.match(file).group('mass'))
    return mass

def make_exp_band(files):
    exp = ROOT.TGraph(len(files))
    onesig = ROOT.TGraphAsymmErrors(len(files))
    twosig = ROOT.TGraphAsymmErrors(len(files))

    for i, file in enumerate(sorted(files)):
        mass = get_mass(file)
        result = json.loads(open(file, 'r').read())
        print result
        exp.SetPoint(i, mass, result['median'])
        onesig.SetPoint(i, mass, result['median'])
        twosig.SetPoint(i, mass, result['median'])
        onesig.SetPointEYlow(i,  result['median'] - result['-1'])
        onesig.SetPointEYhigh(i, result['+1'] - result['median'] )
        twosig.SetPointEYlow(i,  result['median'] - result['-2'])
        twosig.SetPointEYhigh(i, result['+2'] - result['median'] )
    exp.SetLineStyle(2)
    exp.SetLineWidth(2)
    exp.SetLineColor(ROOT.EColor.kBlack)
    #onesig.SetFillStyle(1)
    onesig.SetFillColor(ROOT.EColor.kGreen)
    #twosig.SetFillStyle(1)
    twosig.SetFillColor(ROOT.EColor.kYellow)
    return (exp, onesig, twosig)

def make_obs(files):
    obs = ROOT.TGraph(len(files))
    for i, file in enumerate(sorted(files)):
        mass = get_mass(file)
        result = json.loads(open(file, 'r').read())
        obs.SetPoint(i, mass, result['obs'])
    obs.SetLineWidth(2)
    obs.SetMarkerStyle(20)
    obs.SetMarkerSize(1)
    obs.SetLineColor(ROOT.EColor.kBlack)
    return obs

if __name__ == "__main__":
    prefix = sys.argv[1]
    print prefix
    exp_files = list(glob.glob('cards/%s*.card.exp.json' % prefix))
    obs_files = list(glob.glob('cards/%s*.card.obs.json' % prefix))
    exp, onesig, twosig = make_exp_band(exp_files)
    obs = make_obs(obs_files)

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
    frame = ROOT.TH1F('frame', 'frame', 10, 110, 130)
    frame.SetMaximum(35)
    frame.SetMinimum(0)
    frame.SetTitle("WH(#tau#tau) limits [2.1 fb^{-1}]")
    frame.GetYaxis().SetTitle("95% UL on #sigma/#sigma_{SM}")
    frame.GetXaxis().SetTitle("M_{H} (GeV)")
    frame.Draw()
    twosig.Draw('3')
    onesig.Draw('3')
    exp.Draw('l')
    #obs.Draw('lp')
    legend = ROOT.TLegend(0.19, 0.7, 0.4, 0.89, "", "NDC")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    #legend.AddEntry(obs,"Observed",  'lp')
    legend.AddEntry(exp, "Expected", 'l')
    legend.AddEntry(onesig, "#pm 1 #sigma",  'f')
    legend.AddEntry(twosig, "#pm 2 #sigma",  'f')
    canvas.RedrawAxis()
    legend.Draw()

    canvas.Update()

    canvas.SaveAs("cards/%s_limit.pdf" % prefix)
