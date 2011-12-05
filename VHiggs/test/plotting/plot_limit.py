import ROOT
import sys
import glob
import json
import os
import re

mass_getter = re.compile('.*_(?P<mass>[0-9]+)\.card\.(exp|obs|asymp)\.json')

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
        median = result.get('exp')
        exp.SetPoint(i, mass, median)
        onesig.SetPoint(i, mass, median)
        twosig.SetPoint(i, mass, median)
        onesig.SetPointEYlow(i,  median - result['-1'])
        onesig.SetPointEYhigh(i, result['+1'] - median )
        twosig.SetPointEYlow(i,  median - result['-2'])
        twosig.SetPointEYhigh(i, result['+2'] - median )

    exp.SetLineStyle(2)
    exp.SetLineWidth(2)
    exp.SetLineColor(ROOT.EColor.kBlack)
    #onesig.SetFillStyle(1)
    onesig.SetFillColor(ROOT.EColor.kGreen)
    #twosig.SetFillStyle(1)
    twosig.SetFillColor(ROOT.EColor.kYellow)
    return (exp, onesig, twosig)

def make_tex_table(files):
    tex_output = \
"""
\hline
            &  \multicolumn{5}{c}{Expected limit} &  \\\\
$m_H$ (GeV) & $-2 \sigma$ & $-1 \sigma$ & nominal & $+1 \sigma$ & $+2 \sigma$ & Observed \\\\
\hline
"""
    for i, file in enumerate(sorted(files)):
        mass = get_mass(file)
        result = json.loads(open(file, 'r').read())
        tex_output += \
            "%i & %0.1f & %0.1f & %0.1f & %0.1f & %0.1f & %0.1f \\\\\n" % (
                mass, result['-2'], result['-1'], result['exp'],
                result['+1'], result['+2'], result['obs'])
    return tex_output

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
    exp_files = list(glob.glob('cards/%s*.card.asymp.json' % prefix))
    obs_files = list(glob.glob('cards/%s*.card.asymp.json' % prefix))
    exp, onesig, twosig = make_exp_band(exp_files)
    obs = make_obs(obs_files)

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
    frame = ROOT.TH1F('frame', 'frame', 10, 100, 160)
    frame.SetMaximum(40)
    frame.SetMinimum(0)
    frame.SetTitle("WH(#tau#tau) limits [4.6 fb^{-1}]")
    frame.GetYaxis().SetTitle("95% CL upper limit on #sigma/#sigma_{SM}")
    frame.GetXaxis().SetTitle("M_{H} (GeV)")
    frame.Draw()
    twosig.Draw('3')
    onesig.Draw('3')
    exp.Draw('l')
    obs.Draw('lp')
    #legend = ROOT.TLegend(0.19, 0.7, 0.4, 0.89, "", "NDC")
    legend = ROOT.TLegend(0.7, 0.17, 0.9, 0.45, "", "NDC")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(obs,"Observed",  'lp')
    legend.AddEntry(exp, "Expected", 'l')
    legend.AddEntry(onesig, "#pm 1 #sigma",  'f')
    legend.AddEntry(twosig, "#pm 2 #sigma",  'f')
    canvas.RedrawAxis()
    legend.Draw()

    canvas.Update()
    canvas.SaveAs("cards/%s_limit.pdf" % prefix)

    tex = make_tex_table(exp_files)
    tex_file = open("cards/%s_limit.tex" % prefix, 'w')
    tex_file.write(tex)
